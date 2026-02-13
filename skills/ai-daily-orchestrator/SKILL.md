---
name: ai-daily-orchestrator
description: AI 日报完整工作流编排。从飞书文档到小程序上线的一条龙流程。触发词：日报流程、orchestrator、完整流程、一条龙。
---

# AI Daily Orchestrator

AI 日报完整发布流程编排。

## 完整 Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│  Phase 1: 素材准备                                           │
├─────────────────────────────────────────────────────────────┤
│  飞书文档 (推文链接)                                          │
│      ↓                                                      │
│  ai-daily-filter (筛选排序)                                  │
│      ↓ 输出：优先级排序后的 URL 列表                           │
│  extract-from-x-url (内容提取)                               │
│      ↓ 输出：processed/YYYY-MM-DD.md                        │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 截图采集                                           │
├─────────────────────────────────────────────────────────────┤
│  playwright-screenshot (推文截图)                            │
│      ↓ 输出：screenshots/YYYY-MM-DD/*.png                   │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 发布 (ai-daily-publish)                           │
├─────────────────────────────────────────────────────────────┤
│  md-to-html (HTML 生成)                                     │
│      ↓ 输出：processed/output/ai_posts_summary_YYYY-MM-DD.html│
│                                                             │
│  ⏸️ 确认门禁 ← 暂停等待用户说"发射"                            │
│                                                             │
│  ai-daily-upload (OSS 上传)                                 │
│      ↓ PNG→WebP 转换，上传到阿里云                            │
│  ai-daily-upload (小程序同步)                                │
│      ↓ 同步到微信云数据库                                     │
│                                                             │
│  ✅ Go Production!                                          │
└─────────────────────────────────────────────────────────────┘
```

## Skills 职责表

| 阶段 | Skill | 输入 | 输出 |
|------|-------|------|------|
| 筛选 | `ai-daily-filter` | 飞书文档/URL 列表 | 优先级排序后的 URL |
| 提取 | `extract-from-x-url` | URL 列表 | `processed/YYYY-MM-DD.md` |
| 截图 | `playwright-screenshot` | 推文 URL | `screenshots/YYYY-MM-DD/*.png` |
| HTML | `md-to-html` | Markdown | `processed/output/*.html` |
| 上传 | `ai-daily-upload` | HTML + 截图 | OSS + 云数据库 |

## 目录结构

```
workspace/ai-news/
├── processed/                    # Markdown 输出
│   ├── YYYY-MM-DD.md            # 结构化摘要
│   └── output/                  # HTML 输出
│       ├── ai_posts_summary_YYYY-MM-DD.html
│       └── style.css
├── screenshots/                  # 截图
│   └── YYYY-MM-DD/
│       ├── 01-xxx.png
│       └── 02-xxx.png
└── assets/                       # 静态资源
    └── 小禾说AI logo.png
```

## 执行命令

### Phase 1: 筛选 + 提取
```
用户提供飞书文档 → ai-daily-filter 筛选 → extract-from-x-url 提取
```

### Phase 2: 截图
```powershell
# 使用 playwright-screenshot skill
# 详见 skills/playwright-screenshot/SKILL.md
```

### Phase 3: 发布
```powershell
# Step 1: 生成 HTML (md-to-html skill)

# ⏸️ 等待用户确认

# Step 2: 上传 OSS
cd C:\Users\taoli1\ai-daily-uploader
uv run python upload_openclaw.py YYYY-MM-DD

# Step 3: 同步小程序
node v3/pipeline.js YYYYMMDD
```

## 关键规则

### 日期规则 ⚠️
- **日报日期 = 发布当天日期**
- 例如：2月12日发布的日报，标题写 `2026/02/12`
- 文件名：`2026-02-12.md`、`ai_posts_summary_2026-02-12.html`
- 截图目录：`screenshots/2026-02-12/`

### 确认门禁
- **HTML 生成后必须暂停**
- 等待用户说"发射"、"go"、"确认"后才执行上传
- 这是 go production，必须人工确认

### 总览开场语规范
- 必须是**高层概括**（如："头部公司密集发布产品更新"）
- **禁止**罗列具体产品名（如："OpenAI连续发力，Deep Research升级..."）
- 详见 `extract-from-x-url/SKILL.md`

### 截图规范
- 宽度：560px
- 包含完整 action bar（回复/转发/点赞数）
- 等待 3.5s 让翻译插件完成
- 详见 `playwright-screenshot/SKILL.md`

## 生产环境输出

| 目标 | URL |
|------|-----|
| OSS 截图 | `https://ai-daily.oss-cn-beijing.aliyuncs.com/screenshots/YYYY-MM-DD/*.webp` |
| OSS JSON | `https://ai-daily.oss-cn-beijing.aliyuncs.com/daily_reports/YYYY-MM-DD.json` |
| 小程序 | 微信云数据库 `daily_reports/YYYY-MM-DD` |

## 快捷触发

用户可以说：
- "帮我做今天的日报"（完整流程）
- "筛选这些推文"（Phase 1）
- "截图这些链接"（Phase 2）
- "发布日报"（Phase 3）
- "发射"（确认后继续上传）
