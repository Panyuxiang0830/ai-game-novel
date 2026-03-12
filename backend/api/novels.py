# backend/api/novels.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from models.novel import NovelProject, NovelChapter
from services.novel_engine import novel_engine
from scenarios import scenario_loader


router = APIRouter()


class CreateNovelRequest(BaseModel):
    session_id: str
    scenario_id: str
    player_background: str = ""
    api_key: Optional[str] = None  # 用户提供的 API key


class GenerateChapterRequest(BaseModel):
    event_context: str
    api_key: Optional[str] = None  # 用户提供的 API key


@router.post("/create", response_model=NovelProject)
async def create_novel(request: CreateNovelRequest) -> NovelProject:
    """创建小说项目"""
    # 加载场景
    scenario = scenario_loader.load_preset(request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"场景 {request.scenario_id} 不存在")

    if not request.api_key:
        raise HTTPException(status_code=400, detail="API key is required. Please provide your Anthropic API key.")

    # 创建小说项目
    project = await novel_engine.create_project(
        session_id=request.session_id,
        scenario=scenario,
        player_background=request.player_background,
        api_key=request.api_key
    )
    return project


@router.get("/{novel_id}", response_model=NovelProject)
async def get_novel(novel_id: str) -> NovelProject:
    """获取小说项目"""
    project = novel_engine.get_project(novel_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"小说项目 {novel_id} 不存在")
    return project


@router.get("/{novel_id}/chapter/{chapter_num}", response_model=NovelChapter)
async def get_chapter(novel_id: str, chapter_num: int) -> NovelChapter:
    """获取单个章节"""
    chapter = novel_engine.get_chapter(novel_id, chapter_num)
    if not chapter:
        raise HTTPException(status_code=404, detail=f"章节不存在")
    return chapter


@router.post("/{novel_id}/chapter/{chapter_num}/generate", response_model=NovelChapter)
async def generate_chapter(novel_id: str, chapter_num: int, request: GenerateChapterRequest) -> NovelChapter:
    """生成章节内容"""
    project = novel_engine.get_project(novel_id)
    if not project:
        raise HTTPException(status_code=404, detail=f"小说项目 {novel_id} 不存在")

    # 加载场景
    scenario = scenario_loader.load_preset(project.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"场景 {project.scenario_id} 不存在")

    # 构建 API key（使用请求中的或存储的）
    api_key = request.api_key or novel_engine.get_api_key(novel_id)
    if not api_key:
        raise HTTPException(status_code=400, detail="API key is required. Please provide your Anthropic API key.")

    # 生成章节
    chapter = await novel_engine.generate_chapter(
        novel_id=novel_id,
        chapter_num=chapter_num,
        event_context=request.event_context,
        scenario=scenario,
        api_key=api_key
    )
    return chapter


@router.get("/{novel_id}/export")
async def export_novel(novel_id: str):
    """导出完整小说"""
    text = novel_engine.export_full_text(novel_id)
    if text is None:
        raise HTTPException(status_code=404, detail=f"小说项目 {novel_id} 不存在")
    return {"text": text}


@router.get("/list/all", response_model=List[NovelProject])
async def list_novels() -> List[NovelProject]:
    """列出所有小说项目"""
    return novel_engine.list_projects()


@router.delete("/{novel_id}")
async def delete_novel(novel_id: str):
    """删除小说项目"""
    success = novel_engine.delete_project(novel_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"小说项目 {novel_id} 不存在")
    return {"status": "deleted"}
