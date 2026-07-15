"""
RAG 检索服务（ChromaDB）
关联任务：S2.5 演示接口
作者：AI（芯智云匠）
日期：2026-04-13

职责：
  - 从 ChromaDB 向量库检索与用户问题相关的 ITSM 上下文（DB 结构 / API 文档）
  - 支持按集合名检索（itsm_db_structure / itsm_api_docs）
  - 返回 Top-N 文档片段，供 LLM Prompt 上下文注入
"""

import logging
from dataclasses import dataclass
from typing import Optional

# chromadb 和 sentence_transformers 在 __init__ 中懒加载，
# 避免模块级 import 在未安装依赖的环境（如精简 CI）中导致整体导入失败。
from app.config import get_settings

log = logging.getLogger(__name__)

# 知识库集合名称映射
COLLECTION_DB = "itsm_db_structure"
COLLECTION_API = "itsm_api_docs"
# 真实 MES S3 理解卡片集合（表理解 + 过程理解，入库见 ingest_s3_cards.py）
COLLECTION_MES_S3 = "mes_s3_understanding"


@dataclass
class RagDocument:
    """单条检索结果"""
    doc_id: str
    content: str
    distance: float
    metadata: dict


class RagService:
    """ChromaDB RAG 检索服务"""

    def __init__(self):
        settings = get_settings()
        try:
            import chromadb as _chromadb
            from sentence_transformers import SentenceTransformer
            self._client = _chromadb.PersistentClient(path=settings.chroma_persist_dir)
            # 使用多语言模型，与入库时保持一致（paraphrase-multilingual-MiniLM-L12-v2）
            self._embed_model = SentenceTransformer(
                "paraphrase-multilingual-MiniLM-L12-v2"
            )
            log.info("ChromaDB 已连接：%s", settings.chroma_persist_dir)
            log.info("Embedding 模型：paraphrase-multilingual-MiniLM-L12-v2")
        except Exception as e:
            log.error("ChromaDB/Embedding 初始化失败：%s", e)
            raise

    def retrieve(
        self,
        query: str,
        collection_name: str,
        top_n: Optional[int] = None,
        where: Optional[dict] = None,
    ) -> list[RagDocument]:
        """
        从指定集合检索与 query 最相关的 Top-N 文档

        :param query: 用户查询文本
        :param collection_name: ChromaDB 集合名称
        :param top_n: 返回条数，None 则使用配置默认值
        :param where: 可选元数据过滤（如 {"chunk_type": "s3_table"}）
        :return: 按相关度排序的文档列表（最相关优先）
        """
        settings = get_settings()
        n = top_n or settings.rag_top_n

        try:
            col = self._client.get_collection(collection_name)
        except Exception as e:
            log.warning("集合 %s 不存在或无法访问：%s", collection_name, e)
            return []

        try:
            # 用多语言模型生成查询向量，与入库时保持一致
            query_vector = self._embed_model.encode([query])[0].tolist()
            query_kwargs = {
                "query_embeddings": [query_vector],
                "n_results": min(n, col.count()),
                "include": ["documents", "metadatas", "distances"],
            }
            if where:
                query_kwargs["where"] = where
            results = col.query(**query_kwargs)
        except Exception as e:
            log.error("ChromaDB 查询失败 collection=%s query=%s err=%s", collection_name, query, e)
            return []

        docs: list[RagDocument] = []
        if results and results.get("documents"):
            for i, doc_content in enumerate(results["documents"][0]):
                docs.append(RagDocument(
                    doc_id=results["ids"][0][i] if results.get("ids") else str(i),
                    content=doc_content,
                    distance=results["distances"][0][i] if results.get("distances") else 0.0,
                    metadata=results["metadatas"][0][i] if results.get("metadatas") else {},
                ))
        log.info("RAG 检索完成 collection=%s top_n=%d 命中=%d条", collection_name, n, len(docs))
        return docs

    def retrieve_for_sql(self, question: str, top_n: Optional[int] = None) -> list[RagDocument]:
        """针对 SQL 生成场景，从 ITSM 数据库结构集合检索上下文"""
        return self.retrieve(question, COLLECTION_DB, top_n)

    def retrieve_for_api(self, question: str, top_n: Optional[int] = None) -> list[RagDocument]:
        """针对接口理解场景，从 ITSM API 文档集合检索上下文"""
        return self.retrieve(question, COLLECTION_API, top_n)

    def retrieve_for_fe_component(self, question: str, top_n: Optional[int] = None) -> list[RagDocument]:
        """针对前端组件生成场景，从 ITSM API 文档集合检索上下文"""
        return self.retrieve(question, COLLECTION_API, top_n)

    def retrieve_for_mes(self, question: str, top_n: Optional[int] = None,
                         kind: Optional[str] = None) -> list[RagDocument]:
        """
        从真实 MES S3 理解卡片集合检索上下文（表理解 + 过程理解）。

        :param kind: 可选，"table" 只检索表卡片 / "proc" 只检索过程卡片 / None 混检

        检索调优：入库侧每卡片带「检索锚点」摘要 chunk；此处**按卡片(source_file)去重**，
        先取 4×N 个 chunk 再折叠为不同卡片，避免同一表/过程的多个 chunk 挤占 Top-N 名额
        （实测表级 Top-3 命中 3/10 → 5/10）。
        """
        where = {"chunk_type": f"s3_{kind}"} if kind in ("table", "proc") else None
        n = top_n or get_settings().rag_top_n
        raw = self.retrieve(question, COLLECTION_MES_S3, top_n=max(n * 8, 30), where=where)
        seen: set = set()
        out: list[RagDocument] = []
        for d in raw:
            sf = d.metadata.get("source_file")
            if sf in seen:
                continue
            seen.add(sf)
            out.append(d)
            if len(out) >= n:
                break
        return out

    def retrieve_for_mes_table(self, question: str, top_n: Optional[int] = None) -> list[RagDocument]:
        """MES 表/字段场景，仅检索表理解卡片"""
        return self.retrieve_for_mes(question, top_n, kind="table")

    def retrieve_for_mes_proc(self, question: str, top_n: Optional[int] = None) -> list[RagDocument]:
        """MES 存储过程场景，仅检索过程逻辑卡片"""
        return self.retrieve_for_mes(question, top_n, kind="proc")

    def format_context(self, docs: list[RagDocument]) -> str:
        """
        将检索到的文档列表格式化为 Prompt 上下文注入格式（STANDARD_TEMPLATE §2 规范）
        """
        if not docs:
            return "（未检索到相关文档，请基于通用知识回答）"

        parts = []
        for i, doc in enumerate(docs, 1):
            # 兼容 ITSM（source/type）与 S3 理解卡片（source_file/chunk_type）两套元数据
            source = doc.metadata.get("source") or doc.metadata.get("source_file", "未知来源")
            doc_type = doc.metadata.get("type") or doc.metadata.get("chunk_type", "unknown")
            parts.append(
                f"--- 文档片段 {i}/{len(docs)} ---\n"
                f"来源：{source} | 类型：{doc_type}\n"
                f"{doc.content}\n"
                f"--- END ---"
            )
        return "\n\n".join(parts)


# 单例（模块级，FastAPI 启动时初始化一次）
_rag_service: Optional[RagService] = None


def get_rag_service() -> RagService:
    """获取 RAG 服务单例"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RagService()
    return _rag_service
