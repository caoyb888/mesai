"""
MES 代码字典服务（SCO_CODE_DETAIL 解码值定向注入）
文档编号：AI-MES-GW-2026-003
关联需求单：REQ-MES-AI-20260730-001
作者：AI（芯智云匠）
日期：2026-07-30

背景：mes-sql 生成 SQL 时，LLM 常对代码类字段（*_CD/*_TY/*_GRD）直接用中文业务标签
做等值过滤（如 PROD_TOT_JDG_RSLT_TY='不合格'），而真实码值是 '9' 这类代码，
导致“能执行但结果恒空”的语义错误。根因是 RAG 上下文里缺少码值映射（铁律 9 没有弹药）。

本服务直接读取 SCO_CODE_DETAIL 导出 CSV（glossary_code_mapping.csv，
列名=代码组约定：代码字段名与代码组 master_cd 逐字相同），
把检索上下文中出现的代码组的可用码值作为补充上下文注入，供 LLM 接地使用。

CSV 来源：SCOAPUSER.SCO_CODE_DETAIL（use_yn=Y），S3-0 导出，随仓库版本化
（scripts/kb-ingest/data/glossary_code_mapping.csv）。通用代码字典，不含敏感数据。
"""

import csv
import functools
import logging
import os
import re

log = logging.getLogger(__name__)

# 列名/代码组 token：大写字母开头的大写标识符（至少 3 字符，避免误匹配短词）
_TOKEN_RE = re.compile(r"\b[A-Z][A-Z0-9_]{2,}\b")

# 单次注入上限：最多 5 个代码组、每组最多 40 个码值（控上下文体积与 Token）
MAX_GROUPS = 5
MAX_VALUES_PER_GROUP = 40

# 代码类字段后缀（优先注入）：命中这些后缀的代码组语义价值最高；
# 其余组（如 PROD_NO 这类“编号碰巧同名为代码组”的噪声组）仅在名额有余时补充
_CODE_SUFFIXES = ("_CD", "_TY", "_GRD", "_YN", "_FG", "_TP", "_ST", "_FL")


class CodeDictService:
    """代码字典查询服务：master_cd → [(码值, 中文, 韩文, 英文), ...]（仅启用项）"""

    def __init__(self, csv_path: str):
        self._groups: dict[str, list[tuple[str, str, str, str]]] = {}
        self._load(csv_path)

    def _load(self, csv_path: str) -> None:
        # utf-8-sig：剥离 Excel 导出常见的 BOM
        with open(csv_path, encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # 跳过表头：代码组,代码值,中文,韩文,英文,启用
            for row in reader:
                if len(row) < 6:
                    continue
                master, val, zh, ko, en, use = (c.strip() for c in row[:6])
                if not master or use.upper() != "Y":
                    continue
                self._groups.setdefault(master.upper(), []).append((val, zh, ko, en))
        log.info("[代码字典] 加载完成 groups=%d path=%s", len(self._groups), csv_path)

    def lookup_in_texts(self, texts: list[str],
                        max_groups: int = MAX_GROUPS) -> dict[str, list[tuple[str, str, str, str]]]:
        """
        从文本（问题 + RAG 卡片内容）中提取大写标识符，命中代码组的逐一返回。
        收录后按“代码类后缀优先”排序取前 max_groups 个：
        避免 PROD_NO 这类编号噪声组挤占 PROD_TOT_JDG_RSLT_TY 等关键组的名额。
        """
        found: dict[str, list[tuple[str, str, str, str]]] = {}
        for text in texts:
            for token in _TOKEN_RE.findall(text or ""):
                group = token.upper()
                if group in self._groups and group not in found:
                    found[group] = self._groups[group]
        prioritized = sorted(found.items(),
                             key=lambda kv: 0 if kv[0].endswith(_CODE_SUFFIXES) else 1)
        return dict(prioritized[:max_groups])

    @staticmethod
    def format_groups(groups: dict[str, list[tuple[str, str, str, str]]],
                      max_values: int = MAX_VALUES_PER_GROUP) -> str:
        """格式化为 Prompt 上下文文本：每行一个代码组及其可用码值"""
        lines = []
        for group, values in groups.items():
            pairs = []
            for val, zh, ko, en in values[:max_values]:
                label = zh or ko or en or "（无释义）"
                pairs.append(f"'{val}'={label}")
            suffix = f"（仅列前 {max_values} 个）" if len(values) > max_values else ""
            lines.append(f"- `{group}` 可用代码值{suffix}：" + "，".join(pairs))
        return "\n".join(lines)


def _default_csv_path() -> str:
    """仓库内默认路径：<项目根>/scripts/kb-ingest/data/glossary_code_mapping.csv"""
    services_dir = os.path.dirname(os.path.abspath(__file__))
    gateway_root = os.path.dirname(os.path.dirname(services_dir))   # src/ai-gateway
    project_root = os.path.dirname(os.path.dirname(gateway_root))   # 项目根
    return os.path.join(project_root, "scripts", "kb-ingest", "data", "glossary_code_mapping.csv")


@functools.lru_cache(maxsize=1)
def get_code_dict_service() -> "CodeDictService | None":
    """
    单例获取代码字典服务。
    路径解析顺序：环境变量 CODE_DICT_CSV → 仓库默认路径；均不存在返回 None（注入停用，降级不报错）。
    """
    path = os.environ.get("CODE_DICT_CSV", "").strip() or _default_csv_path()
    if not os.path.exists(path):
        log.warning("[代码字典] CSV 不存在，码值注入停用 path=%s", path)
        return None
    try:
        return CodeDictService(path)
    except Exception as e:  # 字典加载失败不应阻断取数主链路
        log.error("[代码字典] 加载失败，码值注入停用 path=%s err=%s", path, e, exc_info=True)
        return None
