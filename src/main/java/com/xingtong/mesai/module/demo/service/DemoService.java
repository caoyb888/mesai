package com.xingtong.mesai.module.demo.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.demo.dto.DemoQueryRequest;
import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.demo.vo.DemoQueryVO;
import com.xingtong.mesai.module.demo.vo.SqlExecutionResult;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.lang.Nullable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.TransactionStatus;
import org.springframework.transaction.support.TransactionCallback;
import org.springframework.transaction.support.TransactionTemplate;
import org.springframework.web.client.RestTemplate;

import javax.annotation.PostConstruct;
import java.util.*;
import java.util.regex.Pattern;

/**
 * 演示服务
 *
 * <p>职责：
 * 1. 调用 AI 网关 /v1/ai/itsm-demo（RAG + 代码生成）
 * 2. 对生成的 SQL 做安全校验
 * 3. 在 ITSM 测试数据库上执行 SQL，SELECT 直接返回结果集，
 *    DML 在事务内执行后回滚（展示影响行数，不修改真实数据）
 * 4. 组装并返回 DemoQueryVO
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class DemoService {

    /** AI 网关演示端点 URL */
    @Value("${ai.gateway.base-url:http://localhost:8000}")
    private String aiGatewayBaseUrl;

    private String itsmDemoUrl;

    /** ITSM 测试数据源 JdbcTemplate（可能为 null，未配置时不注入）*/
    @Qualifier("itsmJdbcTemplate")
    @Nullable
    private final JdbcTemplate itsmJdbcTemplate;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    /** SELECT 查询结果最大行数（防止结果集过大导致内存溢出）*/
    private static final int MAX_RESULT_ROWS = 200;

    /** 禁止执行的 DDL 关键字（安全红线：不允许变更 ITSM 测试库表结构）*/
    private static final Pattern DDL_PATTERN = Pattern.compile(
            "(?i)\\b(DROP|CREATE|ALTER|TRUNCATE|RENAME|COMMENT ON)\\b"
    );

    /** 禁止的危险操作（无条件全表删除/更新检测）*/
    private static final Pattern DANGEROUS_DML_PATTERN = Pattern.compile(
            "(?i)\\b(DELETE|UPDATE)\\s+\\S+\\s*(?!WHERE)(?:;|$)"
    );

    @PostConstruct
    void init() {
        itsmDemoUrl = aiGatewayBaseUrl + "/v1/ai/itsm-demo";
        log.info("演示服务初始化：AI 网关地址={}", itsmDemoUrl);
        if (itsmJdbcTemplate == null) {
            log.warn("ITSM 测试数据源未配置（ITSM_DB_URL 为空），SQL 执行功能不可用");
        }
    }

    /**
     * 处理演示查询请求
     *
     * @param req 前端请求
     * @return 包含生成代码 + 执行结果的 VO
     */
    public DemoQueryVO query(DemoQueryRequest req) {
        // 1. 调用 AI 网关生成代码
        Map<String, Object> gatewayResp = callAiGateway(req.getQuestion(), req.getMode());

        // 2. 组装基础 VO
        DemoQueryVO vo = new DemoQueryVO();
        vo.setMode(req.getMode());
        vo.setQuestion(req.getQuestion());
        vo.setGeneratedCode(getString(gatewayResp, "generated_code"));
        vo.setExplanation(getString(gatewayResp, "explanation"));
        vo.setTokensUsed(getInt(gatewayResp, "tokens_used"));
        vo.setAiResponseTimeMs(getInt(gatewayResp, "response_time_ms"));

        // 3. 解析 context_docs
        List<ContextDocVO> ctxDocs = parseContextDocs(gatewayResp);
        vo.setContextDocs(ctxDocs);

        // 4. 如果需要执行 SQL
        if (req.isExecuteSql() && !"fe_component".equals(req.getMode())) {
            SqlExecutionResult execResult = executeSql(vo.getGeneratedCode(), req.getMode());
            vo.setExecutionResult(execResult);
        }

        return vo;
    }

    // ── 私有方法 ──────────────────────────────────────────────────

    /**
     * 调用 AI 网关 /v1/ai/itsm-demo 端点
     */
    @SuppressWarnings("unchecked")
    private Map<String, Object> callAiGateway(String question, String mode) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("question", question);
        body.put("mode", mode);

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

        try {
            Map<String, Object> response = restTemplate.postForObject(
                    itsmDemoUrl, entity, Map.class
            );
            if (response == null) {
                throw BizException.of(ResultCode.AI_GATEWAY_ERROR, "AI 网关返回空响应");
            }
            return response;
        } catch (BizException e) {
            throw e;
        } catch (Exception e) {
            log.error("调用 AI 网关失败 url={} err={}", itsmDemoUrl, e.getMessage(), e);
            throw BizException.of(ResultCode.AI_GATEWAY_ERROR, "AI 网关调用失败：" + e.getMessage());
        }
    }

    /**
     * 在 ITSM 测试库上执行 SQL
     *
     * <p>安全规则：
     * - 禁止 DDL（DROP/CREATE/ALTER/TRUNCATE 等）
     * - SELECT：直接执行，最多返回 MAX_RESULT_ROWS 行
     * - DML（INSERT/UPDATE/DELETE）：在事务内执行后回滚，只返回影响行数
     */
    private SqlExecutionResult executeSql(String rawSql, String mode) {
        if (itsmJdbcTemplate == null) {
            return SqlExecutionResult.builder()
                    .execType("SKIPPED")
                    .success(false)
                    .errorMessage("ITSM 测试数据源未配置，请在 .env 中填写 ITSM_DB_URL / ITSM_DB_USERNAME / ITSM_DB_PASSWORD")
                    .build();
        }

        // 提取第一条 SQL（AI 可能生成多条）
        String sql = extractFirstSql(rawSql);
        if (sql == null || sql.isBlank()) {
            return SqlExecutionResult.builder()
                    .execType("SKIPPED")
                    .success(false)
                    .errorMessage("未能从 AI 响应中解析出有效 SQL")
                    .build();
        }

        // DDL 安全校验
        if (DDL_PATTERN.matcher(sql).find()) {
            return SqlExecutionResult.builder()
                    .execType("BLOCKED")
                    .success(false)
                    .errorMessage("安全拦截：禁止执行 DDL 操作（DROP/CREATE/ALTER/TRUNCATE），ITSM 测试库表结构受保护")
                    .build();
        }

        String sqlUpper = sql.trim().toUpperCase();
        long start = System.currentTimeMillis();

        if (sqlUpper.startsWith("SELECT")) {
            return executeSelect(sql, start);
        } else {
            return executeDmlPreview(sql, start);
        }
    }

    /**
     * 执行 SELECT 查询，返回结果集
     */
    private SqlExecutionResult executeSelect(String sql, long startMs) {
        try {
            // 限制最大返回行数（防止 ITSM 大表全扫）
            String limitedSql = appendLimit(sql, MAX_RESULT_ROWS);
            List<Map<String, Object>> rows = itsmJdbcTemplate.queryForList(limitedSql);
            long elapsed = System.currentTimeMillis() - startMs;

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
            log.warn("SELECT 执行失败：{}", e.getMessage());
            return SqlExecutionResult.builder()
                    .execType("SELECT")
                    .success(false)
                    .errorMessage("SQL 执行错误：" + e.getMostSpecificCause().getMessage())
                    .elapsedMs(System.currentTimeMillis() - startMs)
                    .build();
        }
    }

    /**
     * 在事务内执行 DML，然后回滚（仅展示影响行数，不修改真实数据）
     */
    private SqlExecutionResult executeDmlPreview(String sql, long startMs) {
        try {
            // 构建 TransactionTemplate 手动控制回滚
            org.springframework.jdbc.datasource.DataSourceTransactionManager txm =
                    new org.springframework.jdbc.datasource.DataSourceTransactionManager(
                            Objects.requireNonNull(itsmJdbcTemplate.getDataSource())
                    );
            TransactionTemplate txTpl = new TransactionTemplate(txm);

            final int[] affectedRows = {0};
            final String[] errMsg = {null};

            txTpl.execute((TransactionCallback<Void>) status -> {
                try {
                    affectedRows[0] = itsmJdbcTemplate.update(sql);
                } catch (DataAccessException e) {
                    errMsg[0] = e.getMostSpecificCause().getMessage();
                    log.warn("DML 执行失败（已回滚）：{}", e.getMessage());
                } finally {
                    // 无论成功还是失败，都回滚
                    status.setRollbackOnly();
                }
                return null;
            });

            long elapsed = System.currentTimeMillis() - startMs;

            if (errMsg[0] != null) {
                return SqlExecutionResult.builder()
                        .execType("DML_PREVIEW")
                        .success(false)
                        .errorMessage("SQL 执行错误：" + errMsg[0])
                        .elapsedMs(elapsed)
                        .build();
            }

            return SqlExecutionResult.builder()
                    .execType("DML_PREVIEW")
                    .affectedRows(affectedRows[0])
                    .elapsedMs(elapsed)
                    .success(true)
                    .notice("演示模式：DML 已在事务内执行（影响 " + affectedRows[0] + " 行），事务已回滚，ITSM 数据实际未修改")
                    .build();

        } catch (Exception e) {
            log.error("DML 预览执行异常：{}", e.getMessage(), e);
            return SqlExecutionResult.builder()
                    .execType("DML_PREVIEW")
                    .success(false)
                    .errorMessage("执行异常：" + e.getMessage())
                    .elapsedMs(System.currentTimeMillis() - startMs)
                    .build();
        }
    }

    /**
     * 从 AI 生成的多段文本中提取第一条完整 SQL
     */
    private String extractFirstSql(String rawCode) {
        if (rawCode == null) return null;
        String trimmed = rawCode.strip();

        // 尝试提取 SQL 代码块（```sql ... ```）
        int sqlFence = trimmed.indexOf("```sql");
        if (sqlFence >= 0) {
            String after = trimmed.substring(sqlFence + 6);
            int end = after.indexOf("```");
            if (end > 0) return after.substring(0, end).strip();
        }

        // 直接返回第一条 SQL（按分号截取）
        int semicolonIdx = trimmed.indexOf(';');
        if (semicolonIdx > 0) {
            return trimmed.substring(0, semicolonIdx + 1).strip();
        }
        return trimmed;
    }

    /**
     * 为 SELECT SQL 追加 LIMIT 子句（防全表扫描）
     */
    private String appendLimit(String sql, int limit) {
        String upper = sql.trim().toUpperCase();
        if (upper.contains("LIMIT")) {
            return sql;
        }
        String withoutSemicolon = sql.trim().replaceAll(";\\s*$", "");
        return withoutSemicolon + " LIMIT " + limit;
    }

    /**
     * 解析 AI 网关响应中的 context_docs 列表
     */
    @SuppressWarnings("unchecked")
    private List<ContextDocVO> parseContextDocs(Map<String, Object> resp) {
        List<ContextDocVO> result = new ArrayList<>();
        Object rawDocs = resp.get("context_docs");
        if (!(rawDocs instanceof List)) return result;

        for (Object item : (List<?>) rawDocs) {
            if (!(item instanceof Map)) continue;
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

    private String getString(Map<String, Object> map, String key) {
        Object val = map.get(key);
        return val != null ? val.toString() : "";
    }

    private int getInt(Map<String, Object> map, String key) {
        Object val = map.get(key);
        if (val instanceof Number) return ((Number) val).intValue();
        return 0;
    }
}
