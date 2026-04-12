# 芯智云匠 · 技术规范文档（Tech Spec）

## 山东芯通 MES AI 智能体资产化项目

| 项目 | 内容 |
|------|------|
| 文件编号 | AI-MES-TECHSPEC-2026-001 |
| 版本号 | V1.1 |
| 编写日期 | 2026-04-12 |
| 编写单位 | 乙方技术团队 |
| 关联技术方案 | AI-MES-TECH-2026-001（V1.1） |
| 关联数据库设计 | AI-MES-DB-2026-001（V1.1） |
| 关联API规范 | AI-MES-API-2026-001（V1.1） |
| 关联开发规范 | CLAUDE.md（AI-MES-CLAUDE-2026-001 · V1.0） |
| 文件状态 | 正式发布 |

> **说明**：本文档是对技术方案（AI-MES-TECH-2026-001）和 CLAUDE.md 中未充分细化内容的技术决策补充，
> 包括后端分层架构约定、编码实现规范、异常处理标准、日志格式规范、安全编码要求及前端开发规范。
> 本文档与 CLAUDE.md 具有同等约束力，两者共同构成本项目的完整开发规范体系。

---

## 目录

1. [项目技术栈总览](#一项目技术栈总览)
2. [后端分层架构约定](#二后端分层架构约定)
3. [Java 编码规范](#三java-编码规范)
4. [统一响应与错误码规范](#四统一响应与错误码规范)
5. [异常处理标准](#五异常处理标准)
6. [日志格式规范](#六日志格式规范)
7. [数据访问层规范（MyBatis Plus）](#七数据访问层规范mybatis-plus)
8. [事务管理规范](#八事务管理规范)
9. [输入校验规范](#九输入校验规范)
10. [安全编码要求](#十安全编码要求)
11. [前端编码规范（Vue 3）](#十一前端编码规范vue-3)
12. [SQL 编写规范](#十二sql-编写规范)
13. [Git 工作流与提交规范](#十三git-工作流与提交规范)
14. [单元测试规范](#十四单元测试规范)
15. [配置管理规范](#十五配置管理规范)
16. [附录](#十六附录)

---

## 一、项目技术栈总览

### 1.1 后端核心依赖

| 组件 | 版本 | 用途 | 备注 |
|------|------|------|------|
| Java | 11 | 后端语言 | 使用 LTS 版本，强制 |
| Spring Boot | 2.7.x | 应用框架 | 使用最新 2.7.x 补丁版本 |
| MyBatis Plus | 3.5.x | ORM 框架 | 与项目现有版本一致 |
| Spring Security | 5.7.x | 安全框架（JWT辅助） | 随 Spring Boot 2.7.x 版本 |
| MySQL Connector/J | 8.0.x | AI 平台数据库驱动 | 与 AI 平台自建 MySQL 8.x 配套 |
| PostgreSQL JDBC Driver | 42.x | MES 系统数据库只读驱动 | 连接现有 MES PostgreSQL 15.x，只读账号，禁止写操作 |
| Redis（Lettuce） | Spring Boot 内置版本 | 分布式序列号、Token黑名单 | 通过 spring-boot-starter-data-redis 引入 |
| JJWT | 0.11.x | JWT 生成与校验 | `io.jsonwebtoken:jjwt-api/impl/jackson` |
| Lombok | 最新稳定 | 消除样板代码 | `@Slf4j`、`@Data`、`@Builder` 等 |
| Jackson | Spring Boot 内置版本 | JSON 序列化/反序列化 | 统一时间格式配置 |
| Validation（Hibernate） | Spring Boot 内置版本 | Bean 入参校验 | `@Valid`、`@NotBlank` 等 |
| EasyExcel | 3.x | Excel 导出 | 阿里开源，替代 POI 直接操作 |
| Quartz | 2.3.x | 定时任务调度 | 巡检任务、Token 汇总等 |
| WebSocket（STOMP） | Spring Boot 内置 | 实时进展推送 | `spring-boot-starter-websocket` |

> **新增依赖审批**：上表以外的任何第三方依赖，引入前须提交《依赖引入评审申请》，经技术负责人审批后方可在 `pom.xml` 中添加。

### 1.2 前端核心依赖

| 组件 | 版本 | 用途 |
|------|------|------|
| Vue | 3.x | 前端框架（任务管理平台） |
| Element Plus | 2.x | UI 组件库 |
| Axios | 1.x | HTTP 请求封装 |
| Pinia | 2.x | 状态管理 |
| Vue Router | 4.x | 前端路由 |
| Vite | 4.x | 构建工具 |
| ECharts | 5.x | 图表组件（成本统计、断言通过率） |
| STOMP.js | 最新稳定 | WebSocket/STOMP 客户端 |

### 1.3 基础设施

| 组件 | 版本/规格 | 用途 |
|------|---------|------|
| MySQL 8.0.x | AI 平台自建数据库（4 个 Schema，22 张表），部署于 AI 平台服务器（服务器 B） |
| PostgreSQL 15.x | MES 系统现有数据库，部署于 MES 服务器（服务器 A），AI 平台通过只读账号跨服访问，**禁止写入** |
| Redis | 6.x+ | 序列号生成、Token 黑名单 |
| GitLab | 内网私有 | 代码仓库 |
| GitLab CI / Jenkins | — | CI/CD 流水线 |
| SonarQube | 最新 LTS | 代码质量扫描 |
| Gitleaks | 最新稳定 | 硬编码敏感信息扫描 |
| GoReplay | 最新稳定 | 流量录制与回放 |
| Diffy | Twitter 开源 | 差异比对 |
| ChromaDB / Milvus | — | 向量知识库 |
| LangChain（Python） | 最新稳定 | AI 编排、RAG 检索 |

---

## 二、后端分层架构约定

### 2.1 包结构规范

```
com.xingtong.mesai
├── config/                     # 全局配置类
│   ├── SecurityConfig.java     # Spring Security 配置
│   ├── WebSocketConfig.java    # WebSocket 配置
│   ├── MyBatisPlusConfig.java  # MP 分页插件等配置
│   ├── RedisConfig.java        # Redis 序列化配置
│   └── JacksonConfig.java      # 全局 Jackson 时间格式配置
│
├── common/                     # 公共基础组件
│   ├── result/
│   │   ├── ResultVO.java       # 统一响应封装
│   │   └── ResultCode.java     # 业务错误码枚举
│   ├── exception/
│   │   ├── BizException.java   # 业务异常基类
│   │   └── GlobalExceptionHandler.java  # 全局异常处理器
│   ├── constant/               # 项目级常量
│   ├── enums/                  # 枚举定义（状态机枚举等）
│   ├── util/                   # 工具类
│   └── desensitize/            # PII 脱敏处理器
│
├── security/                   # 安全相关
│   ├── JwtUtil.java            # JWT 生成/解析/验证
│   ├── JwtFilter.java          # JWT 请求过滤器
│   ├── UserDetail.java         # UserDetails 实现
│   └── PermissionAspect.java   # 权限注解 AOP 切面
│
├── module/                     # 业务模块（按功能分包）
│   ├── task/                   # 任务管理模块
│   │   ├── controller/         # 控制层（对外 REST 接口）
│   │   ├── service/            # 服务层接口
│   │   │   └── impl/           # 服务层实现
│   │   ├── mapper/             # MyBatis Plus Mapper 接口
│   │   ├── entity/             # 数据库实体（对应数据库表）
│   │   ├── dto/                # 请求 DTO（Controller 入参）
│   │   ├── vo/                 # 响应 VO（Controller 出参）
│   │   └── converter/          # Entity ↔ VO/DTO 转换器
│   ├── review/                 # 评审与授权模块
│   ├── deploy/                 # 部署管理模块
│   ├── monitor/                # 运维监控模块
│   ├── knowledge/              # 知识库模块
│   ├── assertion/              # 断言库模块
│   ├── cost/                   # 成本统计模块
│   └── system/                 # 系统管理模块（鉴权、用户）
│
└── infrastructure/             # 基础设施适配
    ├── ai/                     # AI 调用网关封装
    ├── websocket/              # WebSocket 推送服务
    ├── scheduler/              # 定时任务（Quartz）
    └── storage/                # 文件存储适配
```

### 2.2 各层职责边界

```
HTTP 请求
    │
    ▼
┌──────────────────────────────────────────────────────┐
│  Controller 层  （仅做：请求接收、参数校验、响应封装）  │
│  - 使用 @Valid 触发 Bean Validation                   │
│  - 调用 Service，将结果封装为 ResultVO 返回            │
│  - 禁止：业务逻辑、数据库访问、异常捕获（交给全局处理器）│
└────────────────────────┬─────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────┐
│  Service 层  （业务逻辑的唯一归宿）                    │
│  - 编排业务流程、状态机流转、事务边界                  │
│  - 调用 Mapper 进行数据读写                           │
│  - 调用 Infrastructure 层（AI 网关、文件存储等）       │
│  - 抛出 BizException 表达业务失败                     │
│  - 禁止：直接构造 HTTP 响应、直接操作 HttpServletRequest│
└────────────────────────┬─────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────┐
│  Mapper 层  （数据访问，只做 CRUD）                    │
│  - 继承 BaseMapper<T>，使用 MyBatis Plus 标准操作      │
│  - 复杂查询在 XML 中编写，禁止 Service 层写 SQL        │
│  - 禁止：业务逻辑、事务控制、日志打印                  │
└──────────────────────────────────────────────────────┘
```

### 2.3 DTO / VO / Entity 分离原则

| 对象类型 | 职责 | 放置位置 |
|--------|------|--------|
| **Entity** | 与数据库表一一对应，`@TableName` 注解标注 | `module/xxx/entity/` |
| **DTO（Data Transfer Object）** | Controller 接收前端请求的入参，含 `@Valid` 校验注解 | `module/xxx/dto/` |
| **VO（View Object）** | Controller 返回给前端的出参，字段按需裁剪 | `module/xxx/vo/` |
| **Converter** | Entity ↔ VO/DTO 的转换，禁止在 Service 中手动 set | `module/xxx/converter/` |

**强制规则**：
- **禁止**将 Entity 直接作为 Controller 的入参或返回值
- **禁止**在 VO 中暴露敏感字段（如 `password`、`approver_ip` 原始值）
- **禁止**在 DTO 中放置数据库 ID 作为可写字段（防越权修改）

### 2.4 接口路径命名约定

| 规范项 | 规则 | 示例 |
|--------|------|------|
| 路径风格 | kebab-case，全小写 | `/api/v1/task-requests` |
| 资源名 | 复数名词 | `/tasks`、`/exec-logs`、`/assertions` |
| 嵌套资源 | 最多两级嵌套 | `/tasks/{id}/artifacts` |
| API 版本 | 路径前缀 `/api/v1/` | — |
| 操作动词 | 通过 HTTP Method 表达，路径不含动词 | `GET /tasks`（列表），`POST /tasks`（创建） |
| 特殊操作 | 无法用 REST 动词表达时，用动词后缀 | `/tasks/{id}/accept`、`/approvals/{id}/approve` |

---

## 三、Java 编码规范

### 3.1 命名规范（补充 CLAUDE.md 细化）

#### 3.1.1 类命名

| 类型 | 命名规则 | 示例 |
|------|--------|------|
| Controller | `{模块}Controller` | `TaskRequestController` |
| Service 接口 | `{模块}Service` | `TaskRequestService` |
| Service 实现 | `{模块}ServiceImpl` | `TaskRequestServiceImpl` |
| Mapper 接口 | `{实体}Mapper` | `AiTaskReqMapper` |
| Entity | 与数据库表名对应，UpperCamelCase | `AiTaskReq`（对应 `ai_task_req`） |
| DTO | `{操作}{模块}DTO` | `CreateTaskRequestDTO`、`UpdateTaskStatusDTO` |
| VO | `{模块}VO`、`{模块}DetailVO` | `TaskRequestVO`、`TaskRequestDetailVO` |
| 枚举 | `{含义}Enum` | `TaskStatusEnum`、`TaskTypeEnum` |
| 常量类 | `{模块}Constants` | `TaskConstants`、`SecurityConstants` |
| 异常 | `{业务含义}Exception` | `TaskStatusInvalidException` |
| 配置类 | `{组件}Config` | `RedisConfig`、`JwtConfig` |

#### 3.1.2 方法命名

| 场景 | 命名规则 | 示例 |
|------|--------|------|
| 查询单个 | `getXxx`、`findXxx` | `getTaskById`、`findByTaskNo` |
| 查询列表 | `listXxx`、`pageXxx` | `listPendingTasks`、`pageTaskRequests` |
| 新增 | `createXxx`、`addXxx` | `createTaskRequest` |
| 修改 | `updateXxx`、`modifyXxx` | `updateTaskStatus` |
| 删除 | `deleteXxx`、`removeXxx` | `deleteTaskRequest` |
| 状态流转 | `{动作}Task` | `approveTask`、`rejectTask`、`startTask` |
| 校验 | `validateXxx`、`checkXxx` | `validateTaskStatus`、`checkPermission` |
| 发送通知 | `sendXxxNotification`、`notifyXxx` | `sendApprovalNotification` |

#### 3.1.3 常量命名

```java
// ✅ 正确：UPPER_SNAKE_CASE，放置于 Constants 类或枚举
public final class TaskConstants {
    /** 任务编号前缀 */
    public static final String TASK_NO_PREFIX = "REQ-MES-AI-";
    /** Redis 序列号键前缀 */
    public static final String TASK_SEQ_REDIS_KEY_PREFIX = "task:seq:";
    /** 每批次最大操作条数 */
    public static final int BATCH_MAX_SIZE = 500;
    /** Token 每日预算上限（tokens） */
    public static final long TOKEN_DAILY_BUDGET = 3_000_000L;
    /** Token 降级阈值（tokens） */
    public static final long TOKEN_DEGRADE_THRESHOLD = 2_500_000L;
}

// ❌ 错误：在 Service 中散落魔法值
if (tokenCount > 3000000) { ... }
```

### 3.2 注解使用规范

#### 3.2.1 Controller 层注解

```java
/**
 * 任务管理控制器
 * 提供需求单的增删改查和状态管理接口
 *
 * @author AI
 * @date 2026-04-12
 * @see REQ-MES-AI-20260412-001
 */
@RestController
@RequestMapping("/api/v1/tasks")
@RequiredArgsConstructor       // Lombok：构造器注入，替代 @Autowired
@Slf4j
public class TaskRequestController {

    private final TaskRequestService taskRequestService;

    /**
     * 分页查询需求单列表
     *
     * @param queryDTO 查询条件（状态、优先级、部门、关键词等）
     * @return 分页结果
     */
    @GetMapping
    @PreAuthorize("hasAuthority('task:read')")    // 接口级权限控制
    public ResultVO<PageVO<TaskRequestVO>> pageTaskRequests(
            @Valid @ModelAttribute PageQueryTaskDTO queryDTO) {
        return ResultVO.success(taskRequestService.pageTaskRequests(queryDTO));
    }

    /**
     * 创建需求单
     */
    @PostMapping
    @PreAuthorize("hasAuthority('task:write')")
    public ResultVO<TaskRequestVO> createTaskRequest(
            @Valid @RequestBody CreateTaskRequestDTO dto) {
        return ResultVO.success(taskRequestService.createTaskRequest(dto));
    }
}
```

#### 3.2.2 Service 层注解

```java
@Service
@RequiredArgsConstructor
@Slf4j
public class TaskRequestServiceImpl implements TaskRequestService {

    private final AiTaskReqMapper taskReqMapper;
    private final AiTaskHistoryMapper taskHistoryMapper;
    private final TaskRequestConverter converter;
    private final NotificationService notificationService;

    /**
     * 创建需求单
     * 包含：task_no 生成、初始状态设置、历史记录写入
     */
    @Override
    @Transactional(rollbackFor = Exception.class)    // 多表写操作必须加事务
    public TaskRequestVO createTaskRequest(CreateTaskRequestDTO dto) {
        log.info("创建需求单，标题：{}，提交人：{}", dto.getTitle(), dto.getSubmitterName());
        // 业务逻辑实现
    }
}
```

### 3.3 类头部注释规范

所有新建/修改文件的头部 JavaDoc 必须包含以下信息：

```java
/**
 * 【文件用途描述】
 * 例如：AI执行日志写入服务实现，负责校验脱敏状态、计算Token费用、持久化日志记录
 *
 * @author AI（芯智云匠）
 * @date YYYY-MM-DD
 * @module 所属模块（如：任务管理 / 运维监控 / 知识库）
 * @related REQ-MES-AI-YYYYMMDD-XXX（关联需求单编号）
 */
```

### 3.4 方法注释规范

**必须添加注释的场景**：

```java
// 1. 所有 public 方法（Service 接口方法、Controller 方法）
/**
 * 执行任务状态流转
 * 校验当前状态是否允许流转到目标状态（见数据库设计2.3节状态机）
 *
 * @param taskId    需求单 ID
 * @param targetStatus 目标状态
 * @param operator  操作人账号
 * @throws BizException 30001 当状态流转非法时
 */
void transitionTaskStatus(Long taskId, TaskStatusEnum targetStatus, String operator);

// 2. 复杂业务逻辑内嵌注释
public void approveTask(Long taskId, ApproveTaskDTO dto) {
    AiTaskReq task = taskReqMapper.selectById(taskId);

    // 校验状态机：当前必须是 REVIEWING 状态才能审批通过
    validateStatusTransition(task.getStatus(), TaskStatusEnum.APPROVED);

    // 更新状态，同时写入评审记录（两步在同一事务内）
    doApprove(task, dto);
}
```

**不必要注释**（禁止添加无意义注释）：

```java
// ❌ 无意义注释
// 获取任务
AiTaskReq task = taskReqMapper.selectById(taskId);

// ❌ 显而易见的注释
// 返回结果
return ResultVO.success(vo);
```

### 3.5 禁止使用的写法

```java
// ❌ 禁止1：空 catch 块
try {
    taskReqMapper.insert(task);
} catch (Exception e) {
    // 空捕获，绝对禁止
}

// ✅ 正确：记录错误日志并重新抛出
try {
    taskReqMapper.insert(task);
} catch (Exception e) {
    log.error("创建需求单失败，标题：{}，错误：{}", task.getTitle(), e.getMessage(), e);
    throw new BizException(ResultCode.DB_OPERATION_FAILED, "创建需求单失败", e);
}

// ❌ 禁止2：直接 System.out.println
System.out.println("任务创建成功：" + taskNo);

// ✅ 正确：使用 @Slf4j 日志
log.info("需求单创建成功，编号：{}", taskNo);

// ❌ 禁止3：使用 + 拼接 SQL
String sql = "SELECT * FROM ai_task_req WHERE status = '" + status + "'";

// ✅ 正确：MyBatis Plus 条件构造器或 XML 参数绑定
LambdaQueryWrapper<AiTaskReq> wrapper = new LambdaQueryWrapper<AiTaskReq>()
        .eq(AiTaskReq::getStatus, status)
        .eq(AiTaskReq::getIsDeleted, 0);

// ❌ 禁止4：硬编码 IP / 密码 / 数据库连接串
String apiKey = "sk-ant-api03-xxx";
String dbUrl = "jdbc:mysql://192.168.1.100:3306/mes_ai_task";

// ✅ 正确：通过配置文件/环境变量注入
@Value("${ai.gateway.api-key}")
private String apiKey;
```

---

## 四、统一响应与错误码规范

### 4.1 ResultVO 实现

```java
/**
 * 统一 API 响应封装
 * 所有 REST 接口返回值必须使用本类封装，禁止直接返回裸对象或 Map
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResultVO<T> {

    /** 业务状态码，0 表示成功，非 0 表示业务错误 */
    private Integer code;

    /** 提示信息 */
    private String message;

    /** 业务数据 */
    private T data;

    /** 服务端响应时间（ISO 8601，东八区） */
    private String timestamp;

    /** 链路追踪 ID */
    private String requestId;

    private ResultVO(Integer code, String message, T data) {
        this.code = code;
        this.message = message;
        this.data = data;
        this.timestamp = LocalDateTime.now()
                .atZone(ZoneId.of("Asia/Shanghai"))
                .format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        this.requestId = RequestIdHolder.get();  // 从当前线程上下文取
    }

    /** 成功（有数据） */
    public static <T> ResultVO<T> success(T data) {
        return new ResultVO<>(0, "success", data);
    }

    /** 成功（无数据） */
    public static <T> ResultVO<T> success() {
        return new ResultVO<>(0, "success", null);
    }

    /** 业务失败 */
    public static <T> ResultVO<T> fail(ResultCode code) {
        return new ResultVO<>(code.getCode(), code.getMessage(), null);
    }

    /** 业务失败（自定义 message） */
    public static <T> ResultVO<T> fail(ResultCode code, String message) {
        return new ResultVO<>(code.getCode(), message, null);
    }
}
```

### 4.2 ResultCode 枚举（与 API 规范 4.2 节对应）

```java
/**
 * 业务错误码枚举
 * 与 AI-MES-API-2026-001 第四章错误码规范完全对应
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Getter
@AllArgsConstructor
public enum ResultCode {

    // ── 通用错误（1xxxx）──────────────────────────────────────────
    PARAM_MISSING(10001, "缺少必填参数"),
    PARAM_INVALID(10002, "参数格式错误"),
    PARAM_TOO_LONG(10003, "参数超出最大长度"),
    RESOURCE_NOT_FOUND(10004, "资源不存在"),
    RESOURCE_DELETED(10005, "资源已被删除"),
    DUPLICATE_KEY(10006, "唯一键冲突"),
    OPERATION_FORBIDDEN(10007, "当前状态不允许该操作"),
    CONCURRENT_CONFLICT(10008, "并发冲突，请稍后重试"),
    DATA_INTEGRITY_ERROR(10009, "数据完整性校验失败"),

    // ── 鉴权错误（2xxxx）──────────────────────────────────────────
    TOKEN_MISSING(20001, "请求头缺少 Authorization"),
    TOKEN_EXPIRED(20002, "Token 已过期，请重新登录"),
    TOKEN_INVALID(20003, "Token 签名无效"),
    TOKEN_REVOKED(20004, "Token 已被吊销"),
    PERMISSION_DENIED(20005, "权限不足"),
    DOWNLOAD_TOKEN_EXPIRED(20006, "下载 Token 已过期或已使用"),

    // ── 任务模块（3xxxx）──────────────────────────────────────────
    TASK_STATUS_INVALID(30001, "任务状态流转非法"),
    TASK_NOT_REVIEWABLE(30002, "任务不在可评审状态"),
    TASK_NOT_ACCEPTABLE(30003, "任务不在可验收状态"),
    TASK_ALREADY_REVIEWED(30004, "任务已完成评审"),
    TASK_NO_GENERATE_FAIL(30005, "任务编号生成失败，请重试"),
    ACCEPT_CRITERIA_REQUIRED(30006, "提交任务需填写验收标准"),
    EXPORT_NO_DATA(30007, "导出范围内无数据，请调整筛选条件"),
    EXPORT_RANGE_TOO_LARGE(30008, "导出数据量超过上限，请缩小时间范围"),

    // ── 授权模块（4xxxx）──────────────────────────────────────────
    APPROVAL_EXPIRED(40001, "授权已超时，请重新发起"),
    APPROVAL_ALREADY_DECIDED(40002, "授权已处理，无法重复操作"),
    APPROVAL_NOT_PENDING(40003, "授权不在待处理状态"),
    DDL_CHANGE_NEED_DBA(40004, "DDL 变更需 DBA 审批"),

    // ── 部署模块（5xxxx）──────────────────────────────────────────
    DEPLOY_NOT_ACCEPTED(50001, "任务未通过验收，无法发起部署"),
    DEPLOY_ROLLBACK_PLAN_EMPTY(50002, "回退方案不能为空"),
    DEPLOY_ALREADY_APPLIED(50003, "该任务已有待审批的部署申请"),
    DEPLOY_APPROVAL_REQUIRED(50004, "部署需 IT 负责人签批"),

    // ── AI 执行模块（6xxxx）── 安全红线 ───────────────────────────
    EXEC_LOG_NOT_DESENSITIZED(60001, "日志内容未经脱敏处理，拒绝写入"),
    HARDCODE_DETECTED(60002, "代码包含硬编码敏感信息，拒绝提交"),
    SONAR_CRITICAL_EXIST(60003, "SonarQube 存在 Critical 问题，拒绝提交"),
    TOKEN_BUDGET_EXCEEDED(60004, "当日 Token 预算已超限，非紧急任务已暂停"),
    TASK_NOT_RUNNING(60005, "任务不在 AI_RUNNING 状态，无法写入日志"),

    // ── 知识库/断言模块（7xxxx）──────────────────────────────────
    CHUNK_SYNC_PENDING(70001, "向量块尚未同步完成，请稍后查询"),
    ASSERTION_CHANGE_NEED_APPROVAL(70002, "断言库修改需技术负责人审批"),
    ASSERTION_BATCH_RUNNING(70003, "当前已有断言批次在执行中"),
    CRITICAL_ASSERTION_FAILED(70004, "Critical 断言失败，变更已被阻断"),

    // ── 文件处理（8xxxx）──────────────────────────────────────────
    FILE_FORMAT_NOT_SUPPORTED(80001, "不支持的文件格式"),
    FILE_SIZE_EXCEEDED(80002, "文件大小超过限制（最大 50MB）"),
    FILE_COUNT_EXCEEDED(80003, "单次最多上传 5 个文件"),
    FILE_PARSE_FAILED(80004, "文件解析失败，请检查文件是否损坏"),
    FILE_VIRUS_DETECTED(80005, "文件安全扫描未通过"),
    STORAGE_UNAVAILABLE(80006, "文件存储服务暂不可用，请稍后重试"),

    // ── 系统内部（9xxxx）──────────────────────────────────────────
    DB_OPERATION_FAILED(90001, "数据库操作失败"),
    REDIS_OPERATION_FAILED(90002, "缓存操作失败"),
    AI_GATEWAY_ERROR(90003, "AI 网关调用失败"),
    INTERNAL_ERROR(99999, "系统内部错误");

    private final Integer code;
    private final String message;
}
```

### 4.3 分页响应 VO

```java
/**
 * 分页响应封装
 * 对应 API 规范 3.2 节分页响应结构
 */
@Data
@AllArgsConstructor
public class PageVO<T> {

    /** 数据列表 */
    private List<T> list;

    /** 分页信息 */
    private PaginationVO pagination;

    @Data
    @AllArgsConstructor
    public static class PaginationVO {
        /** 当前页（从 1 开始） */
        private Integer page;
        /** 每页条数 */
        private Integer pageSize;
        /** 总记录数 */
        private Long total;
        /** 总页数 */
        private Integer totalPages;
    }

    /** 从 MyBatis Plus IPage 构建 */
    public static <T, R> PageVO<R> from(IPage<T> page, List<R> list) {
        PaginationVO pagination = new PaginationVO(
                (int) page.getCurrent(),
                (int) page.getSize(),
                page.getTotal(),
                (int) page.getPages()
        );
        return new PageVO<>(list, pagination);
    }
}
```

---

## 五、异常处理标准

### 5.1 异常体系设计

```
Exception
└── RuntimeException
    └── BizException（业务异常基类，对应 ResultCode 中的业务错误码）
        ├── TaskStatusInvalidException（任务状态非法）
        ├── ApprovalExpiredException（授权超时）
        ├── PermissionDeniedException（权限不足，由 AOP 抛出）
        └── DesensitizeRequiredException（未脱敏，安全红线）
```

### 5.2 BizException 定义

```java
/**
 * 业务异常基类
 * 所有可预期的业务失败（状态不合法、权限不足、资源不存在等）均通过本类表达，
 * 不应使用 RuntimeException 直接抛出业务错误
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Getter
public class BizException extends RuntimeException {

    /** 业务错误码（对应 ResultCode 枚举） */
    private final ResultCode resultCode;

    /** 额外的错误上下文信息（用于动态错误 message，如资源 ID、字段名） */
    private final String detail;

    public BizException(ResultCode resultCode) {
        super(resultCode.getMessage());
        this.resultCode = resultCode;
        this.detail = null;
    }

    public BizException(ResultCode resultCode, String detail) {
        super(resultCode.getMessage() + "：" + detail);
        this.resultCode = resultCode;
        this.detail = detail;
    }

    public BizException(ResultCode resultCode, String detail, Throwable cause) {
        super(resultCode.getMessage() + "：" + detail, cause);
        this.resultCode = resultCode;
        this.detail = detail;
    }

    /** 快捷构造：资源不存在 */
    public static BizException notFound(String resourceType, Object id) {
        return new BizException(ResultCode.RESOURCE_NOT_FOUND,
                resourceType + "=" + id);
    }

    /** 快捷构造：状态流转非法 */
    public static BizException invalidStatus(String from, String to) {
        return new BizException(ResultCode.TASK_STATUS_INVALID,
                from + " → " + to);
    }
}
```

### 5.3 全局异常处理器

```java
/**
 * 全局异常处理器
 * 统一捕获所有未处理异常，转换为规范的 ResultVO 响应
 * 保证任何情况下 API 均返回规范格式，不暴露系统内部信息
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    /**
     * 处理业务异常（BizException）
     * HTTP 状态码：200（业务失败用 ResultVO.code 区分）
     */
    @ExceptionHandler(BizException.class)
    public ResultVO<?> handleBizException(BizException e, HttpServletRequest request) {
        // INFO 级别记录业务异常（业务失败是正常流程，非系统错误）
        log.info("业务异常 [{}] code={} message={} path={}",
                RequestIdHolder.get(),
                e.getResultCode().getCode(),
                e.getMessage(),
                request.getRequestURI());

        String message = e.getDetail() != null
                ? e.getResultCode().getMessage() + "：" + e.getDetail()
                : e.getResultCode().getMessage();
        return ResultVO.fail(e.getResultCode(), message);
    }

    /**
     * 处理参数校验异常（@Valid 触发）
     * HTTP 状态码：400
     */
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResultVO<?> handleValidationException(MethodArgumentNotValidException e) {
        // 收集所有字段错误，拼接为友好提示
        String errorMsg = e.getBindingResult().getFieldErrors().stream()
                .map(fe -> fe.getField() + " " + fe.getDefaultMessage())
                .collect(Collectors.joining("；"));
        log.warn("请求参数校验失败：{}", errorMsg);
        return ResultVO.fail(ResultCode.PARAM_INVALID, errorMsg);
    }

    /**
     * 处理参数类型转换异常
     * HTTP 状态码：400
     */
    @ExceptionHandler({MethodArgumentTypeMismatchException.class,
                       HttpMessageNotReadableException.class})
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ResultVO<?> handleParamTypeException(Exception e) {
        log.warn("请求参数类型错误：{}", e.getMessage());
        return ResultVO.fail(ResultCode.PARAM_INVALID, "请求参数格式不正确");
    }

    /**
     * 处理权限不足异常
     * HTTP 状态码：403
     */
    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public ResultVO<?> handleAccessDeniedException(AccessDeniedException e,
                                                    HttpServletRequest request) {
        log.warn("权限不足 [{}] path={} user={}",
                RequestIdHolder.get(),
                request.getRequestURI(),
                SecurityContextHolder.getContext().getAuthentication().getName());
        return ResultVO.fail(ResultCode.PERMISSION_DENIED,
                "需要权限：" + extractRequiredPermission(e));
    }

    /**
     * 处理数据库唯一键冲突
     */
    @ExceptionHandler(DuplicateKeyException.class)
    public ResultVO<?> handleDuplicateKeyException(DuplicateKeyException e) {
        log.warn("数据库唯一键冲突：{}", e.getMessage());
        return ResultVO.fail(ResultCode.DUPLICATE_KEY);
    }

    /**
     * 兜底处理：所有未预期异常
     * HTTP 状态码：500
     * 注意：绝不将异常堆栈信息暴露给客户端
     */
    @ExceptionHandler(Exception.class)
    @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
    public ResultVO<?> handleUnexpectedException(Exception e, HttpServletRequest request) {
        // ERROR 级别，含完整堆栈，便于排查
        log.error("系统内部错误 [{}] path={} error={}",
                RequestIdHolder.get(),
                request.getRequestURI(),
                e.getMessage(), e);

        // 返回给客户端：仅告知 requestId，不暴露内部信息
        return ResultVO.fail(ResultCode.INTERNAL_ERROR,
                "请联系运维人员，追踪ID：" + RequestIdHolder.get());
    }
}
```

### 5.4 异常处理规则汇总

| 场景 | 处理方式 | 日志级别 | HTTP 状态码 |
|------|--------|--------|-----------|
| 业务规则不满足（状态非法、资源不存在等） | 抛出 `BizException` | INFO | 200 |
| 入参格式错误（@Valid 失败） | 全局处理器捕获 | WARN | 400 |
| Token 缺失/过期/无效 | JWT 过滤器处理 | WARN | 401 |
| 权限不足 | Spring Security / AOP 处理 | WARN | 403 |
| 数据库唯一键冲突 | 全局处理器捕获 | WARN | 200 |
| 外部 AI API 调用失败 | `try-catch`，抛出 `BizException(AI_GATEWAY_ERROR)` | ERROR | 200 |
| 未捕获的 RuntimeException | 全局兜底处理器 | ERROR | 500 |
| **空 catch 块** | **绝对禁止** | — | — |

---

## 六、日志格式规范

### 6.1 日志框架与配置

- **框架**：SLF4J + Logback（Spring Boot 默认集成）
- **注解**：全部使用 Lombok `@Slf4j`，禁止手动声明 `Logger`

```java
// ✅ 正确
@Slf4j
public class TaskRequestServiceImpl implements TaskRequestService { }

// ❌ 禁止
private static final Logger logger = LoggerFactory.getLogger(TaskRequestServiceImpl.class);
```

### 6.2 日志级别使用规范

| 级别 | 使用场景 | 示例 |
|------|--------|------|
| **ERROR** | 系统错误、外部依赖调用失败、未预期异常，**必须含完整异常堆栈** | 数据库写入失败、AI API 调用异常 |
| **WARN** | 业务规则触发的非预期情况、超时告警、参数校验失败 | Token 接近预算上限、评审超时 |
| **INFO** | 关键业务节点（任务创建/状态变更/授权操作/巡检执行），**不打印敏感数据** | 任务编号生成、状态流转成功 |
| **DEBUG** | 开发调试信息，生产环境**禁止开启** | SQL 查询参数、中间计算结果 |

### 6.3 日志内容规范

#### 6.3.1 必须打印 INFO 的关键节点

```java
// 任务生命周期
log.info("[任务] 需求单创建成功，编号：{}，标题：{}，提交人：{}", taskNo, title, submitterName);
log.info("[任务] 状态变更，编号：{}，{} → {}，操作人：{}", taskNo, fromStatus, toStatus, operator);
log.info("[任务] IT评审完成，编号：{}，结论：{}，评审人：{}", taskNo, result, reviewer);
log.info("[任务] AI开始执行，编号：{}，预估工时：{}小时", taskNo, estimatedHours);
log.info("[任务] AI执行完成，编号：{}，实际工时：{}小时，质量得分：{}", taskNo, actualHours, score);

// 授权网关
log.info("[授权] 人工授权节点创建，任务编号：{}，类型：{}，超时时间：{}", taskNo, gateType, expireAt);
log.info("[授权] 授权操作，任务编号：{}，结论：{}，授权人：{}", taskNo, decision, approverName);

// 巡检
log.info("[巡检] 每日巡检开始，日期：{}", inspectDate);
log.info("[巡检] 每日巡检完成，日期：{}，整体状态：{}，告警数：{}", inspectDate, status, alertCount);

// Token 预算
log.info("[Token] 当日消耗：{}，预算：{}，使用率：{}%",
        todayUsed, budget, (todayUsed * 100 / budget));
log.warn("[Token] 达到降级阈值（250万），知识库检索降级至 Top-3");
log.warn("[Token] 达到暂停阈值（300万），非紧急任务已暂停");

// AI 网关调用
log.info("[AI调用] 任务：{}，阶段：{}，模型：{}，tokens：{}，延迟：{}ms",
        taskNo, stage, model, totalTokens, latencyMs);
```

#### 6.3.2 ERROR 日志规范

```java
// ✅ 正确：含上下文 + 完整异常堆栈
log.error("[AI网关] 调用失败，任务编号：{}，重试次数：{}，错误：{}",
        taskNo, retryCount, e.getMessage(), e);   // 最后一个参数是 Throwable，Logback 自动打印堆栈

// ❌ 错误：丢失堆栈
log.error("[AI网关] 调用失败：" + e.getMessage());  // 堆栈丢失；且使用了字符串拼接

// ❌ 错误：缺少上下文
log.error("发生异常", e);  // 无法定位是哪个任务、哪个阶段
```

#### 6.3.3 日志脱敏要求

打印日志时，**严禁**记录以下原始值：

| 禁止记录的原始值 | 允许的替代写法 |
|--------|--------|
| 用户密码 | 禁止打印，任何情况下 |
| JWT Token 完整值 | 仅打印前 8 位：`token[8位前缀]***` |
| 设备序列号 | 使用脱敏格式：`[DEVICE_SN_***]` |
| 员工工号 | 使用脱敏格式：`[EMP_ID_***]` |
| 内网 IP（非配置类日志） | 使用脱敏格式：`[IP_ADDR_***]` |
| AI API Key | 禁止打印，任何情况下 |

### 6.4 Logback 配置规范

```xml
<!-- logback-spring.xml 关键配置 -->
<configuration>
    <!-- 日志格式：时间 + 级别 + RequestId + 线程 + 类名 + 消息 -->
    <property name="LOG_PATTERN"
              value="%d{yyyy-MM-dd HH:mm:ss.SSS} [%level] [%X{requestId}] [%thread] %logger{36} - %msg%n"/>

    <!-- 控制台输出 -->
    <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
        <encoder><pattern>${LOG_PATTERN}</pattern></encoder>
    </appender>

    <!-- 按日滚动文件输出 -->
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_PATH}/mesai-application.log</file>
        <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
            <fileNamePattern>${LOG_PATH}/mesai-application.%d{yyyy-MM-dd}.%i.log</fileNamePattern>
            <maxFileSize>100MB</maxFileSize>
            <maxHistory>30</maxHistory>  <!-- 保留 30 天 -->
            <totalSizeCap>5GB</totalSizeCap>
        </rollingPolicy>
        <encoder><pattern>${LOG_PATTERN}</pattern></encoder>
    </appender>

    <!-- ERROR 单独记录到 error.log -->
    <appender name="ERROR_FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_PATH}/mesai-error.log</file>
        <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
            <level>ERROR</level>
        </filter>
        <!-- 滚动配置同上，保留 90 天 -->
    </appender>

    <!-- 生产环境：INFO 级别 -->
    <springProfile name="prod">
        <root level="INFO">
            <appender-ref ref="FILE"/>
            <appender-ref ref="ERROR_FILE"/>
        </root>
    </springProfile>

    <!-- 开发环境：DEBUG 级别，控制台输出 -->
    <springProfile name="dev">
        <root level="DEBUG">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>
</configuration>
```

### 6.5 RequestId 链路追踪

```java
/**
 * 请求 ID 管理
 * 每个 HTTP 请求自动生成唯一 RequestId，贯穿请求全生命周期（日志/响应头）
 */
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestIdFilter implements Filter {

    private static final String HEADER_X_REQUEST_ID = "X-Request-Id";
    private static final String MDC_KEY = "requestId";

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        // 优先使用客户端传入的 X-Request-Id，否则服务端生成
        String requestId = Optional.ofNullable(request.getHeader(HEADER_X_REQUEST_ID))
                .filter(s -> !s.isBlank())
                .orElse("req-" + UUID.randomUUID().toString().replace("-", "").substring(0, 16));

        // 写入 MDC（自动注入日志格式的 %X{requestId}）
        MDC.put(MDC_KEY, requestId);
        RequestIdHolder.set(requestId);
        // 回传给客户端
        response.setHeader(HEADER_X_REQUEST_ID, requestId);

        try {
            chain.doFilter(req, res);
        } finally {
            // 必须清理，防止线程池复用时污染
            MDC.remove(MDC_KEY);
            RequestIdHolder.clear();
        }
    }
}
```

---

## 七、数据访问层规范（MyBatis Plus）

### 7.1 Entity 规范

```java
/**
 * 需求单实体类（对应表 ai_task_req）
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Data
@TableName("ai_task_req")
public class AiTaskReq {

    /** 主键（BIGINT AUTO_INCREMENT） */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 任务编号 REQ-MES-AI-YYYYMMDD-NNN（由 Redis 分布式递增生成，唯一索引） */
    private String taskNo;

    /** 需求标题，不超过 50 汉字 */
    private String title;

    /** 任务类型：FEAT/FIX/REPORT/QUERY/API/BUG/PERF */
    private String taskType;

    /** 优先级：1-紧急 2-高 3-中 4-低 */
    private Integer priority;

    /** 状态，见 TaskStatusEnum */
    private String status;

    // ... 其他字段

    /** 逻辑删除（0-有效 1-已删除），MyBatis Plus @TableLogic 自动处理 */
    @TableLogic
    private Integer isDeleted;

    /** 创建时间，由数据库 CURRENT_TIMESTAMP 填充，Java 层禁止手动赋值 */
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;

    /** 最后更新时间，自动更新 */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
```

### 7.2 Mapper 规范

```java
/**
 * 需求单 Mapper 接口
 * 继承 BaseMapper，获得基础 CRUD 能力
 * 复杂查询在对应 XML 中实现
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Mapper
public interface AiTaskReqMapper extends BaseMapper<AiTaskReq> {

    /**
     * 分页查询需求单（含关联评审记录），复杂 JOIN 查询在 XML 中实现
     *
     * @param page    分页参数（MyBatis Plus IPage）
     * @param queryVO 查询条件
     * @return 分页结果（包含评审人信息）
     */
    IPage<TaskRequestWithReviewVO> pageWithReview(IPage<?> page,
                                                   @Param("q") PageQueryTaskDTO queryVO);

    /**
     * 按状态统计各状态需求单数量（看板计数用）
     *
     * @return 状态 → 数量 映射
     */
    List<TaskStatusCountVO> countByStatus();
}
```

对应的 XML（`AiTaskReqMapper.xml`）：

```xml
<!-- 严格遵循：禁止 SELECT *，明确列出所有查询字段 -->
<select id="pageWithReview" resultType="TaskRequestWithReviewVO">
    SELECT
        t.id,
        t.task_no      AS taskNo,
        t.title,
        t.task_type    AS taskType,
        t.priority,
        t.status,
        t.submitter_name AS submitterName,
        t.dept,
        t.module,
        t.created_at   AS createdAt,
        t.updated_at   AS updatedAt,
        r.reviewer_name    AS reviewerName,
        r.review_result    AS reviewResult,
        r.review_time      AS reviewTime
    FROM ai_task_req t
    LEFT JOIN ai_review_record r ON t.id = r.task_id
    WHERE t.is_deleted = 0
    <if test="q.status != null and q.status != ''">
        AND t.status = #{q.status}
    </if>
    <if test="q.priority != null">
        AND t.priority = #{q.priority}
    </if>
    <if test="q.dept != null and q.dept != ''">
        AND t.dept = #{q.dept}
    </if>
    <if test="q.keyword != null and q.keyword != ''">
        AND (t.title LIKE CONCAT('%', #{q.keyword}, '%')
          OR t.task_no LIKE CONCAT('%', #{q.keyword}, '%')
          OR t.submitter_name LIKE CONCAT('%', #{q.keyword}, '%'))
    </if>
    ORDER BY t.updated_at DESC
</select>
```

### 7.3 禁止在 Mapper 中使用的写法

```xml
<!-- ❌ 禁止 SELECT * -->
<select id="getTask">SELECT * FROM ai_task_req WHERE id = #{id}</select>

<!-- ❌ 禁止字符串拼接 SQL（SQL 注入风险） -->
<select id="search">
    SELECT id, title FROM ai_task_req WHERE status = '${status}'
</select>

<!-- ✅ 正确：使用 #{} 参数绑定 -->
<select id="search">
    SELECT id, title FROM ai_task_req WHERE status = #{status}
</select>
```

### 7.4 条件构造器使用规范

```java
// ✅ 推荐：LambdaQueryWrapper（类型安全，避免字段名拼写错误）
LambdaQueryWrapper<AiTaskReq> wrapper = new LambdaQueryWrapper<AiTaskReq>()
        .eq(AiTaskReq::getIsDeleted, 0)
        .eq(StringUtils.hasText(status), AiTaskReq::getStatus, status)
        .ge(startDate != null, AiTaskReq::getCreatedAt, startDate)
        .orderByDesc(AiTaskReq::getUpdatedAt);

// ❌ 禁止：QueryWrapper 字符串字段名（容易拼写错误，重构时无提示）
new QueryWrapper<AiTaskReq>().eq("is_delete", 0).eq("status", status);
```

### 7.5 批量写操作规范

```java
/**
 * 批量写入执行日志
 * 强制分批执行，每批不超过 500 条（CLAUDE.md 3.3节 SQL规范）
 */
public void batchInsertExecLogs(List<AiExecLog> logs) {
    if (CollectionUtils.isEmpty(logs)) {
        return;
    }
    // 分批处理
    Lists.partition(logs, TaskConstants.BATCH_MAX_SIZE)
            .forEach(batch -> {
                log.info("[日志] 批量写入执行日志，本批数量：{}", batch.size());
                execLogMapper.insertBatchSomeColumn(batch);  // MP 批量插入
            });
    log.info("[日志] 执行日志批量写入完成，总数量：{}", logs.size());
}
```

---

## 八、事务管理规范

### 8.1 事务边界约定

**事务加在 Service 实现层，不加在 Controller 层、Mapper 层。**

```java
// ✅ 正确：多表写操作，Service 层加 @Transactional
@Transactional(rollbackFor = Exception.class)
public TaskRequestVO createTaskRequest(CreateTaskRequestDTO dto) {
    // 1. 生成任务编号（Redis + 降级DB）
    String taskNo = taskNoGenerator.generate();

    // 2. 创建需求单主记录
    AiTaskReq task = converter.toEntity(dto);
    task.setTaskNo(taskNo);
    task.setStatus(TaskStatusEnum.DRAFT.name());
    taskReqMapper.insert(task);

    // 3. 写入操作历史（与上面在同一事务中）
    AiTaskHistory history = buildHistory(task, "CREATE", null, TaskStatusEnum.DRAFT.name());
    taskHistoryMapper.insert(history);

    log.info("[任务] 需求单创建成功，编号：{}，标题：{}", taskNo, dto.getTitle());
    return converter.toVO(task);
}

// ❌ 禁止：只读查询加 @Transactional（性能浪费）
@Transactional    // 错误！查询不需要事务
public TaskRequestVO getTaskById(Long id) { ... }
```

### 8.2 事务传播规范

| 场景 | 传播行为 | 注解写法 |
|------|--------|--------|
| 多表写操作（标准场景） | `REQUIRED`（默认） | `@Transactional(rollbackFor = Exception.class)` |
| 独立记录审计日志（不随外层事务回滚） | `REQUIRES_NEW` | `@Transactional(propagation = Propagation.REQUIRES_NEW)` |
| 只读查询 | 不加注解 | — |
| 需要手动控制提交/回滚 | 编程式事务 | `TransactionTemplate` |

### 8.3 事务回滚规范

```java
// 强制指定 rollbackFor = Exception.class
// 原因：Spring 默认只对 RuntimeException 回滚，
//       IOException 等受检异常不会自动回滚，可能导致数据不一致
@Transactional(rollbackFor = Exception.class)
public void deployTask(Long taskId, DeployRequestDTO dto) {
    // ...
}

// 审计日志使用独立事务，即使外层事务回滚，审计记录也要保留
@Transactional(propagation = Propagation.REQUIRES_NEW, rollbackFor = Exception.class)
public void writeAuditLog(AuditLogDTO dto) {
    auditLogMapper.insert(converter.toEntity(dto));
}
```

---

## 九、输入校验规范

### 9.1 Bean Validation 注解使用

```java
/**
 * 创建需求单请求 DTO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Data
public class CreateTaskRequestDTO {

    /** 需求标题，必填，不超过 100 字符（对应表字段 VARCHAR(100)） */
    @NotBlank(message = "需求标题不能为空")
    @Size(max = 100, message = "需求标题不超过 100 个字符")
    private String title;

    /** 任务类型，必填，枚举值校验 */
    @NotBlank(message = "任务类型不能为空")
    @Pattern(regexp = "FEAT|FIX|REPORT|QUERY|API|BUG|PERF",
             message = "任务类型只能是：FEAT/FIX/REPORT/QUERY/API/BUG/PERF")
    private String taskType;

    /** 优先级：1-紧急 2-高 3-中 4-低 */
    @NotNull(message = "优先级不能为空")
    @Min(value = 1, message = "优先级最小为 1（紧急）")
    @Max(value = 4, message = "优先级最大为 4（低）")
    private Integer priority;

    /** 期望完成日期，不能早于今天+3个工作日 */
    @NotNull(message = "期望完成日期不能为空")
    @Future(message = "期望完成日期必须是未来日期")
    private LocalDate expectedFinishDate;

    /** 验收标准（JSON 数组），必填，最少 3 条 */
    @NotBlank(message = "验收标准不能为空")
    private String acceptCriteria;

    /** 功能描述 */
    @Size(max = 5000, message = "功能描述不超过 5000 字符")
    private String funcDesc;
}
```

### 9.2 Controller 层触发校验

```java
// @Valid 触发 Bean Validation，MethodArgumentNotValidException 由全局处理器捕获
@PostMapping
public ResultVO<TaskRequestVO> createTaskRequest(
        @Valid @RequestBody CreateTaskRequestDTO dto) {
    return ResultVO.success(taskRequestService.createTaskRequest(dto));
}

// GET 请求参数校验
@GetMapping
public ResultVO<PageVO<TaskRequestVO>> pageTaskRequests(
        @Valid @ModelAttribute PageQueryTaskDTO queryDTO) {
    return ResultVO.success(taskRequestService.pageTaskRequests(queryDTO));
}
```

### 9.3 业务层二次校验

Bean Validation 处理格式校验，业务规则校验在 Service 层进行：

```java
public void approveTask(Long taskId, ApproveTaskDTO dto) {
    // 1. 资源存在性校验
    AiTaskReq task = taskReqMapper.selectById(taskId);
    if (task == null || task.getIsDeleted() == 1) {
        throw BizException.notFound("需求单", taskId);
    }

    // 2. 业务状态机校验
    if (!TaskStatusEnum.REVIEWING.name().equals(task.getStatus())) {
        throw new BizException(ResultCode.TASK_NOT_REVIEWABLE,
                "当前状态：" + task.getStatus());
    }

    // 3. 重复操作校验
    AiReviewRecord existing = reviewRecordMapper.selectByTaskId(taskId);
    if (existing != null && !"PENDING_INFO".equals(existing.getReviewResult())) {
        throw new BizException(ResultCode.TASK_ALREADY_REVIEWED);
    }

    // 通过所有校验，执行业务逻辑
    doApprove(task, dto);
}
```

---

## 十、安全编码要求

### 10.1 SQL 注入防护（强制）

```java
// ✅ 正确：MyBatis Plus #{} 参数绑定
LambdaQueryWrapper<AiTaskReq> wrapper = new LambdaQueryWrapper<AiTaskReq>()
        .like(AiTaskReq::getTitle, keyword);

// ✅ 正确：XML 中 #{} 绑定
WHERE title LIKE CONCAT('%', #{keyword}, '%')

// ❌ 绝对禁止：${} 字符串替换（SQL 注入漏洞）
WHERE title LIKE '%${keyword}%'

// ❌ 绝对禁止：Java 字符串拼接 SQL
String sql = "WHERE title LIKE '%" + keyword + "%'";
```

**模糊查询中的特殊字符处理**（防止 LIKE 注入）：

```java
// 对用户输入的关键词转义 SQL 特殊字符
private String escapeLikePattern(String keyword) {
    if (keyword == null) return null;
    return keyword.replace("\\", "\\\\")
                  .replace("%", "\\%")
                  .replace("_", "\\_");
}
```

### 10.2 XSS 防护

```java
// 全局 Jackson 配置：HTML 转义
@Configuration
public class JacksonConfig {
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer customizer() {
        return builder -> builder
                // 禁止将 HTML 特殊字符序列化为 Unicode 转义
                // （使用 Content-Security-Policy 头 + 前端 v-html 替代）
                .featuresToDisable(MapperFeature.USE_ANNOTATIONS);
    }
}

// 文本类字段在写入数据库前，进行基础清理
private String sanitizeInput(String input) {
    if (input == null) return null;
    // 移除控制字符
    return input.replaceAll("[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f]", "");
}
```

### 10.3 文件上传安全

```java
/**
 * 文件上传安全校验
 * 在文件写入存储前执行，所有校验失败均抛出 BizException
 */
private void validateUploadFile(MultipartFile file) {
    // 1. 文件大小校验（≤ 50MB）
    if (file.getSize() > 50 * 1024 * 1024) {
        throw new BizException(ResultCode.FILE_SIZE_EXCEEDED,
                file.getOriginalFilename());
    }

    // 2. 文件格式校验（白名单，不信任 MIME Type，检查文件头魔数）
    String originalName = file.getOriginalFilename();
    String extension = FilenameUtils.getExtension(originalName).toLowerCase();
    Set<String> allowed = Set.of("pdf", "md", "docx", "xlsx", "txt");
    if (!allowed.contains(extension)) {
        throw new BizException(ResultCode.FILE_FORMAT_NOT_SUPPORTED, extension);
    }

    // 3. 文件名安全处理（防路径穿越）
    String safeName = sanitizeFileName(originalName);
    if (!safeName.equals(originalName)) {
        log.warn("[文件上传] 文件名包含非法字符，已进行安全处理：{} → {}", originalName, safeName);
    }
}

private String sanitizeFileName(String filename) {
    // 移除路径分隔符、`.\.`序列、控制字符
    return filename.replaceAll("[/\\\\:*?\"<>|\\x00-\\x1f]", "_");
}
```

### 10.4 JWT 安全规范

```java
/**
 * JWT 工具类
 * 密钥从 HashiCorp Vault（或 KMS）注入，禁止硬编码
 */
@Component
@Slf4j
public class JwtUtil {

    /** 从配置文件/Vault 注入，禁止硬编码 */
    @Value("${security.jwt.secret}")
    private String secret;

    @Value("${security.jwt.access-token-expire-seconds:28800}")   // 默认 8 小时
    private long accessTokenExpireSeconds;

    @Value("${security.jwt.refresh-token-expire-seconds:604800}")  // 默认 7 天
    private long refreshTokenExpireSeconds;

    /**
     * 生成 AccessToken（HMAC-SHA256 签名）
     */
    public String generateAccessToken(UserDetail userDetail) {
        return Jwts.builder()
                .setSubject(userDetail.getUsername())
                .claim("role", userDetail.getRole())
                .claim("userId", userDetail.getUserId())
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + accessTokenExpireSeconds * 1000))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    private SecretKey getSigningKey() {
        return Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }

    /**
     * 解析 Token，失败抛出对应 BizException
     */
    public Claims parseToken(String token) {
        try {
            return Jwts.parserBuilder()
                    .setSigningKey(getSigningKey())
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
        } catch (ExpiredJwtException e) {
            throw new BizException(ResultCode.TOKEN_EXPIRED);
        } catch (JwtException e) {
            throw new BizException(ResultCode.TOKEN_INVALID);
        }
    }
}
```

### 10.5 敏感配置管理规范

```yaml
# application-prod.yml（生产环境配置）
# 所有敏感项通过 ${ENV_VAR} 从环境变量注入，禁止写死值
# 双数据源说明：
#   datasource（主）→ AI 平台自建 MySQL 8.x（可读写）
#   mes-datasource（从）→ MES 系统 PostgreSQL 15.x（只读，禁止写操作）

spring:
  # ── AI 平台主数据源（MySQL 8.x，可读写）─────────────────────
  datasource:
    url: ${DB_URL}                    # ❌ 禁止：jdbc:mysql://192.168.x.x:3306/...
    username: ${DB_USERNAME}          # ❌ 禁止：mesai_user
    password: ${DB_PASSWORD}          # ❌ 禁止：mypassword123
    driver-class-name: com.mysql.cj.jdbc.Driver

  redis:
    host: ${REDIS_HOST}
    port: ${REDIS_PORT}
    password: ${REDIS_PASSWORD}

security:
  jwt:
    secret: ${JWT_SECRET}             # 256位随机密钥，存储于 Vault

ai:
  gateway:
    api-key: ${CLAUDE_API_KEY}        # ❌ 禁止：sk-ant-api03-xxx
    webhook-url: ${WECHAT_WEBHOOK_URL}  # 企业微信 Webhook

logging:
  file:
    path: ${LOG_PATH:/var/log/mesai}

# ── MES 系统只读数据源（PostgreSQL 15.x，禁止写操作）──────────
# 注意：本数据源仅供 AI 平台读取 MES 业务数据用于 RAG 知识库建设
#       所有通过此数据源发出的 SQL 必须为 SELECT，严禁 INSERT/UPDATE/DELETE/DDL
#       账号：itsm_readonly（无 CREATE 权限，已通过 T1-1-5 验收验证）
mes:
  datasource:
    url: ${MES_DB_URL}                # jdbc:postgresql://<host>:5432/itsm_dev
    username: ${MES_DB_USER}          # itsm_readonly
    password: ${MES_DB_PASS}
    driver-class-name: org.postgresql.Driver
    hikari:
      maximum-pool-size: 5            # MES DB 为只读连接，连接池控制在较小值
      minimum-idle: 2
      connection-timeout: 10000
      idle-timeout: 300000
      read-only: true                 # HikariCP 级别只读保护，防止误写
```

**MES 只读数据源对应的 Spring Bean 配置要点**（在 `config/MesDataSourceConfig.java` 中实现）：

```java
/**
 * MES 系统只读数据源配置
 * 独立于 AI 平台主数据源，使用 @Qualifier("mesDataSource") 区分
 * 对应环境变量：MES_DB_URL / MES_DB_USER / MES_DB_PASS
 *
 * 安全约束：
 *   - HikariCP readOnly=true，防止误操作写入 MES 库
 *   - 对应 Mapper 使用 @DS("mes") 注解（dynamic-datasource-spring-boot-starter）
 *   - 禁止在 MES 数据源上执行任何 INSERT/UPDATE/DELETE/DDL
 *
 * @author AI
 * @date 2026-04-12
 * 关联需求单: T1-1-5（测试环境验证通过）
 */
@Configuration
public class MesDataSourceConfig {

    @Bean("mesDataSource")
    @ConfigurationProperties(prefix = "mes.datasource")
    public DataSource mesDataSource() {
        return DataSourceBuilder.create()
                .type(HikariDataSource.class)
                .build();
    }

    @Bean("mesJdbcTemplate")
    public JdbcTemplate mesJdbcTemplate(@Qualifier("mesDataSource") DataSource ds) {
        JdbcTemplate template = new JdbcTemplate(ds);
        // 强制只读：超时设置 5s，防止慢查询影响 AI 平台主业务
        template.setQueryTimeout(5);
        return template;
    }
}
```

### 10.6 PII 脱敏层接口规范

```java
/**
 * PII 脱敏处理器
 * 所有发往外部 AI API 的内容，强制经过本处理器
 * 参见技术方案 9.2 节脱敏规则
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
@Component
@Slf4j
public class PiiDesensitizer {

    // 脱敏规则（正则表达式列表）
    private static final List<DesensitizeRule> RULES = List.of(
        new DesensitizeRule("设备序列号",
                Pattern.compile("[A-Z]{2}\\d{8,12}"), "[DEVICE_SN_***]"),
        new DesensitizeRule("员工工号",
                Pattern.compile("EMP\\d{6}"), "[EMP_ID_***]"),
        new DesensitizeRule("生产批次号",
                Pattern.compile("LOT[A-Z0-9]{10,16}"), "[LOT_NO_***]"),
        new DesensitizeRule("内网IP",
                Pattern.compile("192\\.168\\.\\d{1,3}\\.\\d{1,3}"), "[IP_ADDR_***]"),
        new DesensitizeRule("数据库连接串",
                Pattern.compile("jdbc:mysql://[^\\s\"']+"), "[DB_CONN_***]"),
        new DesensitizeRule("身份证号",
                Pattern.compile("\\d{17}[\\dXx]"), "[ID_CARD_***]")
    );

    /**
     * 对文本进行脱敏处理
     * 同时写入脱敏审计日志
     *
     * @param content   待脱敏内容
     * @param context   调用上下文（任务编号等，用于审计日志）
     * @return 脱敏后的内容
     */
    public String desensitize(String content, String context) {
        if (content == null || content.isBlank()) return content;

        String result = content;
        int totalReplaced = 0;

        for (DesensitizeRule rule : RULES) {
            Matcher matcher = rule.pattern().matcher(result);
            long count = matcher.results().count();
            if (count > 0) {
                result = rule.pattern().matcher(result).replaceAll(rule.replacement());
                totalReplaced += count;
                log.info("[脱敏] 发现并替换 {}，数量：{}，上下文：{}", rule.name(), count, context);
            }
        }

        // 厂区编号：从白名单配置中匹配（正则无法穷举）
        result = replaceFromWhitelist(result, context);

        if (totalReplaced > 0) {
            // 写入脱敏审计日志（异步，独立事务）
            auditService.writeDesensitizeLog(context, totalReplaced,
                    DigestUtils.sha256Hex(content));
        }

        return result;
    }

    /**
     * 强制校验：确认内容已脱敏（写入 ai_exec_log 前调用）
     * 若仍检测到敏感信息，抛出安全异常并阻断写入
     */
    public void assertDesensitized(String content, String taskNo) {
        for (DesensitizeRule rule : RULES) {
            if (rule.pattern().matcher(content).find()) {
                log.error("[安全红线] 内容未经脱敏处理，阻断写入！任务：{}，规则：{}",
                        taskNo, rule.name());
                throw new BizException(ResultCode.EXEC_LOG_NOT_DESENSITIZED,
                        "发现未脱敏的" + rule.name());
            }
        }
    }

    private record DesensitizeRule(String name, Pattern pattern, String replacement) {}
}
```

### 10.7 越权防护规范

```java
/**
 * 资源所有权校验
 * BUSINESS_USER 角色只能查看/操作自己提交的任务，
 * IT及以上角色可查看所有任务
 */
private void assertTaskOwnership(AiTaskReq task, UserDetail currentUser) {
    if ("BUSINESS_USER".equals(currentUser.getRole())
            && !currentUser.getUserId().equals(task.getSubmitterId())) {
        log.warn("[越权] 用户 {} 尝试访问他人任务 {}",
                currentUser.getUsername(), task.getTaskNo());
        throw new BizException(ResultCode.PERMISSION_DENIED,
                "您只能访问自己提交的需求单");
    }
}
```

---

## 十一、前端编码规范（Vue 3）

### 11.1 组件结构规范

```vue
<!-- ✅ 标准 Vue 3 Composition API 组件结构 -->
<!-- 文件名：task-request-list.vue（kebab-case） -->
<!-- 组件名：TaskRequestList（PascalCase） -->

<template>
  <!-- 模板根节点：单一根元素 -->
  <div class="task-request-list">
    <!-- 组件代码 -->
  </div>
</template>

<script setup lang="ts">
/**
 * 需求单列表组件
 * 展示任务看板，支持状态筛选和搜索
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 */
import { ref, reactive, onMounted } from 'vue'
import { getTaskList, exportTasks } from '@/api/task'  // 统一通过 /api 目录调用
import { useUserStore } from '@/stores/user'
import type { TaskRequest, PageQuery } from '@/types/task'

// Props 定义（明确类型）
const props = defineProps<{
  status?: string
  dept?: string
}>()

// Emits 定义
const emit = defineEmits<{
  (e: 'refresh'): void
  (e: 'select', task: TaskRequest): void
}>()

// 响应式状态
const loading = ref(false)
const taskList = ref<TaskRequest[]>([])
const pagination = reactive({ page: 1, pageSize: 20, total: 0 })

// 查询条件
const queryForm = reactive<PageQuery>({
  status: props.status ?? '',
  keyword: '',
  page: 1,
  pageSize: 20
})

// 方法
const loadTaskList = async () => {
  loading.value = true
  try {
    const res = await getTaskList(queryForm)
    taskList.value = res.data.list
    Object.assign(pagination, res.data.pagination)
  } finally {
    loading.value = false
  }
}

onMounted(loadTaskList)
</script>

<style scoped>
/* 样式使用 scoped，避免全局污染 */
.task-request-list { }
</style>
```

### 11.2 API 封装层规范（禁止组件直接调用 axios）

```typescript
// src/api/task.ts
// 所有 API 调用必须通过 /api 目录的封装层，组件禁止直接调用 axios

import request from '@/utils/request'   // 统一 axios 实例（含拦截器）
import type { TaskRequest, CreateTaskDTO, PageQuery, PageResult } from '@/types/task'

/**
 * 分页查询需求单列表
 */
export const getTaskList = (params: PageQuery) =>
  request.get<PageResult<TaskRequest>>('/tasks', { params })

/**
 * 创建需求单
 */
export const createTask = (data: CreateTaskDTO) =>
  request.post<TaskRequest>('/tasks', data)

/**
 * 获取需求单详情
 */
export const getTaskDetail = (id: number) =>
  request.get<TaskRequest>(`/tasks/${id}`)

/**
 * 更新需求单状态
 */
export const updateTaskStatus = (id: number, data: { status: string; remark?: string }) =>
  request.put<void>(`/tasks/${id}/status`, data)

/**
 * 导出任务列表（Excel）
 * 返回 Blob，由调用方触发下载
 */
export const exportTaskList = (params: PageQuery) =>
  request.get('/tasks/export', {
    params,
    responseType: 'blob',
    headers: { Accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
  })
```

### 11.3 统一 axios 封装（含 Token 注入和错误处理）

```typescript
// src/utils/request.ts
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,  // 从环境变量注入，禁止硬编码 IP
  timeout: 30000
})

// 请求拦截：注入 Token
request.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.token) {
    config.headers['Authorization'] = `Bearer ${userStore.token}`
  }
  // 生成 requestId 便于链路追踪
  config.headers['X-Request-Id'] = `req-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`
  return config
})

// 响应拦截：统一处理业务错误码
request.interceptors.response.use(
  response => {
    const data = response.data

    // 文件下载直接返回
    if (response.config.responseType === 'blob') return response

    // 业务失败（code !== 0）
    if (data.code !== 0) {
      ElMessage.error(data.message || '操作失败')

      // Token 相关错误：跳转登录页
      if ([20001, 20002, 20003, 20004].includes(data.code)) {
        useUserStore().clearToken()
        router.push('/login')
      }

      return Promise.reject(new Error(data.message))
    }

    return data  // 返回 ResultVO，调用方取 .data
  },
  error => {
    // HTTP 层面的错误（401/403/500 等）
    if (error.response?.status === 401) {
      useUserStore().clearToken()
      router.push('/login')
    }
    const msg = error.response?.data?.message || error.message || '网络错误'
    ElMessage.error(msg)
    return Promise.reject(error)
  }
)

export default request
```

### 11.4 数据修改二次确认规范

所有涉及数据修改（增删改）的操作，**必须弹出确认对话框**：

```vue
<template>
  <!-- ✅ 正确：删除操作有二次确认 -->
  <el-button type="danger" @click="handleDelete(row)">删除</el-button>
</template>

<script setup>
import { ElMessageBox } from 'element-plus'

const handleDelete = async (task: TaskRequest) => {
  try {
    await ElMessageBox.confirm(
      `确认删除需求单「${task.title}」（编号：${task.taskNo}）？此操作不可恢复。`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )
    await deleteTask(task.id)
    ElMessage.success('删除成功')
    emit('refresh')
  } catch {
    // 用户点击取消，正常流程，不做处理
  }
}
</script>
```

### 11.5 前端类型定义规范

```typescript
// src/types/task.ts
// 所有接口数据类型在 /types 目录统一定义

export interface TaskRequest {
  id: number
  taskNo: string          // REQ-MES-AI-YYYYMMDD-NNN
  title: string
  taskType: 'FEAT' | 'FIX' | 'REPORT' | 'QUERY' | 'API' | 'BUG' | 'PERF'
  priority: 1 | 2 | 3 | 4
  status: TaskStatus
  submitterName: string
  dept: string
  reviewerName?: string
  reviewResult?: 'APPROVED' | 'REJECTED' | 'PENDING_INFO'
  createdAt: string       // ISO 8601
  updatedAt: string
}

export type TaskStatus =
  | 'DRAFT'
  | 'SUBMITTED'
  | 'REVIEWING'
  | 'APPROVED'
  | 'REJECTED'
  | 'AI_RUNNING'
  | 'PENDING_REVIEW'
  | 'ACCEPTED'
  | 'DEPLOYING'
  | 'CLOSED'
  | 'ROLLBACK'
  | 'FAILED'
```

---

## 十二、SQL 编写规范

### 12.1 查询规范

```sql
-- ✅ 正确：明确列出查询字段，禁止 SELECT *
SELECT
    t.id,
    t.task_no,
    t.title,
    t.status,
    t.priority,
    t.submitter_name,
    t.dept,
    t.created_at
FROM ai_task_req t
WHERE t.is_deleted = 0
  AND t.status = #{status}
ORDER BY t.updated_at DESC
LIMIT #{offset}, #{pageSize};

-- ❌ 禁止 SELECT *（浪费带宽、破坏索引覆盖扫描）
SELECT * FROM ai_task_req WHERE status = #{status};
```

### 12.2 超过 3 张表 JOIN 的查询：必须附执行计划说明

```sql
-- 任务详情页：多表 JOIN 查询
-- 执行计划分析：
--   ai_task_req：主驱动表，使用 PRIMARY KEY 查询（期望 type=const）
--   ai_review_record：task_id 有唯一索引，LEFT JOIN 后 type=eq_ref
--   ai_exec_log：task_id 有索引，GROUP BY 聚合，注意数据量控制（加 LIMIT 子查询）
-- 预计执行时间：< 50ms（测试环境验证）
SELECT
    t.id,
    t.task_no,
    t.title,
    t.status,
    r.reviewer_name,
    r.review_result,
    d.deploy_result,
    LOG.log_count
FROM ai_task_req t
LEFT JOIN ai_review_record r ON t.id = r.task_id
LEFT JOIN ai_deploy_record d ON t.id = d.task_id
LEFT JOIN (
    SELECT task_id, COUNT(*) AS log_count
    FROM ai_exec_log
    WHERE task_id = #{taskId}
) LOG ON t.id = LOG.task_id
WHERE t.id = #{taskId}
  AND t.is_deleted = 0;
```

### 12.3 慢 SQL 阈值与优化要求

- 执行时间 **> 2 秒**：触发巡检告警，须在当日提交优化方案
- 执行时间 **> 500ms**：在代码 Review 时标记，下个 Sprint 优化
- 新增索引：必须在变更记录中注明原因和预期效果，经 DBA 审核

```sql
-- 新增索引示例（提交时须说明原因）
-- 原因：任务列表页按状态+部门+时间组合查询频繁，原来 ALL 全表扫描 50ms+
-- 预期：使用复合索引后降至 < 5ms，覆盖率 index 类型
-- EXPLAIN 验证结果：type=ref, key=idx_task_req_status_dept_time, rows=23
CREATE INDEX idx_task_req_status_dept_time
    ON ai_task_req (status, dept, updated_at)
    COMMENT '支持任务列表按状态+部门+时间的组合查询';
```

### 12.4 分页查询规范

```sql
-- ✅ 正确：使用子查询优化深分页（数据量大时避免 OFFSET 扫描大量数据）
SELECT t.*
FROM ai_task_req t
INNER JOIN (
    SELECT id FROM ai_task_req
    WHERE is_deleted = 0
    ORDER BY updated_at DESC
    LIMIT #{offset}, #{pageSize}
) ids ON t.id = ids.id;

-- ⚠️ 注意：当 offset 较小（<1000）时直接 LIMIT OFFSET 即可，无需子查询优化
```

---

## 十三、Git 工作流与提交规范

### 13.1 分支策略

```
main          ← 正式环境（受保护，禁止直接推送，仅通过 MR 合并）
  │
develop       ← 测试环境集成分支（受保护，功能分支 MR 合并至此）
  │
  ├── feature/REQ-MES-AI-20260415-003-工单状态流转功能   ← 功能开发
  ├── fix/REQ-MES-AI-20260416-005-工单查询慢SQL优化      ← 缺陷修复
  ├── test/断言库基准测试验证                             ← 测试分支
  └── hotfix/生产紧急修复-XXX                            ← 紧急修复（从 main 拉出）
```

**分支命名规则**：

| 分支类型 | 命名格式 | 示例 |
|--------|--------|------|
| 功能开发 | `feature/{需求单编号}-{简短描述}` | `feature/REQ-MES-AI-20260415-003-设备点检功能` |
| 缺陷修复 | `fix/{需求单编号}-{简短描述}` | `fix/REQ-MES-AI-20260416-005-慢SQL优化` |
| 热修复 | `hotfix/{日期}-{描述}` | `hotfix/20260420-工单状态回退Bug` |
| 文档更新 | `docs/{描述}` | `docs/更新接口文档` |

### 13.2 提交信息格式

```
[REQ-MES-AI-YYYYMMDD-XXX] <类型>: <简短描述>（≤50字）

<可选：详细说明，72字换行>

<可选：Breaking Change 说明>
```

**类型枚举**：

| 类型 | 含义 | 使用场景 |
|------|------|--------|
| `feat` | 新功能 | 实现需求单中的功能点 |
| `fix` | 缺陷修复 | 修复测试/生产发现的 Bug |
| `refactor` | 重构 | 不影响功能的代码结构优化 |
| `perf` | 性能优化 | 慢 SQL 优化、接口响应时间改进 |
| `docs` | 文档更新 | 接口文档、使用说明更新 |
| `test` | 测试用例 | 新增/修改单元测试、集成测试 |
| `chore` | 构建/配置 | pom.xml 调整、CI 配置修改 |
| `security` | 安全修复 | 安全漏洞修复（优先级最高） |

**正确示例**：

```
[REQ-MES-AI-20260415-003] feat: 新增设备点检记录功能（含前端页面和后端接口）

实现点检记录的CRUD操作，包括：
- 新增 EquipmentCheckController 和对应 Service
- 前端新增 equipment-check-list.vue 页面
- 单元测试覆盖率 83%，SonarQube 0 Critical

Breaking Change: 无
```

**错误示例**：

```
fix: fix bug           ← 无需求单编号，无具体描述
update: 更新代码       ← 类型不规范，描述无意义
[REQ001] feat: 新增工单管理和设备管理和报表功能  ← 混合多个需求
```

### 13.3 MR（Merge Request）规范

- MR 标题格式：`[REQ-MES-AI-YYYYMMDD-XXX] 功能描述`
- MR 描述必须包含：变更说明、测试情况、影响范围、回退方案
- 合并至 `develop` 需要：TL 或 AE 至少 1 人 Approve
- 合并至 `main` 需要：TL Approve + ITM 确认

---

## 十四、单元测试规范

### 14.1 测试框架

| 工具 | 用途 |
|------|------|
| JUnit 5 | 测试框架（`@Test`、`@BeforeEach` 等） |
| Mockito | 依赖 Mock（`@Mock`、`@InjectMocks`） |
| Spring Boot Test | 集成测试（`@SpringBootTest`） |
| AssertJ | 断言库（流式断言，比原生 `assertEquals` 更易读） |

### 14.2 单元测试结构规范

```java
/**
 * 任务管理服务单元测试
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @related REQ-MES-AI-20260415-003
 */
@ExtendWith(MockitoExtension.class)
class TaskRequestServiceImplTest {

    @Mock
    private AiTaskReqMapper taskReqMapper;

    @Mock
    private AiTaskHistoryMapper taskHistoryMapper;

    @Mock
    private TaskNoGenerator taskNoGenerator;

    @InjectMocks
    private TaskRequestServiceImpl taskRequestService;

    /**
     * 测试方法命名规范：
     * should_[预期结果]_when_[触发条件]
     */

    @Test
    void should_createTaskSuccessfully_when_validDtoProvided() {
        // Given（准备数据）
        CreateTaskRequestDTO dto = buildValidCreateDTO();
        when(taskNoGenerator.generate()).thenReturn("REQ-MES-AI-20260415-001");
        when(taskReqMapper.insert(any())).thenReturn(1);
        when(taskHistoryMapper.insert(any())).thenReturn(1);

        // When（执行操作）
        TaskRequestVO result = taskRequestService.createTaskRequest(dto);

        // Then（验证结果）
        assertThat(result).isNotNull();
        assertThat(result.getTaskNo()).isEqualTo("REQ-MES-AI-20260415-001");
        assertThat(result.getStatus()).isEqualTo("DRAFT");
        verify(taskReqMapper, times(1)).insert(any(AiTaskReq.class));
        verify(taskHistoryMapper, times(1)).insert(any(AiTaskHistory.class));
    }

    @Test
    void should_throwBizException_when_approveTaskWithWrongStatus() {
        // Given：任务处于 DRAFT 状态（非 REVIEWING），不允许审批
        AiTaskReq task = buildTask(TaskStatusEnum.DRAFT);
        when(taskReqMapper.selectById(anyLong())).thenReturn(task);

        // When & Then
        assertThatThrownBy(() ->
            taskRequestService.approveTask(1L, new ApproveTaskDTO()))
            .isInstanceOf(BizException.class)
            .hasFieldOrPropertyWithValue("resultCode", ResultCode.TASK_NOT_REVIEWABLE);
    }

    @Test
    void should_throwBizException_when_taskNotFound() {
        // Given
        when(taskReqMapper.selectById(anyLong())).thenReturn(null);

        // When & Then
        assertThatThrownBy(() -> taskRequestService.getTaskById(999L))
            .isInstanceOf(BizException.class)
            .hasFieldOrPropertyWithValue("resultCode", ResultCode.RESOURCE_NOT_FOUND);
    }

    // 测试数据构建方法（避免重复代码）
    private CreateTaskRequestDTO buildValidCreateDTO() {
        CreateTaskRequestDTO dto = new CreateTaskRequestDTO();
        dto.setTitle("工单状态流转功能开发");
        dto.setTaskType("FEAT");
        dto.setPriority(2);
        dto.setExpectedFinishDate(LocalDate.now().plusDays(5));
        dto.setAcceptCriteria("[{\"condition\":\"工单可正常创建\"}]");
        return dto;
    }
}
```

### 14.3 测试覆盖率要求

| 覆盖率类型 | 目标 | 说明 |
|--------|------|------|
| 行覆盖率 | ≥ 70% | CI/CD Pipeline 强制门禁 |
| 分支覆盖率 | ≥ 60% | 状态机逻辑的各分支须覆盖 |
| 核心 Service 方法 | 100% | Service 接口的所有 public 方法必须有对应测试 |

**必须有测试的场景**：
- 状态机流转（合法路径和非法路径）
- 资源不存在异常
- 并发场景（task_no 唯一性）
- 脱敏层处理（正例和边界）
- 权限校验（各角色）

---

## 十五、配置管理规范

### 15.1 多环境配置结构

```
src/main/resources/
├── application.yml              # 公共配置（非敏感）
├── application-dev.yml          # 开发环境
├── application-test.yml         # 测试环境
└── application-prod.yml         # 生产环境（所有敏感项通过环境变量注入）
```

### 15.2 application.yml 公共配置规范

```yaml
# 应用基本配置（不含敏感信息）
spring:
  application:
    name: mesai-platform

  # Jackson 全局配置
  jackson:
    date-format: yyyy-MM-dd'T'HH:mm:ss
    time-zone: Asia/Shanghai
    default-property-inclusion: non_null
    deserialization:
      fail-on-unknown-properties: false

  # 文件上传限制
  servlet:
    multipart:
      max-file-size: 50MB
      max-request-size: 260MB    # 5个文件 × 50MB + 余量

# MyBatis Plus 配置
mybatis-plus:
  mapper-locations: classpath*:mapper/**/*.xml
  global-config:
    db-config:
      logic-delete-field: isDeleted   # 逻辑删除字段
      logic-delete-value: 1
      logic-not-delete-value: 0
  configuration:
    map-underscore-to-camel-case: true
    log-impl: org.apache.ibatis.logging.slf4j.Slf4jImpl   # 开发环境可开

# 业务配置（非敏感）
mesai:
  task:
    batch-max-size: 500            # 批量写操作每批最大条数
    token-daily-budget: 3000000    # Token 每日预算（300万）
    token-degrade-threshold: 2500000  # 降级阈值（250万）
  jwt:
    access-token-expire-seconds: 28800    # 8小时
    refresh-token-expire-seconds: 604800  # 7天
  inspection:
    cron: "0 30 7 * * MON-FRI"    # 每工作日07:30巡检
```

### 15.3 配置项命名规范

```yaml
# ✅ 正确：清晰的层级命名
mesai:
  ai-gateway:
    api-key: ${CLAUDE_API_KEY}
    timeout-seconds: 120
    max-retry: 3
  knowledge:
    chunk-size: 1024
    chunk-overlap: 128
    top-k: 5

# ❌ 禁止：扁平命名（层级不清晰）
apiKey: ${CLAUDE_API_KEY}
mesaiAiGatewayTimeoutSeconds: 120
```

---

## 十六、附录

### 附录 A：技术决策记录（ADR）

| 序号 | 决策项 | 决策内容 | 原因 | 日期 |
|------|--------|--------|------|------|
| ADR-001 | ORM 框架 | 使用 MyBatis Plus，不使用 JPA/Hibernate | MES 系统 SQL 复杂度高，MyBatis Plus 灵活可控；JPA 对复杂联表查询不友好 | 2026-04 |
| ADR-002 | 事务策略 | 使用 `@Transactional(rollbackFor = Exception.class)`，不依赖 Spring 默认 | Spring 默认只对 RuntimeException 回滚，受检异常不回滚，存在数据一致性风险 | 2026-04 |
| ADR-003 | 响应结构 | HTTP 200 + `ResultVO.code` 区分成功/失败，不使用 4xx/5xx 表达业务失败 | 前端统一拦截 200 处理业务码更简洁；4xx/5xx 留给基础设施层 | 2026-04 |
| ADR-004 | 分页起始页码 | 从 1 开始（`page=1`），不使用从 0 开始 | 与前端 Element Plus 分页组件默认行为一致，减少换算错误 | 2026-04 |
| ADR-005 | 时间处理 | 后端统一 UTC+8 存储，接口使用 ISO 8601 格式 | 与甲方 MES 系统时区保持一致，避免跨时区歧义 | 2026-04 |
| ADR-006 | 序列号生成 | Redis INCR 主方案 + MySQL 降级兜底 | 单纯数据库乐观锁在高并发时竞争激烈；Redis 性能更优；降级保障高可用 | 2026-04 |
| ADR-007 | WebSocket 协议 | STOMP over WebSocket（Spring 内置支持） | STOMP 提供订阅/发布语义，按 taskId 订阅比纯 WebSocket 更易管理 | 2026-04 |
| ADR-008 | Excel 导出 | EasyExcel（阿里开源）替代 Apache POI 直接操作 | POI 直接操作 API 繁琐、内存占用高；EasyExcel 流式处理，避免 OOM | 2026-04 |
| ADR-009 | 前端状态管理 | Pinia（Vue 3 官方推荐），不使用 Vuex | Pinia 更轻量、TypeScript 友好、无 mutations 概念，与 Vue 3 配套 | 2026-04 |
| ADR-010 | 向量数据库 | ChromaDB（轻量，测试期）→ Milvus（生产） | 项目初期快速迭代用 ChromaDB；数据量增长后平滑迁移至 Milvus | 2026-04 |
| ADR-011 | 双数据源架构 | AI 平台自建 MySQL 8.x（读写）+ MES 现有 PostgreSQL 15.x（只读） | MES 系统已使用 PostgreSQL（`itsm_dev`），不做迁移；AI 平台业务数据独立建 MySQL，两者隔离，AI 平台通过只读账号 `itsm_readonly` 跨服访问 MES 库，HikariCP `readOnly=true` 作兜底保护；经 T1-1-5 验证通过（2026-04-12） | 2026-04 |

### 附录 B：关键阈值速查表（补充 CLAUDE.md 附录）

| 指标 | 阈值/规则 | 来源 |
|------|--------|------|
| SELECT * | 禁止 | CLAUDE.md 3.3节 |
| 批量写操作每批上限 | ≤ 500 条 | CLAUDE.md 3.3节 |
| 单元测试覆盖率 | ≥ 70% | CLAUDE.md 8.1节 |
| SonarQube Critical | = 0 | CLAUDE.md 附录 |
| 文件上传大小上限 | 50 MB | API规范 3.4节 |
| 单次上传文件数上限 | 5 个 | API规范 3.4节 |
| 分页默认条数 | 20，最大 100 | API规范 1.2节 |
| 知识库分块大小 | 512～1024 tokens | 技术方案 3.2.2节 |
| 知识库分块重叠 | 128 tokens | 技术方案 3.2.2节 |
| 知识库检索 Top-K | 5（降级模式 3） | 技术方案 3.2.2节 |
| 慢 SQL 告警阈值 | > 2 秒 | CLAUDE.md 附录 |
| JWT AccessToken 有效期 | 8 小时 | API规范 2.5节 |
| JWT RefreshToken 有效期 | 7 天 | API规范 2.5节 |
| 下载一次性 Token 有效期 | 5 分钟 | API规范 2.5节 |
| AI Agent Token 有效期 | 30 天 | API规范 2.5节 |
| Token 每日预算 | 300 万 tokens | CLAUDE.md 第十二章 |
| Token 降级阈值 | 250 万 tokens | CLAUDE.md 第十二章 |
| 磁盘告警阈值 | > 80% | CLAUDE.md 第九章 |
| 内存告警阈值 | > 85% | CLAUDE.md 第九章 |
| 巡检执行时间 | 每工作日 07:30 | CLAUDE.md 第九章 |
| 日志保留时间（应用日志） | 30 天 | 本文档 6.4节 |
| 日志保留时间（ERROR日志） | 90 天 | 本文档 6.4节 |
| 授权记录保留期限 | ≥ 3 年 | DB设计 3.1.7节 |
| 审计日志保留期限 | ≥ 3 年 | DB设计 3.4节 |

### 附录 C：文档版本历史

| 版本 | 日期 | 修改人 | 修改内容 |
|------|------|------|--------|
| V1.0 | 2026-04-12 | 项目经理 | 初稿编写，补充技术方案未细化的技术决策 |
| V1.1 | 2026-04-12 | AI | Sprint 1 T1-1-5 验证后更新：确认 MES 系统数据库为 PostgreSQL 15.x；新增双数据源架构规范（ADR-011）；补充 MES 只读数据源配置（10.5节）及 MesDataSourceConfig Bean 规范；新增 PostgreSQL JDBC 驱动依赖（1.1节）；基础设施说明更新（1.3节） |

---

*芯智云匠——山东芯通 MES 岗位 AI 智能体资产化项目*
*技术规范文档 · AI-MES-TECHSPEC-2026-001 · V1.1 · 2026年4月12日*
*本文件受版本控制，修改须经技术负责人批准，变更记录见 Git 历史*
