# 脱敏审计报告（S3 训练前置合规门）

> 关联需求单：REQ-MES-AI-20260706-001 ｜ 工具：`scripts/desensitize/audit_materials.py`
> 规则源：`src/ai-gateway/app/services/desensitize.py`（与网关外发同一套，CLAUDE.md 4.2 全 7 类）
> 目的：确认外发 Kimi 的训练素材无敏感信息泄露；命中项供人工核验误报/真实风险。

## 结论：✅ 未命中任何脱敏规则（素材可外发）

## 一、受审素材

| 素材文件 | 审计单位数 | 方式 |
|----------|-----------|------|
| meta_p0.json | 120 | plsql |
| p0_table_cards.md | 13947 | text |
| glossary_zh_ko_en.csv | 9699 | csv |
| dict_reconcile_report.md | 355 | text |
| split_report.md | 68 | text |

## 二、命中分类统计

（无命中）
