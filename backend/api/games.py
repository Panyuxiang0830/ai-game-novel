# backend/api/games.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from models.scenario import ScenarioSeed, ScenarioConfig
from models.game import GameState, GameTurn, PlayerAction
from services.game_engine import game_engine
from scenarios import scenario_loader


router = APIRouter()


class CreateSessionRequest(BaseModel):
    scenario_id: str
    config: Optional[ScenarioConfig] = None


class ProcessTurnRequest(BaseModel):
    action: str
    input_type: str = "free"
    context: str = ""


@router.post("/create", response_model=GameState)
async def create_session(request: CreateSessionRequest) -> GameState:
    """创建新游戏会话"""
    # 加载场景
    scenario = scenario_loader.load_preset(request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"场景 {request.scenario_id} 不存在")

    # 使用默认或自定义配置
    config = request.config or ScenarioConfig(scenario_id=request.scenario_id)

    # 创建游戏会话
    session = await game_engine.create_session(scenario, config)
    return session


@router.get("/{session_id}", response_model=GameState)
async def get_session(session_id: str) -> GameState:
    """获取游戏会话状态"""
    session = game_engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"游戏会话 {session_id} 不存在")
    return session


@router.post("/{session_id}/turn", response_model=GameTurn)
async def process_turn(session_id: str, request: ProcessTurnRequest) -> GameTurn:
    """处理游戏回合"""
    session = game_engine.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"游戏会话 {session_id} 不存在")

    # 加载场景
    scenario = scenario_loader.load_preset(session.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"场景 {session.scenario_id} 不存在")

    # 构建玩家动作
    player_action = PlayerAction(
        action=request.action,
        input_type=request.input_type
    )

    # 处理回合
    turn = await game_engine.process_turn(
        session_id=session_id,
        player_action=player_action,
        scenario=scenario,
        context=request.context
    )
    return turn


@router.get("/{session_id}/history", response_model=List[GameTurn])
async def get_history(session_id: str) -> List[GameTurn]:
    """获取游戏历史"""
    return game_engine.get_history(session_id)


@router.get("/{session_id}/key-events", response_model=List[GameTurn])
async def get_key_events(session_id: str) -> List[GameTurn]:
    """获取关键事件"""
    return game_engine.get_key_events(session_id)


@router.post("/{session_id}/pause")
async def pause_session(session_id: str):
    """暂停游戏会话"""
    success = game_engine.pause_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"游戏会话 {session_id} 不存在")
    return {"status": "paused"}


@router.post("/{session_id}/resume")
async def resume_session(session_id: str):
    """恢复游戏会话"""
    success = game_engine.resume_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"游戏会话 {session_id} 不存在")
    return {"status": "resumed"}


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """删除游戏会话"""
    success = game_engine.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"游戏会话 {session_id} 不存在")
    return {"status": "deleted"}
