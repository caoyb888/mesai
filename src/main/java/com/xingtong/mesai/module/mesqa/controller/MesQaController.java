package com.xingtong.mesai.module.mesqa.controller;

import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.mesqa.dto.MesQaRequest;
import com.xingtong.mesai.module.mesqa.service.MesQaService;
import com.xingtong.mesai.module.mesqa.vo.MesQaVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * MES 数据问答 Controller
 *
 * <p>对外暴露面向真实 MES 库（钢板/卷材钢厂）的自然语言数据问答能力：
 * - 表结构问答（实绩表/主键/关联）
 * - 存储过程问答（业务主流程/签发链路）
 * - 混合问答（auto）
 *
 * <p>所有接口需要 JWT 鉴权（Bearer Token），无额外权限要求（任意登录用户可用）。
 * 回答严格接地于知识库检索结果，防表名/字段臆造（约束在网关侧系统 Prompt 内）。
 *
 * @author AI（芯智云匠）
 * @date 2026-07-17
 * @module MES数据问答
 * @related REQ-MES-AI-20260716-001（真实 MES 库理解与问答）
 */
@Slf4j
@RestController
@RequestMapping("/mes-qa")
@RequiredArgsConstructor
public class MesQaController {

    private final MesQaService mesQaService;

    /**
     * MES 数据问答接口
     *
     * <p>请求示例：
     * <pre>{@code
     * POST /mes-qa/ask
     * Authorization: Bearer <JWT_TOKEN>
     * {
     *   "question": "热轧钢卷的轧制实绩数据保存在哪张表？主键是什么？",
     *   "kind": "table"
     * }
     * }</pre>
     *
     * @param request 问答请求（问题 + 检索范围 + 可选 topN）
     * @return AI 基于知识库上下文生成的回答 + 引用片段 + Token 用量
     */
    @PostMapping("/ask")
    public ResultVO<MesQaVO> ask(@Validated @RequestBody MesQaRequest request) {
        log.info("MES 问答：kind={} question={}", request.getKind(),
                request.getQuestion().length() > 50
                        ? request.getQuestion().substring(0, 50) + "..."
                        : request.getQuestion());
        MesQaVO result = mesQaService.ask(request);
        return ResultVO.success(result);
    }
}
