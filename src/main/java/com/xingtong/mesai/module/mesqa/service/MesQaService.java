package com.xingtong.mesai.module.mesqa.service;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.mesqa.dto.MesQaRequest;
import com.xingtong.mesai.module.mesqa.vo.MesQaVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * MES 数据问答服务
 *
 * <p>职责：将前端问答请求转发至 AI 网关 /v1/ai/mes-qa（网关侧完成 RAG 检索 +
 * 复用统一链路：PII 脱敏门 → Token 预算闸 → LLM Provider → 用量计入），
 * 再把网关返回的裸 JSON 组装为统一封装的 {@link MesQaVO}。
 *
 * <p>不涉及任何数据库读写：mes-qa 是纯知识库问答，接地约束在网关侧的系统 Prompt 内完成。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @module MES数据问答
 * @related REQ-MES-AI-20260716-001（真实 MES 库理解与问答）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class MesQaService {

    /** AI 网关基地址（不硬编码，由配置注入）*/
    @Value("${ai.gateway.base-url:http://localhost:8000}")
    private String aiGatewayBaseUrl;

    private String mesQaUrl;

    private final RestTemplate restTemplate;

    @PostConstruct
    void init() {
        mesQaUrl = aiGatewayBaseUrl + "/v1/ai/mes-qa";
        log.info("MES 问答服务初始化：AI 网关地址={}", mesQaUrl);
    }

    /**
     * 处理 MES 数据问答请求
     *
     * @param req 前端请求（问题 + 检索范围 + 可选 topN）
     * @return 组装后的问答结果 VO
     */
    public MesQaVO ask(MesQaRequest req) {
        Map<String, Object> gatewayResp = callAiGateway(req);

        MesQaVO vo = new MesQaVO();
        vo.setQuestion(req.getQuestion());
        // kind 以网关实际生效值为准（网关会做归一），缺省回退到请求值
        String respKind = getString(gatewayResp, "kind");
        vo.setKind(respKind.isEmpty() ? req.getKind() : respKind);
        vo.setAnswer(getString(gatewayResp, "answer"));
        vo.setProvider(getString(gatewayResp, "provider"));
        vo.setModel(getString(gatewayResp, "model"));
        vo.setTokensUsed(getInt(gatewayResp, "tokens_used"));
        vo.setAiResponseTimeMs(getInt(gatewayResp, "response_time_ms"));
        vo.setContextDocs(parseContextDocs(gatewayResp));

        return vo;
    }

    // ── 私有方法 ──────────────────────────────────────────────────

    /**
     * 调用 AI 网关 /v1/ai/mes-qa 端点
     */
    @SuppressWarnings("unchecked")
    private Map<String, Object> callAiGateway(MesQaRequest req) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("question", req.getQuestion());
        body.put("kind", req.getKind());
        // topN 为空时不下发，交由网关按配置默认值处理
        if (req.getTopN() != null) {
            body.put("top_n", req.getTopN());
        }

        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);

        try {
            Map<String, Object> response = restTemplate.postForObject(mesQaUrl, entity, Map.class);
            if (response == null) {
                throw BizException.of(ResultCode.AI_GATEWAY_ERROR, "AI 网关返回空响应");
            }
            return response;
        } catch (BizException e) {
            throw e;
        } catch (Exception e) {
            log.error("调用 AI 网关失败 url={} err={}", mesQaUrl, e.getMessage(), e);
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
}
