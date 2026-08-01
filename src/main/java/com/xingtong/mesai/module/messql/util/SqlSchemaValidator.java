package com.xingtong.mesai.module.messql.util;

import lombok.Getter;
import org.springframework.dao.DataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * MES 取数 schema 校验器（防臆造第二道闸）
 *
 * <p>背景：LLM 可能生成“看起来对”但并不存在的表/字段（如把 PROD_TOT_JDG_DTM
 * 近似改写为 PROD_JDG_DTM），执行时报 ORA-00904/ORA-00942 才暴露。
 * 本校验器在执行前用 Oracle 数据字典 {@code all_tab_columns} 核对网关返回的
 * referenced_tables / referenced_columns，凡引用不存在的表或字段即拦截，
 * 把“执行期报错”提前为“执行前拦截并给出可改写提示”。
 *
 * <p>判定口径：表必须在 MESAPUSER 属主下存在；字段存在于任一引用表即视为有效
 * （网关返回的字段清单不带表归属，跨表同名属正常）。
 * 所有查询均参数化，禁止拼接（CLAUDE.md §3.3）。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-30
 * @module MES取数
 * @related REQ-MES-AI-20260730-001（NL → Oracle 只读 SELECT 生成与执行）
 */
public final class SqlSchemaValidator {

    /** MES 业务表属主（与知识库/只读账号 CURRENT_SCHEMA 约定一致）*/
    private static final String MES_OWNER = "MESAPUSER";

    /** 纯标识符（表/列名合法字符）：含括号、星号、空格的条目（如 COUNT(*)、*）不是列名，直接跳过 */
    private static final java.util.regex.Pattern IDENTIFIER =
            java.util.regex.Pattern.compile("^[A-Z0-9_$#]+$");

    /**
     * Oracle 伪列/内置常量：不是真实列，LLM 误列入 referenced_columns 时不参与校验
     * （如 SYSDATE 被当字段核对会误拦合法 SQL）
     */
    private static final Set<String> PSEUDO_COLUMNS = Set.of(
            "SYSDATE", "SYSTIMESTAMP", "CURRENT_DATE", "CURRENT_TIMESTAMP",
            "ROWNUM", "ROWID", "LEVEL", "USER");

    private SqlSchemaValidator() {
    }

    /**
     * 校验引用的表/字段在 MES 库中真实存在。
     *
     * @param mesJdbcTemplate MES 只读数据源
     * @param tables          网关返回的 referenced_tables（可空）
     * @param columns         网关返回的 referenced_columns（可空）
     * @return 校验结果（含不存在的表/字段清单与中文提示）
     */
    public static SchemaCheckResult validate(JdbcTemplate mesJdbcTemplate,
                                             List<String> tables, List<String> columns) {
        List<String> tableNames = normalizeTables(tables);
        List<String> columnNames = normalizeColumns(columns);

        // 无引用清单（generated=true 但模型未给出元数据）：无从校验，放行由执行层兜底
        if (tableNames.isEmpty()) {
            return SchemaCheckResult.pass();
        }

        // 参数化 IN 查询：一次取回所有引用表的真实列清单
        String placeholders = tableNames.stream().map(t -> "?").collect(Collectors.joining(", "));
        String metaSql = "SELECT table_name, column_name FROM all_tab_columns "
                + "WHERE owner = ? AND table_name IN (" + placeholders + ")";
        List<Object> params = new ArrayList<>();
        params.add(MES_OWNER);
        params.addAll(tableNames);

        List<Map<String, Object>> metaRows;
        try {
            metaRows = mesJdbcTemplate.queryForList(metaSql, params.toArray());
        } catch (DataAccessException e) {
            // 元数据查询失败（如字典视图不可读）：不阻断主流程，放行由执行层报错
            return SchemaCheckResult.pass();
        }

        Set<String> existingTables = new LinkedHashSet<>();
        Set<String> existingColumns = new LinkedHashSet<>();
        for (Map<String, Object> row : metaRows) {
            Object t = row.get("TABLE_NAME");
            Object c = row.get("COLUMN_NAME");
            if (t != null) {
                existingTables.add(t.toString());
            }
            if (c != null) {
                existingColumns.add(c.toString());
            }
        }

        List<String> unknownTables = tableNames.stream()
                .filter(t -> !existingTables.contains(t)).collect(Collectors.toList());
        List<String> unknownColumns = columnNames.stream()
                .filter(c -> !existingColumns.contains(c)).collect(Collectors.toList());

        if (unknownTables.isEmpty() && unknownColumns.isEmpty()) {
            return SchemaCheckResult.pass();
        }
        return SchemaCheckResult.fail(unknownTables, unknownColumns);
    }

    /** 归一化：去空白、转大写、去重、去空串 */
    private static List<String> normalize(List<String> names) {
        if (names == null) {
            return Collections.emptyList();
        }
        Set<String> result = new LinkedHashSet<>();
        for (String n : names) {
            if (n != null && !n.isBlank()) {
                result.add(n.trim().toUpperCase());
            }
        }
        return new ArrayList<>(result);
    }

    /**
     * 表名归一化：剔除含「.」的条目。
     * 带点条目是包级存储过程（如 BSIM_BP_FINE_CK_PROD_CONF.PR_F_XXX），不是基表；
     * 其 SQL 是否可执行交由执行层判定，不在此按表校验（否则误拦/误分类）。
     */
    private static List<String> normalizeTables(List<String> tables) {
        List<String> result = new ArrayList<>();
        for (String t : normalize(tables)) {
            if (!t.contains(".")) {
                result.add(t);
            }
        }
        return result;
    }

    /**
     * 列名归一化：剔除非纯标识符条目（COUNT(*)、* 等表达式残留）与 Oracle 伪列
     * （SYSDATE 等）。这些是 LLM 填写 referenced_columns 时的常见噪声，
     * 不是真实列，参与核对会误拦合法 SQL。
     */
    private static List<String> normalizeColumns(List<String> columns) {
        List<String> result = new ArrayList<>();
        for (String c : normalize(columns)) {
            if (IDENTIFIER.matcher(c).matches() && !PSEUDO_COLUMNS.contains(c)) {
                result.add(c);
            }
        }
        return result;
    }

    /**
     * schema 校验结果
     */
    @Getter
    public static final class SchemaCheckResult {

        /** 是否通过（含“无从校验/元数据不可用”的放行情形）*/
        private final boolean passed;

        /** 不存在的表名清单 */
        private final List<String> unknownTables;

        /** 不存在的字段名清单 */
        private final List<String> unknownColumns;

        /** 中文提示（未通过时有值）*/
        private final String message;

        private SchemaCheckResult(boolean passed, List<String> unknownTables,
                                  List<String> unknownColumns, String message) {
            this.passed = passed;
            this.unknownTables = unknownTables;
            this.unknownColumns = unknownColumns;
            this.message = message;
        }

        static SchemaCheckResult pass() {
            return new SchemaCheckResult(true, Collections.emptyList(), Collections.emptyList(), null);
        }

        static SchemaCheckResult fail(List<String> unknownTables, List<String> unknownColumns) {
            StringBuilder msg = new StringBuilder("防臆造拦截：生成 SQL 引用了知识库/数据库中不存在的");
            List<String> parts = new ArrayList<>();
            if (!unknownTables.isEmpty()) {
                parts.add("表 " + unknownTables);
            }
            if (!unknownColumns.isEmpty()) {
                parts.add("字段 " + unknownColumns);
            }
            msg.append(String.join("、", parts));
            msg.append("。请核对表卡片中的真实表名/字段名（逐字一致，勿近似改写）后重新提问");
            return new SchemaCheckResult(false, unknownTables, unknownColumns, msg.toString());
        }
    }
}
