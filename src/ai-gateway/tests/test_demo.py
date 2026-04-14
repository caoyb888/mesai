"""
演示接口与 RAG 服务单元测试
关联任务: S2.5 演示MVP
作者: AI（芯智云匠）
日期: 2026-04-14

测试策略：
- chromadb / sentence_transformers / OpenAI 全部使用 Mock，不依赖外部服务
- 覆盖 rag_service.py 核心路径：初始化、检索、格式化
- 覆盖 demo.py 核心路径：正常生成、RAG 检索为空、LLM 调用失败、模式校验
"""

import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app


# ── 测试夹具 ─────────────────────────────────────────────────

@pytest_asyncio.fixture
async def client():
    """创建测试用 AsyncClient"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


def _make_demo_request(question="查询所有未关闭工单", mode="sql"):
    return {"question": question, "mode": mode}


# ── RagService 单元测试（Mock chromadb + sentence_transformers）────

class TestRagService:
    """测试 RagService 核心逻辑，所有外部依赖全部 Mock"""

    def _make_service(self):
        """构造一个 chromadb/embedding 均已 Mock 的 RagService 实例"""
        from app.services.rag_service import RagService

        mock_chroma_client = MagicMock()
        mock_embed_model = MagicMock()
        import numpy as np
        mock_embed_model.encode.return_value = np.array([[0.1] * 384])

        with patch("app.services.rag_service.get_settings") as mock_settings, \
             patch("builtins.__import__", side_effect=self._selective_import(
                 mock_chroma_client, mock_embed_model
             )):
            mock_settings.return_value.chroma_persist_dir = "/tmp/test_chroma"
            svc = object.__new__(RagService)
            svc._client = mock_chroma_client
            svc._embed_model = mock_embed_model
        return svc, mock_chroma_client, mock_embed_model

    @staticmethod
    def _selective_import(mock_client, mock_model):
        """仅对 chromadb / sentence_transformers 的 import 进行拦截"""
        real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") \
            else __import__

        def _import(name, *args, **kwargs):
            if name == "chromadb":
                m = MagicMock()
                m.PersistentClient.return_value = mock_client
                return m
            if name == "sentence_transformers":
                m = MagicMock()
                m.SentenceTransformer.return_value = mock_model
                return m
            return real_import(name, *args, **kwargs)
        return _import

    def should_return_empty_when_collection_not_found(self):
        """should_返回空列表_when_集合不存在"""
        from app.services.rag_service import RagService
        svc = object.__new__(RagService)
        mock_client = MagicMock()
        mock_client.get_collection.side_effect = Exception("集合不存在")
        mock_embed_model = MagicMock()
        import numpy as np
        mock_embed_model.encode.return_value = np.array([[0.1] * 384])
        svc._client = mock_client
        svc._embed_model = mock_embed_model

        result = svc.retrieve("查询工单", "itsm_db_structure")
        assert result == []

    def should_return_docs_when_collection_has_results(self):
        """should_返回文档列表_when_ChromaDB查询有结果"""
        from app.services.rag_service import RagService, RagDocument
        svc = object.__new__(RagService)

        mock_col = MagicMock()
        mock_col.count.return_value = 5
        mock_col.query.return_value = {
            "ids": [["id1", "id2"]],
            "documents": [["表：itsm_ticket 工单主表", "表：itsm_user 用户表"]],
            "metadatas": [[{"module": "工单核心"}, {"module": "用户权限"}]],
            "distances": [[0.12, 0.25]],
        }
        mock_client = MagicMock()
        mock_client.get_collection.return_value = mock_col
        mock_embed_model = MagicMock()
        import numpy as np
        mock_embed_model.encode.return_value = np.array([[0.1] * 384])
        svc._client = mock_client
        svc._embed_model = mock_embed_model

        with patch("app.services.rag_service.get_settings") as ms:
            ms.return_value.rag_top_n = 5
            result = svc.retrieve("查询工单", "itsm_db_structure")

        assert len(result) == 2
        assert isinstance(result[0], RagDocument)
        assert result[0].distance == 0.12

    def should_return_empty_string_context_when_no_docs(self):
        """should_返回未检索提示_when_文档列表为空"""
        from app.services.rag_service import RagService
        svc = object.__new__(RagService)
        ctx = svc.format_context([])
        assert "未检索到" in ctx

    def should_format_context_with_doc_content(self):
        """should_格式化上下文包含文档内容_when_有检索结果"""
        from app.services.rag_service import RagService, RagDocument
        svc = object.__new__(RagService)
        docs = [
            RagDocument(doc_id="1", content="表：itsm_ticket", distance=0.1,
                        metadata={"source": "test", "type": "table_card"}),
        ]
        ctx = svc.format_context(docs)
        assert "itsm_ticket" in ctx
        assert "文档片段" in ctx

    def should_delegate_sql_query_to_db_collection(self):
        """should_检索DB集合_when_调用retrieve_for_sql"""
        from app.services.rag_service import RagService, COLLECTION_DB
        svc = object.__new__(RagService)

        mock_client = MagicMock()
        mock_col = MagicMock()
        mock_col.count.return_value = 0
        mock_col.query.return_value = {
            "ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]
        }
        mock_client.get_collection.return_value = mock_col
        mock_embed_model = MagicMock()
        import numpy as np
        mock_embed_model.encode.return_value = np.array([[0.1] * 384])
        svc._client = mock_client
        svc._embed_model = mock_embed_model

        with patch("app.services.rag_service.get_settings") as ms:
            ms.return_value.rag_top_n = 5
            svc.retrieve_for_sql("查询工单")

        mock_client.get_collection.assert_called_with(COLLECTION_DB)

    def should_delegate_fe_component_to_api_collection(self):
        """should_检索API集合_when_调用retrieve_for_fe_component"""
        from app.services.rag_service import RagService, COLLECTION_API
        svc = object.__new__(RagService)

        mock_client = MagicMock()
        mock_col = MagicMock()
        mock_col.count.return_value = 0
        mock_col.query.return_value = {
            "ids": [[]], "documents": [[]], "metadatas": [[]], "distances": [[]]
        }
        mock_client.get_collection.return_value = mock_col
        mock_embed_model = MagicMock()
        import numpy as np
        mock_embed_model.encode.return_value = np.array([[0.1] * 384])
        svc._client = mock_client
        svc._embed_model = mock_embed_model

        with patch("app.services.rag_service.get_settings") as ms:
            ms.return_value.rag_top_n = 5
            svc.retrieve_for_fe_component("工单列表组件")

        mock_client.get_collection.assert_called_with(COLLECTION_API)


# ── Demo 接口集成测试（Mock RAG + LLM）───────────────────────

def _mock_rag_service(docs=None, context="表：itsm_ticket 工单主表"):
    """构造返回固定结果的 Mock RagService"""
    from app.services.rag_service import RagDocument
    mock_rag = MagicMock()
    if docs is None:
        docs = [RagDocument(doc_id="1", content=context, distance=0.2,
                            metadata={"source": "test", "type": "table_card"})]
    mock_rag.retrieve_for_sql.return_value = docs
    mock_rag.retrieve_for_api.return_value = docs
    mock_rag.retrieve_for_fe_component.return_value = docs
    mock_rag.format_context.return_value = context
    return mock_rag


def _mock_llm_response(content: str):
    """构造 OpenAI 兼容的 Mock LLM 响应"""
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = content
    mock_resp.usage.total_tokens = 200
    return mock_resp


@pytest.mark.asyncio
async def should_return_sql_when_mode_is_sql(client):
    """should_返回SQL代码_when_mode为sql且LLM调用成功"""
    llm_content = (
        "【SQL代码】\n```sql\n"
        "SELECT id, title FROM itsm_ticket WHERE is_deleted = 0\n"
        "```\n\n【说明】\n查询所有有效工单"
    )
    mock_rag = _mock_rag_service()
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="sql"))

    assert resp.status_code == 200
    data = resp.json()
    assert data["mode"] == "sql"
    assert "itsm_ticket" in data["generated_code"]
    assert data["tokens_used"] == 200


@pytest.mark.asyncio
async def should_return_dml_when_mode_is_dml(client):
    """should_返回DML代码_when_mode为dml"""
    llm_content = (
        "【SQL代码】\n```sql\n"
        "UPDATE itsm_ticket SET status = 'CLOSED', updated_at = NOW() "
        "WHERE id = 1 AND is_deleted = 0;\n"
        "```\n\n【说明】\n关闭工单"
    )
    mock_rag = _mock_rag_service()
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="dml"))

    assert resp.status_code == 200
    assert resp.json()["mode"] == "dml"


@pytest.mark.asyncio
async def should_return_vue_component_when_mode_is_fe_component(client):
    """should_返回Vue组件代码_when_mode为fe_component"""
    llm_content = (
        "【组件代码】\n```vue\n<template><el-table /></template>\n```\n\n"
        "【说明】\n工单列表组件"
    )
    mock_rag = _mock_rag_service()
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="fe_component"))

    assert resp.status_code == 200
    assert resp.json()["mode"] == "fe_component"


@pytest.mark.asyncio
async def should_return_400_when_mode_is_invalid(client):
    """should_返回400_when_mode不在允许范围内"""
    mock_rag = _mock_rag_service()
    with patch("app.routers.demo.get_rag_service", return_value=mock_rag):
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="invalid_mode"))

    assert resp.status_code == 400
    assert "mode" in resp.json()["detail"]


@pytest.mark.asyncio
async def should_return_502_when_llm_call_fails(client):
    """should_返回502_when_LLM调用抛出异常"""
    mock_rag = _mock_rag_service()

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("API连接超时")
        )
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="sql"))

    assert resp.status_code == 502
    assert "AI 服务调用失败" in resp.json()["detail"]


@pytest.mark.asyncio
async def should_include_context_docs_in_response(client):
    """should_响应包含context_docs_when_RAG有检索结果"""
    from app.services.rag_service import RagDocument
    docs = [
        RagDocument(doc_id="1", content="表：itsm_ticket 工单主表字段明细",
                    distance=0.15, metadata={"source": "itsm_ticket.md", "type": "table_card"}),
        RagDocument(doc_id="2", content="表：itsm_user 用户表字段明细",
                    distance=0.30, metadata={"source": "itsm_user.md", "type": "table_card"}),
    ]
    mock_rag = _mock_rag_service(docs=docs)
    llm_content = "【SQL代码】\n```sql\nSELECT id FROM itsm_ticket WHERE is_deleted = 0\n```\n\n【说明】\n查询工单"
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="sql"))

    assert resp.status_code == 200
    data = resp.json()
    assert len(data["context_docs"]) == 2
    assert data["context_docs"][0]["relevance_score"] > data["context_docs"][1]["relevance_score"]


@pytest.mark.asyncio
async def should_still_return_code_when_rag_returns_empty(client):
    """should_仍返回生成代码_when_RAG未检索到文档"""
    mock_rag = _mock_rag_service(docs=[])
    mock_rag.format_context.return_value = "（未检索到相关文档，请基于通用知识回答）"
    llm_content = "【SQL代码】\n```sql\nSELECT id FROM itsm_ticket\n```\n\n【说明】\n通用查询"
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="sql"))

    assert resp.status_code == 200
    assert resp.json()["context_docs"] == []


@pytest.mark.asyncio
async def should_handle_llm_response_without_code_fence(client):
    """should_兜底解析_when_LLM未按格式输出代码围栏"""
    llm_content = "SELECT id FROM itsm_ticket WHERE is_deleted = 0;"
    mock_rag = _mock_rag_service()
    mock_llm = AsyncMock(return_value=_mock_llm_response(llm_content))

    with patch("app.routers.demo.get_rag_service", return_value=mock_rag), \
         patch("openai.AsyncOpenAI") as mock_openai_cls:
        mock_openai_cls.return_value.chat.completions.create = mock_llm
        resp = await client.post("/v1/ai/itsm-demo",
                                 json=_make_demo_request(mode="sql"))

    assert resp.status_code == 200
    # 兜底逻辑应返回原始内容
    assert resp.json()["generated_code"] != ""
