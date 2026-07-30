# AGENTS.md · 芯智云匠 MES AI 项目 · 智能体工作指南

> **本文件是指针文件，不是规范本体。**
> 完整开发行为规范见 **`CLAUDE.md`（十四章，强制约束，不可修改）**——开工前必读。
> 最新项目进展见 **`docs/Session_State_<最新日期>.md`**——每次会话先读最新一份。

## 一、项目身份

芯智云匠——山东芯通 MES 岗位 AI 智能体资产化项目。目标系统为真实钢板/卷材 MES
（Oracle 21c XE / `MESAPUSER`，韩系，1,860 表 / 9,160 PL/SQL 单元，列注释全空、中英韩三语混合）。

## 二、技术栈（不得擅自新增依赖）

| 层 | 选型 |
|----|----|
| 后端 | Java 11 + Spring Boot 2.7 + MyBatis Plus，MySQL 8 |
| 前端 | Vue 3 + Element Plus（任务管理平台）；Vue 2 + Element UI（旧页面）|
| AI 网关 | Python FastAPI（`src/ai-gateway`），ChromaDB + 多语言 Embedding |
| 接口 | RESTful，统一 `ResultVO<T>` 封装 |

## 三、关键红线（CLAUDE.md 摘要，违反即阻断）

- **任务门禁**：只执行评审通过的需求单 `REQ-MES-AI-{YYYYMMDD}-{序号}`（CLAUDE.md §5.1）。
- **脱敏**：任何发往外部 AI API 的内容必须经 ai-gateway 脱敏门（§4.2 七类规则）；发现漏洞立即停止并上报。
- **硬编码禁令**：代码中禁止 IP、连接串、明文密钥、厂区编号等字面量（§4.1）。
- **生产环境**：仅只读（巡检查询）；写操作只能对测试环境，且须配回退脚本（§4.3）。
- **Token 预算**：默认 300 万/日，超限降级/暂停（§12）；批训练须 TL 临时预算闸授权留痕。
- **职责边界**：DDL 变更、>100 行数据修改、新服务首部署、安全配置变更——停止并等待人工授权（§一）。

## 四、工程惯例

- **Git 提交**：`[REQ-MES-AI-YYYYMMDD-XXX] <feat|fix|refactor|docs|test|chore>: 描述`，
  feat / docs / refactor 分开提交，不混合不相关需求。
- **注释**：代码注释、JavaDoc 一律中文；日志用 `@Slf4j`。
- **测试**：覆盖率 ≥ 70%；新增核心功能须同步新增 ≥3 条断言入 `/assertions/`（§7.3）。
- **知识库入库**：遵守 CLAUDE.md §14（多语言 Embedding 模型、入库/查询同模型、入库后必验证 Top-3 召回）。
- **文档**：`docs/` 只读，更新须申请；`prompts/`、`assertions/` 变更须技术负责人审批。

## 五、交付格式（每个任务四项，缺一不可）

1. 实现思路分析（200 字以内）
2. 完整代码（文件头注释标明用途/作者 AI/日期/需求单号）
3. 单元测试用例
4. 使用说明与变更记录

## 六、验证命令速查

```bash
# AI 网关（FastAPI）
cd src/ai-gateway && python -m pytest          # 全量测试

# 后端（Spring Boot）
mvn test                                        # 全量测试

# 前端（Vue 3）
cd frontend && npm run build                    # 构建验证

# 知识库检索验证
python3 scripts/kb-ingest/validate_ingestion.py --module <模块名>
```

---

*本文件维护原则：只记长期稳定的规范指针与红线摘要，不记会话进展等动态状态（漂移风险）。*
