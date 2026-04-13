-- V7__create_notify_audit_tables.sql
-- 模块七：通知与审计
-- 包含表：itsm_notify_channel, itsm_notify_log, itsm_audit_log

CREATE TABLE IF NOT EXISTS itsm.itsm_notify_channel (
    id              BIGINT          NOT NULL,
    channel_type    VARCHAR(32)     NOT NULL,
    name            VARCHAR(64)     NOT NULL,
    config_json     TEXT            NOT NULL,
    is_enabled      SMALLINT        NOT NULL DEFAULT 0,
    last_test_at    TIMESTAMPTZ,
    last_test_result VARCHAR(16),
    last_test_error  VARCHAR(512),
    rate_limit_count INTEGER        NOT NULL DEFAULT 100,
    daily_quota     INTEGER,
    daily_sent_count INTEGER        NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_by      BIGINT          NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_notify_channel PRIMARY KEY (id),
    CONSTRAINT chk_itsm_channel_type CHECK (
        channel_type IN ('EMAIL','SMS','LARK','DINGDING')
    ),
    CONSTRAINT uq_itsm_notify_channel_type UNIQUE (channel_type)
);

COMMENT ON TABLE itsm.itsm_notify_channel IS '消息推送渠道配置表，每种渠道仅一行配置，支持邮件、短信、飞书、钉钉';
COMMENT ON COLUMN itsm.itsm_notify_channel.id IS '主键';
COMMENT ON COLUMN itsm.itsm_notify_channel.channel_type IS '渠道类型：EMAIL邮件 SMS短信 LARK飞书 DINGDING钉钉';
COMMENT ON COLUMN itsm.itsm_notify_channel.name IS '渠道显示名';
COMMENT ON COLUMN itsm.itsm_notify_channel.config_json IS '渠道连接配置，AES-256加密存储，含SMTP地址/API Key等敏感信息';
COMMENT ON COLUMN itsm.itsm_notify_channel.is_enabled IS '强管控开关：0禁用 1启用。变更即时写入Redis，消费者实时读取';
COMMENT ON COLUMN itsm.itsm_notify_channel.last_test_at IS '最近一次测试连接时间';
COMMENT ON COLUMN itsm.itsm_notify_channel.last_test_result IS '最近测试结果：SUCCESS成功 FAIL失败';
COMMENT ON COLUMN itsm.itsm_notify_channel.last_test_error IS '最近测试错误信息';
COMMENT ON COLUMN itsm.itsm_notify_channel.rate_limit_count IS '每分钟最大发送数，限流保护';
COMMENT ON COLUMN itsm.itsm_notify_channel.daily_quota IS '日发送配额（短信渠道必填），控制成本';
COMMENT ON COLUMN itsm.itsm_notify_channel.daily_sent_count IS '今日已发送数，每日零点重置';
COMMENT ON COLUMN itsm.itsm_notify_channel.updated_at IS '最后更新时间';
COMMENT ON COLUMN itsm.itsm_notify_channel.updated_by IS '最后更新人';

CREATE TABLE IF NOT EXISTS itsm.itsm_notify_log (
    id              BIGINT          NOT NULL,
    channel_type    VARCHAR(32)     NOT NULL,
    ticket_id       BIGINT,
    recipient       VARCHAR(128)    NOT NULL,
    subject         VARCHAR(256),
    content         TEXT            NOT NULL,
    status          VARCHAR(16)     NOT NULL DEFAULT 'PENDING',
    retry_count     SMALLINT        NOT NULL DEFAULT 0,
    error_msg       VARCHAR(512),
    sent_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_notify_log PRIMARY KEY (id),
    CONSTRAINT chk_itsm_notify_status CHECK (
        status IN ('PENDING','SENT','FAILED','SKIPPED')
    )
);

COMMENT ON TABLE itsm.itsm_notify_log IS '通知发送日志表，记录所有消息推送历史，用于追踪和重试';
COMMENT ON COLUMN itsm.itsm_notify_log.id IS '主键';
COMMENT ON COLUMN itsm.itsm_notify_log.channel_type IS '使用的渠道类型';
COMMENT ON COLUMN itsm.itsm_notify_log.ticket_id IS '关联工单ID，可为空（如审核通知）';
COMMENT ON COLUMN itsm.itsm_notify_log.recipient IS '接收人（手机号/邮箱/用户ID）';
COMMENT ON COLUMN itsm.itsm_notify_log.subject IS '标题（邮件使用）';
COMMENT ON COLUMN itsm.itsm_notify_log.content IS '发送内容';
COMMENT ON COLUMN itsm.itsm_notify_log.status IS '发送状态：PENDING待发送 SENT已发送 FAILED发送失败 SKIPPED渠道已禁用跳过';
COMMENT ON COLUMN itsm.itsm_notify_log.retry_count IS '已重试次数';
COMMENT ON COLUMN itsm.itsm_notify_log.error_msg IS '失败错误信息';
COMMENT ON COLUMN itsm.itsm_notify_log.sent_at IS '实际发送时间';
COMMENT ON COLUMN itsm.itsm_notify_log.created_at IS '记录创建时间';

CREATE INDEX idx_itsm_notify_log_ticket ON itsm.itsm_notify_log(ticket_id);
CREATE INDEX idx_itsm_notify_log_status ON itsm.itsm_notify_log(status, created_at DESC) 
    WHERE status IN ('PENDING','FAILED');

CREATE TABLE IF NOT EXISTS itsm.itsm_audit_log (
    id              BIGINT          NOT NULL,
    user_id         BIGINT,
    account_no      VARCHAR(64),
    login_ip        VARCHAR(64),
    user_agent      TEXT,
    trace_id        VARCHAR(64),
    module          VARCHAR(32)     NOT NULL,
    action          VARCHAR(64)     NOT NULL,
    resource_type   VARCHAR(64),
    resource_id     VARCHAR(64),
    before_json     TEXT,
    after_json      TEXT,
    result          VARCHAR(16)     NOT NULL,
    error_msg       VARCHAR(512),
    operated_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_audit_log PRIMARY KEY (id),
    CONSTRAINT chk_itsm_audit_result CHECK (result IN ('SUCCESS','FAIL'))
);

COMMENT ON TABLE itsm.itsm_audit_log IS '系统审计日志，永久保留，满足等保三级合规要求，记录所有关键操作';
COMMENT ON COLUMN itsm.itsm_audit_log.id IS '主键';
COMMENT ON COLUMN itsm.itsm_audit_log.user_id IS '操作人ID，NULL表示未登录/系统操作';
COMMENT ON COLUMN itsm.itsm_audit_log.account_no IS '操作人账号（冗余，防用户删除后丢失）';
COMMENT ON COLUMN itsm.itsm_audit_log.login_ip IS '登录/操作IP地址';
COMMENT ON COLUMN itsm.itsm_audit_log.user_agent IS '浏览器UA，可识别是否使用推荐的Chrome环境';
COMMENT ON COLUMN itsm.itsm_audit_log.trace_id IS '请求链路追踪ID，用于分布式追踪';
COMMENT ON COLUMN itsm.itsm_audit_log.module IS '操作模块，如TICKET/USER/SYSTEM';
COMMENT ON COLUMN itsm.itsm_audit_log.action IS '操作动作，如CREATE/UPDATE/DELETE/LOGIN';
COMMENT ON COLUMN itsm.itsm_audit_log.resource_type IS '操作资源类型，如TICKET/USER/KB_ARTICLE';
COMMENT ON COLUMN itsm.itsm_audit_log.resource_id IS '操作资源ID';
COMMENT ON COLUMN itsm.itsm_audit_log.before_json IS '变更前数据快照（JSON），CREATE操作为NULL';
COMMENT ON COLUMN itsm.itsm_audit_log.after_json IS '变更后数据快照（JSON）';
COMMENT ON COLUMN itsm.itsm_audit_log.result IS '操作结果：SUCCESS成功 FAIL失败';
COMMENT ON COLUMN itsm.itsm_audit_log.error_msg IS '失败错误信息';
COMMENT ON COLUMN itsm.itsm_audit_log.operated_at IS '操作时间';

CREATE INDEX idx_itsm_audit_user ON itsm.itsm_audit_log(user_id, operated_at DESC);
CREATE INDEX idx_itsm_audit_resource ON itsm.itsm_audit_log(resource_type, resource_id);
CREATE INDEX idx_itsm_audit_module ON itsm.itsm_audit_log(module, action, operated_at DESC);
CREATE INDEX idx_itsm_audit_time ON itsm.itsm_audit_log(operated_at DESC);