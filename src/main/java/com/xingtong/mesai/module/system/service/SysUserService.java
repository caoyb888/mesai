package com.xingtong.mesai.module.system.service;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.xingtong.mesai.common.exception.BizException;
import com.xingtong.mesai.common.result.PageVO;
import com.xingtong.mesai.common.result.ResultCode;
import com.xingtong.mesai.module.system.dto.CreateUserRequest;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.enums.UserRole;
import com.xingtong.mesai.module.system.mapper.SysUserMapper;
import com.xingtong.mesai.module.system.vo.UserVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

/**
 * 系统用户服务
 *
 * <p>提供用户列表分页查询与用户创建两个核心功能。
 * <p>所有写操作对密码使用 BCrypt 加密，禁止以明文形式存储或日志输出。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class SysUserService {

    private final SysUserMapper   sysUserMapper;
    private final PasswordEncoder passwordEncoder;

    /**
     * 分页查询用户列表（不含 password 字段）。
     *
     * @param pageNum  页码（从 1 开始）
     * @param pageSize 每页条数（最大 100）
     * @param role     角色代码精确筛选，null 时不过滤
     * @param dept     部门名称模糊筛选，null 时不过滤
     * @param isActive 启用状态精确筛选，null 时不过滤
     * @param keyword  关键词（username 或 realName 模糊匹配），null 时不过滤
     * @return 分页结果 VO
     */
    public PageVO<UserVO> listUsers(int pageNum, int pageSize,
                                    String role, String dept,
                                    Integer isActive, String keyword) {
        // 防止超大分页
        int safePageSize = Math.min(pageSize, 100);
        Page<UserVO> page = new Page<>(pageNum, safePageSize);

        Page<UserVO> result = sysUserMapper.selectUserPage(page, role, dept, isActive, keyword);

        return PageVO.from(result, result.getRecords());
    }

    /**
     * 创建新用户（需 system:admin 权限，由控制器注解保证）。
     *
     * <p>校验流程：
     * <ol>
     *   <li>验证 role 字段为合法的 UserRole 枚举值</li>
     *   <li>检查 username 唯一性</li>
     *   <li>BCrypt 加密密码后存入数据库</li>
     * </ol>
     *
     * @param request 创建用户请求 DTO
     * @return 创建成功的用户 VO（不含 password）
     */
    public UserVO createUser(CreateUserRequest request) {
        // 1. 校验角色合法性
        try {
            UserRole.fromCode(request.getRole());
        } catch (IllegalArgumentException e) {
            throw new BizException(ResultCode.PARAM_INVALID, "无效的角色代码：" + request.getRole());
        }

        // 2. 检查用户名唯一性
        long count = sysUserMapper.selectCount(
                new LambdaQueryWrapper<SysUser>().eq(SysUser::getUsername, request.getUsername()));
        if (count > 0) {
            throw new BizException(ResultCode.DUPLICATE_KEY, "用户名已存在：" + request.getUsername());
        }

        // 3. 构建实体并加密密码（禁止日志输出明文密码）
        SysUser user = new SysUser();
        user.setUsername(request.getUsername());
        user.setRealName(request.getRealName());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setRole(request.getRole());
        user.setDept(request.getDept());
        user.setEmail(request.getEmail());
        user.setIsActive(request.getIsActive());

        sysUserMapper.insert(user);

        log.info("创建用户成功：username={} role={}", user.getUsername(), user.getRole());

        // 4. 将实体映射为 VO 返回（不含 password）
        return toVO(user);
    }

    // ── 私有工具方法 ─────────────────────────────────────────────

    /** 实体 → VO 转换（明确排除 password 字段） */
    private UserVO toVO(SysUser user) {
        UserVO vo = new UserVO();
        vo.setUserId(user.getId());
        vo.setUsername(user.getUsername());
        vo.setRealName(user.getRealName());
        vo.setRole(user.getRole());
        vo.setDept(user.getDept());
        vo.setEmail(user.getEmail());
        vo.setIsActive(user.getIsActive());
        vo.setCreatedAt(user.getCreatedAt());
        return vo;
    }
}
