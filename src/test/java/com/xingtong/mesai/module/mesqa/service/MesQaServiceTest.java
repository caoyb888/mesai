package com.xingtong.mesai.module.mesqa.service;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.module.demo.vo.ContextDocVO;
import com.xingtong.mesai.module.mesqa.dto.MesQaRequest;
import com.xingtong.mesai.module.mesqa.vo.MesQaVO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.HttpEntity;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

/**
 * MesQaService 单元测试
 *
 * <p>使用 Mockito 模拟 RestTemplate，覆盖：网关正常响应的字段映射、context_docs 解析、
 * kind 回退、topN 下发与省略、网关空响应/异常转 BizException 等核心与边界场景。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @module MES数据问答
 * @related REQ-MES-AI-20260716-001
 */
@ExtendWith(MockitoExtension.class)
class MesQaServiceTest {

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private MesQaService mesQaService;

    @BeforeEach
    void setUp() {
        // 注入 @Value 字段并触发 @PostConstruct 初始化，拼出网关 URL
        ReflectionTestUtils.setField(mesQaService, "aiGatewayBaseUrl", "http://localhost:8000");
        ReflectionTestUtils.invokeMethod(mesQaService, "init");
    }

    /** 构造一份典型的网关响应 Map */
    private Map<String, Object> mockGatewayResp() {
        Map<String, Object> doc = new LinkedHashMap<>();
        doc.put("source", "SHR_HCOIL_ROLLING_RSLT");
        doc.put("doc_type", "table");
        doc.put("content_preview", "热轧钢卷轧制实绩表，主键 COIL_NO");
        doc.put("relevance_score", 0.83);

        List<Map<String, Object>> docs = new ArrayList<>();
        docs.add(doc);

        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("question", "热轧钢卷的轧制实绩数据保存在哪张表？");
        resp.put("kind", "table");
        resp.put("answer", "保存在 SHR_HCOIL_ROLLING_RSLT 表，主键为 COIL_NO。");
        resp.put("context_docs", docs);
        resp.put("provider", "kimi");
        resp.put("model", "moonshot-v1-32k");
        resp.put("tokens_used", 1709);
        resp.put("response_time_ms", 4200);
        return resp;
    }

    @Test
    void ask_正常响应_字段完整映射并解析上下文() {
        when(restTemplate.postForObject(eq("http://localhost:8000/v1/ai/mes-qa"), any(), eq(Map.class)))
                .thenReturn(mockGatewayResp());

        MesQaRequest req = new MesQaRequest();
        req.setQuestion("热轧钢卷的轧制实绩数据保存在哪张表？");
        req.setKind("table");

        MesQaVO vo = mesQaService.ask(req);

        assertThat(vo.getQuestion()).isEqualTo("热轧钢卷的轧制实绩数据保存在哪张表？");
        assertThat(vo.getKind()).isEqualTo("table");
        assertThat(vo.getAnswer()).contains("SHR_HCOIL_ROLLING_RSLT");
        assertThat(vo.getProvider()).isEqualTo("kimi");
        assertThat(vo.getModel()).isEqualTo("moonshot-v1-32k");
        assertThat(vo.getTokensUsed()).isEqualTo(1709);
        assertThat(vo.getAiResponseTimeMs()).isEqualTo(4200);

        assertThat(vo.getContextDocs()).hasSize(1);
        ContextDocVO doc = vo.getContextDocs().get(0);
        assertThat(doc.getSource()).isEqualTo("SHR_HCOIL_ROLLING_RSLT");
        assertThat(doc.getDocType()).isEqualTo("table");
        assertThat(doc.getRelevanceScore()).isEqualTo(0.83);
    }

    @Test
    void ask_响应缺少kind时回退到请求kind() {
        Map<String, Object> resp = mockGatewayResp();
        resp.remove("kind");
        when(restTemplate.postForObject(any(String.class), any(), eq(Map.class))).thenReturn(resp);

        MesQaRequest req = new MesQaRequest();
        req.setQuestion("质保书是通过哪些存储过程签发的？");
        req.setKind("proc");

        MesQaVO vo = mesQaService.ask(req);

        assertThat(vo.getKind()).isEqualTo("proc");
    }

    @Test
    @SuppressWarnings("unchecked")
    void ask_topN非空时下发top_n_为空时不下发() {
        when(restTemplate.postForObject(any(String.class), any(), eq(Map.class))).thenReturn(mockGatewayResp());
        ArgumentCaptor<HttpEntity> captor = ArgumentCaptor.forClass(HttpEntity.class);

        // 传 topN
        MesQaRequest reqWith = new MesQaRequest();
        reqWith.setQuestion("板坯是按炉次管理的吗？");
        reqWith.setKind("auto");
        reqWith.setTopN(5);
        mesQaService.ask(reqWith);

        // 不传 topN
        MesQaRequest reqWithout = new MesQaRequest();
        reqWithout.setQuestion("板坯是按炉次管理的吗？");
        reqWithout.setKind("auto");
        mesQaService.ask(reqWithout);

        verify(restTemplate, times(2))
                .postForObject(any(String.class), captor.capture(), eq(Map.class));

        Map<String, Object> bodyWith = (Map<String, Object>) captor.getAllValues().get(0).getBody();
        Map<String, Object> bodyWithout = (Map<String, Object>) captor.getAllValues().get(1).getBody();
        assertThat(bodyWith).containsEntry("top_n", 5);
        assertThat(bodyWithout).doesNotContainKey("top_n");
    }

    @Test
    void ask_网关返回空_抛BizException() {
        when(restTemplate.postForObject(any(String.class), any(), eq(Map.class))).thenReturn(null);

        MesQaRequest req = new MesQaRequest();
        req.setQuestion("热轧钢卷的实绩表是哪张？");
        req.setKind("table");

        assertThatThrownBy(() -> mesQaService.ask(req))
                .isInstanceOf(BizException.class)
                .hasMessageContaining("空响应");
    }

    @Test
    void ask_网关调用异常_包装为BizException() {
        when(restTemplate.postForObject(any(String.class), any(), eq(Map.class)))
                .thenThrow(new RestClientException("connection refused"));

        MesQaRequest req = new MesQaRequest();
        req.setQuestion("热轧钢卷的实绩表是哪张？");
        req.setKind("table");

        assertThatThrownBy(() -> mesQaService.ask(req))
                .isInstanceOf(BizException.class)
                .hasMessageContaining("AI 网关调用失败");
    }
}
