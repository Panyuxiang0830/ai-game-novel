# backend/models/game.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class ConditionType(str, Enum):
    """状态类型"""
    HEALTHY = "healthy"
    COLD = "cold"
    FEVER = "fever"
    INJURED = "injured"
    INFECTED = "infected"
    RADIATED = "radiated"
    POISONED = "poisoned"


class Item(BaseModel):
    """物品模型"""
    id: str
    name: str
    description: str
    category: str  # food, water, weapon, medicine, material
    consumable: bool = True
    effects: Optional[Dict[str, int]] = None


class PlayerState(BaseModel):
    """玩家状态模型"""
    # 生存属性 (0-100)
    health: int = Field(default=100, ge=0, le=100)
    hunger: int = Field(default=80, ge=0, le=100)
    thirst: int = Field(default=80, ge=0, le=100)
    temperature: float = Field(default=37.0, description="体温(°C)")
    sanity: int = Field(default=90, ge=0, le=100)

    # 能力属性 (0-100)
    strength: int = Field(default=50, ge=0, le=100)
    agility: int = Field(default=50, ge=0, le=100)
    intelligence: int = Field(default=50, ge=0, le=100)
    charisma: int = Field(default=50, ge=0, le=100)
    perception: int = Field(default=50, ge=0, le=100)

    # 状态标签
    conditions: List[ConditionType] = Field(default_factory=list)

    # 背包
    inventory: List[Item] = Field(default_factory=list)
    max_capacity: int = Field(default=20)

    def add_item(self, item: Item) -> bool:
        """添加物品"""
        if len(self.inventory) >= self.max_capacity:
            return False
        self.inventory.append(item)
        return True

    def remove_item(self, item_id: str) -> bool:
        """移除物品"""
        for i, item in enumerate(self.inventory):
            if item.id == item_id:
                self.inventory.pop(i)
                return True
        return False


class GameState(BaseModel):
    """游戏会话状态"""
    session_id: str
    scenario_id: str
    player: PlayerState
    current_location: str = "unknown"
    time_elapsed: int = Field(default=0, description="经过的回合数")
    status: str = Field(default="active", description="active, ended, paused")
    created_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None


class GameTurn(BaseModel):
    """单回合记录"""
    turn_num: int
    player_input: str
    ai_response: str
    state_changes: Dict[str, int] = Field(default_factory=dict)
    items_gained: List[Item] = Field(default_factory=list)
    items_lost: List[str] = Field(default_factory=list)
    is_key_event: bool = False
    event_type: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class PlayerAction(BaseModel):
    """玩家动作"""
    action: str
    input_type: str = Field(default="free", description="option or free")
