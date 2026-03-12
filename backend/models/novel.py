# backend/models/novel.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class NovelStatus(str, Enum):
    """小说项目状态"""
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class ChapterStatus(str, Enum):
    """章节状态"""
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"


class NovelSkeleton(BaseModel):
    """小说骨架"""
    premise: str = Field(..., description="小说前提")
    estimated_chapters: int = Field(default=5, ge=3, le=10)
    chapter_outlines: List[Dict[str, Any]] = Field(default_factory=list, description="章节大纲")
    narrative_style: str = Field(..., description="叙事风格")
    main_character_arc: str = Field(default="", description="主角成长弧线")


class NovelChapter(BaseModel):
    """小说章节"""
    chapter_num: int
    title: str
    event_title: str = Field(..., description="触发该章节的游戏事件")
    content: str = Field(default="", description="章节内容")
    word_count: int = Field(default=0)
    generated_at: Optional[datetime] = None
    status: ChapterStatus = Field(default=ChapterStatus.PENDING, description="章节状态")


class NovelProject(BaseModel):
    """小说项目"""
    novel_id: str
    session_id: str
    scenario_id: str
    skeleton: Optional[NovelSkeleton] = None
    chapters: List[NovelChapter] = Field(default_factory=list)
    total_words: int = Field(default=0)
    status: NovelStatus = Field(default=NovelStatus.IN_PROGRESS, description="小说状态")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class ChapterRequest(BaseModel):
    """章节生成请求"""
    novel_id: str
    chapter_num: int
    event_context: str = Field(..., description="当前事件上下文")
    previous_chapter: Optional[str] = None
