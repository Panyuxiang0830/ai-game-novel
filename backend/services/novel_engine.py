# backend/services/novel_engine.py
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from models.scenario import ScenarioSeed
from models.game import GameState, GameTurn
from models.novel import (
    NovelProject, NovelSkeleton, NovelChapter,
    ChapterRequest, NovelStatus, ChapterStatus
)
from services.ai_service import ai_service


class NovelEngine:
    """小说引擎 - 处理小说项目创建和章节生成"""

    def __init__(self):
        self._projects: Dict[str, NovelProject] = {}
        self._api_keys: Dict[str, str] = {}  # novel_id -> api_key

    def set_api_key(self, novel_id: str, api_key: str) -> None:
        """设置小说项目的 API key"""
        self._api_keys[novel_id] = api_key

    def get_api_key(self, novel_id: str) -> Optional[str]:
        """获取小说项目的 API key"""
        return self._api_keys.get(novel_id)

    async def create_project(
        self,
        session_id: str,
        scenario: ScenarioSeed,
        player_background: str = "",
        api_key: str = None
    ) -> NovelProject:
        """创建小说项目"""
        novel_id = str(uuid.uuid4())

        # 存储 API key
        if api_key:
            self._api_keys[novel_id] = api_key

        # 生成小说骨架
        skeleton = await ai_service.generate_novel_skeleton(
            scenario=scenario,
            player_background=player_background,
            api_key=api_key
        )

        # 创建章节占位符
        chapters = []
        for i in range(1, skeleton.estimated_chapters + 1):
            outline = skeleton.chapter_outlines[i - 1] if i <= len(skeleton.chapter_outlines) else {}
            chapter = NovelChapter(
                chapter_num=i,
                title=outline.get("title", f"第{i}章"),
                event_title=outline.get("event_hint", ""),
                status=ChapterStatus.PENDING
            )
            chapters.append(chapter)

        # 创建小说项目
        project = NovelProject(
            novel_id=novel_id,
            session_id=session_id,
            scenario_id=scenario.id,
            skeleton=skeleton,
            chapters=chapters,
            status=NovelStatus.IN_PROGRESS
        )

        self._projects[novel_id] = project
        return project

    async def generate_chapter(
        self,
        novel_id: str,
        chapter_num: int,
        event_context: str,
        scenario: ScenarioSeed,
        api_key: str = None
    ) -> NovelChapter:
        """生成单个章节"""
        project = self._projects.get(novel_id)
        if not project:
            raise ValueError(f"Novel project {novel_id} not found")

        if chapter_num < 1 or chapter_num > len(project.chapters):
            raise ValueError(f"Invalid chapter number: {chapter_num}")

        chapter = project.chapters[chapter_num - 1]

        # 如果已生成，直接返回
        if chapter.status == ChapterStatus.COMPLETED:
            return chapter

        # 获取 API key
        effective_api_key = api_key or self._api_keys.get(novel_id)

        # 获取上一章内容（用于上下文）
        previous_chapter = None
        if chapter_num > 1:
            prev_chapter = project.chapters[chapter_num - 2]
            if prev_chapter.status == ChapterStatus.COMPLETED:
                previous_chapter = prev_chapter.content

        # 更新状态为生成中
        chapter.status = ChapterStatus.GENERATING

        # 构建章节请求
        request = ChapterRequest(
            novel_id=novel_id,
            chapter_num=chapter_num,
            event_context=event_context,
            previous_chapter=previous_chapter
        )

        # 调用AI生成章节
        content = await ai_service.generate_chapter(
            request=request,
            skeleton=project.skeleton,
            scenario=scenario,
            api_key=effective_api_key
        )

        # 更新章节
        chapter.content = content
        chapter.word_count = len(content)
        chapter.generated_at = datetime.now()
        chapter.status = ChapterStatus.COMPLETED

        # 更新项目总字数
        project.total_words = sum(c.word_count for c in project.chapters)

        # 检查是否所有章节完成
        if all(c.status == ChapterStatus.COMPLETED for c in project.chapters):
            project.status = NovelStatus.COMPLETED
            project.completed_at = datetime.now()

        return chapter

    def get_project(self, novel_id: str) -> Optional[NovelProject]:
        """获取小说项目"""
        return self._projects.get(novel_id)

    def get_chapter(self, novel_id: str, chapter_num: int) -> Optional[NovelChapter]:
        """获取单个章节"""
        project = self._projects.get(novel_id)
        if not project:
            return None
        if chapter_num < 1 or chapter_num > len(project.chapters):
            return None
        return project.chapters[chapter_num - 1]

    def transform_game_data_to_literary(
        self,
        turns: List[GameTurn],
        scenario: ScenarioSeed
    ) -> str:
        """将游戏数据转化为文学化描述

        用于辅助章节生成，将游戏中的数值和事件转化为文学表达
        """
        if not turns:
            return ""

        literary_parts = []

        for turn in turns:
            # 文学化玩家行动
            action_desc = self._literary_action(turn.player_input)

            # 文学化AI响应
            response_desc = turn.ai_response

            # 文学化状态变化
            state_desc = self._literary_state_changes(turn.state_changes, scenario)

            literary_parts.append(f"{action_desc}\n{response_desc}\n{state_desc}")

        return "\n\n".join(literary_parts)

    def _literary_action(self, action: str) -> str:
        """文学化玩家行动"""
        # 简单处理，实际可以用AI增强
        return f"**{action}**"

    def _literary_state_changes(self, changes: dict, scenario: ScenarioSeed) -> str:
        """文学化状态变化"""
        if not changes:
            return ""

        descriptions = []

        for attr, value in changes.items():
            if value == 0:
                continue

            attr_names = {
                "health": "生命",
                "hunger": "饥饿",
                "thirst": "口渴",
                "temperature": "体温",
                "sanity": "精神",
                "strength": "力量",
                "agility": "敏捷",
                "intelligence": "智力",
                "charisma": "魅力",
                "perception": "感知"
            }

            attr_name = attr_names.get(attr, attr)

            if value > 0:
                descriptions.append(f"{attr_name}得到了恢复")
            else:
                descriptions.append(f"{attr_name}受到了损害")

        return "、".join(descriptions) + "。" if descriptions else ""

    def list_projects(self) -> List[NovelProject]:
        """列出所有小说项目"""
        return list(self._projects.values())

    def delete_project(self, novel_id: str) -> bool:
        """删除小说项目"""
        if novel_id in self._projects:
            del self._projects[novel_id]
            return True
        return False

    def export_full_text(self, novel_id: str) -> Optional[str]:
        """导出完整小说文本"""
        project = self._projects.get(novel_id)
        if not project:
            return None

        parts = [f"# {project.skeleton.premise}\n\n"]

        for chapter in project.chapters:
            if chapter.status == ChapterStatus.COMPLETED:
                parts.append(f"## {chapter.title}\n\n")
                parts.append(chapter.content)
                parts.append("\n\n---\n\n")

        return "".join(parts)


# 全局小说引擎实例
novel_engine = NovelEngine()
