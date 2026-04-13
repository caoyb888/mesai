package com.xingtong.mesai.module.system.controller;

import com.xingtong.mesai.common.result.PageVO;
import com.xingtong.mesai.common.result.ResultVO;
import com.xingtong.mesai.module.system.annotation.RequirePermission;
import com.xingtong.mesai.module.system.dto.CreateUserRequest;
import com.xingtong.mesai.module.system.service.SysUserService;
import com.xingtong.mesai.module.system.vo.UserVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 系统用户管理 Controller
 *
 * <p>提供用户列表查询和用户创建两个管理接口，均需 system:admin 权限。
 * <p>接口基础路径：/system/users
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Slf4j
@RestController
@RequestMapping("/system/users")
@RequiredArgsConstructor
public class SysUserController {

    private final SysUserService sysUserService;

    /**
     * 分页查询用户列表。
     *
     * <p>需要 {@code system:admin} 权限（IT_MANAGER 或 TECH_LEAD）。
     * <p>所有筛选条件可选，不传时不过滤。密码字段不在返回结果中。
     *
     * @param page     页码（默认 1）
     * @param pageSize 每页条数（默认 20，最大 100）
     * @param role     角色代码精确筛选
     * @param dept     部门名称模糊筛选
     * @param isActive 启用状态筛选（1=启用，0=禁用）
     * @param keyword  关键词（匹配 username 或 realName）
     * @return 用户列表分页结果
     */
    @GetMapping
    @RequirePermission("system:admin")
    public ResultVO<PageVO<UserVO>> listUsers(
            @RequestParam(defaultValue = "1")  int page,
            @RequestParam(defaultValue = "20") int pageSize,
            @RequestParam(required = false)    String role,
            @RequestParam(required = false)    String dept,
            @RequestParam(required = false)    Integer isActive,
            @RequestParam(required = false)    String keyword) {

        log.debug("查询用户列表：page={} pageSize={} role={} dept={} isActive={} keyword={}",
                page, pageSize, role, dept, isActive, keyword);

        PageVO<UserVO> result = sysUserService.listUsers(page, pageSize, role, dept, isActive, keyword);
        return ResultVO.success(result);
    }

    /**
     * 创建新用户。
     *
     * <p>需要 {@code system:admin} 权限（IT_MANAGER 或 TECH_LEAD）。
     * <p>密码服务端 BCrypt 加密后存储，响应不含 password 字段。
     *
     * @param request 创建用户请求 DTO
     * @return 创建成功的用户信息 VO（不含 password）
     */
    @PostMapping
    @RequirePermission("system:admin")
    public ResultVO<UserVO> createUser(@Validated @RequestBody CreateUserRequest request) {
        log.info("创建用户请求：username={} role={}", request.getUsername(), request.getRole());
        UserVO userVO = sysUserService.createUser(request);
        return ResultVO.success(userVO);
    }
}
