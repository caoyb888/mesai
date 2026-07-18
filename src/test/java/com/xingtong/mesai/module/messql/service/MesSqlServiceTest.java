package com.xingtong.mesai.module.messql.service;

import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.module.demo.vo.SqlExecutionResult;
import com.xingtong.mesai.module.messql.dto.MesSqlRequest;
import com.xingtong.mesai.module.messql.vo.MesSqlVO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestTemplate;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

/**
 * MesSqlService 单元测试
 *
 * <p>使用 Mockito 模拟 RestTemplate 与只读 JdbcTemplate，覆盖：网关字段映射、
 * 安全校验拦截（SELECT *）、只读数据源未配置降级、未生成跳过、executeSql=false 不执行、
 * 数据源已配置时执行 SELECT 并 Oracle 行数封顶、网关空响应转 BizException。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001
 */
@ExtendWith(MockitoExtension.class)
class MesSqlServiceTest {

    @Mock
    private RestTemplate restTemplate;

    @InjectMocks
    private MesSqlService mesSqlService;

    @BeforeEach
    void setUp() {
        ReflectionTestUtils.setField(mesSqlService, "aiGatewayBaseUrl", "http://localhost:8000");
        ReflectionTestUtils.invokeMethod(mesSqlService, "init");
    }

    /** 构造网关响应 Map */
    private Map<String, Object> mockResp(boolean generated, String sql) {
        Map<String, Object> resp = new LinkedHashMap<>();
        resp.put("question", "查询最近一个月热轧钢卷的轧制实绩");
        resp.put("generated", generated);
        resp.put("sql", sql);
        resp.put("explanation", "查询近30天轧制实绩");
        resp.put("referenced_tables", new ArrayList<>(Arrays.asList("SHR_HCOIL_ROLLING_RSLT")));
        resp.put("referenced_columns", new ArrayList<>(Arrays.asList("COIL_NO", "HEAT_NO")));
        resp.put("unanswerable_reason", null);
        resp.put("context_docs", new ArrayList<>());
        resp.put("provider", "kimi");
        resp.put("model", "moonshot-v1-32k");
        resp.put("tokens_used", 640);
        resp.put("response_time_ms", 3100);
        return resp;
    }

    private MesSqlRequest req(boolean executeSql) {
        MesSqlRequest r = new MesSqlRequest();
        r.setQuestion("查询最近一个月热轧钢卷的轧制实绩");
        r.setExecuteSql(executeSql);
        return r;
    }

    @Test
    void query_正常生成_字段完整映射() {
        String sql = "SELECT COIL_NO, HEAT_NO FROM SHR_HCOIL_ROLLING_RSLT FETCH FIRST 200 ROWS ONLY";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        MesSqlVO vo = mesSqlService.query(req(true));

        assertThat(vo.isGenerated()).isTrue();
        assertThat(vo.getSql()).isEqualTo(sql);
        assertThat(vo.getReferencedTables()).containsExactly("SHR_HCOIL_ROLLING_RSLT");
        assertThat(vo.getReferencedColumns()).contains("COIL_NO", "HEAT_NO");
        assertThat(vo.getProvider()).isEqualTo("kimi");
        assertThat(vo.getTokensUsed()).isEqualTo(640);
        assertThat(vo.getUnanswerableReason()).isNull();
    }

    @Test
    void query_安全生成但数据源未配置_返回SKIPPED() {
        String sql = "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        MesSqlVO vo = mesSqlService.query(req(true));

        SqlExecutionResult exec = vo.getExecutionResult();
        assertThat(exec).isNotNull();
        assertThat(exec.getExecType()).isEqualTo("SKIPPED");
        assertThat(exec.isSuccess()).isFalse();
        assertThat(exec.getErrorMessage()).contains("未配置");
    }

    @Test
    void query_生成SELECT星号_被安全校验拦截_BLOCKED() {
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class)))
                .thenReturn(mockResp(true, "SELECT * FROM SHR_HCOIL_ROLLING_RSLT"));

        MesSqlVO vo = mesSqlService.query(req(true));

        SqlExecutionResult exec = vo.getExecutionResult();
        assertThat(exec.getExecType()).isEqualTo("BLOCKED");
        assertThat(exec.getErrorMessage()).contains("SELECT *");
    }

    @Test
    void query_未生成SQL_跳过执行_SKIPPED() {
        Map<String, Object> resp = mockResp(false, "");
        resp.put("unanswerable_reason", "知识库中未检索到设备能耗相关的表");
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(resp);

        MesSqlVO vo = mesSqlService.query(req(true));

        assertThat(vo.isGenerated()).isFalse();
        assertThat(vo.getUnanswerableReason()).contains("能耗");
        assertThat(vo.getExecutionResult().getExecType()).isEqualTo("SKIPPED");
        assertThat(vo.getExecutionResult().getErrorMessage()).contains("未生成有效 SQL");
    }

    @Test
    void query_executeSql为false_不执行() {
        String sql = "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        MesSqlVO vo = mesSqlService.query(req(false));

        assertThat(vo.getSql()).isEqualTo(sql);
        assertThat(vo.getExecutionResult()).isNull();
    }

    @Test
    void query_数据源已配置_执行SELECT并Oracle行数封顶() {
        String sql = "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        // 注入只读 JdbcTemplate mock
        JdbcTemplate jdbc = org.mockito.Mockito.mock(JdbcTemplate.class);
        List<Map<String, Object>> rows = new ArrayList<>();
        Map<String, Object> row = new LinkedHashMap<>();
        row.put("COIL_NO", "HC202607010001");
        rows.add(row);
        when(jdbc.queryForList(anyString())).thenReturn(rows);
        ReflectionTestUtils.setField(mesSqlService, "mesJdbcTemplate", jdbc);

        MesSqlVO vo = mesSqlService.query(req(true));

        SqlExecutionResult exec = vo.getExecutionResult();
        assertThat(exec.getExecType()).isEqualTo("SELECT");
        assertThat(exec.isSuccess()).isTrue();
        assertThat(exec.getTotalRows()).isEqualTo(1);

        // 校验实际下发的 SQL 已用 ROWNUM 封顶
        ArgumentCaptor<String> sqlCaptor = ArgumentCaptor.forClass(String.class);
        org.mockito.Mockito.verify(jdbc).queryForList(sqlCaptor.capture());
        assertThat(sqlCaptor.getValue()).contains("ROWNUM").contains(sql);
    }

    @Test
    void query_网关空响应_抛BizException() {
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(null);

        assertThatThrownBy(() -> mesSqlService.query(req(true)))
                .isInstanceOf(BizException.class)
                .hasMessageContaining("空响应");
    }

    @Test
    void oracleRowCap_用ROWNUM包裹子查询() {
        String capped = MesSqlService.oracleRowCap("SELECT COIL_NO FROM T", 200);
        assertThat(capped).isEqualTo("SELECT * FROM (SELECT COIL_NO FROM T) WHERE ROWNUM <= 200");
    }
}
