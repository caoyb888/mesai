package com.xingtong.mesai.module.task.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;

import java.time.LocalDateTime;

/**
 * 序列号降级兜底表实体
 *
 * <p>对应数据库表：mes_ai_task.ai_seq_counter
 * <p>正常情况下序列号由 Redis 生成，本表仅在 Redis 不可用时作为降级兜底。
 *
 * @author AI
 * @date 2026-04-12
 * 关联需求单: T0-2-4
 */
@Data
@TableName("ai_seq_counter")
public class AiSeqCounter {

    /** 主键 ID */
    @TableId(type = IdType.AUTO)
    private Long id;

    /** 序列号键，格式 TASK_NO_{YYYYMMDD}，唯一索引 */
    private String seqKey;

    /** 序列号类型：TASK_NO / REPORT_NO / BATCH_NO 等 */
    private String seqType;

    /** 当前序列值（应用层 +1 后使用） */
    private Long currentVal;

    /** 对应日期 YYYYMMDD */
    private String dateStr;

    /** 备注说明 */
    private String description;

    /** 最后更新时间（UTC+8） */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
