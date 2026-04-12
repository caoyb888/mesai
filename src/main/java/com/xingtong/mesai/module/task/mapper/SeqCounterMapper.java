package com.xingtong.mesai.module.task.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.xingtong.mesai.module.task.entity.AiSeqCounter;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

/**
 * 序列号降级兜底表 Mapper
 *
 * <p>正常情况下由 Redis 生成序列号，本 Mapper 仅在 Redis 不可用时调用。
 * <p>关联表: mes_ai_task.ai_seq_counter
 *
 * @author AI
 * @date 2026-04-12
 * 关联需求单: T0-2-4
 */
@Mapper
public interface SeqCounterMapper extends BaseMapper<AiSeqCounter> {

    /**
     * 若当日记录不存在则初始化（INSERT IGNORE 防并发重复插入）
     *
     * @param seqKey  序列键，格式 TASK_NO_{YYYYMMDD}
     * @param seqType 序列类型，如 TASK_NO
     * @param dateStr 日期字符串 YYYYMMDD
     */
    void initIfAbsent(@Param("seqKey") String seqKey,
                      @Param("seqType") String seqType,
                      @Param("dateStr") String dateStr);

    /**
     * 乐观锁递增当前值
     * <p>返回影响行数：1 表示成功，0 表示并发冲突（需重试）
     *
     * @param seqKey  序列键
     * @param dateStr 日期字符串（双重条件，防跨日误操作）
     * @return 影响行数
     */
    int incrementAndGet(@Param("seqKey") String seqKey,
                        @Param("dateStr") String dateStr);

    /**
     * 查询当前序列值
     *
     * @param seqKey 序列键
     * @return 当前序列值
     */
    long getCurrentVal(@Param("seqKey") String seqKey);
}
