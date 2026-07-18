package com.xingtong.mesai.module.messql.util;

import com.xingtong.mesai.module.messql.util.SqlSafetyValidator.SqlSafetyResult;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * SqlSafetyValidator 单元测试
 *
 * <p>覆盖安全红线：仅 SELECT/WITH 只读、禁多语句、禁注释、禁写操作/DDL、禁 FOR UPDATE、
 * 禁 SELECT *，以及归一化（去末尾分号）与常见误报规避（COUNT(*)、*_DATE 列名）。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001
 */
class SqlSafetyValidatorTest {

    @Test
    void validate_合法SELECT_通过并归一化去末尾分号() {
        SqlSafetyResult r = SqlSafetyValidator.validate("  SELECT COIL_NO, HEAT_NO FROM SHR_HCOIL_ROLLING_RSLT ; ");
        assertThat(r.isPassed()).isTrue();
        assertThat(r.getNormalizedSql()).isEqualTo("SELECT COIL_NO, HEAT_NO FROM SHR_HCOIL_ROLLING_RSLT");
        assertThat(r.getReason()).isNull();
    }

    @Test
    void validate_WITH_CTE查询_通过() {
        SqlSafetyResult r = SqlSafetyValidator.validate(
                "WITH t AS (SELECT COIL_NO FROM SHR_HCOIL_ROLLING_RSLT) SELECT COIL_NO FROM t");
        assertThat(r.isPassed()).isTrue();
    }

    @Test
    void validate_小写select_大小写不敏感通过() {
        SqlSafetyResult r = SqlSafetyValidator.validate("select coil_no from shr_hcoil_rolling_rslt");
        assertThat(r.isPassed()).isTrue();
    }

    @Test
    void validate_COUNT星号_不误判为SELECT星号() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COUNT(*) FROM SHR_HCOIL_ROLLING_RSLT");
        assertThat(r.isPassed()).isTrue();
    }

    @Test
    void validate_列名含CREATE_DATE_不误判为DDL() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT CREATE_DATE, UPDATE_TIME FROM SHR_HCOIL_MASTER");
        assertThat(r.isPassed()).isTrue();
    }

    @Test
    void validate_空SQL_拦截() {
        assertThat(SqlSafetyValidator.validate(null).isPassed()).isFalse();
        assertThat(SqlSafetyValidator.validate("   ").isPassed()).isFalse();
    }

    @Test
    void validate_多语句_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO FROM T; DROP TABLE T");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("多语句");
    }

    @Test
    void validate_行注释_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO FROM T -- 注释藏 payload");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("注释");
    }

    @Test
    void validate_块注释_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO /* x */ FROM T");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("注释");
    }

    @Test
    void validate_非SELECT开头_拦截() {
        assertThat(SqlSafetyValidator.validate("UPDATE T SET A=1 WHERE ID=1").isPassed()).isFalse();
        assertThat(SqlSafetyValidator.validate("DELETE FROM T WHERE ID=1").isPassed()).isFalse();
        assertThat(SqlSafetyValidator.validate("DROP TABLE T").isPassed()).isFalse();
        assertThat(SqlSafetyValidator.validate("INSERT INTO T VALUES(1)").isPassed()).isFalse();
    }

    @Test
    void validate_SELECT中夹带写操作关键字_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO FROM T WHERE ID IN (DELETE FROM X)");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("写操作或 DDL");
    }

    @Test
    void validate_SELECT_INTO_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO INTO V_COIL FROM T");
        assertThat(r.isPassed()).isFalse();
    }

    @Test
    void validate_FOR_UPDATE加锁读_拦截() {
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT COIL_NO FROM T FOR UPDATE");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("FOR UPDATE");
    }

    @Test
    void validate_SELECT星号_拦截() {
        assertThat(SqlSafetyValidator.validate("SELECT * FROM T").isPassed()).isFalse();
        assertThat(SqlSafetyValidator.validate("SELECT t.* FROM T t").isPassed()).isFalse();
        SqlSafetyResult r = SqlSafetyValidator.validate("SELECT DISTINCT * FROM T");
        assertThat(r.isPassed()).isFalse();
        assertThat(r.getReason()).contains("SELECT *");
    }
}
