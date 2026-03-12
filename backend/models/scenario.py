# backend/models/scenario.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


class ScenarioSeed(BaseModel):
    """场景种子模型"""
    id: str = Field(..., description="场景唯一标识")
    name: str = Field(..., description="场景名称")
    description: str = Field(..., description="场景描述")
    premise: str = Field(..., description="世界背景设定")
    world_rules: Dict[str, Any] = Field(default_factory=dict, description="世界规则")
    survival_mechanics: Dict[str, Any] = Field(default_factory=dict, description="生存机制")
    possible_events: List[str] = Field(default_factory=list, description="可能发生的事件")
    ending_conditions: Dict[str, Any] = Field(default_factory=dict, description="结局条件")
    narrative_style: str = Field(..., description="叙事风格")
    is_custom: bool = Field(default=False, description="是否为自定义场景")


class ScenarioConfig(BaseModel):
    """场景配置（玩家可调整部分）"""
    scenario_id: str
    starting_supplies: Dict[str, int] = Field(default_factory=lambda: {
        "food": 3, "water": 3, "medicine": 1
    })
    initial_attributes: Dict[str, int] = Field(default_factory=lambda: {
        "health": 100, "hunger": 80, "thirst": 80, "sanity": 90
    })
    difficulty: float = Field(default=1.0, ge=0.5, le=2.0, description="难度系数")
