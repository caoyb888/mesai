-- V8__create_attachment_table.sql
-- 模块八：附件管理
-- 包含表：itsm_attachment

CREATE TABLE IF NOT EXISTS itsm.itsm_attachment (
    id              BIGINT          NOT NULL,
    ref_type        VARCHAR(32)     NOT NULL,
    ref_id          BIGINT          NOT NULL,
    file_name       VARCHAR(256)    NOT NULL,
    file_size       BIGINT          NOT NULL,
    file_type       VARCHAR(64)     NOT NULL,
    file_ext        VARCHAR(16)     NOT NULL,
    bucket_name     VARCHAR(64)     NOT NULL,
    object_key      VARCHAR(512)    NOT NULL,
    md5             VARCHAR(32),
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    created_by      BIGINT          NOT NULL DEFAULT 0,
    is_deleted      SMALLINT        NOT NULL DEFAULT 0,
    
    CONSTRAINT pk_itsm_attachment PRIMARY KEY (id),
    CONSTRAINT chk_itsm_attachment_ref_type CHECK (
        ref_type IN ('TICKET','KB_ARTICLE','COMMENT')
    ),
    CONSTRAINT chk_itsm_attachment_size CHECK (
        file_size BETWEEN 1 AND 20971520
    )
);

COMMENT ON TABLE itsm.itsm_attachment IS '附件元数据表，文件实体存储于MinIO对象存储，此表仅存元数据';
COMMENT ON COLUMN itsm.itsm_attachment.id IS '主键';
COMMENT ON COLUMN itsm.itsm_attachment.ref_type IS '关联业务类型：TICKET工单 KB_ARTICLE知识条目 COMMENT评论';
COMMENT ON COLUMN itsm.itsm_attachment.ref_id IS '关联业务ID';
COMMENT ON COLUMN itsm.itsm_attachment.file_name IS '原始文件名';
COMMENT ON COLUMN itsm.itsm_attachment.file_size IS '文件大小（字节），最大20MB（20971520字节）';
COMMENT ON COLUMN itsm.itsm_attachment.file_type IS 'MIME类型，如application/pdf image/png';
COMMENT ON COLUMN itsm.itsm_attachment.file_ext IS '文件扩展名，如pdf png docx';
COMMENT ON COLUMN itsm.itsm_attachment.bucket_name IS 'MinIO bucket名称';
COMMENT ON COLUMN itsm.itsm_attachment.object_key IS 'MinIO对象路径，格式：{ref_type}/{year}/{month}/{uuid}.{ext}';
COMMENT ON COLUMN itsm.itsm_attachment.md5 IS '文件MD5哈希，用于完整性校验';
COMMENT ON COLUMN itsm.itsm_attachment.created_at IS '上传时间';
COMMENT ON COLUMN itsm.itsm_attachment.created_by IS '上传人ID';
COMMENT ON COLUMN itsm.itsm_attachment.is_deleted IS '逻辑删除标记';

CREATE INDEX idx_itsm_attachment_ref ON itsm.itsm_attachment(ref_type, ref_id) WHERE is_deleted = 0;