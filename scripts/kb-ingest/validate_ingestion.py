#!/usr/bin/env python3
"""
知识库入库验证脚本

验证内容：
1. ChromaDB 中指定模块的 chunk 数量和内容
2. MySQL 中 ai_kb_document / ai_kb_chunk 记录状态
3. 对代表性表名执行向量检索测试（相似度 Top-3）

用法：
    python validate_ingestion.py --module 工艺管理 --collection mes_db_structure

关联任务：S2-1 T2-1-1
作者：AI（芯智云匠）
日期：2026-04-12
"""

import os
import sys
import logging
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)


def load_config() -> dict:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return {
        "ai_api_key":      os.environ.get("AI_API_KEY", ""),
        "ai_api_base_url": os.environ.get("AI_API_BASE_URL", "https://api.moonshot.cn/v1"),
        "ai_model":        os.environ.get("AI_EMBED_MODEL", "moonshot-v1-embedding"),
        "chroma_persist_dir": os.environ.get("CHROMA_PERSIST_DIR", "./data/chromadb"),
        "db_url":          os.environ.get("DB_URL", ""),
        "db_username":     os.environ.get("DB_USERNAME", ""),
        "db_password":     os.environ.get("DB_PASSWORD", ""),
    }


def check_chromadb(cfg: dict, collection_name: str, module: str) -> bool:
    """检查 ChromaDB 中指定模块的 chunk"""
    try:
        import chromadb
    except ImportError:
        log.error("缺少 chromadb 依赖")
        return False

    client = chromadb.PersistentClient(path=cfg["chroma_persist_dir"])
    try:
        collection = client.get_collection(collection_name)
    except Exception:
        log.error("ChromaDB 集合 '%s' 不存在", collection_name)
        return False

    # 查询指定模块的所有 chunk
    result = collection.get(
        where={"module": module},
        include=["metadatas", "documents"]
    )
    ids = result["ids"]
    log.info("ChromaDB 验证：模块=%s，chunk 数=%d", module, len(ids))

    if not ids:
        log.error("未找到模块 '%s' 的 chunk，请检查入库是否成功", module)
        return False

    # 显示前 3 条
    for i, (id_, meta, doc) in enumerate(
        zip(ids[:3], result["metadatas"][:3], result["documents"][:3])
    ):
        log.info(
            "  [%d] id=%s type=%s tokens=%s",
            i, id_, meta.get("chunk_type"), meta.get("token_count")
        )
        log.info("      text[:80]=%s...", doc[:80].replace("\n", " "))

    return True


def test_similarity_search(cfg: dict, collection_name: str, module: str) -> None:
    """执行代表性查询，验证向量检索效果"""
    if not cfg["ai_api_key"]:
        log.warning("AI_API_KEY 未配置，跳过相似度检索测试")
        return

    # 测试查询（根据模块选择有代表性的业务问题）
    test_queries = {
        "基础数据":  "查询某个产品的 BOM 物料清单",
        "工艺管理":  "获取某个产品的工艺路线和工序列表",
        "生产计划":  "查询某生产工单的当前状态和计划完工时间",
        "作业管理":  "统计某工位今日的报工数量和完成率",
        "设备管理":  "查询某设备的最近一次点检记录",
        "质量管理":  "统计某产品本月的不良品率",
    }
    query = test_queries.get(module, f"查询{module}模块的核心表结构")

    try:
        from openai import OpenAI
        import chromadb
    except ImportError:
        log.warning("缺少依赖，跳过相似度检索测试")
        return

    # 生成查询向量
    client = OpenAI(
        api_key=cfg["ai_api_key"],
        base_url=cfg["ai_api_base_url"]
    )
    embed_model = cfg["ai_model"]
    try:
        resp = client.embeddings.create(input=[query], model=embed_model)
        query_vector = resp.data[0].embedding
    except Exception as e:
        log.warning("查询向量化失败：%s", e)
        return

    # 相似度检索
    chroma_client = chromadb.PersistentClient(path=cfg["chroma_persist_dir"])
    collection = chroma_client.get_collection(collection_name)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3,
        where={"module": module}
    )

    log.info("相似度检索测试：query='%s'", query)
    for i, (id_, dist, doc) in enumerate(zip(
        results["ids"][0],
        results["distances"][0],
        results["documents"][0]
    )):
        log.info(
            "  Top-%d: id=%s 相似度=%.4f\n         %s...",
            i + 1, id_, 1 - dist, doc[:100].replace("\n", " ")
        )


def check_mysql(cfg: dict, module: str) -> None:
    """检查 MySQL 中的文档和 chunk 记录"""
    if not cfg["db_url"]:
        log.info("DB_URL 未配置，跳过 MySQL 验证")
        return

    try:
        import pymysql
    except ImportError:
        log.warning("缺少 pymysql，跳过 MySQL 验证")
        return

    sep = "://"
    raw_url = cfg["db_url"]
    db_url = raw_url[raw_url.index(sep) + len(sep):]  # 跳过 scheme://
    host_port, _, rest = db_url.partition("/")
    database = rest.split("?")[0]
    host, _, port = host_port.partition(":")

    try:
        conn = pymysql.connect(
            host=host, port=int(port) if port else 3306,
            database=database,
            user=cfg["db_username"], password=cfg["db_password"],
            charset="utf8mb4"
        )
        with conn.cursor() as cur:
            cur.execute("""
                SELECT d.title, d.chunk_count, d.total_tokens, d.sync_status
                FROM mes_ai_knowledge.ai_kb_document d
                WHERE d.module = %s
            """, (module,))
            rows = cur.fetchall()
            log.info("MySQL ai_kb_document：模块=%s，文档数=%d", module, len(rows))
            for row in rows:
                log.info("  文档：%s chunks=%s tokens=%s status=%s", *row)
        conn.close()
    except Exception as e:
        log.warning("MySQL 查询失败：%s", e)


def parse_args():
    p = argparse.ArgumentParser(description="知识库入库验证脚本")
    p.add_argument("--module",     required=True, help="MES 模块名")
    p.add_argument("--collection", default="mes_db_structure", help="ChromaDB 集合名")
    return p.parse_args()


def main():
    args = parse_args()
    cfg = load_config()

    log.info("====== 知识库入库验证 ======")
    log.info("模块：%s  集合：%s", args.module, args.collection)

    ok = check_chromadb(cfg, args.collection, args.module)
    if ok:
        test_similarity_search(cfg, args.collection, args.module)
    check_mysql(cfg, args.module)

    log.info("====== 验证完成 ======")


if __name__ == "__main__":
    main()
