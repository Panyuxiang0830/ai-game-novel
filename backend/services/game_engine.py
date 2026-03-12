# backend/services/game_engine.py
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from models.scenario import ScenarioSeed, ScenarioConfig
from models.game import (
    PlayerState, GameState, GameTurn, PlayerAction,
    GameStatus, ConditionType, Item
)
from models.novel import NovelProject
from services.ai_service import ai_service


class GameEngine:
    """游戏引擎 - 处理游戏逻辑和回合管理"""

    def __init__(self):
        self._sessions: Dict[str, GameState] = {}
        self._histories: Dict[str, List[GameTurn]] = {}

    async def create_session(
        self,
        scenario: ScenarioSeed,
        config: ScenarioConfig
    ) -> GameState:
        """创建新游戏会话"""
        session_id = str(uuid.uuid4())

        # 应用难度系数到初始属性
        difficulty_multiplier = 1.0 / config.difficulty

        # 创建玩家状态
        player = PlayerState(
            health=config.initial_attributes.get("health", 100),
            hunger=config.initial_attributes.get("hunger", 80),
            thirst=config.initial_attributes.get("thirst", 80),
            temperature=37.0,
            sanity=config.initial_attributes.get("sanity", 90),
            strength=50,
            agility=50,
            intelligence=50,
            charisma=50,
            perception=50
        )

        # 添加初始物品
        for item_name, count in config.starting_supplies.items():
            for _ in range(count):
                item = self._create_starter_item(item_name)
                if item:
                    player.add_item(item)

        # 创建游戏状态
        session = GameState(
            session_id=session_id,
            scenario_id=scenario.id,
            player=player,
            current_location="starting_point",
            status=GameStatus.ACTIVE
        )

        self._sessions[session_id] = session
        self._histories[session_id] = []

        return session

    def _create_starter_item(self, item_name: str) -> Optional[Item]:
        """创建初始物品"""
        items = {
            "food": Item(
                id=f"food_{uuid.uuid4().hex[:8]}",
                name="压缩饼干",
                description="一块高能量压缩饼干，可以补充饥饿值。",
                category="food",
                effects={"hunger": 20}
            ),
            "water": Item(
                id=f"water_{uuid.uuid4().hex[:8]}",
                name="纯净水",
                description="一瓶500ml的纯净水。",
                category="water",
                effects={"thirst": 25}
            ),
            "medicine": Item(
                id=f"medicine_{uuid.uuid4().hex[:8]}",
                name="急救包",
                description="基础医疗用品，可以治疗轻伤。",
                category="medicine",
                effects={"health": 15}
            )
        }
        return items.get(item_name)

    async def process_turn(
        self,
        session_id: str,
        player_action: PlayerAction,
        scenario: ScenarioSeed,
        context: str
    ) -> GameTurn:
        """处理游戏回合"""
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        if session.status != GameStatus.ACTIVE:
            raise ValueError(f"Session {session_id} is not active")

        # 构建历史摘要
        history_summary = self._build_history_summary(session_id)

        # 调用AI生成响应
        ai_result = await ai_service.generate_turn_response(
            scenario=scenario,
            player_state=session.player,
            player_action=player_action,
            context=context,
            history_summary=history_summary
        )

        # 应用状态变化
        state_changes = ai_result.get("state_changes", {})
        self._apply_state_changes(session.player, state_changes, scenario)

        # 检查游戏结束条件
        end_reason = self._check_end_conditions(session, scenario)
        if end_reason:
            session.status = GameStatus.ENDED
            session.ended_at = datetime.now()

        # 创建回合记录
        turn = GameTurn(
            turn_num=len(self._histories[session_id]) + 1,
            player_input=player_action.action,
            ai_response=ai_result.get("narrative", ""),
            state_changes=state_changes,
            is_key_event=ai_result.get("is_key_event", False),
            event_type="key_event" if ai_result.get("is_key_event") else None
        )

        self._histories[session_id].append(turn)
        session.time_elapsed += 1

        return turn

    def _apply_state_changes(
        self,
        player: PlayerState,
        changes: Dict[str, int],
        scenario: ScenarioSeed
    ) -> None:
        """应用状态变化"""
        for attr, value in changes.items():
            if hasattr(player, attr):
                current = getattr(player, attr)
                if isinstance(current, int):
                    setattr(player, attr, max(0, min(100, current + value)))
                elif isinstance(current, float):
                    setattr(player, attr, current + value)

        # 根据场景特定规则更新状态
        self._apply_scenario_rules(player, scenario)

    def _apply_scenario_rules(self, player: PlayerState, scenario: ScenarioSeed) -> None:
        """应用场景特定规则"""
        # 全球冰封：体温持续下降
        if scenario.id == "ice_age":
            # 体温在室外会自然下降
            pass  # 具体逻辑在AI生成的state_changes中

        # 丧尸末世：饥饿/口渴下降更快
        if scenario.id == "zombie":
            pass

        # 核战废墟：辐射影响
        if scenario.id == "nuclear":
            pass

    def _check_end_conditions(
        self,
        session: GameState,
        scenario: ScenarioSeed
    ) -> Optional[str]:
        """检查游戏结束条件"""
        player = session.player

        # 死亡条件
        if player.health <= 0:
            return "死亡"
        if player.hunger <= 0 and player.thirst <= 0:
            return "饿死/渴死"
        if player.temperature < 30:
            return "冻死"
        if player.sanity <= 0:
            return "精神崩溃"

        # 胜利条件由AI判定
        return None

    def _build_history_summary(self, session_id: str, max_turns: int = 5) -> str:
        """构建历史摘要"""
        history = self._histories.get(session_id, [])
        if not history:
            return ""

        recent_turns = history[-max_turns:]
        summary_parts = []
        for turn in recent_turns:
            summary_parts.append(f"回合{turn.turn_num}: {turn.player_input[:50]}...")

        return "\n".join(summary_parts)

    def get_session(self, session_id: str) -> Optional[GameState]:
        """获取游戏会话"""
        return self._sessions.get(session_id)

    def get_history(self, session_id: str) -> List[GameTurn]:
        """获取游戏历史"""
        return self._histories.get(session_id, [])

    def get_key_events(self, session_id: str) -> List[GameTurn]:
        """获取关键事件"""
        history = self._histories.get(session_id, [])
        return [t for t in history if t.is_key_event]

    def pause_session(self, session_id: str) -> bool:
        """暂停游戏会话"""
        session = self._sessions.get(session_id)
        if session:
            session.status = GameStatus.PAUSED
            return True
        return False

    def resume_session(self, session_id: str) -> bool:
        """恢复游戏会话"""
        session = self._sessions.get(session_id)
        if session:
            session.status = GameStatus.ACTIVE
            return True
        return False

    def delete_session(self, session_id: str) -> bool:
        """删除游戏会话"""
        if session_id in self._sessions:
            del self._sessions[session_id]
            del self._histories[session_id]
            return True
        return False


# 全局游戏引擎实例
game_engine = GameEngine()
