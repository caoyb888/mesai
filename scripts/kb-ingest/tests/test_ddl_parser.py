"""
DDL 解析器单元测试

关联任务：S2-1 T2-1-1
作者：AI（芯智云匠）
日期：2026-04-12
"""

import sys
import textwrap
import tempfile
from pathlib import Path

# 将父目录加入 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ddl_parser import PostgresDDLParser, MarkdownRenderer, TableDef


# ── 测试辅助函数 ──────────────────────────────────────────────

def parse_sql(sql: str, module: str = "测试模块") -> list[TableDef]:
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".sql", encoding="utf-8", delete=False
    ) as f:
        f.write(sql)
        tmp_path = Path(f.name)
    parser = PostgresDDLParser()
    return parser.parse_file(tmp_path, module=module)


# ── 基础解析测试 ──────────────────────────────────────────────

def test_parse_simple_table():
    """解析最简单的建表语句"""
    sql = textwrap.dedent("""
        CREATE TABLE products (
            id   BIGSERIAL PRIMARY KEY,
            code VARCHAR(50) NOT NULL,
            name VARCHAR(200)
        );
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    t = tables[0]
    assert t.name == "products"
    assert len(t.columns) == 3
    assert t.primary_key == ["id"]


def test_parse_table_with_schema():
    """解析带 Schema 前缀的建表语句"""
    sql = textwrap.dedent("""
        CREATE TABLE public.work_orders (
            id          BIGSERIAL,
            order_no    VARCHAR(50) NOT NULL,
            status      SMALLINT NOT NULL DEFAULT 1,
            created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
            PRIMARY KEY (id)
        );
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    t = tables[0]
    assert t.schema == "public"
    assert t.name == "work_orders"
    assert t.primary_key == ["id"]
    # status 字段有默认值
    status_col = next(c for c in t.columns if c.name == "status")
    assert status_col.nullable is False
    assert status_col.default is not None


def test_parse_table_comments():
    """解析 COMMENT ON TABLE 和 COMMENT ON COLUMN"""
    sql = textwrap.dedent("""
        CREATE TABLE process_route (
            id         BIGSERIAL PRIMARY KEY,
            route_no   VARCHAR(50) NOT NULL,
            route_name VARCHAR(200) NOT NULL,
            status     SMALLINT NOT NULL DEFAULT 1
        );

        COMMENT ON TABLE process_route IS '工艺路线主表，定义产品生产路径';
        COMMENT ON COLUMN process_route.route_no IS '工艺路线编号，全局唯一';
        COMMENT ON COLUMN process_route.status IS '状态：1=有效，0=停用';
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    t = tables[0]
    assert t.comment == "工艺路线主表，定义产品生产路径"
    route_no = next(c for c in t.columns if c.name == "route_no")
    assert route_no.comment == "工艺路线编号，全局唯一"
    status = next(c for c in t.columns if c.name == "status")
    assert status.comment == "状态：1=有效，0=停用"


def test_parse_indexes():
    """解析 CREATE INDEX / CREATE UNIQUE INDEX"""
    sql = textwrap.dedent("""
        CREATE TABLE work_orders (
            id       BIGSERIAL PRIMARY KEY,
            order_no VARCHAR(50) NOT NULL,
            status   SMALLINT NOT NULL,
            dept     VARCHAR(50)
        );

        CREATE UNIQUE INDEX idx_wo_order_no ON work_orders (order_no);
        CREATE INDEX idx_wo_status ON work_orders (status, dept);
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    t = tables[0]
    assert len(t.indexes) == 2
    unique_idx = next(idx for idx in t.indexes if idx.unique)
    assert unique_idx.name == "idx_wo_order_no"
    assert unique_idx.columns == ["order_no"]
    multi_idx = next(idx for idx in t.indexes if not idx.unique)
    assert "status" in multi_idx.columns
    assert "dept" in multi_idx.columns


def test_parse_multiple_tables():
    """解析多张表的 DDL 文件"""
    sql = textwrap.dedent("""
        CREATE TABLE departments (
            id   BIGSERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        );

        CREATE TABLE employees (
            id      BIGSERIAL PRIMARY KEY,
            name    VARCHAR(100) NOT NULL,
            dept_id BIGINT NOT NULL
        );

        CREATE TABLE products (
            id   BIGSERIAL PRIMARY KEY,
            code VARCHAR(50) NOT NULL
        );
    """)
    tables = parse_sql(sql)
    assert len(tables) == 3
    names = {t.name for t in tables}
    assert names == {"departments", "employees", "products"}


def test_parse_nullable_and_not_null():
    """正确区分可空和非空字段"""
    sql = textwrap.dedent("""
        CREATE TABLE test_table (
            required_col VARCHAR(50) NOT NULL,
            optional_col VARCHAR(50),
            defaulted    INTEGER NOT NULL DEFAULT 0
        );
    """)
    tables = parse_sql(sql)
    t = tables[0]
    req = next(c for c in t.columns if c.name == "required_col")
    opt = next(c for c in t.columns if c.name == "optional_col")
    dft = next(c for c in t.columns if c.name == "defaulted")
    assert req.nullable is False
    assert opt.nullable is True
    assert dft.nullable is False
    assert dft.default is not None


def test_parse_if_not_exists():
    """解析 CREATE TABLE IF NOT EXISTS"""
    sql = textwrap.dedent("""
        CREATE TABLE IF NOT EXISTS inspection_records (
            id      BIGSERIAL PRIMARY KEY,
            result  SMALLINT NOT NULL
        );
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    assert tables[0].name == "inspection_records"


def test_skip_constraints():
    """约束定义行（CONSTRAINT/FOREIGN KEY 等）不被解析为字段"""
    sql = textwrap.dedent("""
        CREATE TABLE order_items (
            id         BIGSERIAL,
            order_id   BIGINT NOT NULL,
            product_id BIGINT NOT NULL,
            quantity   INTEGER NOT NULL,
            PRIMARY KEY (id),
            CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES orders(id),
            CONSTRAINT chk_qty  CHECK (quantity > 0)
        );
    """)
    tables = parse_sql(sql)
    assert len(tables) == 1
    t = tables[0]
    col_names = {c.name for c in t.columns}
    # CONSTRAINT / CHECK 行不应被解析为字段
    assert "fk_order" not in col_names
    assert "chk_qty" not in col_names
    assert {"id", "order_id", "product_id", "quantity"} == col_names


def test_markdown_render_contains_key_info():
    """Markdown 渲染结果包含表名、字段名和注释"""
    sql = textwrap.dedent("""
        CREATE TABLE equipment (
            id        BIGSERIAL PRIMARY KEY,
            equip_no  VARCHAR(50) NOT NULL,
            equip_name VARCHAR(200)
        );
        COMMENT ON TABLE equipment IS '设备台账';
        COMMENT ON COLUMN equipment.equip_no IS '设备编码';
    """)
    tables = parse_sql(sql, module="设备管理")
    renderer = MarkdownRenderer()
    md = renderer.render(tables[0])

    assert "equipment" in md
    assert "设备台账" in md
    assert "equip_no" in md
    assert "设备编码" in md
    assert "设备管理" in md
    assert "chunk_id" in md   # 尾注包含 chunk_id


def test_module_field_set():
    """解析时正确设置 module 字段"""
    sql = "CREATE TABLE t (id BIGSERIAL PRIMARY KEY);"
    tables = parse_sql(sql, module="质量管理")
    assert tables[0].module == "质量管理"


if __name__ == "__main__":
    # 简单运行所有测试（无需 pytest）
    test_funcs = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for fn in test_funcs:
        try:
            fn()
            print(f"  ✅ {fn.__name__}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {fn.__name__}: {e}")
            failed += 1
    print(f"\n共 {passed+failed} 个测试，通过 {passed} 个，失败 {failed} 个")
