-- ============================================================
-- MES 基础数据模块 · DDL 脚本
-- 数据库：PostgreSQL 15.x（MES 生产库，只读接入）
-- 模块：01-基础数据
-- 包含表：产品主数据、物料主数据、BOM主表、BOM明细、
--         客户主数据、供应商主数据、仓库主数据、储位主数据
-- 导出时间：2026-04-01
-- 说明：本文件由 DBA 从生产库导出，已移除分区定义和存储参数，
--       保留字段注释供 AI 知识库训练使用。
-- ============================================================


-- ------------------------------------------------------------
-- 1. 产品主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.product (
    id              BIGSERIAL,
    product_code    VARCHAR(50)  NOT NULL,
    product_name    VARCHAR(200) NOT NULL,
    product_type    SMALLINT     NOT NULL DEFAULT 1,
    spec            VARCHAR(200),
    unit            VARCHAR(20)  NOT NULL DEFAULT '片',
    net_weight      NUMERIC(12,4),
    gross_weight    NUMERIC(12,4),
    lead_time       INTEGER,
    min_order_qty   NUMERIC(12,2) NOT NULL DEFAULT 0,
    safety_stock    NUMERIC(12,2) NOT NULL DEFAULT 0,
    shelf_life_days INTEGER,
    is_serialized   BOOLEAN      NOT NULL DEFAULT FALSE,
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(500),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50),
    updated_at      TIMESTAMP,
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

COMMENT ON TABLE public.product IS '产品主数据，记录封测厂所有产品的基本属性';
COMMENT ON COLUMN public.product.id IS '产品ID，自增主键';
COMMENT ON COLUMN public.product.product_code IS '产品编码，全局唯一，格式如 XTP-001-A';
COMMENT ON COLUMN public.product.product_name IS '产品名称';
COMMENT ON COLUMN public.product.product_type IS '产品类型：1=成品，2=半成品，3=测试品';
COMMENT ON COLUMN public.product.spec IS '规格型号，如封装形式 QFN48、DIP16 等';
COMMENT ON COLUMN public.product.unit IS '计量单位，常用值：片、卷、盒';
COMMENT ON COLUMN public.product.net_weight IS '净重（克）';
COMMENT ON COLUMN public.product.gross_weight IS '毛重（克）';
COMMENT ON COLUMN public.product.lead_time IS '标准生产提前期（天）';
COMMENT ON COLUMN public.product.min_order_qty IS '最小订单量';
COMMENT ON COLUMN public.product.safety_stock IS '安全库存量';
COMMENT ON COLUMN public.product.shelf_life_days IS '保质期（天），NULL 表示无限期';
COMMENT ON COLUMN public.product.is_serialized IS '是否序列号管理：true=每片有唯一序列号，false=批次管理';
COMMENT ON COLUMN public.product.status IS '状态：1=有效，0=停用，2=研发中';
COMMENT ON COLUMN public.product.deleted IS '逻辑删除：0=正常，1=已删除';

CREATE UNIQUE INDEX idx_product_code ON public.product (product_code) WHERE deleted = 0;
CREATE INDEX idx_product_type_status ON public.product (product_type, status);


-- ------------------------------------------------------------
-- 2. 物料主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.material (
    id              BIGSERIAL,
    material_code   VARCHAR(50)  NOT NULL,
    material_name   VARCHAR(200) NOT NULL,
    material_type   SMALLINT     NOT NULL DEFAULT 1,
    spec            VARCHAR(200),
    unit            VARCHAR(20)  NOT NULL DEFAULT '片',
    supplier_code   VARCHAR(50),
    lead_time       INTEGER,
    safety_stock    NUMERIC(12,2) NOT NULL DEFAULT 0,
    unit_price      NUMERIC(14,4),
    currency        VARCHAR(10)  NOT NULL DEFAULT 'CNY',
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(500),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50),
    updated_at      TIMESTAMP,
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

COMMENT ON TABLE public.material IS '物料主数据，记录生产所需原材料和辅助物料';
COMMENT ON COLUMN public.material.id IS '物料ID，自增主键';
COMMENT ON COLUMN public.material.material_code IS '物料编码，全局唯一';
COMMENT ON COLUMN public.material.material_name IS '物料名称';
COMMENT ON COLUMN public.material.material_type IS '物料类型：1=原材料（芯片），2=辅料（引线框），3=包材，4=化学品';
COMMENT ON COLUMN public.material.spec IS '规格描述';
COMMENT ON COLUMN public.material.unit IS '计量单位';
COMMENT ON COLUMN public.material.supplier_code IS '默认供应商编码，关联 supplier.supplier_code';
COMMENT ON COLUMN public.material.lead_time IS '采购提前期（天）';
COMMENT ON COLUMN public.material.safety_stock IS '安全库存量';
COMMENT ON COLUMN public.material.unit_price IS '含税单价';
COMMENT ON COLUMN public.material.currency IS '货币：CNY=人民币，USD=美元';
COMMENT ON COLUMN public.material.status IS '状态：1=有效，0=停用';
COMMENT ON COLUMN public.material.deleted IS '逻辑删除：0=正常，1=已删除';

CREATE UNIQUE INDEX idx_material_code ON public.material (material_code) WHERE deleted = 0;
CREATE INDEX idx_material_type ON public.material (material_type, status);


-- ------------------------------------------------------------
-- 3. BOM 主表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.bom_header (
    id              BIGSERIAL,
    bom_no          VARCHAR(50)  NOT NULL,
    product_code    VARCHAR(50)  NOT NULL,
    bom_version     VARCHAR(20)  NOT NULL DEFAULT '1.0',
    effective_date  DATE         NOT NULL,
    expire_date     DATE,
    status          SMALLINT     NOT NULL DEFAULT 1,
    approved_by     VARCHAR(50),
    approved_at     TIMESTAMP,
    remark          VARCHAR(500),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50),
    updated_at      TIMESTAMP,
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    CONSTRAINT uq_bom_product_version UNIQUE (product_code, bom_version)
);

COMMENT ON TABLE public.bom_header IS 'BOM主表（物料清单头），一个产品可有多版本BOM，同时只有一个有效版本';
COMMENT ON COLUMN public.bom_header.id IS 'BOM头ID，自增主键';
COMMENT ON COLUMN public.bom_header.bom_no IS 'BOM编号，如 BOM-XTP001-V1';
COMMENT ON COLUMN public.bom_header.product_code IS '产品编码，关联 product.product_code';
COMMENT ON COLUMN public.bom_header.bom_version IS 'BOM版本号，同产品升版时递增';
COMMENT ON COLUMN public.bom_header.effective_date IS '生效日期';
COMMENT ON COLUMN public.bom_header.expire_date IS '失效日期，NULL 表示永久有效';
COMMENT ON COLUMN public.bom_header.status IS 'BOM状态：1=有效，0=停用，2=草稿，3=待审批';
COMMENT ON COLUMN public.bom_header.approved_by IS '审批人工号';
COMMENT ON COLUMN public.bom_header.approved_at IS '审批时间';
COMMENT ON COLUMN public.bom_header.deleted IS '逻辑删除：0=正常，1=已删除';

CREATE UNIQUE INDEX idx_bom_no ON public.bom_header (bom_no) WHERE deleted = 0;
CREATE INDEX idx_bom_product ON public.bom_header (product_code, status);


-- ------------------------------------------------------------
-- 4. BOM 明细表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.bom_item (
    id              BIGSERIAL,
    bom_id          BIGINT       NOT NULL,
    item_seq        INTEGER      NOT NULL,
    material_code   VARCHAR(50)  NOT NULL,
    qty_per_unit    NUMERIC(14,6) NOT NULL,
    scrap_rate      NUMERIC(8,4)  NOT NULL DEFAULT 0,
    supply_type     SMALLINT     NOT NULL DEFAULT 1,
    is_key_material BOOLEAN      NOT NULL DEFAULT FALSE,
    remark          VARCHAR(200),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT fk_bom_item_header FOREIGN KEY (bom_id) REFERENCES public.bom_header(id)
);

COMMENT ON TABLE public.bom_item IS 'BOM明细，每条记录为某BOM下一种物料的用量定义';
COMMENT ON COLUMN public.bom_item.id IS '明细ID，自增主键';
COMMENT ON COLUMN public.bom_item.bom_id IS 'BOM头ID，关联 bom_header.id';
COMMENT ON COLUMN public.bom_item.item_seq IS '行号，同BOM内从1开始递增';
COMMENT ON COLUMN public.bom_item.material_code IS '物料编码，关联 material.material_code';
COMMENT ON COLUMN public.bom_item.qty_per_unit IS '每单位产品用量（6位小数支持微克级精度）';
COMMENT ON COLUMN public.bom_item.scrap_rate IS '损耗率（0.05 表示 5%）';
COMMENT ON COLUMN public.bom_item.supply_type IS '供料方式：1=自制，2=外购，3=客供';
COMMENT ON COLUMN public.bom_item.is_key_material IS '是否关键物料（影响批次追溯和进料检验策略）';

CREATE INDEX idx_bom_item_bom ON public.bom_item (bom_id);
CREATE INDEX idx_bom_item_material ON public.bom_item (material_code);


-- ------------------------------------------------------------
-- 5. 客户主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.customer (
    id              BIGSERIAL,
    customer_code   VARCHAR(50)  NOT NULL,
    customer_name   VARCHAR(200) NOT NULL,
    customer_abbr   VARCHAR(50),
    customer_type   SMALLINT     NOT NULL DEFAULT 1,
    country         VARCHAR(50)  NOT NULL DEFAULT '中国',
    contact_person  VARCHAR(50),
    contact_phone   VARCHAR(30),
    contact_email   VARCHAR(100),
    credit_limit    NUMERIC(16,2) NOT NULL DEFAULT 0,
    payment_terms   VARCHAR(100),
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(500),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50),
    updated_at      TIMESTAMP,
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

COMMENT ON TABLE public.customer IS '客户主数据，记录所有委托封测的客户信息';
COMMENT ON COLUMN public.customer.id IS '客户ID，自增主键';
COMMENT ON COLUMN public.customer.customer_code IS '客户编码，全局唯一';
COMMENT ON COLUMN public.customer.customer_name IS '客户全称';
COMMENT ON COLUMN public.customer.customer_abbr IS '客户简称，用于报表展示';
COMMENT ON COLUMN public.customer.customer_type IS '客户类型：1=设计公司（Fabless），2=IDM，3=研究院所';
COMMENT ON COLUMN public.customer.contact_phone IS '联系电话（脱敏存储，展示时仅显示末4位）';
COMMENT ON COLUMN public.customer.credit_limit IS '信用额度（元）';
COMMENT ON COLUMN public.customer.payment_terms IS '付款条件，如"月结30天"';
COMMENT ON COLUMN public.customer.status IS '状态：1=有效，0=停用，2=黑名单';
COMMENT ON COLUMN public.customer.deleted IS '逻辑删除：0=正常，1=已删除';

CREATE UNIQUE INDEX idx_customer_code ON public.customer (customer_code) WHERE deleted = 0;
CREATE INDEX idx_customer_status ON public.customer (status);


-- ------------------------------------------------------------
-- 6. 供应商主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.supplier (
    id              BIGSERIAL,
    supplier_code   VARCHAR(50)  NOT NULL,
    supplier_name   VARCHAR(200) NOT NULL,
    supplier_abbr   VARCHAR(50),
    supplier_type   SMALLINT     NOT NULL DEFAULT 1,
    country         VARCHAR(50)  NOT NULL DEFAULT '中国',
    contact_person  VARCHAR(50),
    contact_phone   VARCHAR(30),
    contact_email   VARCHAR(100),
    qualify_date    DATE,
    qualify_expire  DATE,
    rating          SMALLINT,
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(500),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_by      VARCHAR(50),
    updated_at      TIMESTAMP,
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

COMMENT ON TABLE public.supplier IS '供应商主数据，记录原材料和辅料的采购供应商';
COMMENT ON COLUMN public.supplier.id IS '供应商ID，自增主键';
COMMENT ON COLUMN public.supplier.supplier_code IS '供应商编码，全局唯一';
COMMENT ON COLUMN public.supplier.supplier_name IS '供应商全称';
COMMENT ON COLUMN public.supplier.supplier_abbr IS '供应商简称';
COMMENT ON COLUMN public.supplier.supplier_type IS '供应商类型：1=原材料，2=辅料，3=设备，4=化学品';
COMMENT ON COLUMN public.supplier.qualify_date IS '供应商资质认证日期';
COMMENT ON COLUMN public.supplier.qualify_expire IS '资质有效期，NULL 表示长期有效';
COMMENT ON COLUMN public.supplier.rating IS '供应商评级：1=A级，2=B级，3=C级，NULL=未评级';
COMMENT ON COLUMN public.supplier.status IS '状态：1=合格，0=停用，2=考察中，3=黑名单';
COMMENT ON COLUMN public.supplier.deleted IS '逻辑删除：0=正常，1=已删除';

CREATE UNIQUE INDEX idx_supplier_code ON public.supplier (supplier_code) WHERE deleted = 0;


-- ------------------------------------------------------------
-- 7. 仓库主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.warehouse (
    id              BIGSERIAL,
    warehouse_code  VARCHAR(50)  NOT NULL,
    warehouse_name  VARCHAR(100) NOT NULL,
    warehouse_type  SMALLINT     NOT NULL DEFAULT 1,
    area_sqm        NUMERIC(10,2),
    manager_emp_no  VARCHAR(20),
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(200),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

COMMENT ON TABLE public.warehouse IS '仓库主数据，定义厂区内各仓库（实物存放场所）';
COMMENT ON COLUMN public.warehouse.id IS '仓库ID，自增主键';
COMMENT ON COLUMN public.warehouse.warehouse_code IS '仓库编码，全局唯一，如 WH-RAW（原料仓）';
COMMENT ON COLUMN public.warehouse.warehouse_name IS '仓库名称';
COMMENT ON COLUMN public.warehouse.warehouse_type IS '仓库类型：1=原料仓，2=成品仓，3=半成品仓，4=不良品仓，5=客供料仓';
COMMENT ON COLUMN public.warehouse.area_sqm IS '仓库面积（平方米）';
COMMENT ON COLUMN public.warehouse.manager_emp_no IS '仓库管理员工号，关联 employee.emp_no';
COMMENT ON COLUMN public.warehouse.status IS '状态：1=启用，0=停用';

CREATE UNIQUE INDEX idx_warehouse_code ON public.warehouse (warehouse_code) WHERE deleted = 0;


-- ------------------------------------------------------------
-- 8. 储位主数据表
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS public.warehouse_location (
    id              BIGSERIAL,
    location_code   VARCHAR(50)  NOT NULL,
    location_name   VARCHAR(100) NOT NULL,
    warehouse_id    BIGINT       NOT NULL,
    aisle           VARCHAR(20),
    shelf           VARCHAR(20),
    level_no        SMALLINT,
    max_capacity    NUMERIC(12,2),
    capacity_unit   VARCHAR(20),
    location_type   SMALLINT     NOT NULL DEFAULT 1,
    status          SMALLINT     NOT NULL DEFAULT 1,
    remark          VARCHAR(200),
    created_by      VARCHAR(50)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    deleted         SMALLINT     NOT NULL DEFAULT 0,
    PRIMARY KEY (id),
    CONSTRAINT fk_location_warehouse FOREIGN KEY (warehouse_id) REFERENCES public.warehouse(id)
);

COMMENT ON TABLE public.warehouse_location IS '储位主数据，仓库内货架/储位的精细化管理';
COMMENT ON COLUMN public.warehouse_location.id IS '储位ID，自增主键';
COMMENT ON COLUMN public.warehouse_location.location_code IS '储位编码，同仓库内唯一，如 A-01-03（A巷第1架第3层）';
COMMENT ON COLUMN public.warehouse_location.warehouse_id IS '所属仓库ID，关联 warehouse.id';
COMMENT ON COLUMN public.warehouse_location.aisle IS '巷道号';
COMMENT ON COLUMN public.warehouse_location.shelf IS '货架号';
COMMENT ON COLUMN public.warehouse_location.level_no IS '层号（从1开始）';
COMMENT ON COLUMN public.warehouse_location.max_capacity IS '最大存放量（按 capacity_unit 计）';
COMMENT ON COLUMN public.warehouse_location.capacity_unit IS '容量单位，如 片、卷、箱';
COMMENT ON COLUMN public.warehouse_location.location_type IS '储位类型：1=普通，2=隔离区（不良品），3=冷藏，4=危化品';
COMMENT ON COLUMN public.warehouse_location.status IS '状态：1=可用，0=停用，2=维修中，3=已满';

CREATE UNIQUE INDEX idx_location_code ON public.warehouse_location (location_code, warehouse_id) WHERE deleted = 0;
CREATE INDEX idx_location_warehouse ON public.warehouse_location (warehouse_id, status);
