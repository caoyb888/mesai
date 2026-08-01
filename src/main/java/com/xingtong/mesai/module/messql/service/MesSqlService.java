package com.xingtong.mesai.module.messql.service;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.demo.vo.SqlExecutionResult;
import com.xingtong.mesai.module.messql.dto.MesSqlRequest;
import com.xingtong.mesai.module.messql.util.SqlSafetyValidator;
import com.xingtong.mesai.module.messql.util.SqlSafetyValidator.SqlSafetyResult;
import com.xingtong.mesai.module.messql.util.SqlSchemaValidator;
import com.xingtong.mesai.module.messql.vo.MesSqlVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * MES 取数服务
 *
 * <p>职责：
 * <ol>
 *   <li>转发取数需求至 AI 网关 /v1/ai/mes-sql，由网关 RAG 检索 + LLM 生成 Oracle 只读 SELECT
 *       （网关侧复用统一链路：PII 脱敏门 → Token 预算闸 → LLM Provider → 用量计入）；</li>
 *   <li>对生成的 SQL 执行安全校验（{@link SqlSafetyValidator}：仅 SELECT / 禁 DDL·DML /
 *       禁 SELECT * / 禁多语句），校验不通过则拦截不执行；</li>
 *   <li>校验通过且只读数据源已配置时，在 MES 只读数据源上执行 SELECT（Oracle ROWNUM 行数封顶），
 *       返回结果集；未配置数据源或未开启执行时，仅返回生成的 SQL。</li>
 * </ol>
 *
 * <p>安全边界（CLAUDE.md §4.3）：本服务对 MES 库只做只读查询，never 写操作；
 * 执行链路受“应用层 SQL 校验 + Hikari read-only + 只读账号”三重保护。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MesSqlService {

    /** AI 网关基地址（不硬编码，由配置注入）*/
    @Value("${ai.gateway.base-url:http://localhost:8000}")
    private String aiGatewayBaseUrl;

    private String mesSqlUrl;

    /** MES 只读数据源 JdbcTemplate（可能为 null，未配置 MES_DB_URL 时不注入）*/
    @Autowired(required = false)
    @Qualifier("mesJdbcTemplate")
    @Nullable
    private JdbcTemplate mesJdbcTemplate;

    private final RestTemplate restTemplate;

    /** SELECT 结果最大返回行数（防止大表全扫导致内存溢出）*/
    private static final int MAX_RESULT_ROWS = 200;

    /** 自纠错重试开关（REQ-MES-AI-20260730-002 G 段：retry.enabled，仅影响失败路径）*/
    @Value("${mes.sql.retry.enabled:true}")
    private boolean retryEnabled;

    /** 重试轮次硬上限（D1：≤3 轮）*/
    @Value("${mes.sql.retry.max-rounds:3}")
    private int retryMaxRounds;

    /** 含重试全链路超时上限毫秒（F4.2：建议 ≤60s）*/
    @Value("${mes.sql.retry.timeout-ms:60000}")
    private long retryTimeoutMs;

    /** 回喂真实列清单裁剪上限（F6.3）：每表最多列数 */
    @Value("${mes.sql.retry.feedback-cols-per-table:40}")
    private int feedbackColsPerTable;

    /** ORA 错误码提取（提前终止判定用，F4.1）*/
    private static final java.util.regex.Pattern ORA_CODE =
            java.util.regex.Pattern.compile("ORA-\\d{5}");

    /** ORA-00904 等错误中的无效对象名提取（如 "SPEC_CD"）*/
    private static final java.util.regex.Pattern ORA_OBJECT =
            java.util.regex.Pattern.compile("\"([A-Z0-9_$#]+)\"");

    @PostConstruct
    void init() {
        mesSqlUrl = aiGatewayBaseUrl + "/v1/ai/mes-sql";
        log.info("MES 取数服务初始化：AI 网关地址={}", mesSqlUrl);
        if (mesJdbcTemplate == null) {
            log.warn("MES 只读数据源未配置（MES_DB_URL 为空），取数接口将仅生成 SQL 不执行");
        }
    }

    /**
     * 处理 MES 取数请求
     *
     * @param req 前端请求（取数需求 + 可选 topN + 是否执行）
     * @return 生成的 SQL + 安全校验/执行结果
     */
    public MesSqlVO query(MesSqlRequest req) {
        Map<String, Object> gatewayResp = callAiGateway(req, null);

        MesSqlVO vo = new MesSqlVO();
        vo.setQuestion(req.getQuestion());
        vo.setGenerated(getBool(gatewayResp, "generated"));
        vo.setSql(getString(gatewayResp, "sql"));
        vo.setExplanation(getString(gatewayResp, "explanation"));
        vo.setReferencedTables(parseStringList(gatewayResp, "referenced_tables"));
        vo.setReferencedColumns(parseStringList(gatewayResp, "referenced_columns"));
        String unanswerable = getString(gatewayResp, "unanswerable_reason");
        vo.setUnanswerableReason(unanswerable.isEmpty() ? null : unanswerable);
        vo.setContextDocs(parseContextDocs(gatewayResp));
        vo.setProvider(getString(gatewayResp, "provider"));
        vo.setModel(getString(gatewayResp, "model"));
        vo.setTokensUsed(getInt(gatewayResp, "tokens_used"));
        vo.setAiResponseTimeMs(getInt(gatewayResp, "response_time_ms"));

        // 执行阶段：仅在开启执行 + 已生成 SQL 时进入校验/执行
        if (req.isExecuteSql()) {
            vo.setExecutionResult(executeWithRetry(req, vo));
        }

        return vo;
    }

    // ── 私有方法 ──────────────────────────────────────────────────

    /**
     * 执行 + 自纠错重试（B2.1）。
     *
     * <p>首轮失败（schema 校验拦截 / 执行 ORA 错误）且 retry.enabled 时，
     * 把「失败 SQL + 失败原因 + 涉及表真实列清单」回喂网关重新生成，最多
     * {@code retryMaxRounds} 轮；每轮仍过安全校验 + schema 校验（F6.1 防线不降级）。
     *
     * <p>终止条件（F4）：轮次上限 / 全链路超时 / 连续两轮同一错误码+同一错误对象（提前终止）。
     * 重试耗尽返回 generated=false + 可读原因，不返回未通过校验的 SQL（F3.3）。
     */
    private SqlExecutionResult executeWithRetry(MesSqlRequest req, MesSqlVO vo) {
        SqlExecutionResult result = runIfSafe(vo.isGenerated(), vo.getSql(),
                vo.getReferencedTables(), vo.getReferencedColumns());
        if (!retryEnabled || !shouldRetry(result)) {
            return result;
        }

        long deadline = System.currentTimeMillis() + retryTimeoutMs;
        String prevSignature = null;
        int attempts = 1;   // 已完成的生成次数（含首轮）
        while (attempts < retryMaxRounds && System.currentTimeMillis() < deadline) {
            String signature = errorSignature(result);
            if (signature != null && signature.equals(prevSignature)) {
                log.warn("MES 取数自纠错提前终止：连续两轮同一错误 {}", signature);
                break;
            }
            prevSignature = signature;

            Map<String, Object> feedback = buildRetryFeedback(vo, result);
            Map<String, Object> resp = callAiGateway(req, feedback);
            attempts++;
            applyGeneration(vo, resp);
            log.info("[MES取数] 自纠错第 {} 轮：generated={} sql={}",
                    attempts, vo.isGenerated(), abbrev(vo.getSql()));

            result = runIfSafe(vo.isGenerated(), vo.getSql(),
                    vo.getReferencedTables(), vo.getReferencedColumns());
            if (!shouldRetry(result)) {
                break;
            }
        }

        vo.setRetryCount(attempts - 1);
        if (shouldRetry(result)) {
            // 重试耗尽/超时/提前终止：不返回未通过校验的 SQL（F3.3）
            String reason = "自纠错重试 " + (attempts - 1) + " 轮仍未通过："
                    + (result.getErrorMessage() == null ? "未知原因" : result.getErrorMessage());
            log.warn("MES 取数自纠错耗尽：{}", reason);
            vo.setGenerated(false);
            vo.setSql("");
            vo.setUnanswerableReason(reason);
        }
        return result;
    }

    /**
     * 是否应进入/继续重试：schema 校验拦截 或 执行期 ORA 错误（B2.1 触发口径）。
     * 安全校验拦截（SELECT * 等）不触发重试（属模型违规，直接拦截）。
     */
    private boolean shouldRetry(SqlExecutionResult result) {
        if (result == null || result.isSuccess()) {
            return false;
        }
        if ("BLOCKED".equals(result.getExecType())) {
            return result.getErrorMessage() != null && result.getErrorMessage().contains("防臆造");
        }
        return "SELECT".equals(result.getExecType())
                && result.getErrorMessage() != null && result.getErrorMessage().contains("ORA-");
    }

    /**
     * 错误签名（F4.1 提前终止判定）：ORA 错误码 + 首个错误对象；
     * schema 拦截取「防臆造 + 具体表/字段清单」。无法提取时返回 null（不参与提前终止）。
     */
    private String errorSignature(SqlExecutionResult result) {
        String msg = result.getErrorMessage();
        if (msg == null) {
            return null;
        }
        java.util.regex.Matcher code = ORA_CODE.matcher(msg);
        if (code.find()) {
            String obj = "";
            java.util.regex.Matcher om = ORA_OBJECT.matcher(msg);
            if (om.find()) {
                obj = om.group(1);
            }
            return code.group() + ":" + obj;
        }
        if (msg.contains("防臆造拦截")) {
            return msg.length() > 120 ? msg.substring(0, 120) : msg;
        }
        return null;
    }

    /**
     * 组装重试反馈（F6.3 裁剪口径）：失败 SQL + 失败原因 + 涉及表真实列清单。
     * 列清单仅含「referenced_tables 中真实存在的表」，每表上限 feedbackColsPerTable 列，
     * referenced_columns 与错误对象近似列优先，其余按字典物理序补足。
     */
    private Map<String, Object> buildRetryFeedback(MesSqlVO vo, SqlExecutionResult result) {
        Map<String, Object> feedback = new LinkedHashMap<>();
        feedback.put("failed_sql", vo.getSql() == null ? "" : vo.getSql());
        String error = result.getErrorMessage() == null ? "未知错误" : result.getErrorMessage();
        feedback.put("error_message", error.length() > 800 ? error.substring(0, 800) : error);
        feedback.put("real_schema", fetchRealSchema(
                vo.getReferencedTables(), vo.getReferencedColumns(), error));
        return feedback;
    }

    /**
     * 查询涉及表的真实列清单（列名+类型），供回喂修正。
     * 元数据查询失败时返回空串（重试仍可进行，仅缺少结构提示）。
     */
    private String fetchRealSchema(List<String> tables, List<String> refColumns, String errorMessage) {
        if (mesJdbcTemplate == null || tables == null || tables.isEmpty()) {
            return "";
        }
        List<String> cleanTables = new ArrayList<>();
        for (String t : tables) {
            if (t != null && !t.isBlank() && !t.contains(".")) {
                cleanTables.add(t.trim().toUpperCase());
            }
        }
        if (cleanTables.isEmpty()) {
            return "";
        }
        String errorObject = "";
        java.util.regex.Matcher om = ORA_OBJECT.matcher(errorMessage);
        if (om.find()) {
            errorObject = om.group(1);
        }

        String placeholders = cleanTables.stream().map(t -> "?").collect(Collectors.joining(", "));
        String metaSql = "SELECT table_name, column_name, data_type, data_length "
                + "FROM all_tab_columns WHERE owner = ? AND table_name IN (" + placeholders + ") "
                + "ORDER BY table_name, column_id";
        List<Object> params = new ArrayList<>();
        params.add("MESAPUSER");
        params.addAll(cleanTables);
        List<Map<String, Object>> rows;
        try {
            rows = mesJdbcTemplate.queryForList(metaSql, params.toArray());
        } catch (DataAccessException e) {
            log.warn("MES 取数回喂列清单查询失败（降级为空）：{}", e.getMessage());
            return "";
        }

        Map<String, List<String>> byTable = new LinkedHashMap<>();
        for (String t : cleanTables) {
            byTable.put(t, new ArrayList<>());
        }
        for (Map<String, Object> row : rows) {
            String t = String.valueOf(row.get("TABLE_NAME"));
            String col = String.valueOf(row.get("COLUMN_NAME"));
            String type = String.valueOf(row.get("DATA_TYPE"));
            Object len = row.get("DATA_LENGTH");
            if ("VARCHAR2".equals(type) || "CHAR".equals(type)) {
                type = type + "(" + len + ")";
            }
            if (byTable.containsKey(t)) {
                byTable.get(t).add(col + " " + type);
            }
        }

        String finalErrorObject = errorObject;
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, List<String>> e : byTable.entrySet()) {
            if (e.getValue().isEmpty()) {
                continue;   // 表不存在（臆造表）：不输出，让模型从上下文重新选表
            }
            List<String> cols = e.getValue();
            // 裁剪：referenced_columns 与错误对象近似列优先，其余按字典序补足
            List<String> priority = cols.stream()
                    .filter(c -> {
                        String name = c.split(" ")[0];
                        return (refColumns != null && refColumns.contains(name))
                                || (!finalErrorObject.isEmpty() && name.contains(finalErrorObject))
                                || (!finalErrorObject.isEmpty() && finalErrorObject.length() >= 4
                                    && name.startsWith(finalErrorObject.substring(0, 4)));
                    })
                    .collect(Collectors.toList());
            List<String> rest = cols.stream().filter(c -> !priority.contains(c)).collect(Collectors.toList());
            List<String> selected = new ArrayList<>(priority);
            selected.addAll(rest);
            selected = selected.subList(0, Math.min(selected.size(), feedbackColsPerTable));
            sb.append(e.getKey()).append("(").append(String.join(", ", selected)).append(")\n");
        }
        return sb.toString().trim();
    }

    /** 网关重试响应 → 更新 VO 的生成结果字段（保留首轮 contextDocs/provider 等元数据）*/
    private void applyGeneration(MesSqlVO vo, Map<String, Object> gatewayResp) {
        vo.setGenerated(getBool(gatewayResp, "generated"));
        vo.setSql(getString(gatewayResp, "sql"));
        vo.setExplanation(getString(gatewayResp, "explanation"));
        vo.setReferencedTables(parseStringList(gatewayResp, "referenced_tables"));
        vo.setReferencedColumns(parseStringList(gatewayResp, "referenced_columns"));
        String unanswerable = getString(gatewayResp, "unanswerable_reason");
        vo.setUnanswerableReason(unanswerable.isEmpty() ? null : unanswerable);
        vo.setTokensUsed(vo.getTokensUsed() + getInt(gatewayResp, "tokens_used"));
    }

    private String abbrev(String sql) {
        if (sql == null) {
            return "";
        }
        return sql.length() > 80 ? sql.substring(0, 80) + "..." : sql;
    }

    /**
     * 生成成功则校验并执行；各前置条件不满足时返回 SKIPPED/BLOCKED 结果。
     */
    private SqlExecutionResult runIfSafe(boolean generated, String sql,
                                         List<String> referencedTables, List<String> referencedColumns) {
        if (!generated || sql == null || sql.isBlank()) {
            return SqlExecutionResult.builder()
                    .execType("SKIPPED")
                    .success(false)
                    .errorMessage("未生成有效 SQL，跳过执行")
                    .build();
        }

        // 1. 安全校验（安全红线，无论数据源是否配置都先校验）
        SqlSafetyResult safety = SqlSafetyValidator.validate(sql);
        if (!safety.isPassed()) {
            log.warn("MES 取数 SQL 安全校验拦截：{}", safety.getReason());
            return SqlExecutionResult.builder()
                    .execType("BLOCKED")
                    .success(false)
                    .errorMessage(safety.getReason())
                    .build();
        }

        // 2. 只读数据源未配置 → 仅生成不执行
        if (mesJdbcTemplate == null) {
            return SqlExecutionResult.builder()
                    .execType("SKIPPED")
                    .success(false)
                    .errorMessage("MES 只读数据源未配置（MES_DB_URL 为空），已生成 SQL 但未执行；"
                            + "配置只读账号后可自动开启执行")
                    .build();
        }

        // 3. schema 校验（防臆造第二道闸）：引用的表/字段必须真实存在，否则拦截不执行
        SqlSchemaValidator.SchemaCheckResult schemaCheck =
                SqlSchemaValidator.validate(mesJdbcTemplate, referencedTables, referencedColumns);
        if (!schemaCheck.isPassed()) {
            log.warn("MES 取数 schema 校验拦截：{}", schemaCheck.getMessage());
            return SqlExecutionResult.builder()
                    .execType("BLOCKED")
                    .success(false)
                    .errorMessage(schemaCheck.getMessage())
                    .build();
        }

        // 4. 只读执行（Oracle 行数封顶）
        return executeSelect(safety.getNormalizedSql());
    }

    /**
     * 在 MES 只读数据源上执行 SELECT，返回结果集（Oracle ROWNUM 封顶）。
     */
    private SqlExecutionResult executeSelect(String safeSql) {
        long start = System.currentTimeMillis();
        try {
            String cappedSql = oracleRowCap(safeSql, MAX_RESULT_ROWS);
            List<Map<String, Object>> rows = mesJdbcTemplate.queryForList(cappedSql);
            long elapsed = System.currentTimeMillis() - start;
            return SqlExecutionResult.builder()
                    .execType("SELECT")
                    .rows(rows)
                    .totalRows(rows.size())
                    .elapsedMs(elapsed)
                    .success(true)
                    .notice(rows.size() >= MAX_RESULT_ROWS
                            ? "结果集已截断，最多显示 " + MAX_RESULT_ROWS + " 行"
                            : "查询完成，共 " + rows.size() + " 行")
                    .build();
        } catch (DataAccessException e) {
            log.warn("MES 只读 SELECT 执行失败：{}", e.getMessage());
            return SqlExecutionResult.builder()
                    .execType("SELECT")
                    .success(false)
                    .errorMessage("SQL 执行错误：" + e.getMostSpecificCause().getMessage())
                    .elapsedMs(System.currentTimeMillis() - start)
                    .build();
        }
    }

    /**
     * 用 Oracle 语法为查询封顶行数：外层包裹 ROWNUM 过滤。
     *
     * <p>{@code SELECT * FROM ( <safeSql> ) WHERE ROWNUM <= max}
     * 外层 SELECT * 作用于子查询派生结果（非基表），不违反“禁 SELECT *”对用户 SQL 的约束。
     */
    static String oracleRowCap(String safeSql, int max) {
        return "SELECT * FROM (" + safeSql + ") WHERE ROWNUM <= " + max;
    }

    /**
     * 调用 AI 网关 /v1/ai/mes-sql 端点
     *
     * @param retryFeedback 自纠错重试反馈（B2.1，首轮为 null；含 failed_sql/error_message/real_schema）
     */
    @SuppressWarnings("unchecked")
    private Map<String, Object> callAiGateway(MesSqlRequest req, Map<String, Object> retryFeedback) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("question", req.getQuestion());
        if (req.getTopN() != null) {
            body.put("top_n", req.getTopN());
        }
        if (req.getTemperature() != null) {
            body.put("temperature", req.getTemperature());
        }
        if (req.getCaller() != null && !req.getCaller().isBlank()) {
            body.put("caller", req.getCaller());
        }
        if (retryFeedback != null) {
            body.put("retry_feedback", retryFeedback);
        }

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

        try {
            Map<String, Object> response = restTemplate.postForObject(mesSqlUrl, entity, Map.class);
            if (response == null) {
                throw BizException.of(ResultCode.AI_GATEWAY_ERROR, "AI 网关返回空响应");
            }
            return response;
        } catch (BizException e) {
            throw e;
        } catch (Exception e) {
            log.error("调用 AI 网关失败 url={} err={}", mesSqlUrl, e.getMessage(), e);
            throw BizException.of(ResultCode.AI_GATEWAY_ERROR, "AI 网关调用失败：" + e.getMessage());
        }
    }

    /**
     * 解析 AI 网关响应中的 context_docs 列表
     */
    @SuppressWarnings("unchecked")
    private List<ContextDocVO> parseContextDocs(Map<String, Object> resp) {
        List<ContextDocVO> result = new ArrayList<>();
        Object rawDocs = resp.get("context_docs");
        if (!(rawDocs instanceof List)) {
            return result;
        }
        for (Object item : (List<?>) rawDocs) {
            if (!(item instanceof Map)) {
                continue;
            }
            Map<String, Object> m = (Map<String, Object>) item;
            ContextDocVO doc = new ContextDocVO();
            doc.setSource(getString(m, "source"));
            doc.setDocType(getString(m, "doc_type"));
            doc.setContentPreview(getString(m, "content_preview"));
            Object score = m.get("relevance_score");
            doc.setRelevanceScore(score instanceof Number ? ((Number) score).doubleValue() : 0.0);
            result.add(doc);
        }
        return result;
    }

    /**
     * 解析网关响应中的字符串数组字段（referenced_tables / referenced_columns）
     */
    private List<String> parseStringList(Map<String, Object> resp, String key) {
        List<String> result = new ArrayList<>();
        Object raw = resp.get(key);
        if (!(raw instanceof List)) {
            return result;
        }
        for (Object item : (List<?>) raw) {
            if (item != null && !item.toString().isBlank()) {
                result.add(item.toString());
            }
        }
        return result;
    }

    private String getString(Map<String, Object> map, String key) {
        Object val = map.get(key);
        return val != null ? val.toString() : "";
    }

    private int getInt(Map<String, Object> map, String key) {
        Object val = map.get(key);
        if (val instanceof Number) {
            return ((Number) val).intValue();
        }
        return 0;
    }

    private boolean getBool(Map<String, Object> map, String key) {
        Object val = map.get(key);
        return val instanceof Boolean && (Boolean) val;
    }
}
