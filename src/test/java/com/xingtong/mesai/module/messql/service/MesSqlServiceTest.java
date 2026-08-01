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
    @SuppressWarnings("unchecked")
    void query_temperature透传与省略() {
        String sql = "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        // 显式传 0（评测场景）：应透传给网关
        MesSqlRequest withTemp = req(false);
        withTemp.setTemperature(0.0);
        mesSqlService.query(withTemp);
        ArgumentCaptor<Object> bodyCaptor = ArgumentCaptor.forClass(Object.class);
        org.mockito.Mockito.verify(restTemplate).postForObject(anyString(), bodyCaptor.capture(), eq(Map.class));
        Map<String, Object> sentBody = (Map<String, Object>) ((org.springframework.http.HttpEntity<?>) bodyCaptor.getValue()).getBody();
        assertThat(sentBody).containsEntry("temperature", 0.0);

        // 不传：请求体中不应携带 temperature 字段（由网关用默认值）
        org.mockito.Mockito.clearInvocations(restTemplate);
        mesSqlService.query(req(false));
        org.mockito.Mockito.verify(restTemplate).postForObject(anyString(), bodyCaptor.capture(), eq(Map.class));
        Map<String, Object> sentBody2 = (Map<String, Object>) ((org.springframework.http.HttpEntity<?>) bodyCaptor.getValue()).getBody();
        assertThat(sentBody2).doesNotContainKey("temperature");
        assertThat(sentBody2).doesNotContainKey("caller");
    }

    @Test
    @SuppressWarnings("unchecked")
    void query_caller透传_评测流量分账标识() {
        String sql = "SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT";
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(mockResp(true, sql));

        MesSqlRequest evalReq = req(false);
        evalReq.setCaller("eval");
        mesSqlService.query(evalReq);

        ArgumentCaptor<Object> bodyCaptor = ArgumentCaptor.forClass(Object.class);
        org.mockito.Mockito.verify(restTemplate).postForObject(anyString(), bodyCaptor.capture(), eq(Map.class));
        Map<String, Object> sentBody = (Map<String, Object>) ((org.springframework.http.HttpEntity<?>) bodyCaptor.getValue()).getBody();
        assertThat(sentBody).containsEntry("caller", "eval");
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
        // schema 校验的元数据查询（all_tab_columns，带参数重载）：表与字段均存在
        when(jdbc.queryForList(org.mockito.ArgumentMatchers.contains("all_tab_columns"),
                org.mockito.ArgumentMatchers.<Object>any())).thenReturn(buildMetaRows("SHR_HCOIL_ROLLING_RSLT", "COIL_NO", "HEAT_NO"));
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
    void query_引用不存在字段_被schema校验拦截_BLOCKED() {
        // 近义臆造场景：真实列为 PROD_TOT_JDG_DTM，模型生成了 PROD_JDG_DTM
        String sql = "SELECT PROD_NO, PROD_JDG_DTM FROM SQM_TOT_JDG_RSLT";
        Map<String, Object> resp = mockResp(true, sql);
        resp.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        resp.put("referenced_columns", new ArrayList<>(Arrays.asList("PROD_NO", "PROD_JDG_DTM")));
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(resp);

        JdbcTemplate jdbc = org.mockito.Mockito.mock(JdbcTemplate.class);
        // 元数据中只有真实列 PROD_TOT_JDG_DTM，没有臆造的 PROD_JDG_DTM
        when(jdbc.queryForList(org.mockito.ArgumentMatchers.contains("all_tab_columns"),
                org.mockito.ArgumentMatchers.<Object>any())).thenReturn(buildMetaRows("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM"));
        ReflectionTestUtils.setField(mesSqlService, "mesJdbcTemplate", jdbc);

        MesSqlVO vo = mesSqlService.query(req(true));

        SqlExecutionResult exec = vo.getExecutionResult();
        assertThat(exec.getExecType()).isEqualTo("BLOCKED");
        assertThat(exec.isSuccess()).isFalse();
        assertThat(exec.getErrorMessage()).contains("防臆造拦截").contains("PROD_JDG_DTM");
        // 被拦截时不得触碰业务 SQL 执行（单参 queryForList 零调用）
        org.mockito.Mockito.verify(jdbc, org.mockito.Mockito.never()).queryForList(anyString());
    }

    /** 构造 all_tab_columns 元数据行（TABLE_NAME/COLUMN_NAME 为大写列标签，与 Oracle 一致）*/
    private List<Map<String, Object>> buildMetaRows(String table, String... columns) {
        List<Map<String, Object>> meta = new ArrayList<>();
        for (String c : columns) {
            Map<String, Object> r = new LinkedHashMap<>();
            r.put("TABLE_NAME", table);
            r.put("COLUMN_NAME", c);
            r.put("DATA_TYPE", "VARCHAR2");
            r.put("DATA_LENGTH", 20);
            meta.add(r);
        }
        return meta;
    }

    // ── 自纠错重试循环（REQ-MES-AI-20260730-002 B2.1/F3/F4）──────────

    /** 开启重试并注入只读数据源（元数据含真实列）*/
    private JdbcTemplate setupRetryEnv(String table, String... realColumns) {
        JdbcTemplate jdbc = org.mockito.Mockito.mock(JdbcTemplate.class);
        org.mockito.Mockito.lenient().when(jdbc.queryForList(
                org.mockito.ArgumentMatchers.contains("all_tab_columns"),
                org.mockito.ArgumentMatchers.<Object>any()))
                .thenReturn(buildMetaRows(table, realColumns));
        ReflectionTestUtils.setField(mesSqlService, "mesJdbcTemplate", jdbc);
        ReflectionTestUtils.setField(mesSqlService, "retryEnabled", true);
        ReflectionTestUtils.setField(mesSqlService, "retryMaxRounds", 3);
        ReflectionTestUtils.setField(mesSqlService, "retryTimeoutMs", 60000L);
        ReflectionTestUtils.setField(mesSqlService, "feedbackColsPerTable", 40);
        return jdbc;
    }

    @Test
    void query_首轮schema拦截_重试第2轮成功_RETRY成功收敛() {
        // 首轮：臆造列 PROD_JDG_DTM → schema 拦截；次轮：修正为真实列 → 执行成功
        Map<String, Object> bad = mockResp(true, "SELECT PROD_NO, PROD_JDG_DTM FROM SQM_TOT_JDG_RSLT");
        bad.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        bad.put("referenced_columns", new ArrayList<>(Arrays.asList("PROD_NO", "PROD_JDG_DTM")));
        Map<String, Object> good = mockResp(true, "SELECT PROD_NO, PROD_TOT_JDG_DTM FROM SQM_TOT_JDG_RSLT");
        good.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        good.put("referenced_columns", new ArrayList<>(Arrays.asList("PROD_NO", "PROD_TOT_JDG_DTM")));
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(bad, good);

        JdbcTemplate jdbc = setupRetryEnv("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM");
        List<Map<String, Object>> rows = new ArrayList<>();
        rows.add(new LinkedHashMap<>(Map.of("PROD_NO", "P1")));
        when(jdbc.queryForList(anyString())).thenReturn(rows);

        MesSqlVO vo = mesSqlService.query(req(true));

        assertThat(vo.getRetryCount()).isEqualTo(1);
        assertThat(vo.getSql()).contains("PROD_TOT_JDG_DTM");
        assertThat(vo.getExecutionResult().getExecType()).isEqualTo("SELECT");
        assertThat(vo.getExecutionResult().isSuccess()).isTrue();

        // 第 2 次网关调用必须携带 retry_feedback（失败 SQL + 真实列清单）
        ArgumentCaptor<Object> bodyCaptor = ArgumentCaptor.forClass(Object.class);
        org.mockito.Mockito.verify(restTemplate, org.mockito.Mockito.times(2))
                .postForObject(anyString(), bodyCaptor.capture(), eq(Map.class));
        Map<String, Object> retryBody = (Map<String, Object>)
                ((org.springframework.http.HttpEntity<?>) bodyCaptor.getAllValues().get(1)).getBody();
        Map<String, Object> feedback = (Map<String, Object>) retryBody.get("retry_feedback");
        assertThat(feedback).isNotNull();
        assertThat(feedback.get("failed_sql").toString()).contains("PROD_JDG_DTM");
        assertThat(feedback.get("error_message").toString()).contains("防臆造拦截");
        assertThat(feedback.get("real_schema").toString()).contains("PROD_TOT_JDG_DTM");
    }

    @Test
    void query_重试耗尽_返回未生成且不返回未通过SQL() {
        // 连续生成不同的臆造列（避免提前终止），3 轮全部失败
        Map<String, Object> bad1 = mockResp(true, "SELECT BAD_COL_A FROM SQM_TOT_JDG_RSLT");
        bad1.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        bad1.put("referenced_columns", new ArrayList<>(Arrays.asList("BAD_COL_A")));
        Map<String, Object> bad2 = mockResp(true, "SELECT BAD_COL_B FROM SQM_TOT_JDG_RSLT");
        bad2.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        bad2.put("referenced_columns", new ArrayList<>(Arrays.asList("BAD_COL_B")));
        Map<String, Object> bad3 = mockResp(true, "SELECT BAD_COL_C FROM SQM_TOT_JDG_RSLT");
        bad3.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        bad3.put("referenced_columns", new ArrayList<>(Arrays.asList("BAD_COL_C")));
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class)))
                .thenReturn(bad1, bad2, bad3);

        setupRetryEnv("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM");

        MesSqlVO vo = mesSqlService.query(req(true));

        // F3.3：耗尽后不返回未通过校验的 SQL
        assertThat(vo.isGenerated()).isFalse();
        assertThat(vo.getSql()).isEmpty();
        assertThat(vo.getUnanswerableReason()).contains("自纠错");
        assertThat(vo.getRetryCount()).isEqualTo(2);
        org.mockito.Mockito.verify(restTemplate, org.mockito.Mockito.times(3))
                .postForObject(anyString(), any(), eq(Map.class));
    }

    @Test
    void query_连续两轮同一错误_提前终止() {
        // 两轮均 ORA-00904 "SPEC_CD"（referenced 元数据只声明真实列，schema 校验放行，
        // 执行期才报错）→ 第 2 轮同错误即终止，不打满 3 轮
        Map<String, Object> bad = mockResp(true, "SELECT COIL_NO, SPEC_CD FROM SHR_HCOIL_ROLLING_RSLT");
        bad.put("referenced_columns", new ArrayList<>(Arrays.asList("COIL_NO")));
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(bad);

        JdbcTemplate jdbc = setupRetryEnv("SHR_HCOIL_ROLLING_RSLT", "COIL_NO", "RLG_THK");
        when(jdbc.queryForList(anyString())).thenThrow(
                new org.springframework.jdbc.BadSqlGrammarException("test", "sql",
                        new java.sql.SQLSyntaxErrorException("ORA-00904: \"SPEC_CD\": invalid identifier")));

        MesSqlVO vo = mesSqlService.query(req(true));

        assertThat(vo.isGenerated()).isFalse();
        assertThat(vo.getRetryCount()).isEqualTo(1);   // 仅重试 1 次即提前终止
        org.mockito.Mockito.verify(restTemplate, org.mockito.Mockito.times(2))
                .postForObject(anyString(), any(), eq(Map.class));
    }

    @Test
    void query_retryDisabled_不重试() {
        Map<String, Object> bad = mockResp(true, "SELECT PROD_JDG_DTM FROM SQM_TOT_JDG_RSLT");
        bad.put("referenced_tables", new ArrayList<>(Arrays.asList("SQM_TOT_JDG_RSLT")));
        bad.put("referenced_columns", new ArrayList<>(Arrays.asList("PROD_JDG_DTM")));
        when(restTemplate.postForObject(anyString(), any(), eq(Map.class))).thenReturn(bad);

        setupRetryEnv("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM");
        ReflectionTestUtils.setField(mesSqlService, "retryEnabled", false);

        MesSqlVO vo = mesSqlService.query(req(true));

        assertThat(vo.getExecutionResult().getExecType()).isEqualTo("BLOCKED");
        assertThat(vo.getRetryCount()).isEqualTo(0);
        org.mockito.Mockito.verify(restTemplate, org.mockito.Mockito.times(1))
                .postForObject(anyString(), any(), eq(Map.class));
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
