package com.xingtong.mesai.module.messql.service;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.demo.vo.SqlExecutionResult;
import com.xingtong.mesai.module.messql.dto.MesSqlRequest;
import com.xingtong.mesai.module.messql.util.SqlSafetyValidator;
import com.xingtong.mesai.module.messql.util.SqlSafetyValidator.SqlSafetyResult;
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
        Map<String, Object> gatewayResp = callAiGateway(req);

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
            vo.setExecutionResult(runIfSafe(vo.isGenerated(), vo.getSql()));
        }

        return vo;
    }

    // ── 私有方法 ──────────────────────────────────────────────────

    /**
     * 生成成功则校验并执行；各前置条件不满足时返回 SKIPPED/BLOCKED 结果。
     */
    private SqlExecutionResult runIfSafe(boolean generated, String sql) {
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

        // 3. 只读执行（Oracle 行数封顶）
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
     */
    @SuppressWarnings("unchecked")
    private Map<String, Object> callAiGateway(MesSqlRequest req) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("question", req.getQuestion());
        if (req.getTopN() != null) {
            body.put("top_n", req.getTopN());
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
