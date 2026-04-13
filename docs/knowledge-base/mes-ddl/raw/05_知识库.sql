-- V5__create_knowledge_tables.sql
-- 模块五：知识库
-- 包含表：itsm_kb_category, itsm_kb_article, itsm_kb_article_version

CREATE TABLE IF NOT EXISTS itsm.itsm_kb_category (
    id          BIGINT      NOT NULL,
    name        VARCHAR(64) NOT NULL,
    parent_id   BIGINT      NOT NULL DEFAULT 0,
    sort_order  INTEGER     NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    is_deleted  SMALLINT    NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_kb_category PRIMARY KEY (id)
);

COMMENT ON TABLE itsm.itsm_kb_category IS '知识库分类表，支持多级分类树';
COMMENT ON COLUMN itsm.itsm_kb_category.id IS '主键';
COMMENT ON COLUMN itsm.itsm_kb_category.name IS '分类名称';
COMMENT ON COLUMN itsm.itsm_kb_category.parent_id IS '父分类ID，0表示顶级';
COMMENT ON COLUMN itsm.itsm_kb_category.sort_order IS '同级排序';
COMMENT ON COLUMN itsm.itsm_kb_category.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_kb_category.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_kb_category.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_kb_category.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_kb_cat_parent ON itsm.itsm_kb_category(parent_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_kb_article (
    id              BIGINT          NOT NULL,
    category_id     BIGINT          NOT NULL,
    title           VARCHAR(256)    NOT NULL,
    summary         VARCHAR(512),
    keywords        VARCHAR(256),
    status          VARCHAR(32)     NOT NULL DEFAULT 'Draft',
    current_version INTEGER         NOT NULL DEFAULT 1,
    probe_ref_id    VARCHAR(128),
    published_at    TIMESTAMPTZ,
    published_by    BIGINT,
    reviewer_id     BIGINT,
    reviewed_at     TIMESTAMPTZ,
    review_comment  VARCHAR(512),
    view_count      INTEGER         NOT NULL DEFAULT 0,
    useful_count    INTEGER         NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL DEFAULT 0,
    is_deleted      SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_kb_article PRIMARY KEY (id),
    CONSTRAINT chk_itsm_kb_status CHECK (
        status IN ('Draft','Pending_Review','Published','Rejected','Archived')
    )
);

COMMENT ON TABLE itsm.itsm_kb_article IS '知识条目主表，内容体存于版本表，支持版本管理和生命周期控制';
COMMENT ON COLUMN itsm.itsm_kb_article.id IS '主键';
COMMENT ON COLUMN itsm.itsm_kb_article.category_id IS '所属分类ID';
COMMENT ON COLUMN itsm.itsm_kb_article.title IS '知识标题';
COMMENT ON COLUMN itsm.itsm_kb_article.summary IS '摘要，用于列表展示';
COMMENT ON COLUMN itsm.itsm_kb_article.keywords IS '关键词，逗号分隔，辅助全文搜索';
COMMENT ON COLUMN itsm.itsm_kb_article.status IS '生命周期：Draft草稿→Pending_Review待审核→Published已发布/Rejected驳回，Published可归档为Archived';
COMMENT ON COLUMN itsm.itsm_kb_article.current_version IS '当前版本号，对应itsm_kb_article_version的版本';
COMMENT ON COLUMN itsm.itsm_kb_article.probe_ref_id IS '监控探针关联标识，故障发生时自动推荐相关知识条目';
COMMENT ON COLUMN itsm.itsm_kb_article.published_at IS '发布时间';
COMMENT ON COLUMN itsm.itsm_kb_article.published_by IS '发布人ID';
COMMENT ON COLUMN itsm.itsm_kb_article.reviewer_id IS '审核人ID';
COMMENT ON COLUMN itsm.itsm_kb_article.reviewed_at IS '审核时间';
COMMENT ON COLUMN itsm.itsm_kb_article.review_comment IS '审核意见';
COMMENT ON COLUMN itsm.itsm_kb_article.view_count IS '浏览次数统计';
COMMENT ON COLUMN itsm.itsm_kb_article.useful_count IS '被标记为有用次数';
COMMENT ON COLUMN itsm.itsm_kb_article.created_at IS '创建时间';
COMMENT ON COLUMN itsm.itsm_kb_article.updated_at IS '更新时间';
COMMENT ON COLUMN itsm.itsm_kb_article.created_by IS '创建人';
COMMENT ON COLUMN itsm.itsm_kb_article.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_kb_article_status ON itsm.itsm_kb_article(status) WHERE is_deleted = 0;
CREATE INDEX idx_itsm_kb_article_category ON itsm.itsm_kb_article(category_id) WHERE is_deleted = 0;

CREATE TABLE IF NOT EXISTS itsm.itsm_kb_article_version (
    id          BIGINT      NOT NULL,
    article_id  BIGINT      NOT NULL,
    version     INTEGER     NOT NULL,
    content     TEXT        NOT NULL,
    change_note VARCHAR(256),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by  BIGINT      NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_kb_version PRIMARY KEY (id),
    CONSTRAINT uq_itsm_kb_version UNIQUE (article_id, version)
);

COMMENT ON TABLE itsm.itsm_kb_article_version IS '知识条目版本历史表，每次发布创建新版本，保留全部历史便于回溯';
COMMENT ON COLUMN itsm.itsm_kb_article_version.id IS '主键';
COMMENT ON COLUMN itsm.itsm_kb_article_version.article_id IS '知识条目ID';
COMMENT ON COLUMN itsm.itsm_kb_article_version.version IS '版本号，从1开始递增';
COMMENT ON COLUMN itsm.itsm_kb_article_version.content IS '富文本内容（HTML格式）';
COMMENT ON COLUMN itsm.itsm_kb_article_version.change_note IS '本版本修改说明';
COMMENT ON COLUMN itsm.itsm_kb_article_version.created_at IS '版本创建时间';
COMMENT ON COLUMN itsm.itsm_kb_article_version.created_by IS '版本创建人';

CREATE INDEX idx_itsm_kb_version_article ON itsm.itsm_kb_article_version(article_id, version DESC);