-- V2__create_service_config_tables.sql
-- 模块二：服务配置引擎
-- 包含表：itsm_service_catalog, itsm_service_model, itsm_form_field, itsm_workflow_def

CREATE TABLE IF NOT EXISTS itsm.itsm_service_catalog (
    id          BIGINT      NOT NULL,
    name        VARCHAR(64) NOT NULL,
    parent_id   BIGINT      NOT NULL DEFAULT 0,
    icon_url    VARCHAR(256),
    sort_order  INTEGER     NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_service_catalog PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_service_catalog IS '服务目录表，支持多级分类树，如IT服务->账号权限->邮箱开通';
COMMENT ON COLUMN itsm.itsm_service_catalog.id IS '主键';
COMMENT ON COLUMN itsm.itsm_service_catalog.name IS '目录名称';
COMMENT ON COLUMN itsm.itsm_service_catalog.parent_id IS '父目录ID，0表示顶级目录';
COMMENT ON COLUMN itsm.itsm_service_catalog.icon_url IS '目录图标路径';
COMMENT ON COLUMN itsm.itsm_service_catalog.sort_order IS '同级排序';
COMMENT ON COLUMN itsm.itsm_service_catalog.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_service_catalog.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_service_catalog.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_service_catalog.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_catalog_parent ON itsm.itsm_service_catalog(parent_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_service_model (
    id                  BIGINT          NOT NULL,
    catalog_id          BIGINT          NOT NULL,
    name                VARCHAR(64)     NOT NULL,
    code                VARCHAR(64)     NOT NULL,
    description         VARCHAR(512),
    workflow_def_id     BIGINT          NOT NULL,
    sla_policy_id       BIGINT,
    default_group_id    BIGINT,
    status              SMALLINT        NOT NULL DEFAULT 1,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by          BIGINT          NOT NULL DEFAULT 0,
    is_deleted          SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_service_model PRIMARY KEY (id),
    CONSTRAINT chk_itsm_model_status CHECK (status IN (0, 1))
);

COMMENT ON TABLE itsm.itsm_service_model IS '服务模型表，定义每类服务的表单结构、处理流程与SLA策略，如"软件安装申请"';
COMMENT ON COLUMN itsm.itsm_service_model.id IS '主键';
COMMENT ON COLUMN itsm.itsm_service_model.catalog_id IS '所属服务目录ID';
COMMENT ON COLUMN itsm.itsm_service_model.name IS '服务名称';
COMMENT ON COLUMN itsm.itsm_service_model.code IS '服务编码，规则引擎按此路由到默认处理组';
COMMENT ON COLUMN itsm.itsm_service_model.description IS '服务描述';
COMMENT ON COLUMN itsm.itsm_service_model.workflow_def_id IS '绑定的工作流定义ID';
COMMENT ON COLUMN itsm.itsm_service_model.sla_policy_id IS '关联SLA策略，为空则不计算SLA';
COMMENT ON COLUMN itsm.itsm_service_model.default_group_id IS '默认分配用户组';
COMMENT ON COLUMN itsm.itsm_service_model.status IS '服务状态：1上线 0下线';
COMMENT ON COLUMN itsm.itsm_service_model.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_service_model.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_service_model.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_service_model.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_service_model_code ON itsm.itsm_service_model(code) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_model_catalog ON itsm.itsm_service_model(catalog_id) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_model_workflow ON itsm.itsm_service_model(workflow_def_id);

CREATE TABLE IF NOT EXISTS itsm.itsm_form_field (
    id              BIGINT          NOT NULL,
    model_id        BIGINT          NOT NULL,
    field_key       VARCHAR(64)     NOT NULL,
    field_type      VARCHAR(32)     NOT NULL,
    label           VARCHAR(64)     NOT NULL,
    placeholder     VARCHAR(128),
    required        BOOLEAN         NOT NULL DEFAULT FALSE,
    options_json    TEXT,
    validation_json TEXT,
    default_value   VARCHAR(256),
    sort_order      INTEGER         NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL DEFAULT 0,
    is_deleted      SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_form_field PRIMARY KEY (id),
    CONSTRAINT chk_itsm_field_type CHECK (
        field_type IN ('TEXT', 'TEXTAREA', 'SELECT', 'MULTI_SELECT', 'DATE', 'DATETIME', 
                       'FILE', 'CI_REF', 'USER_REF', 'CASCADE')
    )
);

COMMENT ON TABLE itsm.itsm_form_field IS '动态表单字段定义表，支持无代码配置服务表单，定义字段类型、校验规则等';
COMMENT ON COLUMN itsm.itsm_form_field.id IS '主键';
COMMENT ON COLUMN itsm.itsm_form_field.model_id IS '所属服务模型ID';
COMMENT ON COLUMN itsm.itsm_form_field.field_key IS '字段唯一键，如apply_reason，用于JSON数据存储';
COMMENT ON COLUMN itsm.itsm_form_field.field_type IS '字段类型：TEXT单行文本 TEXTAREA多行文本 SELECT单选下拉 MULTI_SELECT多选 DATE日期 DATETIME日期时间 FILE文件上传 CI_REF配置项关联 USER_REF人员选择器 CASCADE级联选择器';
COMMENT ON COLUMN itsm.itsm_form_field.label IS '前端显示标签';
COMMENT ON COLUMN itsm.itsm_form_field.placeholder IS '输入提示文本';
COMMENT ON COLUMN itsm.itsm_form_field.required IS '是否必填';
COMMENT ON COLUMN itsm.itsm_form_field.options_json IS '下拉/多选选项，JSON数组格式：[{"label":"选项名","value":"值"}]';
COMMENT ON COLUMN itsm.itsm_form_field.validation_json IS '自定义校验规则，JSON格式：{"minLength":2,"maxLength":100}';
COMMENT ON COLUMN itsm.itsm_form_field.default_value IS '默认值';
COMMENT ON COLUMN itsm.itsm_form_field.sort_order IS '字段排序';
COMMENT ON COLUMN itsm.itsm_form_field.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_form_field.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_form_field.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_form_field.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_form_field_key ON itsm.itsm_form_field(model_id, field_key) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_form_field_model ON itsm.itsm_form_field(model_id, sort_order);

CREATE TABLE IF NOT EXISTS itsm.itsm_workflow_def (
    id                  BIGINT          NOT NULL,
    name                VARCHAR(64)     NOT NULL,
    code                VARCHAR(64)     NOT NULL,
    states_json         TEXT            NOT NULL,
    transitions_json    TEXT            NOT NULL,
    allow_close_states  VARCHAR(256)    NOT NULL DEFAULT 'Created,Processing',
    version             INTEGER         NOT NULL DEFAULT 1,
    status              SMALLINT        NOT NULL DEFAULT 1,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by          BIGINT          NOT NULL DEFAULT 0,
    is_deleted          SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_workflow_def PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_workflow_def IS '工作流定义表，FSM有限状态机配置持久化，支持热更新';
COMMENT ON COLUMN itsm.itsm_workflow_def.id IS '主键';
COMMENT ON COLUMN itsm.itsm_workflow_def.name IS '流程名称';
COMMENT ON COLUMN itsm.itsm_workflow_def.code IS '流程编码，全局唯一';
COMMENT ON COLUMN itsm.itsm_workflow_def.states_json IS 'JSON格式状态节点定义：[{"code":"Created","label":"已创建","isInitial":true}]';
COMMENT ON COLUMN itsm.itsm_workflow_def.transitions_json IS 'JSON格式转换规则：[{"from":"Created","to":"Pending","action":"AUTO_ROUTE","actor":"SYSTEM"}]';
COMMENT ON COLUMN itsm.itsm_workflow_def.allow_close_states IS '允许执行关闭操作的状态列表，逗号分隔，Pending状态不可关闭';
COMMENT ON COLUMN itsm.itsm_workflow_def.version IS '版本号，变更时递增';
COMMENT ON COLUMN itsm.itsm_workflow_def.status IS '流程状态：1启用 0禁用';
COMMENT ON COLUMN itsm.itsm_workflow_def.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_workflow_def.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_workflow_def.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_workflow_def.is_deleted IS '逻辑删除标记';

CREATE UNIQUE INDEX uq_itsm_workflow_def_code ON itsm.itsm_workflow_def(code) WHERE is_deleted = 0;