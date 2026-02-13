---
name: ai-daily-publish
description: One-stop AI Daily publishing pipeline. Convert Markdown to HTML, upload to OSS, sync to mini-program. Activate when user wants to publish AI news, generate shareable HTML, or mentions "发布日报/AI Daily/一条龙/go production".
---

# AI Daily 一条龙发布流程

将 AI 日报从 Markdown 转换为可分享的 HTML 页面，上传到 OSS，同步到小程序。

## 完整流程

```
processed/YYYY-MM-DD.md (筛选后的 Markdown)
    ↓
① 使用 md-to-html skill 生成 HTML
    ↓
② 上传截图到 OSS (WebP 转换) + JSON
    ↓
③ 同步到微信小程序云数据库
    ↓
✅ Go Production!
```

## 触发方式

直接说：
- "帮我发布今天的 AI 日报"
- "把这个 Markdown 转成可分享的 HTML"
- "处理 2026-01-29 的 AI Daily"
- "一条龙"
- "go production"
- "上传到小程序"

## 依赖 Skills

| Skill | 作用 |
|-------|------|
| **md-to-html** | Markdown → HTML 转换 |
| **ai-daily-upload** | OSS 上传 + 小程序同步 |

## 文件位置约定

| 文件类型 | 位置 |
|----------|------|
| Markdown 源 | `ai-news/processed/YYYY-MM-DD.md` |
| 截图目录 | `ai-news/screenshots/YYYY-MM-DD/` |
| HTML 输出 | `ai-news/processed/output/ai_posts_summary_YYYY-MM-DD.html` |

## 执行步骤

### Step 1: 生成 HTML

1. 读取 `processed/YYYY-MM-DD.md`
2. 使用 `md-to-html` skill 生成 HTML
3. 保存到 `processed/output/ai_posts_summary_YYYY-MM-DD.html`

### ⏸️ 确认门禁

**生成 HTML 后必须暂停，等待用户确认！**

告知用户：
- HTML 已生成，路径是 xxx
- 请检查内容无误后说"发射"或"go"继续上传

**只有用户明确确认后，才执行 Step 2-3！**

### Step 2: 上传到 OSS（需确认后执行）

```powershell
cd C:\Users\taoli1\ai-daily-uploader
uv run python upload_openclaw.py YYYY-MM-DD
```

输出：
- 截图转为 WebP 并上传
- JSON 生成并上传
- 本地保存 `output/YYYY-MM-DD.json`

### Step 3: 同步到小程序

```powershell
node v3/pipeline.js YYYYMMDD
```

输出：
- 日报同步到微信云数据库
- statistic 更新

## 路径规则

**HTML 中引用截图**（HTML 在 `processed/output/`）：
```html
<img src="../../screenshots/2026-02-11/01-xxx.png">
```

## 生产环境输出

| 目标 | URL |
|------|-----|
| OSS 截图 | `https://ai-daily.oss-cn-beijing.aliyuncs.com/screenshots/YYYY-MM-DD/*.webp` |
| OSS JSON | `https://ai-daily.oss-cn-beijing.aliyuncs.com/daily_reports/YYYY-MM-DD.json` |
| 小程序云数据库 | `daily_reports/YYYY-MM-DD` |

## 图片优化

上传时自动：
- PNG → WebP 转换
- 最大宽度 750px
- 质量 80%
- 压缩率 40%-80%

## 注意事项

1. **顺序重要**：先 OSS 后小程序（pipeline.js 依赖 output/*.json）
2. **日期一致**：HTML 文件名、截图目录、命令参数日期必须一致
3. **生产环境**：Step 2-3 是 go production，执行前确认内容无误
4. **水印保护**：HTML 自带 6% 透明度水印
