"""
PII 脱敏服务（CLAUDE.md 4.2 全 7 类实现）
关联任务: T1-2-1（存根）→ S3 训练前置补全（2026-07-14，对接真实 MES 外发 Kimi）
作者: AI（芯智云匠 MES AI 开发工程师）
日期: 2026-07-14（原存根 2026-04-12）

设计要点（真实 MES 调优）：
- 规则精准锚定，避免误伤钢厂业务语义。**厂区码 LZ/RZ/SHIP 是核心业务标识
  （包名/表名里就有），绝不能当 PII 抹掉**——故「厂区编号」只匹配 CLAUDE.md
  示例的 `FAB-XX-NN` 显式格式，不匹配裸两字母码。
- 「设备序列号」用正则候选 + 校验器（字母≥2 且 数字≥4 且 长度≥8），避免把
  任务单号（REQ-...-20260412-001，纯数字段无字母）、牌号（Q235B，过短）、
  下划线标识符（列名，\b 边界天然切分）误判。
- 规则按序应用：**数据库连接串先于 IP**，使整段 DSN（host:port/service）作为
  一个单元被抹除，而非只抹主机 IP。

对外契约：
- `desensitize(text) -> (clean_text, hit_count)`  —— 兼容旧签名，网关使用。
- `desensitize_verbose(text) -> (clean_text, hits)` —— hits 为逐条命中明细，审计使用。
"""

import re
import logging
from collections import namedtuple

log = logging.getLogger(__name__)

# 一条脱敏规则：名称 / 类别标签 / 预编译正则 / 替换串 / 可选校验器
# 校验器返回 False 时该次命中视为误报，保留原文不替换。
Rule = namedtuple("Rule", "name category pattern replacement validator")


def _valid_ipv4(text: str) -> bool:
    """四段均 0-255 才算合法 IPv4，排除 999.1.1.1 之类误报。"""
    parts = text.split(".")
    return len(parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)


def _valid_device_sn(text: str) -> bool:
    """设备序列号候选校验：字母≥2 且 数字≥4（排除纯数字日期段、短牌号）。"""
    letters = sum(c.isalpha() for c in text)
    digits = sum(c.isdigit() for c in text)
    return letters >= 2 and digits >= 4


# 规则表（顺序敏感：连接串 → IP → 身份证 → 工号 → 批次 → 厂区 → 设备SN）
_RULES = [
    # 数据库连接串：jdbc URL / Oracle easy-connect(host:port/service) / user:pwd@host
    Rule("数据库连接串", "DB_CONN",
         re.compile(
             r"jdbc:[a-zA-Z0-9]+:[^\s\"']+"
             r"|\b(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}/[A-Za-z0-9_$]+"
             r"|\b[A-Za-z0-9_]+/[^\s@/]{3,}@[\w.:/\-]+"
         ),
         "[DB_CONN_***]", None),
    # 内网/任意 IPv4（四段 0-255 校验）
    Rule("内网IP", "IP_ADDR",
         re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
         "[IP_ADDR_***]", _valid_ipv4),
    # 身份证号：18 位，含合法出生日期段
    Rule("身份证号", "ID_CARD",
         re.compile(r"\b[1-9]\d{5}(?:18|19|20)\d{2}"
                    r"(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b"),
         "[ID_CARD_***]", None),
    # 员工工号：EMP + 6~10 位数字
    Rule("员工工号", "EMP_ID",
         re.compile(r"\bEMP\d{6,10}\b"),
         "[EMP_ID_***]", None),
    # 生产批次号：LOT + 2 字母 + 6~12 位数字
    Rule("生产批次号", "LOT_NO",
         re.compile(r"\bLOT[A-Z]{2}\d{6,12}\b"),
         "[LOT_NO_***]", None),
    # 厂区编号：仅 CLAUDE.md 示例的显式 FAB-XX-NN 格式（不误伤裸厂区码 LZ/RZ/SHIP）
    Rule("厂区编号", "SITE_PARAM",
         re.compile(r"\bFAB-[A-Z]{2,4}-\d{2,3}\b"),
         "[SITE_PARAM_***]", None),
    # 设备序列号：大写字母数字 ≥8，经校验器过滤（字母≥2 且 数字≥4）
    Rule("设备序列号", "DEVICE_SN",
         re.compile(r"\b[A-Z0-9]{8,}\b"),
         "[DEVICE_SN_***]", _valid_device_sn),
]


def _run(text: str):
    """按序应用全部规则，返回 (脱敏文本, 命中明细列表)。"""
    hits = []
    result = text
    for rule in _RULES:
        def _repl(m, _rule=rule):
            val = m.group(0)
            if _rule.validator and not _rule.validator(val):
                return val  # 误报，保留原文
            hits.append({"category": _rule.category, "name": _rule.name, "match": val})
            return _rule.replacement
        result = rule.pattern.sub(_repl, result)
    return result, hits


def desensitize(text: str) -> tuple[str, int]:
    """
    对发往外部 AI API 的文本进行 PII 脱敏（CLAUDE.md 4.2，全 7 类）。

    :param text: 原始文本
    :return: (脱敏后文本, 命中规则数)
    """
    if not text:
        return text, 0
    result, hits = _run(text)
    if hits:
        by_cat = {}
        for h in hits:
            by_cat[h["name"]] = by_cat.get(h["name"], 0) + 1
        log.warning("[脱敏] 命中敏感信息 %d 处，分类：%s（请排查上游数据）",
                    len(hits), by_cat)
    return result, len(hits)


def desensitize_verbose(text: str) -> tuple[str, list]:
    """
    与 desensitize 同规则，但返回逐条命中明细（含类别/名称/命中串），供审计报告使用。

    :return: (脱敏后文本, [{"category","name","match"}, ...])
    """
    if not text:
        return text, []
    return _run(text)
