"""
PII 脱敏服务单元测试（CLAUDE.md 4.2 全 7 类 + 误伤防护）

覆盖：7 类敏感信息各自命中；关键误报防护（钢厂厂区码 LZ/RZ/SHIP、钢牌号、
     下划线标识符/列名、任务单号、纯数字日期段不得被抹）；desensitize_verbose 明细。

关联任务：S3 训练前置——脱敏链路补全（对接真实 MES 外发 Kimi）
作者：AI（芯智云匠）
日期：2026-07-14
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.desensitize import desensitize, desensitize_verbose


# ── 7 类命中 ─────────────────────────────────────────────────
def should_mask_internal_ip():
    clean, hits = desensitize("服务器 192.168.1.100 连接异常")
    assert "192.168.1.100" not in clean and "[IP_ADDR_***]" in clean and hits == 1


def should_mask_internal_ranges_10_172_100():
    # 内网段：RFC1918 的 10./172.16-31. 与 CGNAT 100.64-127. 均脱敏
    clean, hits = desensitize("节点 10.0.5.9、172.16.3.4、100.90.1.2 内网互通")
    assert "10.0.5.9" not in clean and "172.16.3.4" not in clean and "100.90.1.2" not in clean
    assert hits == 3


def should_not_mask_version_number_like_ip():
    # 版本号/层级号 2.1.2.1 非内网地址，不应误判（这是真实 P0 源码里的误报来源）
    clean, hits = desensitize("指标版本 2.1.2.1 与 2.2.3.1 升级")
    assert hits == 0 and clean == "指标版本 2.1.2.1 与 2.2.3.1 升级"


def should_not_mask_public_ip():
    # 按 CLAUDE.md「内网IP」原意，仅收窄内网段；公网地址不在脱敏范围
    clean, hits = desensitize("外部 203.0.113.5 非内网")
    assert hits == 0


def should_mask_db_connection_string_jdbc():
    clean, hits = desensitize("配置 jdbc:mysql://dbhost:3306/mes?useSSL=false 已加载")
    assert "jdbc:mysql" not in clean and "[DB_CONN_***]" in clean and hits == 1


def should_mask_oracle_dsn_as_whole_unit():
    # 整段 DSN host:port/service 作为一个单元被抹，而非只抹 IP。
    # 用文档保留地址 + 虚构服务名，不写真实 DSN。
    clean, hits = desensitize("MES_DB_DSN=203.0.113.5:1521/DEMOPDB")
    assert "DEMOPDB" not in clean and "1521" not in clean
    assert "[DB_CONN_***]" in clean and hits == 1


def should_mask_id_card():
    clean, hits = desensitize("身份证 110105199003072345 已登记")
    assert "110105199003072345" not in clean and "[ID_CARD_***]" in clean and hits == 1


def should_mask_emp_id():
    clean, hits = desensitize("操作人 EMP001234 提交")
    assert "EMP001234" not in clean and "[EMP_ID_***]" in clean and hits == 1


def should_mask_lot_no():
    clean, hits = desensitize("批次 LOTAB202601001 入库")
    assert "LOTAB202601001" not in clean and "[LOT_NO_***]" in clean and hits == 1


def should_mask_site_param_fab_format():
    clean, hits = desensitize("厂区 FAB-NJ-01 巡检")
    assert "FAB-NJ-01" not in clean and "[SITE_PARAM_***]" in clean and hits == 1


def should_mask_device_sn_asterisk_format():
    # CLAUDE.md 示例的带星号 SN 字面量 AB****3456
    clean, hits = desensitize("设备 AB****3456 报警")
    assert "AB****3456" not in clean and "[DEVICE_SN_***]" in clean and hits == 1


def should_not_mask_business_codes_as_device_sn():
    # 消息码/模块码 MSG00108、SPGC0030、SMS00001 结构似 SN 但为业务标识，不得抹掉
    text = "消息 MSG00108 模块 SPGC0030 画面 SMS00001"
    clean, hits = desensitize(text)
    assert clean == text and hits == 0


# ── 误伤防护（关键：不得抹掉钢厂业务语义）────────────────────
def should_not_mask_bare_factory_codes():
    # LZ/RZ/SHIP 是钢厂厂区业务码（包名/表名里就有），绝不能当厂区编号抹掉
    text = "包 BSQM_MTC_ISSUE_LZ 与 BSQM_MTC_ISSUE_RZ、BSQM_MTC_ISSUE_SHIP 按厂区复制"
    clean, hits = desensitize(text)
    assert clean == text and hits == 0


def should_not_mask_steel_grade():
    clean, hits = desensitize("牌号 Q235B 与 SPHC 合格")
    assert clean == "牌号 Q235B 与 SPHC 合格" and hits == 0


def should_not_mask_underscore_identifiers():
    # 列名/标识符含下划线，\b 边界天然切分，不应触发设备SN
    text = "字段 CRT_USER_ID、SLAB_NO、UPD_OBJ_ID 为审计列"
    clean, hits = desensitize(text)
    assert clean == text and hits == 0


def should_not_mask_requirement_number():
    text = "请分析工单 REQ-MES-AI-20260412-001 的执行状态"
    clean, hits = desensitize(text)
    assert clean == text and hits == 0


def should_not_mask_pure_numeric_sentinel():
    # 235959 类哨兵/时间常量（纯数字无字母）不应被设备SN误判
    clean, hits = desensitize("默认值 235959 表示 23:59:59")
    assert hits == 0


# ── verbose 明细 ─────────────────────────────────────────────
def should_return_hit_details_in_verbose():
    clean, hits = desensitize_verbose("EMP001234 在 192.168.0.1 操作")
    cats = {h["category"] for h in hits}
    assert cats == {"EMP_ID", "IP_ADDR"}
    assert all("match" in h and "name" in h for h in hits)


def should_count_multiple_classes():
    text = "员工 EMP123456 在 192.168.0.1 操作批次 LOTAB202601001"
    clean, hits = desensitize(text)
    assert hits == 3


def should_handle_empty_text():
    assert desensitize("") == ("", 0)
    assert desensitize_verbose("") == ("", [])
