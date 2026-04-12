package com.xingtong.mesai.common.constant;

/**
 * 任务管理模块常量
 *
 * <p>所有魔法值必须在此处定义为常量，禁止在业务代码中直接使用字面量。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
public final class TaskConstants {

    private TaskConstants() {
        // 工具类，禁止实例化
    }

    /** 需求单编号前缀 */
    public static final String TASK_NO_PREFIX = "REQ-MES-AI-";

    /** Redis 任务序列号键前缀，完整 Key 格式：seq:TASK_NO:{YYYYMMDD} */
    public static final String TASK_SEQ_REDIS_KEY_PREFIX = "seq:TASK_NO:";

    /** 每批次最大操作条数（CLAUDE.md 3.3节 SQL规范：批量写操作每批 ≤ 500 条） */
    public static final int BATCH_MAX_SIZE = 500;

    /** Token 每日预算上限（tokens）— 对应 CLAUDE.md 第十二章 */
    public static final long TOKEN_DAILY_BUDGET = 3_000_000L;

    /** Token 降级阈值（tokens）— 超出则 Top-5 降级为 Top-3 */
    public static final long TOKEN_DEGRADE_THRESHOLD = 2_500_000L;

    /** 分页查询默认每页条数 */
    public static final int DEFAULT_PAGE_SIZE = 20;

    /** 分页查询每页最大条数 */
    public static final int MAX_PAGE_SIZE = 100;

    /** 逻辑删除：有效 */
    public static final int NOT_DELETED = 0;

    /** 逻辑删除：已删除 */
    public static final int DELETED = 1;
}
