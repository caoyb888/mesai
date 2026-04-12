"""
Token 预算管控服务
关联任务: T1-2-3 / T1-2-4
作者: AI
日期: 2026-04-12

职责：
    1. 累计当日 Token 消耗
    2. 触发降级告警（>250万：RAG Top-5 → Top-3）
    3. 触发暂停告警（>300万：停止非紧急任务）
    4. 发送企业微信告警通知
    5. 将消耗记录写入 ai_exec_log（数据库层，Sprint 3 集成后启用）

当前阶段（Sprint 1）：消耗数据存储于内存计数器，数据库集成在 Sprint 3 完成后启用。
"""

import logging
import httpx
from datetime import date
from threading import Lock
from app.config import get_settings
from app.models import BudgetStatus

log = logging.getLogger(__name__)


class TokenBudgetService:
    """Token 预算管控服务（线程安全）"""

    def __init__(self):
        self._settings = get_settings()
        self._lock = Lock()
        # 内存计数器：{date_str: used_tokens}
        # Sprint 3 数据库初始化完成后，改为从 ai_token_daily 表读取
        self._daily_counters: dict[str, int] = {}
        # 告警状态（防重复告警）
        self._alerted_degrade: set[str] = set()
        self._alerted_pause: set[str] = set()

    def _today(self) -> str:
        return date.today().strftime("%Y%m%d")

    def get_today_usage(self) -> int:
        """获取当日已消耗 Token 数"""
        today = self._today()
        with self._lock:
            return self._daily_counters.get(today, 0)

    def add_usage(self, tokens: int, task_no: str, caller: str) -> BudgetStatus:
        """
        累加 Token 消耗并检查预算

        :param tokens: 本次消耗的 Token 数
        :param task_no: 需求单编号（用于日志）
        :param caller: 调用来源模块
        :return: 当前预算状态
        """
        today = self._today()
        settings = self._settings

        with self._lock:
            used = self._daily_counters.get(today, 0) + tokens
            self._daily_counters[today] = used

        usage_rate = used / settings.token_daily_budget
        is_degraded = used >= settings.token_degrade_threshold
        is_paused = used >= settings.token_pause_threshold

        log.info(
            "[Token] 当日消耗：%d，预算：%d，使用率：%.1f%%，"
            "任务：%s，来源：%s",
            used, settings.token_daily_budget, usage_rate * 100, task_no, caller
        )

        # 降级告警（首次触发）
        if is_degraded and today not in self._alerted_degrade:
            self._alerted_degrade.add(today)
            self._send_alert(
                level="警告",
                title="Token 预算降级告警",
                content=(
                    f"当日 Token 消耗已达 {used:,}（{usage_rate:.1%}），"
                    f"超过降级阈值 {settings.token_degrade_threshold:,}。\n"
                    f"已自动降级：RAG 检索 Top-5 → Top-3，压缩输出格式。"
                )
            )

        # 暂停告警（首次触发）
        if is_paused and today not in self._alerted_pause:
            self._alerted_pause.add(today)
            self._send_alert(
                level="紧急",
                title="Token 预算超限——非紧急任务已暂停",
                content=(
                    f"当日 Token 消耗已达 {used:,}（{usage_rate:.1%}），"
                    f"超出每日预算上限 {settings.token_daily_budget:,}。\n"
                    f"已自动暂停非紧急任务，仅处理进行中任务和 Critical 级巡检告警。\n"
                    f"请 IT 审核专员评估是否扩大预算。"
                )
            )

        return BudgetStatus(
            date=today,
            used_tokens=used,
            daily_budget=settings.token_daily_budget,
            usage_rate=usage_rate,
            is_degraded=is_degraded,
            is_paused=is_paused,
        )

    def check_budget(self) -> BudgetStatus:
        """检查当前预算状态（不累加消耗）"""
        today = self._today()
        settings = self._settings
        used = self.get_today_usage()
        usage_rate = used / settings.token_daily_budget
        return BudgetStatus(
            date=today,
            used_tokens=used,
            daily_budget=settings.token_daily_budget,
            usage_rate=usage_rate,
            is_degraded=used >= settings.token_degrade_threshold,
            is_paused=used >= settings.token_pause_threshold,
        )

    def _send_alert(self, level: str, title: str, content: str):
        """
        发送企业微信机器人告警（CLAUDE.md 9.4 / 11.1）
        Webhook 地址通过环境变量 WECHAT_WEBHOOK_URL 注入
        """
        webhook_url = self._settings.wechat_webhook_url
        if not webhook_url:
            log.warning("[Token告警] WECHAT_WEBHOOK_URL 未配置，跳过告警通知：%s", title)
            return

        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": (
                    f"## 【{level}】芯智云匠 · {title}\n"
                    f"{content}\n\n"
                    f"> 请登录任务管理平台查看详情"
                )
            }
        }
        try:
            resp = httpx.post(webhook_url, json=payload, timeout=5)
            if resp.status_code == 200:
                log.info("[Token告警] 企业微信通知发送成功：%s", title)
            else:
                log.error("[Token告警] 企业微信通知发送失败，状态码：%d", resp.status_code)
        except Exception as e:
            log.error("[Token告警] 企业微信通知异常：%s", str(e), exc_info=True)


# 全局单例
_token_service: TokenBudgetService | None = None


def get_token_service() -> TokenBudgetService:
    global _token_service
    if _token_service is None:
        _token_service = TokenBudgetService()
    return _token_service
