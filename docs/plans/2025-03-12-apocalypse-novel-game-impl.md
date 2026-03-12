# 末世生存小说生成器 - 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 构建一个末世题材的互动游戏系统，玩家在游戏中自由行动，AI根据行为实时生成对应情节的小说章节。

**Architecture:** 前后端分离，React前端 + FastAPI后端，Claude API负责内容生成。游戏数据文学化转化，关键事件触发小说章节生成。

**Tech Stack:**
- 前端: React + Vite + TailwindCSS + Zustand + react-markdown
- 后端: FastAPI + SQLAlchemy + SQLite + Anthropic SDK
- AI: Claude API (claude-opus-4-6)

---

## Phase 1: 项目初始化

### Task 1: 克隆仓库并设置基础结构

**Files:**
- Create: `/home/pan/Develop/小说生成器/` (整个项目结构)
- Create: `README.md`

**Step 1: 克隆远程仓库**

```bash
cd /home/pan/Develop
git clone git@github.com:Panyuxiang0830/ai-game-novel.git 小说生成器
cd 小说生成器
```

**Step 2: 创建项目目录结构**

```bash
mkdir -p backend/{models,services,scenarios/{presets,custom},database,migrations}
mkdir -p frontend/src/{components,pages,hooks,lib,styles}
mkdir -p docs
touch backend/.gitkeep frontend/.gitkeep
```

**Step 3: 创建项目README**

```markdown
# 末世生存小说生成器

一个结合末世生存游戏和AI实时小说生成的互动体验系统。

## 技术栈

- 前端: React + Vite + TailwindCSS
- 后端: FastAPI + SQLite
- AI: Claude API

## 快速开始

### 后端

\`\`\`bash
cd backend
pip install -r requirements.txt
python main.py
\`\`\`

### 前端

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

## 项目结构

\`\`\`
小说生成器/
├── backend/          # FastAPI后端
├── frontend/         # React前端
└── docs/            # 文档
\`\`\`
```

**Step 4: 提交初始结构**

```bash
git add README.md
git commit -m "feat: initialize project structure

- Create backend and frontend directories
- Add project README

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 2: 后端依赖配置

**Files:**
- Create: `backend/requirements.txt`

**Step 1: 创建 requirements.txt**

```txt
# FastAPI and server
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.0

# Database
sqlalchemy==2.0.35
aiosqlite==0.20.0

# AI
anthropic==0.40.0

# Utilities
python-dotenv==1.0.1
pydantic-settings==2.6.0

# CORS
python-multipart==0.0.12
```

**Step 2: 创建环境变量模板**

```bash
cat > backend/.env.example << 'EOF'
# Claude API配置
ANTHROPIC_API_KEY=your_api_key_here

# 数据库配置
DATABASE_URL=sqlite+aiosqlite:///./game.db

# 服务配置
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
EOF
```

**Step 3: 提交**

```bash
git add backend/requirements.txt backend/.env.example
git commit -m "feat: add backend dependencies

- Add FastAPI, SQLAlchemy, Anthropic SDK
- Add environment variable template

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3: 前端项目初始化

**Files:**
- Create: `frontend/`

**Step 1: 创建Vite + React项目**

```bash
cd /home/pan/Develop/小说生成器

# 使用npm create创建项目
npm create vite@latest frontend -- --template react-ts

cd frontend
npm install
```

**Step 2: 安装前端依赖**

```bash
cd frontend

# 状态管理
npm install zustand

# 样式
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Markdown渲染
npm install react-markdown

# 路由
npm install react-router-dom

# HTTP客户端
npm install axios

# 图标
npm install lucide-react
```

**Step 3: 配置TailwindCSS**

创建 `frontend/tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 末世主题色
        apocalypse: {
          bg: '#0a0a0f',
          card: '#12121a',
          border: '#1e1e2e',
          text: '#e0e0e0',
          muted: '#6b6b7b',
          danger: '#ff4757',
          warning: '#ffa502',
          success: '#2ed573',
        }
      }
    },
  },
  plugins: [],
}
```

修改 `frontend/src/index.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-apocalypse-bg text-apocalypse-text;
  }
}
```

**Step 4: 提交**

```bash
git add frontend/
git commit -m "feat: initialize frontend with Vite + React + TailwindCSS

- Setup Vite + React + TypeScript
- Add TailwindCSS with apocalypse theme
- Add zustand, react-router-dom, react-markdown, axios

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 2: 后端核心

### Task 4: 数据模型定义

**Files:**
- Create: `backend/models/__init__.py`
- Create: `backend/models/scenario.py`
- Create: `backend/models/game.py`
- Create: `backend/models/novel.py`

**Step 1: 创建场景模型**

```python
# backend/models/scenario.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional


class ScenarioSeed(BaseModel):
    """场景种子模型"""
    id: str = Field(..., description="场景唯一标识")
    name: str = Field(..., description="场景名称")
    description: str = Field(..., description="场景描述")
    premise: str = Field(..., description="世界背景设定")
    world_rules: Dict = Field(default_factory=dict, description="世界规则")
    survival_mechanics: Dict = Field(default_factory=dict, description="生存机制")
    possible_events: List[str] = Field(default_factory=list, description="可能发生的事件")
    ending_conditions: Dict = Field(default_factory=dict, description="结局条件")
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
```

**Step 2: 创建玩家状态模型**

```python
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
```

**Step 3: 创建小说模型**

```python
# backend/models/novel.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class NovelSkeleton(BaseModel):
    """小说骨架"""
    premise: str = Field(..., description="小说前提")
    estimated_chapters: int = Field(default=5, ge=3, le=10)
    chapter_outlines: List[Dict] = Field(default_factory=list, description="章节大纲")
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
    status: str = Field(default="pending", description="pending, generating, completed")


class NovelProject(BaseModel):
    """小说项目"""
    novel_id: str
    session_id: str
    scenario_id: str
    skeleton: Optional[NovelSkeleton] = None
    chapters: List[NovelChapter] = Field(default_factory=list)
    total_words: int = Field(default=0)
    status: str = Field(default="in_progress", description="in_progress, completed")
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class ChapterRequest(BaseModel):
    """章节生成请求"""
    novel_id: str
    chapter_num: int
    event_context: str = Field(..., description="当前事件上下文")
    previous_chapter: Optional[str] = None
```

**Step 4: 提交**

```bash
git add backend/models/
git commit -m "feat: define core data models

- Add ScenarioSeed and ScenarioConfig
- Add PlayerState with 15+ attributes
- Add GameState, GameTurn, PlayerAction
- Add NovelProject, NovelChapter, NovelSkeleton

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 5: 数据库设置

**Files:**
- Create: `backend/database/db.py`
- Create: `backend/database/__init__.py`

**Step 1: 创建数据库连接**

```python
# backend/database/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from contextlib import asynccontextmanager
import os


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./game.db")

        self.engine = create_async_engine(
            database_url,
            echo=False,
        )
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def init_db(self):
        """初始化数据库表"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


# 全局数据库实例
db = Database()


async def get_db():
    """依赖注入：获取数据库会话"""
    async with db.get_session() as session:
        yield session
```

**Step 2: 创建数据库模型（ORM）**

```python
# backend/database/models.py
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class SessionModel(Base):
    """游戏会话表"""
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    scenario_id = Column(String, nullable=False)
    player_state = Column(JSON, nullable=False)
    current_location = Column(String)
    time_elapsed = Column(Integer, default=0)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now)
    ended_at = Column(DateTime, nullable=True)

    # 关联
    turns = relationship("GameTurnModel", back_populates="session", cascade="all, delete-orphan")
    novel = relationship("NovelModel", back_populates="session", uselist=False, cascade="all, delete-orphan")


class GameTurnModel(Base):
    """游戏回合表"""
    __tablename__ = "game_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, nullable=False)
    turn_num = Column(Integer, nullable=False)
    player_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    state_changes = Column(JSON)
    items_gained = Column(JSON)
    items_lost = Column(JSON)
    is_key_event = Column(Boolean, default=False)
    event_type = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

    # 关联
    session = relationship("SessionModel", back_populates="turns")


class NovelModel(Base):
    """小说项目表"""
    __tablename__ = "novels"

    id = Column(String, primary_key=True)
    session_id = Column(String, nullable=False)
    scenario_id = Column(String, nullable=False)
    skeleton = Column(JSON)
    status = Column(String, default="in_progress")
    total_words = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    # 关联
    session = relationship("SessionModel", back_populates="novel")
    chapters = relationship("ChapterModel", back_populates="novel", cascade="all, delete-orphan")


class ChapterModel(Base):
    """小说章节表"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    novel_id = Column(String, nullable=False)
    chapter_num = Column(Integer, nullable=False)
    title = Column(String)
    event_title = Column(String)
    content = Column(Text)
    word_count = Column(Integer, default=0)
    status = Column(String, default="pending")
    generated_at = Column(DateTime, nullable=True)

    # 关联
    novel = relationship("NovelModel", back_populates="chapters")


class ScenarioModel(Base):
    """自定义场景表"""
    __tablename__ = "scenarios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    premise = Column(Text, nullable=False)
    world_rules = Column(JSON)
    survival_mechanics = Column(JSON)
    possible_events = Column(JSON)
    ending_conditions = Column(JSON)
    narrative_style = Column(String)
    is_custom = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
```

**Step 3: 提交**

```bash
git add backend/database/
git commit -m "feat: setup database with SQLAlchemy

- Add async SQLite connection
- Add ORM models for sessions, turns, novels, chapters
- Add scenario storage for custom scenarios

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 6: 场景种子数据

**Files:**
- Create: `backend/scenarios/presets/ice_age.json`
- Create: `backend/scenarios/presets/zombie.json`
- Create: `backend/scenarios/presets/nuclear.json`
- Create: `backend/scenarios/__init__.py`

**Step 1: 创建全球冰封场景**

```json
{
  "id": "ice_age",
  "name": "全球冰封",
  "description": "太阳活动异常，地球进入新冰河期，全球平均气温降至-40°C，人类文明在严寒中崩溃。",
  "premise": "202X年，太阳活动突然异常减弱。短短半年内，全球平均气温骤降至-40°C。大部分地区被永久冰雪覆盖，电力系统瘫痪，供暖设施停摆。幸存者们躲在废墟中，争夺着越来越少的燃料和食物。你在一座废弃的商业大楼地下仓库中苏醒，这里曾是紧急避难所，如今物资告急，你必须离开这里寻找新的生存希望。",
  "world_rules": {
    "temperature": "-40°C ~ -60°C，极端情况可达-80°C",
    "daylight": "极昼极夜交替，每次持续数周",
    "resources": "极度稀缺，优先级：燃料>食物>水>武器",
    "shelter": "必须寻找有热源的避难所",
    "threats": ["严寒", "冻伤", "雪盲症", "掠夺者", "雪地野兽"]
  },
  "survival_mechanics": {
    "体温": "核心生存属性，暴露室外每回合下降5-10°C，低于30°C开始扣除生命值",
    "饥饿": "食物极度稀缺，搜刮困难，饥饿值下降速度加快50%",
    "口渴": "水源冻结，需要融化冰雪才能饮用",
    "精神": "长期黑暗和孤独导致精神值下降，极夜期间加速",
    "取暖": "需要燃料维持体温，燃料耗尽后体温快速下降"
  },
  "possible_events": [
    "发现避难所遗迹",
    "遇到其他幸存者",
    "暴风雪来袭",
    "物资耗尽被迫转移",
    "发现燃料储备",
    "遭遇掠夺者",
    "野兽袭击",
    "体温过低",
    "发现其他幸存者的营地",
    "找到热源（地热/核废热）"
  ],
  "ending_conditions": {
    "death": ["冻死", "饿死", "渴死", "被掠夺者杀死", "被野兽杀死"],
    "victory": ["找到有稳定热源的永久避难所", "逃离到赤道地区", "建立自己的幸存者营地"]
  },
  "narrative_style": "冷酷、绝望、人性考验。重点描写严寒的残酷、生存的艰难、以及在极端环境下人性的光辉与阴暗面。"
}
```

**Step 2: 创建丧尸末世场景**

```json
{
  "id": "zombie",
  "name": "丧尸末世",
  "description": "未知病毒爆发，感染者变成嗜血丧尸。文明在短短数周内崩溃，幸存者在丧尸横行的世界中艰难求生。",
  "premise": "一种被称为'狂暴病毒'的病原体在全球范围内爆发。感染者会在数小时内变成嗜血的丧尸，通过咬伤传播病毒。短短一个月，全球秩序崩塌，90%的人口变成丧尸或死去。你在一家医院的隔离病房中醒来，这里是丧尸爆发初期的临时隔离点，如今已是一片死寂。你必须在这片丧尸横行的废土中寻找出路。",
  "world_rules": {
    "infection": "被丧尸抓伤或咬伤有感染风险",
    "horde": "丧尸会聚集成群，声音和气味会吸引它们",
    "daylight": "夜间丧尸更活跃，但也有夜视能力的变异种",
    "resources": "稀缺，优先级：武器>药品>食物>水",
    "shelter": "需要加固的避难所，防止丧尸突破"
  },
  "survival_mechanics": {
    "感染": "受伤后有感染概率，感染后每回合扣除生命值和精神值，需要抗生素",
    "饥饿": "食物相对容易获取但风险高",
    "精神": "目睹丧尸和死亡会降低精神值",
    "战斗": "近战有感染风险，远程需要弹药",
    "潜行": "避免战斗是最佳策略"
  },
  "possible_events": [
    "丧尸群逼近",
    "发现幸存者聚落",
    "被丧尸围困",
    "发现武器库",
    "遇到武装幸存者",
    "感染症状出现",
    "发现疫苗线索",
    "避难所被攻破",
    "遇到不怀好意的幸存者",
    "发现无线电信号"
  ],
  "ending_conditions": {
    "death": ["被丧尸咬死", "感染死亡", "饿死", "被幸存者杀死"],
    "victory": ["找到真正的免疫疫苗", "到达传说中的安全区", "建立大型幸存者基地"]
  },
  "narrative_style": "紧张恐怖、生存本能。重点描写丧尸的恐怖、生存的压力、以及末世中人与人之间复杂的关系。"
}
```

**Step 3: 创建核战废墟场景**

```json
{
  "id": "nuclear",
  "name": "核战废墟",
  "description": "核战争摧毁了现代文明，辐射尘埃覆盖大地。幸存者在辐射废土中挣扎求生，寻找着没有污染的净土。",
  "premise": "2030年，一场核战争摧毁了现代文明。数万枚核弹在城市上空爆炸，城市化为废墟，辐射尘埃覆盖全球。大部分人类在核爆中死亡或因辐射病死去。你在深山中的一个废弃防空洞中苏醒，这里曾是一座军事基地，如今只剩下你一个幸存者。传说在遥远的某个地方，有一片没有辐射的净土，你决定踏上寻找的旅程。",
  "world_rules": {
    "radiation": "辐射无处不在，需要盖革计数器监测",
    "zones": "分为高辐射区（死亡）、中辐射区（危险）、低辐射区（相对安全）",
    "water": "大部分水源被辐射污染",
    "mutation": "长期辐射会导致生物变异",
    "resources": "极度稀缺，优先级：防辐射装备>纯净水源>食物>药品"
  },
  "survival_mechanics": {
    "辐射": "核心生存属性，高辐射区每回合大幅增加辐射值",
    "抗辐射": "需要防辐射装备和碘片",
    "变异": "辐射值过高会触发随机变异（正向或负向）",
    "净化": "需要特殊的净化设备或药物降低辐射值",
    "水源": "必须使用辐射检测仪检测水源"
  },
  "possible_events": [
    "进入高辐射区",
    "发现变异生物",
    "找到防辐射装备",
    "辐射症状加重",
    "发现未被污染的水源",
    "遇到拾荒者团体",
    "发现旧世界科技",
    "触发身体变异",
    "发现军事掩体",
    "获得辐射净化剂"
  ],
  "ending_conditions": {
    "death": ["辐射病死亡", "饿死", "渴死", "被变异生物杀死", "被拾荒者杀死"],
    "victory": ["到达无辐射的净土", "获得完整抗辐射改造", "建立自己的辐射防护基地"]
  },
  "narrative_style": "苍凉悲壮、文明反思。重点描写核战的残酷后果、辐射的恐怖、以及人类在毁灭后对文明的反思和对希望的追寻。"
}
```

**Step 4: 创建场景加载器**

```python
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
```

**Step 5: 提交**

```bash
git add backend/scenarios/
git commit -m "feat: add preset scenario seeds

- Add ice_age: global freezing scenario
- Add zombie: zombie apocalypse scenario
- Add nuclear: nuclear wasteland scenario
- Add ScenarioLoader for loading presets and custom scenarios

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Phase 3: 游戏引擎

### Task 7: AI服务层

**Files:**
- Create: `backend/services/ai_service.py`

**Step 1: 创建AI服务**

```python
# backend/services/ai_service.py
import os
from anthropic import Anthropic
from typing import Dict, List, Optional
from ..models.scenario import ScenarioSeed
from ..models.game import PlayerState, PlayerAction
from ..models.novel import NovelSkeleton, ChapterRequest


class AIService:
    """Claude API服务"""

    def __init__(self, api_key: str = None):
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-opus-4-6"

    async def generate_turn_response(
        self,
        scenario: ScenarioSeed,
        player_state: PlayerState,
        player_action: PlayerAction,
        context: str,
        history_summary: str = ""
    ) -> Dict:
        """生成游戏回合响应

        Returns:
            Dict with keys:
            - narrative: str - 故事描述
            - state_changes: Dict - 属性变化
            - options: List[str] - 选项
            - is_key_event: bool - 是否关键事件
        """
        system_prompt = self._build_game_system_prompt(scenario, player_state)
        user_message = self._build_turn_user_message(
            scenario, player_action, context, history_summary
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.8
        )

        # 解析响应
        content = response.content[0].text
        return self._parse_game_response(content)

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
根据玩家行动，生成：
1. 沉浸式的故事描述（200-400字）
2. 合理的属性变化（基于行为后果）
3. 3个有趣的选项供玩家选择
4. 判断是否为关键事件（重要情节转折）

【关键事件判定标准】
- 首次遇到重要NPC
- 重大环境变化
- 属性到达临界点（生命<20%，精神<30%等）
- 获得重要物品
- 玩家遭遇重大危机或转机

【响应格式】
请按以下格式响应（在XML标签内）：
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
        import re

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
                import json
                state_changes = json.loads(changes_match.group(1).strip())
            except:
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
            "narrative": narrative or content,  # 如果解析失败，返回原始内容
            "state_changes": state_changes,
            "options": options,
            "is_key_event": is_key_event
        }

    async def generate_novel_skeleton(
        self,
        scenario: ScenarioSeed,
        player_background: str = ""
    ) -> NovelSkeleton:
        """生成小说骨架"""
        system_prompt = f"""你是末世小说的架构师。根据游戏场景生成小说骨架。

【场景信息】
类型: {scenario.name}
设定: {scenario.premise}
风格: {scenario.narrative_style}

【任务】
生成一个5-7章的小说骨架，包含：
1. 核心冲突和主题
2. 每章预期的事件和情节
3. 主角的成长弧线

请以JSON格式返回：
{{
  "premise": "小说前提",
  "estimated_chapters": 5,
  "chapter_outlines": [
    {{"chapter": 1, "title": "章名", "event_hint": "预期事件", "theme": "主题"}}
  ],
  "narrative_style": "{scenario.narrative_style}",
  "main_character_arc": "主角成长弧线描述"
}}"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=system_prompt,
            messages=[{
                "role": "user",
                "content": f"玩家背景: {player_background}\n\n请生成小说骨架。"
            }],
            temperature=0.7
        )

        import json
        content = response.content[0].text

        # 尝试提取JSON
        try:
            # 查找JSON代码块
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # 尝试直接解析
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    content = json_match.group(0)

            skeleton_data = json.loads(content)
            return NovelSkeleton(**skeleton_data)
        except:
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

    async def generate_chapter(
        self,
        request: ChapterRequest,
        skeleton: NovelSkeleton,
        scenario: ScenarioSeed
    ) -> str:
        """生成单个小说章节（独立AI实例）"""
        # 获取上下文信息（骨架 + 上一章 + 当前事件）
        context_info = self._build_chapter_context(request, skeleton, scenario)

        system_prompt = f"""你是末世小说作家，正在撰写《末世生存》第{request.chapter_num}章。

【小说骨架】
前提: {skeleton.premise}
风格: {skeleton.narrative_style}
主角弧线: {skeleton.main_character_arc}

【本章大纲】
{skeleton.chapter_outlines[request.chapter_num - 1] if request.chapter_num <= len(skeleton.chapter_outlines) else {}}

【写作要求】
1. 纯文学化，绝不要出现数值描述（如"生命值-10"）
2. 重点描写：感官体验、内心活动、环境氛围
3. 用"展示而非讲述"的手法
4. 保持与前文的连贯性
5. 字数：1000-1500字
6. 根据游戏事件文学化处理，而非简单记录

【文学化转化示例】
游戏数据: "生命值下降，感到虚弱"
小说描写: "视线开始模糊，每一次呼吸都像是有刀片在肺里切割。他靠在墙上，冷汗浸透了后背。"

游戏数据: "精神值下降，产生幻觉"
小说描写: "阴影在墙角蠕动。他眨了眨眼，那东西又不见了——是幻觉吗？还是有什么东西在暗中窥视？"

【当前事件】
{request.event_context}"""

        messages = [{"role": "user", "content": "请撰写这一章节。"}]

        # 如果有上一章，添加作为参考
        if request.previous_chapter:
            messages.insert(0, {
                "role": "assistant",
                "content": f"【上一章内容】\n{request.previous_chapter}"
            })

        response = self.client.messages.create(
            model=self.model,
            max_tokens=3000,
            system=system_prompt,
            messages=messages,
            temperature=0.9
        )

        content = response.content[0].text
        return content

    def _build_chapter_context(
        self,
        request: ChapterRequest,
        skeleton: NovelSkeleton,
        scenario: ScenarioSeed
    ) -> str:
        """构建章节生成上下文"""
        context = {
            "scenario": scenario.name,
            "premise": scenario.premise,
            "chapter_num": request.chapter_num,
            "event": request.event_context
        }
        return str(context)


# 全局AI服务实例
ai_service = AIService()
```

**Step 2: 提交**

```bash
git add backend/services/ai_service.py
git commit -m "feat: implement AI service layer

- Add generate_turn_response for game interaction
- Add generate_novel_skeleton for story structure
- Add generate_chapter for literary chapter generation
- Implement literary transformation from game data

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 实施计划说明

以上是前7个任务的详细实施步骤。由于计划较长，剩余任务将在后续阶段继续完成：

- **Phase 3剩余**: 游戏引擎实现、小说引擎实现
- **Phase 4**: 后端API路由
- **Phase 5**: 前端组件实现
- **Phase 6**: 前后端集成
- **Phase 7**: 测试和文档

每个任务都遵循TDD原则，包含测试、实现、提交的完整流程。
