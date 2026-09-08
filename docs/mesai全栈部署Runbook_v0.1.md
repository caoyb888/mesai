# mesai 全栈部署 Runbook v0.1

> 关联需求单：`REQ-MES-AI-20260716-001`
> 用途：在测试/演示环境把 mesai 产品全栈（MySQL + Redis + Spring Boot 后端 + Vue 前端）跑起来，用于 `/mes-qa` 数据问答等功能的浏览器端 e2e 验证。
> 首次编制：2026-07-18 · 基于 2026-07-17 在共享内网机 `100.95.76.81` 的实测过程回填。

| 项 | 内容 |
|----|----|
| 适用环境 | 测试 / 演示环境（**非生产**）。本 Runbook 用容器自建 MySQL/Redis，不依赖宿主原生实例 |
| 前置 | 目标机具备 `docker`、`java 21`（或兼容）、`maven`、`node`+`npm`、`tmux`；AI 网关已在 `:8000` 运行 |
| 数据持久化 | ⚠️ 下述容器**未挂持久卷**，`docker rm` 后数据丢失，重启需重跑迁移。正式固化请另加 `-v` 卷 |

---

## 0. 端口规划（关键：共享机必须避冲突）

若与其它服务共机，先探明占用端口再选空闲端口。本文示例端口（按需替换）：

| 服务 | 端口 | 说明 |
|----|----|----|
| MySQL（容器）| `13306` | 映射容器内 3306 |
| Redis（容器）| `16390` | 映射容器内 6379 |
| Spring Boot 后端 | `8095` | 默认 8080 若被占则改此 |
| Vue 前端（vite）| `5173` | dev server |
| AI 网关（既有）| `8000` | 后端经此调 LLM，须已运行 |

探端口：`ss -ltn | grep -E ":13306|:16390|:8095|:5173"`（无输出即空闲）。

---

## 1. 起 MySQL 容器并初始化库

```bash
# 1.1 起容器（口令按环境改，勿沿用示例值到正式环境）
docker rm -f mesai-mysql 2>/dev/null
docker run -d --name mesai-mysql \
  -e MYSQL_ROOT_PASSWORD="MesAiRoot@2026" -e MYSQL_ROOT_HOST="%" \
  -p 13306:3306 \
  docker.m.daocloud.io/library/mysql:8.0 \
  --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# 1.2 等就绪
for i in $(seq 1 30); do
  docker exec mesai-mysql mysqladmin ping -uroot -pMesAiRoot@2026 --silent 2>/dev/null && break
  sleep 3
done

# 1.3 按序 apply 迁移（V1~V5 在 scripts/init/，V6 在 src/main/resources/db/migration/）
cd <项目根>
MYSQL="docker exec -i mesai-mysql mysql -uroot -pMesAiRoot@2026 --default-character-set=utf8mb4"
for f in scripts/init/V1__mes_ai_task_schema.sql \
         scripts/init/V2__mes_ai_monitor_schema.sql \
         scripts/init/V3__mes_ai_knowledge_schema.sql \
         scripts/init/V4__mes_ai_audit_schema.sql \
         scripts/init/V5__init_base_data.sql \
         src/main/resources/db/migration/V6__system_user.sql; do
  $MYSQL < "$f"
done

# 1.4 校验：应得 mes_ai_task=11 / mes_ai_monitor=3 / mes_ai_knowledge=6 / mes_ai_audit=3
$MYSQL -e "SELECT table_schema, COUNT(*) FROM information_schema.tables
 WHERE table_schema IN ('mes_ai_task','mes_ai_monitor','mes_ai_knowledge','mes_ai_audit')
 AND table_type='BASE TABLE' GROUP BY table_schema;"
```

### 1.5 修正 admin 登录口令（重要）

`V6` 种子里 `admin` 的 BCrypt hash 与注释口令**不一致**，直接登录会报「用户名或密码错误」。需用 Spring 兼容的 `$2a$` 强度 10 重算并更新：

```bash
PY=<可用python，如 ai-gateway .venv/bin/python，需装 bcrypt>
HASH=$($PY -c "import bcrypt; print(bcrypt.hashpw(b'Xingtong@2026', bcrypt.gensalt(rounds=10, prefix=b'2a')).decode())")
docker exec -i mesai-mysql mysql -uroot -pMesAiRoot@2026 mes_ai_task \
  -e "UPDATE sys_user SET password='$HASH' WHERE username='admin';"
# 之后即可用 admin / Xingtong@2026 登录
```

---

## 2. 起 Redis 容器

```bash
docker rm -f mesai-redis 2>/dev/null
docker run -d --name mesai-redis -p 16390:6379 redis:7-alpine
docker exec mesai-redis redis-cli ping   # 期望 PONG
```

> 用途：JWT 刷新令牌存储、`task_no` 分布式序列。若宿主已有可用无密码 Redis 也可直连，但**不要**复用带业务数据的共享实例。

---

## 3. 起 Spring Boot 后端

### 3.1 打包

```bash
cd <项目根> && mvn -q -DskipTests package
# 产物 target/mesai-1.0.0-SNAPSHOT.jar
```

### 3.2 启动脚本 `run-mesai.sh`

```bash
#!/usr/bin/env bash
LOG=$HOME/mesai-run.log
echo "=== START $(date) ===" > "$LOG"
cd <项目根> || exit 1
export SERVER_PORT=8095
export SPRING_PROFILES_ACTIVE=dev
# characterEncoding 必须是 Java 字符集名 UTF-8，不能写 utf8mb4（Connector/J 会报 Unsupported）
export DB_URL="jdbc:mysql://127.0.0.1:13306/mes_ai_task?useSSL=false&serverTimezone=Asia/Shanghai&characterEncoding=UTF-8&useUnicode=true&allowPublicKeyRetrieval=true"
export DB_USERNAME=root
export DB_PASSWORD="MesAiRoot@2026"
export REDIS_HOST=127.0.0.1
export REDIS_PORT=16390
# logback 默认写 /var/log/mesai（无权限会启动失败），必须重定向到可写目录
/usr/bin/java -jar target/mesai-1.0.0-SNAPSHOT.jar \
  --logging.file.path=$HOME/mesai-logs >> "$LOG" 2>&1
```

### 3.3 用 tmux 拉起（**durable，勿用会自杀的 pkill**）

```bash
mkdir -p $HOME/mesai-logs
tmux new-session -d -s mesai "bash $HOME/run-mesai.sh"
# 探活
for i in $(seq 1 30); do
  [ "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8095/system/health)" = 200 ] && { echo OK; break; }
  sleep 2
done
```

---

## 4. 起 Vue 前端

```bash
cd <项目根>/frontend
# 依赖：若首次或 lock 变更，先 npm install（须用官方/可达源，见 §6 坑3）
cat > $HOME/run-frontend.sh <<'SH'
#!/usr/bin/env bash
cd <项目根>/frontend
export VITE_API_TARGET=http://127.0.0.1:8095   # 指向后端端口；默认 8080
exec npm run dev -- --host 0.0.0.0 --port 5173 > $HOME/frontend-run.log 2>&1
SH
chmod +x $HOME/run-frontend.sh
tmux new-session -d -s mesfe "bash $HOME/run-frontend.sh"
```

访问：**http://<机器IP>:5173/** → 登录 `admin` / `Xingtong@2026` → 左侧「MES 数据问答」。

---

## 5. 端到端自检（curl，走 vite 代理即等价浏览器路径）

```bash
BASE=http://127.0.0.1:5173/api        # 经 vite 代理；直连后端则 http://127.0.0.1:8095
TOKEN=$(curl -s -X POST $BASE/system/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"Xingtong@2026"}' | grep -oP '"accessToken":"\K[^"]+')
curl -s -X POST $BASE/mes-qa/ask -H 'Content-Type: application/json' -H "Authorization: Bearer $TOKEN" \
  -d '{"question":"热轧钢卷的轧制实绩数据保存在哪张表？主键是什么？","kind":"table"}'
# 期望 code:0，answer 命中 SHR_HCOIL_ROLLING_RSLT / 主键 COIL_NO，附 contextDocs
```

---

## 6. 排障备忘（实测踩过的坑）

| 现象 | 根因 | 处置 |
|----|----|----|
| detach 后台老失败、日志空、进程秒退 | `pkill -f "…SNAPSHOT.jar"` **匹配到启动命令自身命令行**，把启动壳自杀 | 停服务用 `tmux kill-session -t mesai` 或 `fuser -k 8095/tcp`（不含 jar 名）；**切勿**用会命中自身的 pkill 模式 |
| 启动即 `Logback configuration error … /var/log/mesai … No such file` | logback-spring.xml 默认 `LOG_PATH=/var/log/mesai`，无写权限 | 传 `--logging.file.path=<可写目录>` 或设 `logging.file.path` |
| 登录 500 `Unsupported character encoding 'utf8mb4'` | JDBC `characterEncoding` 只认 Java 字符集名 | 写 `characterEncoding=UTF-8`，服务端字符集用 utf8mb4 由建库/连接参数保证 |
| 登录 `用户名或密码错误` | V6 种子 BCrypt hash 与注释口令不符 | 见 §1.5 用 bcrypt 重算并 UPDATE |
| `npm install` 在腾讯云外 ENOTFOUND | 旧 `package-lock.json` 的 `resolved` 硬编码 `mirrors.tencentyun.com` | 已用官方源重生 lock（commit 2aa5e18）；他机装依赖用 `--registry=https://registry.npmjs.org` |

---

## 7. 关停 / 重启

```bash
# 停应用（保留数据容器）
tmux kill-session -t mesai; tmux kill-session -t mesfe
# 停数据（数据非持久，重启需重跑 §1、§2）
docker rm -f mesai-mysql mesai-redis
# 重启应用：重跑 §3.3、§4 的 tmux new-session 即可
```

---

*mesai 全栈部署 Runbook v0.1 · REQ-MES-AI-20260716-001 · 2026-07-18*
*示例口令/端口仅供测试环境，正式环境须改强口令、挂持久卷、按 CLAUDE.md §四 走授权部署*
