# 末世生存小说生成器

一个结合末世生存游戏和AI实时小说生成的互动体验系统。

## 特性

- 3个预设末世场景（全球冰封、丧尸末世、核战废墟）
- 玩家可自定义创建场景
- 15+属性RPG系统
- 选项引导 + 自由输入交互
- 关键事件触发小说章节生成
- 游戏数据文学化转化为小说内容

## 技术栈

- 前端: React + Vite + TailwindCSS
- 后端: FastAPI + SQLite
- AI: Claude API

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python main.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
小说生成器/
├── backend/          # FastAPI后端
│   ├── models/       # 数据模型
│   ├── services/     # 业务逻辑
│   ├── scenarios/    # 场景种子
│   └── database/     # 数据库
├── frontend/         # React前端
│   └── src/
│       ├── components/  # 组件
│       ├── pages/      # 页面
│       └── hooks/      # 自定义hooks
└── docs/            # 文档
```

## 文档

- [设计文档](docs/plans/2026-03-12-apocalypse-novel-game-design.md)
- [实施计划](docs/plans/2026-03-12-apocalypse-novel-game-impl.md)

## License

MIT
