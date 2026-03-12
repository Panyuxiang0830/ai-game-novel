# backend/main.py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    # API
    api_title: str = "末世生存小说生成器 API"
    api_version: str = "1.0.0"

    # Claude API
    anthropic_api_key: str = ""

    # 数据库
    database_url: str = "sqlite+aiosqlite:///./game.db"

    # 服务
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# 解析 CORS origins
cors_origins_list = settings.cors_origins.split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 启动末世生存小说生成器 API...")
    print(f"   Claude API: {'✅ 已配置' if settings.anthropic_api_key else '❌ 未配置'}")
    print(f"   数据库: {settings.database_url}")

    # 初始化数据库
    from database.db import db
    await db.init_db()
    print("   数据库初始化完成")

    yield

    # 关闭时
    print("👋 关闭 API...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 导入路由
from api.scenarios import router as scenarios_router
from api.games import router as games_router
from api.novels import router as novels_router

# 注册路由
app.include_router(scenarios_router, prefix="/api/scenarios", tags=["场景"])
app.include_router(games_router, prefix="/api/games", tags=["游戏"])
app.include_router(novels_router, prefix="/api/novels", tags=["小说"])


# 根路径
@app.get("/")
async def root():
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "status": "running"
    }


# 健康检查
@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    )
