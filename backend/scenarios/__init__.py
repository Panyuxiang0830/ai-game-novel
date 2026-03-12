# backend/scenarios/__init__.py
import json
from pathlib import Path
from typing import Dict, List, Optional
from ..models.scenario import ScenarioSeed


class ScenarioLoader:
    """场景加载器"""

    def __init__(self, presets_dir: str = None):
        if presets_dir is None:
            presets_dir = Path(__file__).parent / "presets"
        self.presets_dir = Path(presets_dir)
        self._cache: Dict[str, ScenarioSeed] = {}

    def load_preset(self, scenario_id: str) -> Optional[ScenarioSeed]:
        """加载预设场景"""
        if scenario_id in self._cache:
            return self._cache[scenario_id]

        scenario_file = self.presets_dir / f"{scenario_id}.json"
        if not scenario_file.exists():
            return None

        with open(scenario_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        scenario = ScenarioSeed(**data)
        self._cache[scenario_id] = scenario
        return scenario

    def list_presets(self) -> List[ScenarioSeed]:
        """列出所有预设场景"""
        scenarios = []
        for json_file in self.presets_dir.glob("*.json"):
            scenario_id = json_file.stem
            scenario = self.load_preset(scenario_id)
            if scenario:
                scenarios.append(scenario)
        return scenarios

    async def load_custom(self, scenario_id: str, db_session) -> Optional[ScenarioSeed]:
        """从数据库加载自定义场景"""
        from ..database.models import ScenarioModel
        from sqlalchemy import select

        result = await db_session.execute(
            select(ScenarioModel).where(ScenarioModel.id == scenario_id)
        )
        scenario_model = result.scalar_one_or_none()
        if not scenario_model:
            return None

        return ScenarioSeed(
            id=scenario_model.id,
            name=scenario_model.name,
            description=scenario_model.description or "",
            premise=scenario_model.premise,
            world_rules=scenario_model.world_rules or {},
            survival_mechanics=scenario_model.survival_mechanics or {},
            possible_events=scenario_model.possible_events or [],
            ending_conditions=scenario_model.ending_conditions or {},
            narrative_style=scenario_model.narrative_style,
            is_custom=True
        )


# 全局场景加载器
scenario_loader = ScenarioLoader()
