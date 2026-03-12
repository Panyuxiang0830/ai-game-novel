# backend/api/scenarios.py
from fastapi import APIRouter, HTTPException
from typing import List

from models.scenario import ScenarioSeed, ScenarioConfig
from scenarios import scenario_loader


router = APIRouter()


@router.get("/list", response_model=List[ScenarioSeed])
async def list_scenarios() -> List[ScenarioSeed]:
    """获取所有预设场景"""
    return scenario_loader.list_presets()


@router.get("/{scenario_id}", response_model=ScenarioSeed)
async def get_scenario(scenario_id: str) -> ScenarioSeed:
    """获取单个场景详情"""
    scenario = scenario_loader.load_preset(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail=f"场景 {scenario_id} 不存在")
    return scenario
