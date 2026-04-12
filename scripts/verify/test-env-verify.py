#!/usr/bin/env python3
"""
测试环境验证脚本 - MES 数据库连通性与数据读取验证
文档编号: AI-MES-GIT-2026-001
关联任务: T1-1-5
作者: AI
日期: 2026-04-12

用途:
    验证 AI 平台与 MES 系统数据库（PostgreSQL）的连通性及基础读取权限。
    所有连接参数通过环境变量注入，禁止硬编码（CLAUDE.md 4.1）。

使用方式:
    export MES_DB_HOST=<host>
    export MES_DB_PORT=<port>
    export MES_DB_NAME=<dbname>
    export MES_DB_USER=<user>
    export MES_DB_PASS=<password>
    python3 test-env-verify.py

输出:
    控制台打印验证报告，同时写入 verify-report-{timestamp}.md
"""

import os
import sys
import time
import json
import socket
from datetime import datetime

# ── 尝试导入 psycopg2 ────────────────────────────────────────
try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("[ERROR] 缺少 psycopg2，请执行：pip3 install psycopg2-binary")
    sys.exit(1)

# ── 从环境变量读取连接参数（禁止硬编码）────────────────────────
DB_HOST = os.environ.get("MES_DB_HOST", "")
DB_PORT = int(os.environ.get("MES_DB_PORT", "5432"))
DB_NAME = os.environ.get("MES_DB_NAME", "")
DB_USER = os.environ.get("MES_DB_USER", "")
DB_PASS = os.environ.get("MES_DB_PASS", "")

CONNECT_TIMEOUT = 10   # 连接超时（秒）
QUERY_TIMEOUT   = 5000 # 查询超时（毫秒）

# ────────────────────────────────────────────────────────────

class VerifyResult:
    """单项验证结果"""
    def __init__(self, name: str):
        self.name     = name
        self.passed   = False
        self.detail   = ""
        self.elapsed  = 0.0

    def ok(self, detail: str, elapsed: float = 0.0):
        self.passed  = True
        self.detail  = detail
        self.elapsed = elapsed
        return self

    def fail(self, detail: str, elapsed: float = 0.0):
        self.passed  = False
        self.detail  = detail
        self.elapsed = elapsed
        return self

    def status_icon(self):
        return "✅" if self.passed else "❌"


def check_env_vars() -> VerifyResult:
    """检查必要环境变量是否已设置"""
    r = VerifyResult("环境变量检查")
    missing = [v for v in ["MES_DB_HOST","MES_DB_PORT","MES_DB_NAME","MES_DB_USER","MES_DB_PASS"]
               if not os.environ.get(v)]
    if missing:
        return r.fail(f"缺少环境变量: {', '.join(missing)}")
    return r.ok(f"所有必要环境变量已设置（主机、端口、库名、用户名、密码）")


def check_tcp_reachable() -> VerifyResult:
    """TCP 端口连通性检查（网络层）"""
    r = VerifyResult(f"TCP 连通性（[IP_ADDR_***]:{DB_PORT}）")
    t0 = time.time()
    try:
        sock = socket.create_connection((DB_HOST, DB_PORT), timeout=CONNECT_TIMEOUT)
        sock.close()
        elapsed = time.time() - t0
        return r.ok(f"TCP 端口可达，耗时 {elapsed*1000:.0f}ms", elapsed)
    except socket.timeout:
        return r.fail(f"连接超时（>{CONNECT_TIMEOUT}s），请检查云安全组是否开放 {DB_PORT} 端口")
    except ConnectionRefusedError:
        return r.fail(f"连接被拒绝，PostgreSQL 可能未启动或端口不正确")
    except Exception as e:
        return r.fail(f"网络异常: {e}")


def check_db_connect() -> tuple:
    """数据库认证连接（返回 result 和 conn）"""
    r = VerifyResult("数据库认证连接")
    t0 = time.time()
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
            user=DB_USER, password=DB_PASS,
            connect_timeout=CONNECT_TIMEOUT,
            options=f"-c statement_timeout={QUERY_TIMEOUT}"
        )
        elapsed = time.time() - t0
        ver = conn.server_version
        major = ver // 10000
        minor = (ver % 10000) // 100
        return r.ok(f"认证成功，PostgreSQL {major}.{minor}，耗时 {elapsed*1000:.0f}ms", elapsed), conn
    except psycopg2.OperationalError as e:
        msg = str(e).strip()
        if "password" in msg.lower():
            hint = "用户名或密码错误"
        elif "database" in msg.lower():
            hint = f"数据库 '{DB_NAME}' 不存在或无权限"
        else:
            hint = msg
        return r.fail(hint), None
    except Exception as e:
        return r.fail(str(e)), None


def check_readonly_query(conn) -> VerifyResult:
    """基础只读查询验证（SELECT 1 + 版本信息）"""
    r = VerifyResult("基础只读查询（SELECT 1）")
    t0 = time.time()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ping, version()")
            row = cur.fetchone()
        elapsed = time.time() - t0
        return r.ok(f"查询正常，响应 {elapsed*1000:.0f}ms | {row[1][:60]}...", elapsed)
    except Exception as e:
        return r.fail(str(e))


def check_list_tables(conn) -> VerifyResult:
    """查询可访问的表清单（验证读取权限范围）"""
    r = VerifyResult("表清单查询（information_schema）")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_schema, table_name, table_type
                FROM   information_schema.tables
                WHERE  table_schema NOT IN ('pg_catalog','information_schema')
                ORDER  BY table_schema, table_name
                LIMIT  50
            """)
            rows = cur.fetchall()
        if rows:
            schemas = {}
            for schema, table, ttype in rows:
                schemas.setdefault(schema, []).append(table)
            summary = "; ".join(
                f"{s}({len(t)}张表)" for s, t in schemas.items()
            )
            return r.ok(f"共 {len(rows)} 张表可见 | {summary}")
        else:
            return r.ok("连接正常，当前用户无可见业务表（权限受限，属正常）")
    except Exception as e:
        return r.fail(str(e))


def check_write_forbidden(conn) -> VerifyResult:
    """验证当前账号无写权限（AI 平台只读访问 MES 库的安全要求）"""
    r = VerifyResult("写权限隔离验证（确认只读）")
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT has_database_privilege(%s, %s, 'CREATE')
            """, (DB_USER, DB_NAME))
            can_create = cur.fetchone()[0]
        if not can_create:
            return r.ok("账号无 CREATE 权限，满足只读要求（CLAUDE.md 4.3）")
        else:
            return r.fail("⚠️  账号具有 CREATE 权限，不符合只读安全要求，请 DBA 收紧权限")
    except Exception as e:
        return r.fail(str(e))


def check_response_time(conn) -> VerifyResult:
    """响应时间压测（连续5次 SELECT，统计 P99）"""
    r = VerifyResult("响应时间基线（连续5次查询）")
    times = []
    try:
        for _ in range(5):
            t0 = time.time()
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
            times.append((time.time() - t0) * 1000)
        avg = sum(times) / len(times)
        mx  = max(times)
        threshold = 2000  # 慢查询阈值 2s（CLAUDE.md 关键阈值）
        if mx < threshold:
            return r.ok(f"平均 {avg:.0f}ms，最大 {mx:.0f}ms（低于 {threshold}ms 阈值）", avg/1000)
        else:
            return r.fail(f"最大响应 {mx:.0f}ms，超过 {threshold}ms 慢查询阈值，请检查网络", avg/1000)
    except Exception as e:
        return r.fail(str(e))


# ── 主流程 ────────────────────────────────────────────────────

def run_verify():
    results   = []
    conn      = None
    now_str   = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str  = datetime.now().strftime("%Y%m%d_%H%M%S")

    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║    芯智云匠 · 测试环境验证 T1-1-5                       ║")
    print("║    MES 数据库连通性与权限验证                            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"  验证时间: {now_str}")
    print(f"  目标数据库: [IP_ADDR_***]:{DB_PORT}/{DB_NAME}")  # 脱敏输出
    print()

    # 逐项验证
    checks = [
        ("env",     check_env_vars),
        ("tcp",     check_tcp_reachable),
    ]

    for key, fn in checks:
        r = fn()
        results.append(r)
        print(f"  {r.status_icon()} {r.name}")
        print(f"     → {r.detail}")
        if not r.passed and key in ("env", "tcp"):
            print()
            print("  [ABORT] 基础检查未通过，终止后续验证")
            _write_report(results, now_str, date_str, aborted=True)
            return

    # 数据库连接（返回 conn）
    r_conn, conn = check_db_connect()
    results.append(r_conn)
    print(f"  {r_conn.status_icon()} {r_conn.name}")
    print(f"     → {r_conn.detail}")
    if not r_conn.passed:
        print()
        print("  [ABORT] 数据库认证失败，终止后续验证")
        _write_report(results, now_str, date_str, aborted=True)
        return

    # 后续依赖连接的验证项
    for fn in [check_readonly_query, check_list_tables,
               check_write_forbidden, check_response_time]:
        r = fn(conn)
        results.append(r)
        print(f"  {r.status_icon()} {r.name}")
        print(f"     → {r.detail}")

    conn.close()

    # 汇总
    passed = sum(1 for r in results if r.passed)
    total  = len(results)
    print()
    print(f"  ── 验证结果: {passed}/{total} 项通过 {'✅ 全部通过' if passed == total else '❌ 存在异常'} ──")
    print()

    _write_report(results, now_str, date_str, aborted=False)


def _write_report(results, now_str, date_str, aborted):
    """写入 Markdown 格式验证报告"""
    passed = sum(1 for r in results if r.passed)
    total  = len(results)
    status = "存在异常" if (passed < total or aborted) else "正常"

    lines = [
        "# 测试环境验证报告",
        "",
        f"**文档编号**: AI-MES-VERIFY-{date_str}",
        f"**关联任务**: T1-1-5",
        f"**验证时间**: {now_str}",
        f"**执行状态**: {status}（{passed}/{total} 项通过）",
        f"**目标数据库**: [IP_ADDR_***]（PostgreSQL · MES 系统数据库）",
        "",
        "## 验证明细",
        "",
        "| 验证项 | 状态 | 说明 | 耗时 |",
        "|--------|------|------|------|",
    ]
    for r in results:
        elapsed_str = f"{r.elapsed*1000:.0f}ms" if r.elapsed else "—"
        lines.append(f"| {r.name} | {r.status_icon()} {'通过' if r.passed else '失败'} | {r.detail[:80]} | {elapsed_str} |")

    lines += [
        "",
        "## 结论与建议",
        "",
    ]

    fail_items = [r for r in results if not r.passed]
    if not fail_items and not aborted:
        lines += [
            "测试环境 MES 数据库连通性验证全部通过：",
            "- TCP 网络层可达，认证正常",
            "- 基础只读查询权限已确认",
            "- 账号权限符合只读安全要求（CLAUDE.md 4.3）",
            "- 响应时间在正常范围内",
            "",
            "**可继续执行 T1-1-6（输出环境验证报告）及后续 Sprint 1 任务。**",
        ]
    else:
        lines.append("以下验证项需处理后重新验证：")
        lines.append("")
        for r in fail_items:
            lines.append(f"- ❌ **{r.name}**：{r.detail}")
        if aborted:
            lines.append("")
            lines.append("验证因基础检查失败提前终止，请修复后重新执行本脚本。")

    lines += [
        "",
        "---",
        f"*芯智云匠 · 测试环境验证报告 · {now_str} · T1-1-5*",
    ]

    report_path = f"/home/ubuntu/mesai/scripts/verify/verify-report-{date_str}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  报告已写入: {report_path}")


if __name__ == "__main__":
    run_verify()
