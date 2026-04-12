"""
AI 网关服务入口
文档编号: AI-MES-GW-2026-001
关联任务: T1-2-1
作者: AI
日期: 2026-04-12

启动方式（开发）：
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

启动方式（生产）：
    gunicorn app.main:app -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
"""

import logging
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routers import gateway

# ── 日志配置 ─────────────────────────────────────────────────
settings = get_settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    "root": {
        "level": settings.log_level,
        "handlers": ["console"],
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
log = logging.getLogger(__name__)


# ── 生命周期 ─────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动/关闭时的初始化与清理"""
    cfg = get_settings()
    log.info(
        "芯智云匠 AI 网关启动 | Provider: %s | Model: %s | Port: %d",
        cfg.ai_provider, cfg.ai_model, cfg.gateway_port
    )
    if not cfg.ai_api_key:
        log.warning("AI_API_KEY 未配置，/v1/ai/chat 接口调用将失败")
    yield
    log.info("芯智云匠 AI 网关关闭")


# ── FastAPI 应用 ──────────────────────────────────────────────
app = FastAPI(
    title="芯智云匠 AI 网关",
    description=(
        "MES AI 智能体统一调用网关。\n\n"
        "所有发往外部 AI API 的请求经此网关统一管控：\n"
        "- PII 脱敏（CLAUDE.md 4.2）\n"
        "- Token 预算管控（CLAUDE.md 第十二章）\n"
        "- 调用日志记录（Token 消耗、响应时间、调用来源）\n"
        "- Provider 切换（Kimi 开发 → Claude 生产，仅改环境变量）"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(gateway.router)


# ── 全局异常处理 ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("[网关] 未捕获异常：%s %s → %s", request.method, request.url, str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"code": 99999, "message": "网关内部错误，请联系技术负责人"},
    )
