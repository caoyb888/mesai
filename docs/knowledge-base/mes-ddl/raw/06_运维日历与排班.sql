-- V6__create_calendar_roster_tables.sql
-- 模块六：运维日历与排班
-- 包含表：itsm_calendar_event, itsm_roster_team, itsm_roster_team_member, itsm_roster_schedule

CREATE TABLE IF NOT EXISTS itsm.itsm_calendar_event (
    id              BIGINT          NOT NULL,
    title           VARCHAR(128)    NOT NULL,
    event_type      VARCHAR(32)     NOT NULL,
    description     TEXT,
    start_time      TIMESTAMPTZ     NOT NULL,
    end_time        TIMESTAMPTZ     NOT NULL,
    all_day         BOOLEAN         NOT NULL DEFAULT FALSE,
    related_group_id BIGINT,
    color           VARCHAR(16),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL DEFAULT 0,
    is_deleted      SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_calendar_event PRIMARY KEY (id),
    CONSTRAINT chk_itsm_event_type CHECK (
        event_type IN ('INSPECTION', 'CHANGE_WINDOW', 'MAINTENANCE', 'ASSET_SCAN', 'ON_DUTY')
    ),
    CONSTRAINT chk_itsm_event_time CHECK (end_time > start_time)
);

COMMENT ON TABLE itsm.itsm_calendar_event IS '运维日历事件表，记录巡检计划、变更窗口、维护期等';
COMMENT ON COLUMN itsm.itsm_calendar_event.id IS '主键';
COMMENT ON COLUMN itsm.itsm_calendar_event.title IS '事件标题';
COMMENT ON COLUMN itsm.itsm_calendar_event.event_type IS '事件类型：INSPECTION例行巡检 CHANGE_WINDOW变更窗口 MAINTENANCE系统维护期 ASSET_SCAN资产扫描 ON_DUTY值班排班';
COMMENT ON COLUMN itsm.itsm_calendar_event.description IS '详细描述';
COMMENT ON COLUMN itsm.itsm_calendar_event.start_time IS '开始时间';
COMMENT ON COLUMN itsm.itsm_calendar_event.end_time IS '结束时间';
COMMENT ON COLUMN itsm.itsm_calendar_event.all_day IS '是否全天事件';
COMMENT ON COLUMN itsm.itsm_calendar_event.related_group_id IS '关联用户组（可选）';
COMMENT ON COLUMN itsm.itsm_calendar_event.color IS '日历显示颜色（十六进制，如#FF5733）';
COMMENT ON COLUMN itsm.itsm_calendar_event.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_calendar_event.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_calendar_event.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_calendar_event.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_calendar_time ON itsm.itsm_calendar_event(start_time, end_time) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_calendar_type ON itsm.itsm_calendar_event(event_type) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_calendar_group ON itsm.itsm_calendar_event(related_group_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_roster_team (
    id          BIGINT      NOT NULL,
    name        VARCHAR(64) NOT NULL,
    description VARCHAR(256),
    group_id    BIGINT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_roster_team PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_roster_team IS '值班团队表，定义可排班的团队，如"基础设施值班组"';
COMMENT ON COLUMN itsm.itsm_roster_team.id IS '主键';
COMMENT ON COLUMN itsm.itsm_roster_team.name IS '团队名称';
COMMENT ON COLUMN itsm.itsm_roster_team.description IS '团队描述';
COMMENT ON COLUMN itsm.itsm_roster_team.group_id IS '关联用户组ID';
COMMENT ON COLUMN itsm.itsm_roster_team.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_roster_team.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_roster_team.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_roster_team.is_deleted IS '逻辑删除标记';

CREATE TABLE IF NOT EXISTS itsm.itsm_roster_team_member (
    team_id     BIGINT      NOT NULL,
    user_id     BIGINT      NOT NULL,
    sort_order  INTEGER     NOT NULL DEFAULT 0,
    joined_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_roster_team_member PRIMARY KEY (team_id, user_id)
);

COMMENT ON TABLE itsm.itsm_roster_team_member IS '值班团队成员表，定义团队成员及轮班顺序';
COMMENT ON COLUMN itsm.itsm_roster_team_member.team_id IS '团队ID';
COMMENT ON COLUMN itsm.itsm_roster_team_member.user_id IS '用户ID';
COMMENT ON COLUMN itsm.itsm_roster_team_member.sort_order IS '轮班顺序，数字小的先值班';
COMMENT ON COLUMN itsm.itsm_roster_team_member.joined_at IS '加入团队时间';

CREATE INDEX idx_itsm_roster_member_user ON itsm.itsm_roster_team_member(user_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_roster_schedule (
    id              BIGINT      NOT NULL,
    team_id         BIGINT      NOT NULL,
    user_id         BIGINT      NOT NULL,
    schedule_date   DATE        NOT NULL,
    shift_type      VARCHAR(16) NOT NULL DEFAULT 'DAY',
    start_time      TIME        NOT NULL,
    end_time        TIME        NOT NULL,
    is_on_duty      SMALLINT    NOT NULL DEFAULT 1,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      BIGINT      NOT NULL DEFAULT 0,
    is_deleted      SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_roster_schedule PRIMARY KEY (id),
    CONSTRAINT chk_itsm_shift_type CHECK (shift_type IN ('DAY','NIGHT','FULL'))
);

COMMENT ON TABLE itsm.itsm_roster_schedule IS '排班记录表，工单分配时查询当日值班人作为默认处理人';
COMMENT ON COLUMN itsm.itsm_roster_schedule.id IS '主键';
COMMENT ON COLUMN itsm.itsm_roster_schedule.team_id IS '团队ID';
COMMENT ON COLUMN itsm.itsm_roster_schedule.user_id IS '值班人ID';
COMMENT ON COLUMN itsm.itsm_roster_schedule.schedule_date IS '值班日期';
COMMENT ON COLUMN itsm.itsm_roster_schedule.shift_type IS '班次类型：DAY白班 NIGHT夜班 FULL全天班';
COMMENT ON COLUMN itsm.itsm_roster_schedule.start_time IS '班次开始时间';
COMMENT ON COLUMN itsm.itsm_roster_schedule.end_time IS '班次结束时间';
COMMENT ON COLUMN itsm.itsm_roster_schedule.is_on_duty IS '值班状态：1正常值班 0调班/请假';
COMMENT ON COLUMN itsm.itsm_roster_schedule.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_roster_schedule.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_roster_schedule.created_by IS '排班创建人';
COMMENT ON COLUMN itsm.itsm_roster_schedule.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_roster_schedule 
    ON itsm.itsm_roster_schedule(team_id, user_id, schedule_date, shift_type) 
    WHERE is_deleted = 0;
CREATE INDEX idx_itsm_roster_date ON itsm.itsm_roster_schedule(schedule_date) WHERE is_deleted = 0;