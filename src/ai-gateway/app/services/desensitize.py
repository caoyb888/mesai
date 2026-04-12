"""
PII 脱敏服务（存根）
关联任务: T1-2-1（存根）/ T5-2-1（完整实现，Sprint 5）
作者: AI
日期: 2026-04-12

当前阶段（Sprint 1）：提供存根实现，仅做日志记录。
完整的 7 类 PII 脱敏规则将在 Sprint 5 T5-2-1 中实现。
"""

import re
import logging

log = logging.getLogger(__name__)

# 预编译正则（Sprint 5 完整实现时扩充，当前仅兜底最高风险的3类）
_PATTERNS = [
    (re.compile(r"\b(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
     "[IP_ADDR_***]"),
    (re.compile(r"\bEMP\d{6,10}\b"),
     "[EMP_ID_***]"),
    (re.compile(r"\bLOT[A-Z]{2}\d{6,12}\b"),
     "[LOT_NO_***]"),
]


def desensitize(text: str) -> tuple[str, int]:
    """
    对发往 AI API 的文本进行 PII 脱敏处理（CLAUDE.md 4.2）

    :param text: 原始文本
    :return: (脱敏后文本, 命中规则数)

    注意：当前为 Sprint 1 存根，仅覆盖内网IP / 员工工号 / 批次号三类。
          Sprint 5 T5-2-1 将补全全部 7 类规则并集成 NLP 辅助识别。
    """
    result = text
    hit_count = 0
    for pattern, replacement in _PATTERNS:
        new_result, n = pattern.subn(replacement, result)
        if n > 0:
            hit_count += n
            result = new_result
            log.warning(
                "[脱敏] 发现敏感信息，规则匹配 %d 处，已替换为 %s（Sprint 5前为存根）",
                n, replacement
            )
    return result, hit_count
