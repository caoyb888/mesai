-- V4__create_sla_tables.sql
-- 模块四：SLA 引擎
-- 包含表：itsm_sla_policy, itsm_holiday, itsm_sla_record

CREATE TABLE IF NOT EXISTS itsm.itsm_sla_policy (
    id                      BIGINT          NOT NULL,
    name                    VARCHAR(64)     NOT NULL,
    service_time_type       VARCHAR(16)     NOT NULL,
    service_time_json       TEXT,
    response_minutes_low      INTEGER,
    response_minutes_medium   INTEGER,
    response_minutes_high     INTEGER,
    response_minutes_critical INTEGER,
    resolve_minutes_low       INTEGER,
    resolve_minutes_medium    INTEGER,
    resolve_minutes_high     INTEGER,
    resolve_minutes_critical  INTEGER,
    created_warn_minutes      INTEGER,
    created_escalate_minutes  INTEGER,
    warn_threshold_pct        INTEGER NOT NULL DEFAULT 80,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_sla_policy PRIMARY KEY (id),
    CONSTRAINT chk_itsm_sla_service_type CHECK (
        service_time_type IN ('5x8','7x24','CUSTOM')
    ),
    CONSTRAINT chk_itsm_sla_warn_pct CHECK (
        warn_threshold_pct BETWEEN 1 AND 99
    )
);

COMMENT ON TABLE itsm.itsm_sla_policy IS 'SLA策略表，按优先级分别定义响应和解决时限，支持不同服务时间窗口';
COMMENT ON COLUMN itsm.itsm_sla_policy.id IS '主键';
COMMENT ON COLUMN itsm.itsm_sla_policy.name IS '策略名称';
COMMENT ON COLUMN itsm.itsm_sla_policy.service_time_type IS '服务时间类型：5x8工作日8小时 7x24全天候 CUSTOM自定义';
COMMENT ON COLUMN itsm.itsm_sla_policy.service_time_json IS 'CUSTOM时的自定义时间段配置，JSON格式';
COMMENT ON COLUMN itsm.itsm_sla_policy.response_minutes_low IS '低优先级响应时限（分钟）';
COMMENT ON COLUMN itsm.itsm_sla_policy.response_minutes_medium IS '中优先级响应时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.response_minutes_high IS '高优先级响应时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.response_minutes_critical IS '紧急优先级响应时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.resolve_minutes_low IS '低优先级解决时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.resolve_minutes_medium IS '中优先级解决时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.resolve_minutes_high IS '高优先级解决时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.resolve_minutes_critical IS '紧急优先级解决时限';
COMMENT ON COLUMN itsm.itsm_sla_policy.created_warn_minutes IS 'Created状态停留超时一级告警阈值（分钟），不可绑定SLA时仍生效';
COMMENT ON COLUMN itsm.itsm_sla_policy.created_escalate_minutes IS 'Created状态超时第二级升级阈值';
COMMENT ON COLUMN itsm.itsm_sla_policy.warn_threshold_pct IS '预警触发百分比，默认80%时限已用时触发告警';
COMMENT ON COLUMN itsm.itsm_sla_policy.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_sla_policy.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_sla_policy.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_sla_policy.is_deleted IS '逻辑删除标记';

CREATE TABLE IF NOT EXISTS itsm.itsm_holiday (
    id          BIGINT      NOT NULL,
    holiday_date DATE        NOT NULL,
    name        VARCHAR(64) NOT NULL,
    year        SMALLINT    NOT NULL,
    is_workday  SMALLINT    NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_holiday PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_holiday IS '节假日日历表，SLA时间计算时排除休息日，支持调休工作日设置';
COMMENT ON COLUMN itsm.itsm_holiday.id IS '主键';
COMMENT ON COLUMN itsm.itsm_holiday.holiday_date IS '节假日日期';
COMMENT ON COLUMN itsm.itsm_holiday.name IS '节假日名称，如"元旦"、"春节"';
COMMENT ON COLUMN itsm.itsm_holiday.year IS '所属年份，方便按年查询';
COMMENT ON COLUMN itsm.itsm_holiday.is_workday IS '0=法定休息日 1=法定调休工作日（如周末上班）';
COMMENT ON COLUMN itsm.itsm_holiday.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_holiday.created_by IS '创建人';

CREATE UNIQUE INDEX uq_itsm_holiday_date ON itsm.itsm_holiday(holiday_date);
CREATE INDEX idx_itsm_holiday_year ON itsm.itsm_holiday(year);

CREATE TABLE IF NOT EXISTS itsm.itsm_sla_record (
    id                      BIGINT          NOT NULL,
    ticket_id               BIGINT          NOT NULL UNIQUE,
    sla_policy_id           BIGINT          NOT NULL,
    priority                VARCHAR(16)     NOT NULL,
    created_at_tick         TIMESTAMPTZ     NOT NULL,
    response_deadline       TIMESTAMPTZ,
    resolve_deadline        TIMESTAMPTZ,
    actual_response_at      TIMESTAMPTZ,
    actual_resolve_at       TIMESTAMPTZ,
    response_work_minutes   INTEGER,
    resolve_work_minutes    INTEGER,
    response_status         VARCHAR(16)     NOT NULL DEFAULT 'NORMAL',
    resolve_status          VARCHAR(16)     NOT NULL DEFAULT 'NORMAL',
    suspended_minutes       INTEGER         NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_sla_record PRIMARY KEY (id),
    CONSTRAINT chk_sla_response_status CHECK (
        response_status IN ('NORMAL','WARNING','BREACH')
    ),
    CONSTRAINT chk_sla_resolve_status CHECK (
        resolve_status IN ('NORMAL','WARNING','BREACH')
    )
);

COMMENT ON TABLE itsm.itsm_sla_record IS '工单SLA计算记录表，每工单一行，精确记录SLA达成情况';
COMMENT ON COLUMN itsm.itsm_sla_record.id IS '主键';
COMMENT ON COLUMN itsm.itsm_sla_record.ticket_id IS '工单ID，唯一';
COMMENT ON COLUMN itsm.itsm_sla_record.sla_policy_id IS '应用的SLA策略ID';
COMMENT ON COLUMN itsm.itsm_sla_record.priority IS '工单优先级';
COMMENT ON COLUMN itsm.itsm_sla_record.created_at_tick IS '工单创建时间（计时起点）';
COMMENT ON COLUMN itsm.itsm_sla_record.response_deadline IS '响应截止时间';
COMMENT ON COLUMN itsm.itsm_sla_record.resolve_deadline IS '解决截止时间';
COMMENT ON COLUMN itsm.itsm_sla_record.actual_response_at IS '实际响应时间';
COMMENT ON COLUMN itsm.itsm_sla_record.actual_resolve_at IS '实际解决时间';
COMMENT ON COLUMN itsm.itsm_sla_record.response_work_minutes IS '响应阶段有效工作时长（分钟），排除节假日和非工作时段后的净时长';
COMMENT ON COLUMN itsm.itsm_sla_record.resolve_work_minutes IS '总解决有效工作时长（分钟）';
COMMENT ON COLUMN itsm.itsm_sla_record.response_status IS 'SLA响应达成状态：NORMAL正常 WARNING预警 BREACH违约';
COMMENT ON COLUMN itsm.itsm_sla_record.resolve_status IS 'SLA解决达成状态';
COMMENT ON COLUMN itsm.itsm_sla_record.suspended_minutes IS 'Suspend挂起期间累计分钟数，SLA暂停计时，关闭时从总时长中扣除';
COMMENT ON COLUMN itsm.itsm_sla_record.created_at IS '记录创建时间';
COMMENT ON COLUMN itsm.itsm_sla_record.updated_at IS '记录更新时间';

CREATE INDEX idx_itsm_sla_record_ticket ON itsm.itsm_sla_record(ticket_id);
CREATE INDEX idx_itsm_sla_record_deadline ON itsm.itsm_sla_record(resolve_deadline) 
    WHERE resolve_status != 'BREACH';