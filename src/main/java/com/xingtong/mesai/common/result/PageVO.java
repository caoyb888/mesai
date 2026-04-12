package com.xingtong.mesai.common.result;

import com.baomidou.mybatisplus.core.metadata.IPage;
import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;

/**
 * 分页响应封装
 *
 * <p>对应 API 规范 3.2 节分页响应结构，与 MyBatis Plus IPage 对接。
 * <p>使用示例：
 * <pre>
 * IPage&lt;AiTaskReq&gt; page = taskMapper.selectPage(new Page&lt;&gt;(1, 20), wrapper);
 * List&lt;TaskRequestVO&gt; voList = converter.toVOList(page.getRecords());
 * return ResultVO.success(PageVO.from(page, voList));
 * </pre>
 *
 * @param <T> 列表元素类型
 * @author AI（芯智云匠）
 * @date 2026-04-12
 * @module 公共基础组件
 * @related REQ-MES-AI-20260412-005（S1-5 后端项目骨架）
 */
@Data
@AllArgsConstructor
public class PageVO<T> {

    /** 数据列表 */
    private List<T> list;

    /** 分页信息 */
    private PaginationVO pagination;

    /**
     * 从 MyBatis Plus IPage 对象构建分页响应
     *
     * @param page   MP 分页对象（含 current/size/total/pages）
     * @param list   已转换为 VO 的数据列表
     * @param <E>    Entity 类型
     * @param <R>    VO 类型
     * @return 分页响应
     */
    public static <E, R> PageVO<R> from(IPage<E> page, List<R> list) {
        PaginationVO pagination = new PaginationVO(
                (int) page.getCurrent(),
                (int) page.getSize(),
                page.getTotal(),
                (int) page.getPages()
        );
        return new PageVO<>(list, pagination);
    }

    /**
     * 分页信息子对象
     */
    @Data
    @AllArgsConstructor
    public static class PaginationVO {
        /** 当前页（从 1 开始） */
        private Integer page;
        /** 每页条数 */
        private Integer pageSize;
        /** 总记录数 */
        private Long total;
        /** 总页数 */
        private Integer totalPages;
    }
}
