"""
AI 网关配置模块
文档编号: AI-MES-GW-2026-001
关联任务: T1-2-1 / T1-2-2
作者: AI
日期: 2026-04-12

所有敏感配置通过环境变量注入，禁止硬编码（CLAUDE.md 4.1）。
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    网关配置项
    所有字段均从环境变量读取，.env 文件仅用于本地开发（不入 Git）。
    """

    # ── AI Provider 配置 ──────────────────────────────────────
    # 支持的值：kimi（开发阶段）/ claude（生产阶段）
    ai_provider: str = "kimi"

    # OpenAI 兼容接口（Kimi / 其他 OpenAI 兼容服务）
    ai_api_key: str = ""                               # 必填，通过 AI_API_KEY 注入
    ai_api_base_url: str = "https://api.moonshot.cn/v1"  # Kimi 地址；切 OpenAI 改此值
    ai_model: str = "moonshot-v1-8k"                   # 开发用小模型；生产用 claude-sonnet-4-6

    # Claude 原生 SDK 配置（生产阶段使用，开发阶段留空）
    claude_api_key: str = ""
    claude_model: str = "claude-sonnet-4-6"

    # ── 请求超时与重试 ────────────────────────────────────────
    ai_request_timeout: int = 120       # 请求超时（秒）
    ai_max_retries: int = 3             # 最大重试次数
    ai_retry_delay: float = 1.0        # 重试间隔（秒）

    # ── Token 预算配置（CLAUDE.md 第十二章）────────────────────
    token_daily_budget: int = 3_000_000       # 每日预算上限（300万）
    token_degrade_threshold: int = 2_500_000  # 降级阈值（250万，RAG Top-5 → Top-3）
    token_pause_threshold: int = 3_000_000    # 暂停阈值（300万，停止非紧急任务）

    # ── MES 数据库（用于写入 ai_exec_log / ai_token_daily）────
    db_url: str = ""          # MySQL AI 平台数据库连接串，通过 DB_URL 注入
    db_pool_size: int = 5

    # ── 网关服务自身配置 ──────────────────────────────────────
    gateway_host: str = "0.0.0.0"
    gateway_port: int = 8000
    gateway_workers: int = 2
    log_level: str = "INFO"

    # ── 企业微信告警 Webhook ──────────────────────────────────
    wechat_webhook_url: str = ""   # 告警通知，通过 WECHAT_WEBHOOK_URL 注入

    model_config = {
        "env_file": ".env",             # 本地开发用，.env 文件在 .gitignore 中
        "env_file_encoding": "utf-8",
        "case_sensitive": False,        # 环境变量不区分大小写
    }


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例（lru_cache 保证全局只初始化一次）
    """
    return Settings()
