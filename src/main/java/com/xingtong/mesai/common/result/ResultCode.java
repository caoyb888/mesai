package com.xingtong.mesai.common.result;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 业务错误码枚举
 *
 * <p>与 AI-MES-API-2026-001 第四章错误码规范完全对应，code=0 代表成功。
 * <p>新增错误码须在 API 规范文档中同步更新，并提交变更记录。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
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
    /**
     * 系统繁忙（序列号生成失败、重试耗尽等场景使用）
     */
    SYSTEM_BUSY(90004, "系统繁忙，请稍后重试"),
    INTERNAL_ERROR(99999, "系统内部错误");

    /** 业务错误码 */
    private final Integer code;

    /** 默认错误信息 */
    private final String message;
}
