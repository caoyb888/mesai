package com.xingtong.mesai.module.demo.controller;

import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.demo.dto.DemoQueryRequest;
import com.xingtong.mesai.module.demo.service.DemoService;
import com.xingtong.mesai.module.demo.vo.DemoQueryVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

/**
 * 演示接口 Controller
 *
 * <p>对外暴露 AI 代码生成演示能力：
 * - SQL 查询生成（mode=sql）并可选执行 ITSM 测试库
 * - 数据变更 SQL 生成（mode=dml）并可选在事务内预演（自动回滚）
 * - Vue 3 前端组件生成（mode=fe_component）
 *
 * <p>所有接口需要 JWT 鉴权（Bearer Token），无额外权限要求（任意登录用户可用）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 演示模块
 * @related REQ-MES-AI-20260412-005（S2.5 演示MVP）
 */
@Slf4j
@RestController
@RequestMapping("/demo")
@RequiredArgsConstructor
public class DemoController {

    private final DemoService demoService;

    /**
     * AI 代码生成演示接口
     *
     * <p>请求示例：
     * <pre>{@code
     * POST /demo/query
     * Authorization: Bearer <JWT_TOKEN>
     * {
     *   "question": "查询过去7天内所有状态为OPEN的工单，按创建时间倒序",
     *   "mode": "sql",
     *   "executeSql": true
     * }
     * }</pre>
     *
     * @param request 演示查询请求（自然语言 + 模式 + 是否执行）
     * @return AI 生成代码 + 执行结果（如有）
     */
    @PostMapping("/query")
    public ResultVO<DemoQueryVO> query(@Validated @RequestBody DemoQueryRequest request) {
        log.info("演示查询：mode={} executeSql={} question={}", request.getMode(), request.isExecuteSql(),
                request.getQuestion().length() > 50 ? request.getQuestion().substring(0, 50) + "..." : request.getQuestion());
        DemoQueryVO result = demoService.query(request);
        return ResultVO.success(result);
    }
}
