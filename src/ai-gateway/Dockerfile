# AI 网关 Dockerfile
# 关联任务: T1-2-1
# 作者: AI
# 日期: 2026-04-12

FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装依赖（单独一层，利用 Docker 缓存）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/

# 安全：以非 root 用户运行
RUN adduser --disabled-password --gecos "" mesai
USER mesai

# 暴露端口（实际端口由 GATEWAY_PORT 环境变量控制）
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/v1/ai/health').raise_for_status()"

# 启动命令（所有配置通过环境变量注入，禁止硬编码）
CMD ["gunicorn", "app.main:app", \
     "-w", "2", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "180", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
