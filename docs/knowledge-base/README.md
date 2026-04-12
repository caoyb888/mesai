# MES AI 知识库 · 材料管理规范

**文件编号**：AI-MES-KB-2026-001
**版本**：V1.0 · 2026-04-12
**关联 Story**：S2-1 MES数据库结构理解训练

---

## 一、目录结构说明

```
docs/knowledge-base/
├── README.md                   # 本文件：材料管理规范与入库流程
│
├── mes-ddl/                    # ① 甲方提供的 PostgreSQL DDL 文件（原始）
│   ├── 01-基础数据/
│   │   ├── raw/                #   原始 .sql 文件（保持甲方原样）
│   │   └── parsed/             #   解析后的 Markdown 表卡片
│   ├── 02-工艺管理/
│   ├── 03-生产计划/
│   ├── 04-作业管理/
│   ├── 05-设备管理/
│   └── 06-质量管理/
│
├── data-dict/                  # ② 甲方提供的数据字典（整理后 Markdown）
│   ├── 01-基础数据.md
│   ├── 02-工艺管理.md
│   ├── 03-生产计划.md
│   ├── 04-作业管理.md
│   ├── 05-设备管理.md
│   └── 06-质量管理.md
│
├── module-overviews/            # ③ 各模块业务概述（训练上下文用）
│   └── mes-modules-overview.md
│
└── validation/                  # ④ 验收测试题库（T2-1-4/T2-1-5）
    ├── questions.md             #   题目与评分标准
    └── answer-key.md            #   参考答案（人工评分用）
```

---

## 二、甲方材料交付要求（需提前与甲方确认）

### 2.1 必要材料清单

| # | 材料名称 | 格式要求 | 优先级 | 备注 |
|---|--------|--------|------|------|
| 1 | MES 数据库 DDL 脚本 | `.sql` PostgreSQL 格式 | 🔴 Critical | 必须含 `COMMENT ON COLUMN` 注释 |
| 2 | 数据字典 | Excel `.xlsx` 或 Word `.docx` | 🔴 Critical | 含字段中文说明、枚举值定义 |
| 3 | 模块功能说明文档 | Word/PDF | 🟠 High | 描述各模块业务流程 |
| 4 | 表间关系图（ERD） | PNG / Visio / PowerDesigner | 🟠 High | 辅助理解外键关联 |
| 5 | 枚举值字典 | Excel | 🟠 High | status/type 等字段的所有可选值 |
| 6 | MES 操作手册 | Word/PDF | 🟡 Medium | 理解业务操作背景 |

### 2.2 DDL 文件格式要求

**理想格式**（含注释，AI 理解质量最高）：

```sql
-- ============================================================
-- 模块：工艺管理
-- 表名：process_route（工艺路线主表）
-- 版本：V2.3
-- ============================================================
CREATE TABLE process_route (
    id            BIGSERIAL PRIMARY KEY,
    route_no      VARCHAR(50)  NOT NULL,   -- 工艺路线编号，格式：PR-YYYYMM-NNN
    route_name    VARCHAR(200) NOT NULL,   -- 工艺路线名称
    product_code  VARCHAR(50)  NOT NULL,   -- 产品编码，关联 product.product_code
    status        SMALLINT     NOT NULL DEFAULT 1,  -- 状态：1-有效 0-停用
    created_at    TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP    NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE  process_route IS '工艺路线主表，定义产品的生产工艺路径';
COMMENT ON COLUMN process_route.route_no IS '工艺路线编号，格式：PR-YYYYMM-NNN，全局唯一';
COMMENT ON COLUMN process_route.status   IS '状态：1=有效可用，0=已停用，停用后不可新建工单';
```

**最低格式**（无注释，需配合数据字典补充）：

```sql
CREATE TABLE process_route (
    id           BIGSERIAL PRIMARY KEY,
    route_no     VARCHAR(50)  NOT NULL,
    route_name   VARCHAR(200) NOT NULL,
    ...
);
```

> **注意**：无注释的 DDL 必须配合数据字典 Excel 才能完整入库。

---

## 三、知识库入库流程（T2-1-1 执行步骤）

```
① 材料接收
   甲方提供 → 存入 mes-ddl/XX-模块名/raw/
                    data-dict/XX-模块名.xlsx

② DDL 解析（自动）
   python scripts/kb-ingest/ddl_parser.py \
       --input  docs/knowledge-base/mes-ddl/02-工艺管理/raw/ \
       --output docs/knowledge-base/mes-ddl/02-工艺管理/parsed/ \
       --module 工艺管理

③ 数据字典格式化（半自动）
   python scripts/kb-ingest/dict_formatter.py \
       --input  docs/knowledge-base/data-dict/02-工艺管理.xlsx \
       --output docs/knowledge-base/data-dict/02-工艺管理.md

④ 合并 & 入库（自动）
   python scripts/kb-ingest/kb_ingest.py \
       --module 工艺管理 \
       --ddl-dir   docs/knowledge-base/mes-ddl/02-工艺管理/parsed/ \
       --dict-file docs/knowledge-base/data-dict/02-工艺管理.md \
       --collection mes_db_structure

⑤ 验证入库结果
   python scripts/kb-ingest/validate_ingestion.py \
       --module 工艺管理
```

---

## 四、Chunk 设计规范

| Chunk 类型 | 来源 | 大小（约） | 覆盖内容 |
|-----------|------|---------|--------|
| `module_overview` | 人工编写 | 400~600 tokens | 模块业务背景、核心实体、关键流程 |
| `table_card` | DDL + 数据字典 | 300~600 tokens | 单表结构（字段/类型/约束/注释） |
| `table_relation` | ERD + DDL | 200~400 tokens | 表间关联关系、外键约束 |
| `enum_values` | 数据字典枚举值 | 100~300 tokens | 状态/类型字段的所有枚举值说明 |
| `business_rule` | 操作手册 | 200~500 tokens | 字段取值限制、业务约束规则 |

**Chunk 命名规范**：`{模块英文}_{表名}_{chunk_type}_{序号}`
例：`process_route_table_card_001`

---

## 五、MES 核心模块范围（验收必须覆盖）

| 模块编号 | 模块名称 | 关键表（预计） | 验收 SQL 题数 |
|---------|--------|------------|------------|
| 01 | 基础数据（Master Data） | 产品、物料、BOM、工位、班组 | ≥5 |
| 02 | 工艺管理（Process） | 工艺路线、工序、标准工时 | ≥5 |
| 03 | 生产计划（Planning） | 生产计划、工单、排程 | ≥5 |
| 04 | 作业管理（Operation） | 报工记录、在制品跟踪、异常记录 | ≥5 |
| 05 | 设备管理（Equipment） | 设备台账、点检记录、维修工单 | ≥5 |
| 06 | 质量管理（Quality） | 检验方案、检验记录、不良品处理 | ≥5 |

---

*最后更新：2026-04-12 · AI（芯智云匠） · REQ-MES-AI-20260412-005*
