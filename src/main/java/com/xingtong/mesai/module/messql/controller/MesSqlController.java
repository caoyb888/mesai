package com.xingtong.mesai.module.messql.controller;

import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.messql.dto.MesSqlRequest;
import com.xingtong.mesai.module.messql.service.MesSqlService;
import com.xingtong.mesai.module.messql.vo.MesSqlVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * MES 取数 Controller
 *
 * <p>恢复原始系统设计：AI 基于真实 MES 数据库结构知识，生成满足需求的 SELECT 查询 SQL，
 * 并在 MES 只读数据源上执行返回结果。
 *
 * <p>安全边界（CLAUDE.md §4.3）：仅对 MES 库执行只读查询，SQL 经安全校验后执行；
 * 所有接口需要 JWT 鉴权（Bearer Token），无额外权限要求（任意登录用户可用）。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-18
 * @module MES取数
 * @related REQ-MES-AI-20260716-001（NL → Oracle 只读 SELECT 生成与执行）
 */
@Slf4j
@RestController
@RequestMapping("/mes-sql")
@RequiredArgsConstructor
public class MesSqlController {

    private final MesSqlService mesSqlService;

    /**
     * MES 取数接口
     *
     * <p>请求示例：
     * <pre>{@code
     * POST /mes-sql/query
     * Authorization: Bearer <JWT_TOKEN>
     * {
     *   "question": "查询最近一个月热轧钢卷的轧制实绩，包含卷号、炉次号、轧制日期",
     *   "executeSql": true
     * }
     * }</pre>
     *
     * @param request 取数请求（需求 + 可选 topN + 是否执行）
     * @return 生成的 Oracle SELECT + 安全校验/只读执行结果
     */
    @PostMapping("/query")
    public ResultVO<MesSqlVO> query(@Validated @RequestBody MesSqlRequest request) {
        log.info("MES 取数：execute={} question={}", request.isExecuteSql(),
                request.getQuestion().length() > 50
                        ? request.getQuestion().substring(0, 50) + "..."
                        : request.getQuestion());
        MesSqlVO result = mesSqlService.query(request);
        return ResultVO.success(result);
    }
}
