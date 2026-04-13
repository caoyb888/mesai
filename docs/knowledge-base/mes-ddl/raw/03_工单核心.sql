-- V3__create_ticket_tables.sql
-- 模块三：工单核心
-- 包含表：itsm_ticket, itsm_ticket_flow_log, itsm_ticket_comment, itsm_ticket_ci_map

CREATE TABLE IF NOT EXISTS itsm.itsm_ticket (
    id                      BIGINT          NOT NULL,
    ticket_no               VARCHAR(32)     NOT NULL,
    model_id                BIGINT          NOT NULL,
    title                   VARCHAR(256)    NOT NULL,
    description             TEXT,
    status                  VARCHAR(32)     NOT NULL DEFAULT 'Created',
    priority                VARCHAR(16)     NOT NULL DEFAULT 'MEDIUM',
    source                  VARCHAR(16)     NOT NULL DEFAULT 'PORTAL',
    created_user_id         BIGINT          NOT NULL,
    assigned_group_id       BIGINT,
    assigned_user_id        BIGINT,
    form_data_json          TEXT,
    sla_deadline_response   TIMESTAMPTZ,
    sla_deadline_resolve    TIMESTAMPTZ,
    response_at             TIMESTAMPTZ,
    resolved_at             TIMESTAMPTZ,
    sla_response_status     VARCHAR(16),
    sla_resolve_status      VARCHAR(16),
    close_reason            VARCHAR(512),
    closed_at               TIMESTAMPTZ,
    created_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by              BIGINT          NOT NULL DEFAULT 0,
    is_deleted              SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_ticket PRIMARY KEY (id),
    CONSTRAINT chk_itsm_ticket_status CHECK (
        status IN ('Created','Pending','Processing','Suspended','Pending_Review','Closed')
    ),
    CONSTRAINT chk_itsm_ticket_priority CHECK (
        priority IN ('LOW','MEDIUM','HIGH','CRITICAL')
    ),
    CONSTRAINT chk_itsm_ticket_source CHECK (
        source IN ('PORTAL','API','WORKBENCH','MONITOR')
    ),
    CONSTRAINT chk_itsm_ticket_sla_response CHECK (
        sla_response_status IS NULL OR sla_response_status IN ('NORMAL','WARNING','BREACH')
    ),
    CONSTRAINT chk_itsm_ticket_sla_resolve CHECK (
        sla_resolve_status IS NULL OR sla_resolve_status IN ('NORMAL','WARNING','BREACH')
    )
);

COMMENT ON TABLE itsm.itsm_ticket IS '工单主表，ITSM系统核心数据表，记录服务请求、故障申报等全生命周期';
COMMENT ON COLUMN itsm.itsm_ticket.id IS '雪花算法主键';
COMMENT ON COLUMN itsm.itsm_ticket.ticket_no IS '业务编号，格式TK-YYYY-XXXXXX，流水号由Redis INCR生成，供用户可读';
COMMENT ON COLUMN itsm.itsm_ticket.model_id IS '服务模型ID，决定表单结构和处理流程';
COMMENT ON COLUMN itsm.itsm_ticket.title IS '工单标题';
COMMENT ON COLUMN itsm.itsm_ticket.description IS '工单详细描述';
COMMENT ON COLUMN itsm.itsm_ticket.status IS 'FSM状态：Created已创建→Pending待处理→Processing处理中→Pending_Review待审核→Closed已关闭';
COMMENT ON COLUMN itsm.itsm_ticket.priority IS '优先级：LOW低 MEDIUM中 HIGH高 CRITICAL紧急';
COMMENT ON COLUMN itsm.itsm_ticket.source IS '工单来源：PORTAL用户门户 API外部接口 WORKBENCH运维台直录 MONITOR监控系统自动创建';
COMMENT ON COLUMN itsm.itsm_ticket.created_user_id IS '提单人ID';
COMMENT ON COLUMN itsm.itsm_ticket.assigned_group_id IS '当前处理用户组ID';
COMMENT ON COLUMN itsm.itsm_ticket.assigned_user_id IS '当前处理人ID，接单后分配';
COMMENT ON COLUMN itsm.itsm_ticket.form_data_json IS '动态表单填写数据，JSON格式，key与form_field.field_key对应';
COMMENT ON COLUMN itsm.itsm_ticket.sla_deadline_response IS '响应截止时间，由SLA引擎计算';
COMMENT ON COLUMN itsm.itsm_ticket.sla_deadline_resolve IS '解决截止时间';
COMMENT ON COLUMN itsm.itsm_ticket.response_at IS '实际响应时间，进入Processing状态时记录';
COMMENT ON COLUMN itsm.itsm_ticket.resolved_at IS '实际解决时间，进入Closed状态时记录';
COMMENT ON COLUMN itsm.itsm_ticket.sla_response_status IS 'SLA响应状态：NORMAL正常 WARNING预警(80%阈值) BREACH已违约';
COMMENT ON COLUMN itsm.itsm_ticket.sla_resolve_status IS 'SLA解决状态';
COMMENT ON COLUMN itsm.itsm_ticket.close_reason IS '关闭原因说明';
COMMENT ON COLUMN itsm.itsm_ticket.closed_at IS '关闭时间';
COMMENT ON COLUMN itsm.itsm_ticket.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_ticket.updated_at IS '最后更新时间';
COMMENT ON COLUMN itsm.itsm_ticket.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_ticket.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_ticket_no ON itsm.itsm_ticket(ticket_no);
CREATE INDEX idx_itsm_ticket_status ON itsm.itsm_ticket(status) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_ticket_group_status ON itsm.itsm_ticket(assigned_group_id, status) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_ticket_user_status ON itsm.itsm_ticket(assigned_user_id, status) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_ticket_creator ON itsm.itsm_ticket(created_user_id) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_ticket_model ON itsm.itsm_ticket(model_id);
CREATE INDEX idx_itsm_ticket_sla_deadline ON itsm.itsm_ticket(sla_deadline_resolve) 
    WHERE is_deleted = 0 AND status NOT IN ('Closed');

CREATE TABLE IF NOT EXISTS itsm.itsm_ticket_flow_log (
    id              BIGINT          NOT NULL,
    ticket_id       BIGINT          NOT NULL,
    from_status     VARCHAR(32),
    to_status       VARCHAR(32)     NOT NULL,
    action          VARCHAR(64)     NOT NULL,
    actor_type      VARCHAR(16)     NOT NULL DEFAULT 'USER',
    operator_id     BIGINT,
    remark          VARCHAR(1024),
    extra_json      TEXT,
    operated_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    
    CONSTRAINT pk_itsm_ticket_flow_log PRIMARY KEY (id),
    CONSTRAINT chk_itsm_flow_actor_type CHECK (actor_type IN ('USER','SYSTEM'))
);

COMMENT ON TABLE itsm.itsm_ticket_flow_log IS '工单流转日志，不可删除，全量记录每次状态变更，用于审计和流程分析';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.id IS '主键';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.ticket_id IS '工单ID';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.from_status IS '流转前状态，NULL表示初始创建';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.to_status IS '流转后状态';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.action IS '触发动作：AUTO_ROUTE自动分单 CLAIM接单 TRANSFER转单 SUSPEND挂起 RESUME恢复 SUBMIT_REVIEW提交审核 APPROVE审批通过 REJECT驳回 CLOSE关闭';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.actor_type IS '操作者类型：USER人工操作 SYSTEM系统自动';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.operator_id IS '操作人ID，SYSTEM操作时为NULL';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.remark IS '备注/处理说明';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.extra_json IS '扩展数据，如转单目标组信息';
COMMENT ON COLUMN itsm.itsm_ticket_flow_log.operated_at IS '操作时间';

CREATE INDEX idx_itsm_flow_log_ticket ON itsm.itsm_ticket_flow_log(ticket_id, operated_at DESC);
CREATE INDEX idx_itsm_flow_log_operator ON itsm.itsm_ticket_flow_log(operator_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_ticket_comment (
    id          BIGINT      NOT NULL,
    ticket_id   BIGINT      NOT NULL,
    user_id     BIGINT      NOT NULL,
    content     TEXT        NOT NULL,
    is_internal SMALLINT    NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_ticket_comment PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_ticket_comment IS '工单评论表，支持提单人与处理人沟通，支持内部备注';
COMMENT ON COLUMN itsm.itsm_ticket_comment.id IS '主键';
COMMENT ON COLUMN itsm.itsm_ticket_comment.ticket_id IS '工单ID';
COMMENT ON COLUMN itsm.itsm_ticket_comment.user_id IS '评论人ID';
COMMENT ON COLUMN itsm.itsm_ticket_comment.content IS '评论内容，支持富文本HTML';
COMMENT ON COLUMN itsm.itsm_ticket_comment.is_internal IS '0=公开（用户和运维均可见） 1=内部（仅运维可见）';
COMMENT ON COLUMN itsm.itsm_ticket_comment.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_ticket_comment.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_ticket_comment.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_ticket_comment.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_comment_ticket ON itsm.itsm_ticket_comment(ticket_id, created_at DESC) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_ticket_ci_map (
    ticket_id       BIGINT      NOT NULL,
    ci_id           BIGINT      NOT NULL,
    ci_type         VARCHAR(64) NOT NULL,
    ci_name         VARCHAR(128),
    relation_type   VARCHAR(32) NOT NULL DEFAULT 'AFFECTED',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by      BIGINT      NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_ticket_ci_map PRIMARY KEY (ticket_id, ci_id),
    CONSTRAINT chk_itsm_ci_relation CHECK (
        relation_type IN ('AFFECTED','CAUSED_BY','RELATED')
    )
);

COMMENT ON TABLE itsm.itsm_ticket_ci_map IS '工单与CMDB配置项关联表，支持多对多，记录故障影响范围';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.ticket_id IS '工单ID';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.ci_id IS 'CMDB配置项ID（外系统主键）';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.ci_type IS 'CI类型，如SERVER服务器/DATABASE数据库/NETWORK网络设备';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.ci_name IS 'CI名称冗余存储，防止CMDB数据变更后历史记录失效';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.relation_type IS '关联类型：AFFECTED受影响资产 CAUSED_BY故障根因 RELATED相关资产';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_ticket_ci_map.created_by IS '创建人';

CREATE INDEX idx_itsm_ci_map_ci_id ON itsm.itsm_ticket_ci_map(ci_id);