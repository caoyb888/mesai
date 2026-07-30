"""
MES 代码字典服务与码值注入单元测试
关联需求单：REQ-MES-AI-20260730-001
作者：AI（芯智云匠）
日期：2026-07-30

覆盖：
- CodeDictService：CSV 加载（BOM/表头/停用行过滤）、lookup_in_texts、format_groups、上限控制
- 端点级注入：命中代码组时上下文追加 code_dict 文档；字典缺失时降级不报错
"""

import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models import GatewayResponse, UsageInfo
from app.services.code_dict import CodeDictService
from app.services.rag_service import RagDocument


# ── CodeDictService 单元测试 ─────────────────────────────────

CSV_CONTENT = """﻿代码组(master_cd),代码值(cd_val),中文(zh),韩文(ko),英文(en),启用(use_yn)
PROD_TOT_JDG_GRD,1,合格,합격,,Y
PROD_TOT_JDG_GRD,9,不合格,불합격,,Y
PROD_TOT_JDG_GRD,3,停用项,정지,,N
JDG_REQ_GRD,A,必检,필검,,Y
JDG_REQ_GRD,B,抽检,추출검사,,Y
"""


@pytest.fixture
def csv_path(tmp_path):
    p = tmp_path / "dict.csv"
    p.write_text(CSV_CONTENT, encoding="utf-8")
    return str(p)


def test_load_filters_disabled_and_bom(csv_path):
    """加载：BOM 表头正确剥离；use_yn=N 的行被过滤"""
    svc = CodeDictService(csv_path)
    groups = svc.lookup_in_texts(["PROD_TOT_JDG_GRD"])
    assert "PROD_TOT_JDG_GRD" in groups
    values = groups["PROD_TOT_JDG_GRD"]
    assert len(values) == 2                       # 停用行（N）已剔除
    assert values[0] == ("1", "合格", "합격", "")


def test_lookup_matches_verbatim_column_name(csv_path):
    """列名=代码组逐字匹配：卡片中的列名 token 可命中，非代码组 token 不命中"""
    svc = CodeDictService(csv_path)
    text = "- `JDG_REQ_GRD`（判定要求分类）：可能取值含义「待字典解码」。另有 NOT_A_GROUP 字段。"
    groups = svc.lookup_in_texts([text])
    assert list(groups.keys()) == ["JDG_REQ_GRD"]


def test_lookup_max_groups_cap(csv_path):
    """代码组数量上限：超出 max_groups 即停止收录"""
    svc = CodeDictService(csv_path)
    text = "PROD_TOT_JDG_GRD 和 JDG_REQ_GRD 都出现"
    groups = svc.lookup_in_texts([text], max_groups=1)
    assert len(groups) == 1


def test_format_groups_renders_value_label_pairs(csv_path):
    """格式化：输出 '码值'=中文 形式，供 Prompt 直接接地"""
    svc = CodeDictService(csv_path)
    groups = svc.lookup_in_texts(["PROD_TOT_JDG_GRD"])
    rendered = svc.format_groups(groups)
    assert "`PROD_TOT_JDG_GRD`" in rendered
    assert "'9'=不合格" in rendered


# ── 端点级注入测试 ────────────────────────────────────────────

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def _doc(doc_id: str, content: str) -> RagDocument:
    return RagDocument(
        doc_id=doc_id,
        content=content,
        distance=0.2,
        metadata={"source_file": f"{doc_id}.md", "chunk_type": "s3_table"},
    )


def _mock_rag(docs):
    rag = MagicMock()
    rag.retrieve_for_mes.side_effect = lambda question, top_n=None, kind=None: (
        docs if kind != "proc" else []
    )
    rag.format_context.side_effect = lambda ds: "\n".join(d.content for d in ds)
    return rag


def _mock_provider():
    provider = AsyncMock()
    provider.chat.return_value = GatewayResponse(
        task_no="T",
        content=json.dumps({
            "generated": True,
            "sql": "SELECT PROD_NO FROM SQM_TOT_JDG_RSLT WHERE PROD_TOT_JDG_GRD = '9'",
            "explanation": "按码值过滤不合格品。",
            "referenced_tables": ["SQM_TOT_JDG_RSLT"],
            "referenced_columns": ["PROD_NO", "PROD_TOT_JDG_GRD"],
            "unanswerable_reason": None,
        }, ensure_ascii=False),
        provider="kimi",
        model="moonshot-v1-32k",
        usage=UsageInfo(prompt_tokens=100, completion_tokens=50, total_tokens=150),
        response_time_ms=100,
        call_seq=1,
    )
    return provider


_CARD = "- `PROD_TOT_JDG_GRD`（产品综合判定等级）：综合质量判定等级，可能取值含义「待字典解码」。"


@pytest.mark.asyncio
async def test_endpoint_injects_code_dict_context(client, csv_path):
    """命中代码组时：上下文中追加 code_dict 文档，且码值随请求进入用户消息"""
    provider = _mock_provider()

    with patch("app.routers.mes_sql.get_rag_service", return_value=_mock_rag([_doc("T1", _CARD)])), \
         patch("app.routers.mes_sql.get_code_dict_service", return_value=CodeDictService(csv_path)), \
         patch("app.routers.gateway._get_provider", return_value=provider):
        resp = await client.post("/v1/ai/mes-sql", json={"question": "查不合格钢卷", "top_n": 3})

    assert resp.status_code == 200
    data = resp.json()
    code_docs = [d for d in data["context_docs"] if d["doc_type"] == "code_dict"]
    assert len(code_docs) == 1
    sent_req = provider.chat.call_args.args[0]
    assert "'9'=不合格" in sent_req.messages[-1].content


@pytest.mark.asyncio
async def test_endpoint_degrades_when_dict_missing(client):
    """字典服务不可用（None）时：正常走主链路，不报错、不注入"""
    with patch("app.routers.mes_sql.get_rag_service", return_value=_mock_rag([_doc("T1", _CARD)])), \
         patch("app.routers.mes_sql.get_code_dict_service", return_value=None), \
         patch("app.routers.gateway._get_provider", return_value=_mock_provider()):
        resp = await client.post("/v1/ai/mes-sql", json={"question": "查不合格钢卷", "top_n": 3})

    assert resp.status_code == 200
    data = resp.json()
    assert all(d["doc_type"] != "code_dict" for d in data["context_docs"])
