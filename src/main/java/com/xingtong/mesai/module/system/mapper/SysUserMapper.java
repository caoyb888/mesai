package com.xingtong.mesai.module.system.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.xingtong.mesai.module.system.entity.SysUser;
import com.xingtong.mesai.module.system.vo.UserVO;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 系统用户 Mapper
 *
 * <p>继承 MyBatis Plus BaseMapper 获得基础 CRUD 能力。
 * <p>复杂查询（分页列表）通过 SysUserMapper.xml 中的自定义 SQL 实现。
 * <p>注意：所有 SQL 使用参数化查询，严禁字符串拼接（SQL 注入防护）。
 *
 * @author AI（芯智云匠）
 * @date 2026-04-13
 * @module 系统管理模块
 * @related REQ-MES-AI-20260412-005（S2-3 T2-3-6）
 */
@Mapper
public interface SysUserMapper extends BaseMapper<SysUser> {

    /**
     * 分页查询用户列表（自定义 SQL，见 SysUserMapper.xml）。
     *
     * <p>密码字段不在查询列中，响应安全。
     *
     * @param page     分页参数（MyBatis Plus Page 对象，自动注入分页信息）
     * @param role     角色代码筛选，null 时不过滤
     * @param dept     部门名称筛选（模糊匹配），null 时不过滤
     * @param isActive 启用状态筛选，null 时不过滤
     * @param keyword  关键词（匹配 username 或 realName），null 时不过滤
     * @return 用户 VO 分页结果（不含 password 字段）
     */
    Page<UserVO> selectUserPage(
            Page<UserVO> page,
            @Param("role")     String role,
            @Param("dept")     String dept,
            @Param("isActive") Integer isActive,
            @Param("keyword")  String keyword
    );
}
