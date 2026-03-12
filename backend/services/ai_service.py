# backend/services/ai_service.py
import os
import json
import re
import asyncio
from concurrent.futures import ThreadPoolExecutor
from anthropic import Anthropic
from typing import Dict, List, Optional
from models.scenario import ScenarioSeed
from models.game import PlayerState, PlayerAction
from models.novel import NovelSkeleton, ChapterRequest


class AIService:
    """Claude API服务"""

    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        self.default_api_key = api_key
        self.model = "claude-3-5-sonnet-20241022"
        self._executor = ThreadPoolExecutor(max_workers=4)

    def _get_client(self, api_key: str = None) -> Anthropic:
        """获取 API 客户端"""
        key = api_key or self.default_api_key
        if not key:
            raise ValueError("API key is required. Please set ANTHROPIC_API_KEY in .env or provide it when creating a game.")
        return Anthropic(api_key=key)

    async def generate_turn_response(
        self,
        scenario: ScenarioSeed,
        player_state: PlayerState,
        player_action: PlayerAction,
        context: str,
        history_summary: str = "",
        api_key: str = None
    ) -> Dict:
        """生成游戏回合响应"""
        loop = asyncio.get_event_loop()

        def _generate():
            client = self._get_client(api_key)
            system_prompt = self._build_game_system_prompt(scenario, player_state)
            user_message = self._build_turn_user_message(
                scenario, player_action, context, history_summary
            )

            response = client.messages.create(
                model=self.model,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
                temperature=0.8
            )

            content = response.content[0].text
            return self._parse_game_response(content)

        return await loop.run_in_executor(self._executor, _generate)

    def _build_game_system_prompt(self, scenario: ScenarioSeed, player_state: PlayerState) -> str:
        """构建游戏系统提示词"""
        return f"""你是末世生存游戏的AI叙事引擎。

【场景设定】
{scenario.premise}

【世界规则】
{json.dumps(scenario.world_rules, ensure_ascii=False, indent=2)}

【生存机制】
{json.dumps(scenario.survival_mechanics, ensure_ascii=False, indent=2)}

【叙事风格】
{scenario.narrative_style}

【玩家当前状态】
生命: {player_state.health}/100
饥饿: {player_state.hunger}/100
口渴: {player_state.thirst}/100
体温: {player_state.temperature}°C
精神: {player_state.sanity}/100

【你的任务】
根据玩家行动,生成:
1. 沉浸式的故事描述(200-400字)
2. 合理的属性变化(基于行为后果)
3. 3个有趣的选项供玩家选择
4. 判断是否为关键事件(重要情节转折)

【关键事件判定标准】
- 首次遇到重要NPC
- 重大环境变化
- 属性到达临界点(生命<20%,精神<30%等)
- 获得重要物品
- 玩家遭遇重大危机或转机

【响应格式】
请按以下格式响应(在XML标签内):
<narrative>
故事描述内容...
</narrative>
<state_changes>
{{"health": -5, "sanity": -3}}
</state_changes>
<options>
A. 选项描述
B. 选项描述
C. 选项描述
</options>
<is_key_event>
true/false
</is_key_event>
"""

    def _build_turn_user_message(
        self,
        scenario: ScenarioSeed,
        player_action: PlayerAction,
        context: str,
        history_summary: str
    ) -> str:
        """构建回合用户消息"""
        return f"""【当前情境】
{context}

【玩家行动】
{player_action.action}

{f"【之前情节摘要】\n{history_summary}" if history_summary else ""}

请生成响应。"""

    def _parse_game_response(self, content: str) -> Dict:
        """解析游戏响应"""
        narrative = ""
        state_changes = {}
        options = []
        is_key_event = False

        # 提取narrative
        narrative_match = re.search(r'<narrative>(.*?)</narrative>', content, re.DOTALL)
        if narrative_match:
            narrative = narrative_match.group(1).strip()

        # 提取state_changes
        changes_match = re.search(r'<state_changes>(.*?)</state_changes>', content, re.DOTALL)
        if changes_match:
            try:
                state_changes = json.loads(changes_match.group(1).strip())
            except (json.JSONDecodeError, KeyError):
                pass

        # 提取options
        options_match = re.search(r'<options>(.*?)</options>', content, re.DOTALL)
        if options_match:
            options_text = options_match.group(1).strip()
            options = [line.strip().lstrip("ABCDEF.") for line in options_text.split('\n') if line.strip()]

        # 提取is_key_event
        event_match = re.search(r'<is_key_event>(.*?)</is_key_event>', content, re.DOTALL)
        if event_match:
            is_key_event = event_match.group(1).strip().lower() == "true"

        return {
            "narrative": narrative or content,
            "state_changes": state_changes,
            "options": options,
            "is_key_event": is_key_event
        }

    async def generate_novel_skeleton(
        self,
        scenario: ScenarioSeed,
        player_background: str = "",
        api_key: str = None
    ) -> NovelSkeleton:
        """生成小说骨架"""
        loop = asyncio.get_event_loop()

        def _generate():
            client = self._get_client(api_key)
            system_prompt = f"""你是末世小说的架构师。根据游戏场景生成小说骨架。

【场景信息】
类型: {scenario.name}
设定: {scenario.premise}
风格: {scenario.narrative_style}

【任务】
生成一个5-7章的小说骨架,包含:
1. 核心冲突和主题
2. 每章预期的事件和情节
3. 主角的成长弧线

请以JSON格式返回:
{{
  "premise": "小说前提",
  "estimated_chapters": 5,
  "chapter_outlines": [
    {{"chapter": 1, "title": "章名", "event_hint": "预期事件", "theme": "主题"}}
  ],
  "narrative_style": "{scenario.narrative_style}",
  "main_character_arc": "主角成长弧线描述"
}}"""

            response = client.messages.create(
                model=self.model,
                max_tokens=1500,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": f"玩家背景: {player_background}\n\n请生成小说骨架。"
                }],
                temperature=0.7
            )

            content = response.content[0].text

            # 尝试提取JSON
            try:
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    content = json_match.group(1)
                else:
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(0)

                skeleton_data = json.loads(content)
                return NovelSkeleton(**skeleton_data)
            except (json.JSONDecodeError, ValueError, KeyError):
                # 返回默认骨架
                return NovelSkeleton(
                    premise=scenario.premise,
                    estimated_chapters=5,
                    chapter_outlines=[
                        {"chapter": i, "title": f"第{i}章", "event_hint": "待定", "theme": "生存"}
                        for i in range(1, 6)
                    ],
                    narrative_style=scenario.narrative_style,
                    main_character_arc="末世中的求生与成长"
                )

        return await loop.run_in_executor(self._executor, _generate)

    async def generate_chapter(
        self,
        request: ChapterRequest,
        skeleton: NovelSkeleton,
        scenario: ScenarioSeed,
        api_key: str = None
    ) -> str:
        """生成单个小说章节"""
        client = self._get_client(api_key)
        chapter_info = skeleton.chapter_outlines[request.chapter_num - 1] if request.chapter_num <= len(skeleton.chapter_outlines) else {}

        system_prompt = f"""你是末世小说作家,正在撰写《末世生存》第{request.chapter_num}章。

【小说骨架】
前提: {skeleton.premise}
风格: {skeleton.narrative_style}
主角弧线: {skeleton.main_character_arc}

【本章大纲】
{json.dumps(chapter_info, ensure_ascii=False, indent=2)}

【写作要求】
1. 纯文学化,绝不要出现数值描述(如"生命值-10")
2. 重点描写:感官体验、内心活动、环境氛围
3. 用"展示而非讲述"的手法
4. 保持与前文的连贯性
5. 字数:1000-1500字
6. 根据游戏事件文学化处理,而非简单记录

【文学化转化示例】
游戏数据: "生命值下降,感到虚弱"
小说描写: "视线开始模糊,每一次呼吸都像是有刀片在肺里切割。他靠在墙上,冷汗浸透了后背。"

游戏数据: "精神值下降,产生幻觉"
小说描写: "阴影在墙角蠕动。他眨了眨眼,那东西又不见了——是幻觉吗?还是有什么东西在暗中窥视?"

【当前事件】
{request.event_context}"""

        messages = [{"role": "user", "content": "请撰写这一章节。"}]

        # 如果有上一章,添加作为参考
        if request.previous_chapter:
            messages.insert(0, {
                "role": "assistant",
                "content": f"【上一章内容】\n{request.previous_chapter}"
            })

        response = client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=system_prompt,
            messages=messages,
            temperature=0.9
        )

        content = response.content[0].text
        return content

        # 在异步函数中需要使用 executor
        loop = asyncio.get_event_loop()

        def _generate():
            client = self._get_client(api_key)
            chapter_info = skeleton.chapter_outlines[request.chapter_num - 1] if request.chapter_num <= len(skeleton.chapter_outlines) else {}

            system_prompt = f"""你是末世小说作家,正在撰写《末世生存》第{request.chapter_num}章。

【小说骨架】
前提: {skeleton.premise}
风格: {skeleton.narrative_style}
主角弧线: {skeleton.main_character_arc}

【本章大纲】
{json.dumps(chapter_info, ensure_ascii=False, indent=2)}

【写作要求】
1. 纯文学化,绝不要出现数值描述(如"生命值-10")
2. 重点描写:感官体验、内心活动、环境氛围
3. 用"展示而非讲述"的手法
4. 保持与前文的连贯性
5. 字数:1000-1500字
6. 根据游戏事件文学化处理,而非简单记录

【文学化转化示例】
游戏数据: "生命值下降,感到虚弱"
小说描写: "视线开始模糊,每一次呼吸都像是有刀片在肺里切割。他靠在墙上,冷汗浸透了后背。"

游戏数据: "精神值下降,产生幻觉"
小说描写: "阴影在墙角蠕动。他眨了眨眼,那东西又不见了——是幻觉吗?还是有什么东西在暗中窥视?"

【当前事件】
{request.event_context}"""

            messages = [{"role": "user", "content": "请撰写这一章节。"}]

            # 如果有上一章,添加作为参考
            if request.previous_chapter:
                messages.insert(0, {
                    "role": "assistant",
                    "content": f"【上一章内容】\n{request.previous_chapter}"
                })

            response = client.messages.create(
                model=self.model,
                max_tokens=3000,
                system=system_prompt,
                messages=messages,
                temperature=0.9
            )

            content = response.content[0].text
            return content

        return await loop.run_in_executor(self._executor, _generate)


# 全局AI服务实例
ai_service = AIService()
