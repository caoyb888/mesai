"""
RAG proc hybrid 检索单元测试（纯逻辑，绕开 chromadb/sentence-transformers 重依赖）

覆盖：二次切分片段父过程归并（_proc_parent）、proc 标签 bigram、
     标签驱动 RRF 融合把「向量排名靠后但中文标签命中」的过程提进 Top-N。

关联需求单：REQ-MES-AI-20260716-001（超大过程二次切分 hybrid 调优）
作者：AI（芯智云匠）  日期：2026-07-17
"""
from app.services.rag_service import RagService, RagDocument


def _doc(parent_or_frag):
    """构造一条以 source_file 标识过程身份的检索结果"""
    return RagDocument(doc_id=f"proc:{parent_or_frag}:0", content=f"[过程] {parent_or_frag}",
                       distance=0.5, metadata={"source_file": f"{parent_or_frag}.md",
                                               "chunk_type": "s3_proc"})


def _make_svc(proc_labels, vector_docs):
    """用 object.__new__ 造一个不加载重依赖的 RagService，注入受控向量结果与标签"""
    svc = object.__new__(RagService)
    svc._labels = {}
    svc._proc_labels = proc_labels
    svc._cache = {"anc_proc": {}}          # 锚点置空，避免触及 _client
    svc.retrieve = lambda *a, **k: list(vector_docs)   # 桩：返回受控向量排序
    return svc


def test_proc_parent_strips_fragment_suffix():
    assert RagService._proc_parent("PKG.PR_X_p01") == "PKG.PR_X"
    assert RagService._proc_parent("PKG.PR_X_p12") == "PKG.PR_X"
    assert RagService._proc_parent("PKG.PR_X") == "PKG.PR_X"        # 非片段原样


def test_proc_vector_dedup_by_parent():
    # 同一父过程的两个片段不应各占一席，应归并为一个身份
    target = "PKG.PR_MECH_ITEM_JDG"
    docs = [_doc(f"{target}_p01"), _doc(f"{target}_p02"), _doc("PKG.PR_OTHER")]
    svc = _make_svc({}, docs)   # 无标签 → 纯向量去重
    out = svc.retrieve_for_mes("任意查询", top_n=5, kind="proc")
    ids = [d.metadata["source_file"].replace(".md", "") for d in out]
    parents = [RagService._proc_parent(i) for i in ids]
    assert parents.count(target) == 1          # 父过程只出现一次
    assert "PKG.PR_OTHER" in parents


def test_proc_hybrid_boosts_label_match_into_topn():
    # 向量把 target 排在第 4（Top-3 之外），但其中文标签命中查询 → RRF 应提进 Top-3
    target = "PKG.PR_MECH_ITEM_JDG"
    distractors = ["PKG.D1", "PKG.D2", "PKG.D3"]
    docs = [_doc(d) for d in distractors] + [_doc(f"{target}_p01")]
    labels = {target: {"label": "机械测试项判定", "aliases": ["力学性能判定", "机械性能判定"]}}
    svc = _make_svc(labels, docs)

    # 纯向量（无标签）Top-3 不含 target
    vec_only = _make_svc({}, docs)
    vec_ids = [RagService._proc_parent(d.metadata["source_file"].replace(".md", ""))
               for d in vec_only.retrieve_for_mes("力学性能项目判定逻辑", top_n=3, kind="proc")]
    assert target not in vec_ids

    # hybrid：标签命中 → 进 Top-3
    hyb_ids = [RagService._proc_parent(d.metadata["source_file"].replace(".md", ""))
               for d in svc.retrieve_for_mes("力学性能项目判定逻辑", top_n=3, kind="proc")]
    assert target in hyb_ids


def test_proc_labels_used_not_table_labels():
    # kind=proc 必须用 proc 标签路；表标签不应影响 proc 检索
    target = "PKG.PR_SEARCH_STOCK"
    docs = [_doc("PKG.D1"), _doc("PKG.D2"), _doc("PKG.D3"), _doc(target)]
    svc = _make_svc({target: {"label": "库存信息查询", "aliases": ["库存查询", "在库查询"]}}, docs)
    svc._labels = {target: {"label": "不相关表", "aliases": ["无关"]}}  # 表标签故意错
    out_ids = [RagService._proc_parent(d.metadata["source_file"].replace(".md", ""))
               for d in svc.retrieve_for_mes("样品库存查询", top_n=3, kind="proc")]
    assert target in out_ids
