package com.xingtong.mesai.module.system.controller;

import com.xingtong.mesai.common.result.ResultVO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * 健康检查 Controller
 *
 * <p>提供简单的存活探测接口 GET /system/health，
 * 无需 Token（白名单路径）。
 * <p>适用于 K8s Readiness Probe、监控平台可用性巡检等场景。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-7）
 */
@Slf4j
@RestController
@RequestMapping("/system")
public class HealthController {

    /**
     * 系统健康检查。
     *
     * <p>响应结构：
     * <pre>
     * {
     *   "code": 0,
     *   "message": "success",
     *   "data": {
     *     "status": "UP",
     *     "serverTime": "2026-04-13T07:30:00+08:00",
     *     "app": "mesai"
     *   }
     * }
     * </pre>
     *
     * @return 健康状态信息
     */
    @GetMapping("/health")
    public ResultVO<Map<String, Object>> health() {
        Map<String, Object> info = new LinkedHashMap<>();
        info.put("status", "UP");
        info.put("serverTime", LocalDateTime.now(ZoneId.of("Asia/Shanghai")).toString());
        info.put("app", "mesai");
        return ResultVO.success(info);
    }
}
