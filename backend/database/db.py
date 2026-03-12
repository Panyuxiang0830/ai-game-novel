# backend/database/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager
import os


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./game.db")

        self.engine = create_async_engine(
            database_url,
            echo=False,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def init_db(self):
        """初始化数据库表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# 全局数据库实例
db = Database()


async def get_db():
    """依赖注入：获取数据库会话"""
    async with db.get_session() as session:
        yield session
