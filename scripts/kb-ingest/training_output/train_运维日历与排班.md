# 训练结果：运维日历与排班

**训练时间**：2026-04-13T10:58:41.117831

**Tokens**：{'prompt_tokens': 1634, 'completion_tokens': 801, 'total_tokens': 2435}

---

1. **表清单确认**

| 表名 | 中文业务含义 |
|--------|--------|
| `itsm_calendar_event` | 运维日历事件表，记录巡检计划、变更窗口、维护期等 |
| `itsm_roster_schedule` | 排班记录表，工单分配时查询当日值班人作为默认处理人 |
| `itsm_roster_team_member` | 值班团队成员表，定义团队成员及轮班顺序 |
| `itsm_roster_team` | 值班团队表，定义可排班的团队，如"基础设施值班组" |

2. **核心实体识别**

该模块中最重要的 2 张表是：

- `itsm_calendar_event`：运维日历事件表，业务角色是记录和跟踪运维相关的各种事件，如巡检计划、变更窗口等，是运维日历与排班模块的核心数据记录。
- `itsm_roster_schedule`：排班记录表，业务角色是记录每个团队成员的值班安排，确保在工单分配时能够快速找到当日值班人员，对运维工作的顺利进行至关重要。

3. **主键与外键梳理**

```
+----------------+         +----------------+         +----------------+
| itsm_calendar_  |         | itsm_roster_   |         | itsm_roster_   |
| event           |         | schedule      |         | team_member   |
| +----+----------+         | +----+----------+         | +----+----------+
| | id| <PK>     |         | | id| <PK>      |         | | team_id| <PK>  |
+----+----------+         +----+----------+         +----+----------+
          |                         |                         |
          |                         |                         |
          |                         |                         |
          +-------------------------+--------------------------+
          |                                        |
          |                                        |
          |                                        |
          v                                        v
          |                                        |
          |                                        |
+----------------+         +----------------+         +----------------+
| itsm_roster_   |         | itsm_roster_   |
| team           |         | team           |
| +----+----------+         | +----+----------+
| | id| <PK>      |         | | id| <PK>      |
+----------------+         +----------------+
```

- `itsm_roster_schedule` 表中的 `team_id` 字段是外键，关联 `itsm_roster_team` 表的 `id` 字段。
- `itsm_roster_team_member` 表中的 `team_id` 字段是外键，关联 `itsm_roster_team` 表的 `id` 字段。

4. **关键状态字段**

- `itsm_calendar_event` 表中的 `event_type` 字段，包含运维事件的类型，如 INSPECTION（例行巡检）、CHANGE_WINDOW（变更窗口）、MAINTENANCE（系统维护期）、ASSET_SCAN（资产扫描）、ON_DUTY（值班排班）。
- `itsm_roster_schedule` 表中的 `shift_type` 字段，包含班次类型，如 DAY（白班）、NIGHT（夜班）、FULL（全天班）。
- `itsm_roster_schedule` 表中的 `is_on_duty` 字段，包含值班状态，1 表示正常值班，0 表示调班/请假。
- `itsm_calendar_event` 表和 `itsm_roster_schedule` 表以及 `itsm_roster_team` 表中的 `is_deleted` 字段，包含逻辑删除标记，0 表示未删除，1 表示已删除。

5. **疑问记录**

目前没有发现字段含义不清晰或注释缺失的情况。