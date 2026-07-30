package com.xingtong.mesai.module.messql.util;

import org.junit.jupiter.api.Test;
import org.springframework.dao.DataAccessException;
import org.springframework.jdbc.core.JdbcTemplate;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * SqlSchemaValidator 单元测试
 *
 * <p>覆盖：全存在通过 / 表不存在拦截 / 字段不存在拦截 / 大小写归一 /
 * 空引用放行 / 元数据查询异常放行（不阻断主流程）。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-30
 * @module MES取数
 * @related REQ-MES-AI-20260730-001
 */
class SqlSchemaValidatorTest {

    /** 构造 all_tab_columns 查询结果行 */
    private List<Map<String, Object>> metaRows(String table, String... columns) {
        List<Map<String, Object>> rows = new ArrayList<>();
        for (String c : columns) {
            Map<String, Object> r = new LinkedHashMap<>();
            r.put("TABLE_NAME", table);
            r.put("COLUMN_NAME", c);
            rows.add(r);
        }
        return rows;
    }

    private JdbcTemplate mockJdbc(List<Map<String, Object>> metaRows) {
        JdbcTemplate jdbc = mock(JdbcTemplate.class);
        when(jdbc.queryForList(anyString(), org.mockito.ArgumentMatchers.<Object>any())).thenReturn(metaRows);
        return jdbc;
    }

    @Test
    void validate_表字段全存在_通过() {
        JdbcTemplate jdbc = mockJdbc(metaRows("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM"));

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("SQM_TOT_JDG_RSLT"), Arrays.asList("PROD_NO", "PROD_TOT_JDG_DTM"));

        assertThat(result.isPassed()).isTrue();
        assertThat(result.getMessage()).isNull();
    }

    @Test
    void validate_表不存在_拦截并给出表名() {
        JdbcTemplate jdbc = mockJdbc(Collections.emptyList());

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("NOT_EXIST_TABLE"), Collections.emptyList());

        assertThat(result.isPassed()).isFalse();
        assertThat(result.getUnknownTables()).containsExactly("NOT_EXIST_TABLE");
        assertThat(result.getMessage()).contains("防臆造拦截").contains("NOT_EXIST_TABLE");
    }

    @Test
    void validate_近义臆造字段_拦截并给出字段名() {
        // 真实列 PROD_TOT_JDG_DTM；模型臆造 PROD_JDG_DTM
        JdbcTemplate jdbc = mockJdbc(metaRows("SQM_TOT_JDG_RSLT", "PROD_NO", "PROD_TOT_JDG_DTM"));

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("SQM_TOT_JDG_RSLT"), Arrays.asList("PROD_NO", "PROD_JDG_DTM"));

        assertThat(result.isPassed()).isFalse();
        assertThat(result.getUnknownColumns()).containsExactly("PROD_JDG_DTM");
        assertThat(result.getMessage()).contains("PROD_JDG_DTM").contains("逐字一致");
    }

    @Test
    void validate_大小写混合输入_归一后通过() {
        JdbcTemplate jdbc = mockJdbc(metaRows("SQM_TOT_JDG_RSLT", "PROD_NO"));

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("sqm_tot_jdg_rslt"), Arrays.asList("prod_no"));

        assertThat(result.isPassed()).isTrue();
    }

    @Test
    void validate_字段存在于任一引用表即通过() {
        List<Map<String, Object>> meta = metaRows("T1", "C1");
        meta.addAll(metaRows("T2", "C2"));
        JdbcTemplate jdbc = mockJdbc(meta);

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("T1", "T2"), Arrays.asList("C1", "C2"));

        assertThat(result.isPassed()).isTrue();
    }

    @Test
    void validate_空引用清单_放行() {
        JdbcTemplate jdbc = mock(JdbcTemplate.class);

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Collections.emptyList(), Arrays.asList("C1"));

        assertThat(result.isPassed()).isTrue();
    }

    @Test
    void validate_元数据查询异常_放行不阻断() {
        JdbcTemplate jdbc = mock(JdbcTemplate.class);
        when(jdbc.queryForList(anyString(), org.mockito.ArgumentMatchers.<Object>any()))
                .thenThrow(new DataAccessException("字典视图不可读") {
                });

        SqlSchemaValidator.SchemaCheckResult result = SqlSchemaValidator.validate(
                jdbc, Arrays.asList("T1"), Arrays.asList("C1"));

        assertThat(result.isPassed()).isTrue();
    }
}
