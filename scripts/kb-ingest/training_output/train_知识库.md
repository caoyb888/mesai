# 训练结果：知识库

**训练时间**：2026-04-13T10:58:18.191710

**Tokens**：{'prompt_tokens': 1389, 'completion_tokens': 650, 'total_tokens': 2039}

---

1. **表清单确认**

以下是我理解的所有表名及其中文业务含义：

| 表名               | 中文业务含义       |
|-------------------|----------------|
| itsm_kb_article    | 知识库文章表       |
| itsm_kb_article_version | 知识库文章版本历史表 |
| itsm_kb_category   | 知识库分类表       |

2. **核心实体识别**

该模块中最重要的 2 张表是：

- **itsm_kb_article（知识库文章表）**：存储知识库文章的基本信息和状态，是知识库模块的核心数据实体。
- **itsm_kb_article_version（知识库文章版本历史表）**：记录知识库文章的每次发布版本，支持版本管理和历史回溯。

业务角色：
- **itsm_kb_article**：主要服务于知识库管理员和用户，管理员负责文章的创建、审核、发布等操作，用户可以浏览和使用知识库文章。
- **itsm_kb_article_version**：主要服务于知识库管理员和审计人员，管理员负责文章版本的创建和维护，审计人员可以通过版本历史表进行审计和回溯。

3. **主键与外键梳理**

以下是各表的主键字段及跨表关联关系：

```
+----------------+         +-------------------+
| itsm_kb_article |         | itsm_kb_article_version |
+----------------+         +-------------------+
| id (PK)        |         | id (PK)           |
| category_id    | --->    | article_id        |
| ...            |         | version           |
+----------------+         | content          |
                     |         | change_note      |
                     +         | created_at       |
                     |         | created_by       |
                     +-------------------+
```

```
+----------------+         +-------------------+
| itsm_kb_article |         | itsm_kb_category   |
+----------------+         +-------------------+
| id (PK)        |         | id (PK)           |
| category_id    | --->    | parent_id         |
| ...            |         | name             |
+----------------+         | sort_order        |
                     +-------------------+
```

4. **关键状态字段**

以下是含 status / type / deleted 类字段的表及其含义：

- **itsm_kb_article（知识库文章表）**
  - `status`：生命周期状态，取值有：
    - `Draft`：草稿
    - `Pending_Review`：待审核
    - `Published`：已发布
    - `Rejected`：驳回
    - `Archived`：已归档
  - `is_deleted`：逻辑删除标记，取值有：
    - `0`：未删除
    - `1`：已删除

- **itsm_kb_category（知识库分类表）**
  - `is_deleted`：逻辑删除标记，取值有：
    - `0`：未删除
    - `1`：已删除

5. **疑问记录**

目前没有发现字段含义不清晰或注释缺失的情况。