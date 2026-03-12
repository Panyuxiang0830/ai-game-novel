# backend/database/models.py
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class SessionModel(Base):
    """游戏会话表"""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    scenario_id = Column(String, nullable=False)
    player_state = Column(JSON, nullable=False)
    current_location = Column(String)
    time_elapsed = Column(Integer, default=0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now)
    ended_at = Column(DateTime, nullable=True)

    # 关联
    turns = relationship("GameTurnModel", back_populates="session", cascade="all, delete-orphan")
    novel = relationship("NovelModel", back_populates="session", uselist=False, cascade="all, delete-orphan")


class GameTurnModel(Base):
    """游戏回合表"""
    __tablename__ = "game_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, nullable=False)
    turn_num = Column(Integer, nullable=False)
    player_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    state_changes = Column(JSON)
    items_gained = Column(JSON)
    items_lost = Column(JSON)
    is_key_event = Column(Boolean, default=False)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    # 关联
    session = relationship("SessionModel", back_populates="turns")


class NovelModel(Base):
    """小说项目表"""
    __tablename__ = "novels"

    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    scenario_id = Column(String, nullable=False)
    skeleton = Column(JSON)
    status = Column(String, default="in_progress")
    total_words = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    # 关联
    session = relationship("SessionModel", back_populates="novel")
    chapters = relationship("ChapterModel", back_populates="novel", cascade="all, delete-orphan")


class ChapterModel(Base):
    """小说章节表"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(String, nullable=False)
    chapter_num = Column(Integer, nullable=False)
    title = Column(String)
    event_title = Column(String)
    content = Column(Text)
    word_count = Column(Integer, default=0)
    status = Column(String, default="pending")
    generated_at = Column(DateTime, nullable=True)

    # 关联
    novel = relationship("NovelModel", back_populates="chapters")


class ScenarioModel(Base):
    """自定义场景表"""
    __tablename__ = "scenarios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    premise = Column(Text, nullable=False)
    world_rules = Column(JSON)
    survival_mechanics = Column(JSON)
    possible_events = Column(JSON)
    ending_conditions = Column(JSON)
    narrative_style = Column(String)
    is_custom = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
