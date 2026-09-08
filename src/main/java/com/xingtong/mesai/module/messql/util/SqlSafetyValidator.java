package com.xingtong.mesai.module.messql.util;

import lombok.Getter;

import java.util.regex.Pattern;

/**
 * MES 取数 SQL 安全校验器
 *
 * <p>安全红线（CLAUDE.md §3.3 / §4.3）：AI 生成的 SQL 在执行前必须逐项通过校验，
 * 只允许对 MES 只读数据源执行单条 SELECT 查询：
 * <ol>
 *   <li>非空；</li>
 *   <li>单语句（禁止分号分隔的多语句注入）；</li>
 *   <li>禁止 SQL 注释（-- 与 /* *\/），防止藏匿 payload；</li>
 *   <li>必须以 SELECT / WITH 开头（只读查询，WITH 用于 CTE 分析查询）；</li>
 *   <li>禁止任何写操作与 DDL 关键字（INSERT/UPDATE/DELETE/MERGE/DROP/CREATE/ALTER/
 *       TRUNCATE/GRANT/REVOKE/CALL/EXEC 等），以及 SELECT INTO / FOR UPDATE 加锁读；</li>
 *   <li>禁止 SELECT *，必须显式列名（同时规避全列扫描与字段漂移）。</li>
 * </ol>
 *
 * <p>安全取向：本校验器基于关键字匹配，宁可“误拦合法查询”也不放过潜在写操作。
 * 若查询字符串字面量中恰好含被禁关键字（如 WHERE remark = 'CREATE'）会被拦截，
 * 属可接受的保守副作用，使用方应改写为参数化条件或调整措辞后重试。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
public final class SqlSafetyValidator {

    private SqlSafetyValidator() {
    }

    /** 只读查询允许的起始关键字（SELECT 常规查询 / WITH CTE 分析查询）*/
    private static final Pattern STARTS_WITH_SELECT = Pattern.compile(
            "(?is)^(SELECT|WITH)\\b.*"
    );

    /** 禁止的写操作与 DDL/权限/事务/加锁关键字（按词边界匹配）*/
    private static final Pattern FORBIDDEN_KEYWORDS = Pattern.compile(
            "(?i)\\b(INSERT|UPDATE|DELETE|MERGE|UPSERT|DROP|CREATE|ALTER|TRUNCATE|RENAME|"
                    + "GRANT|REVOKE|EXEC|EXECUTE|CALL|COMMIT|ROLLBACK|SAVEPOINT|LOCK|INTO)\\b"
    );

    /** 加锁读：FOR UPDATE（Oracle 会持有行锁，只读场景禁止）*/
    private static final Pattern FOR_UPDATE = Pattern.compile("(?i)\\bFOR\\s+UPDATE\\b");

    /** SELECT *（含 SELECT DISTINCT * 与 SELECT t.*），COUNT(*) 不会命中 */
    private static final Pattern SELECT_STAR = Pattern.compile(
            "(?i)\\bSELECT\\s+(?:DISTINCT\\s+|ALL\\s+)?([A-Za-z_][A-Za-z0-9_]*\\s*\\.\\s*)?\\*"
    );

    /**
     * 校验 SQL 安全性。
     *
     * @param rawSql AI 生成的原始 SQL
     * @return 校验结果（含归一化后的 SQL 与失败原因）
     */
    public static SqlSafetyResult validate(String rawSql) {
        if (rawSql == null || rawSql.trim().isEmpty()) {
            return SqlSafetyResult.fail("SQL 为空，无法执行");
        }

        // 归一化：去首尾空白，去掉末尾唯一分号
        String sql = rawSql.trim();
        if (sql.endsWith(";")) {
            sql = sql.substring(0, sql.length() - 1).trim();
        }

        // 多语句拦截：归一化后仍含分号，视为多语句注入
        if (sql.contains(";")) {
            return SqlSafetyResult.fail("安全拦截：禁止多语句执行（检测到分号分隔的多条语句）");
        }

        // 注释拦截：防止 -- 或 /* */ 藏匿 payload
        if (sql.contains("--") || sql.contains("/*")) {
            return SqlSafetyResult.fail("安全拦截：禁止 SQL 注释（-- 或 /* */），防止注入隐藏语句");
        }

        // 必须为只读查询
        if (!STARTS_WITH_SELECT.matcher(sql).matches()) {
            return SqlSafetyResult.fail("安全拦截：只允许 SELECT/WITH 只读查询，禁止其他类型语句");
        }

        // 加锁读拦截（先于通用写操作关键字，给出更精确的 FOR UPDATE 提示；
        // 注意 FOR UPDATE 含 UPDATE 关键字，若不先判会被下方 FORBIDDEN 兜住成泛化提示）
        if (FOR_UPDATE.matcher(sql).find()) {
            return SqlSafetyResult.fail("安全拦截：禁止 FOR UPDATE 加锁读，只读数据源不允许持锁");
        }

        // 写操作 / DDL 关键字拦截
        if (FORBIDDEN_KEYWORDS.matcher(sql).find()) {
            return SqlSafetyResult.fail("安全拦截：检测到写操作或 DDL 关键字，MES 数据源仅允许只读查询");
        }

        // SELECT * 拦截（CLAUDE.md §3.3：禁止 SELECT *）
        if (SELECT_STAR.matcher(sql).find()) {
            return SqlSafetyResult.fail("安全拦截：禁止 SELECT *，必须显式列出查询字段");
        }

        return SqlSafetyResult.pass(sql);
    }

    /**
     * SQL 安全校验结果
     */
    @Getter
    public static final class SqlSafetyResult {

        /** 是否通过校验 */
        private final boolean passed;

        /** 归一化后的 SQL（通过时有值：已去除末尾分号与首尾空白）*/
        private final String normalizedSql;

        /** 失败原因（未通过时有值）*/
        private final String reason;

        private SqlSafetyResult(boolean passed, String normalizedSql, String reason) {
            this.passed = passed;
            this.normalizedSql = normalizedSql;
            this.reason = reason;
        }

        static SqlSafetyResult pass(String normalizedSql) {
            return new SqlSafetyResult(true, normalizedSql, null);
        }

        static SqlSafetyResult fail(String reason) {
            return new SqlSafetyResult(false, null, reason);
        }
    }
}
