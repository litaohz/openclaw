# AI Daily Upload Skill

上传 AI 日报到生产环境（OSS + 微信小程序云数据库）。

## 触发条件

用户提到：
- "上传日报"、"发布日报"、"deploy"、"go production"
- "上传到 OSS"、"同步小程序"
- "upload daily"、"publish daily"

## 目录结构要求

```
ai-news/
├── processed/output/ai_posts_summary_YYYY-MM-DD.html
└── screenshots/YYYY-MM-DD/*.png
```

## 使用方法

### 完整发布流程（推荐）

分两步执行：

```powershell
# Step 1: 上传截图和 JSON 到阿里云 OSS
cd C:\Users\taoli1\ai-daily-uploader
uv run python upload_openclaw.py YYYY-MM-DD

# Step 2: 同步到微信小程序云数据库
node v3/pipeline.js YYYYMMDD
```

### 日期格式

- Python 脚本接受：`2026-02-11` 或 `20260211`
- Node.js 脚本接受：`20260211`

## 输出

### OSS（阿里云对象存储）
- 截图：`https://ai-daily.oss-cn-beijing.aliyuncs.com/screenshots/YYYY-MM-DD/*.webp`
- JSON：`https://ai-daily.oss-cn-beijing.aliyuncs.com/daily_reports/YYYY-MM-DD.json`
- 统计：`https://ai-daily.oss-cn-beijing.aliyuncs.com/statistic.json`

### 微信云数据库
- 日报记录：`daily_reports/YYYY-MM-DD`
- 统计记录：`statistic`

## 关键文件

| 文件 | 用途 |
|------|------|
| `upload_openclaw.py` | OpenClaw 适配的 OSS 上传脚本 |
| `upload_daily_v2.py` | 核心上传逻辑（WebP 转换、HTML 解析） |
| `v3/pipeline.js` | 微信云数据库同步 |
| `v3/full-pipeline.js` | 完整流程（OSS + 云数据库，但目录结构不同） |
| `.env` | 阿里云和微信凭证 |

## 环境变量

在 `C:\Users\taoli1\ai-daily-uploader\.env` 中配置：

```env
# 阿里云 OSS
ALIYUN_ACCESS_KEY_ID=xxx
ALIYUN_ACCESS_KEY_SECRET=xxx
ALIYUN_OSS_BUCKET=ai-daily
ALIYUN_OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com

# 微信云开发
WECHAT_ENV_ID=xxx
WECHAT_APPID=xxx
WECHAT_SECRET=xxx
```

## 图片优化

上传时自动进行：
- PNG → WebP 转换
- 最大宽度 750px（小程序标准）
- 质量 80%（视觉无损）
- 压缩率通常 40%-80%

## 注意事项

1. **先 OSS 后云数据库**：pipeline.js 依赖 `output/YYYY-MM-DD.json`（由 upload_openclaw.py 生成）
2. **日期一致性**：确保 HTML 文件名、截图目录、命令参数日期一致
3. **生产环境**：此步骤是 go production，执行前确认内容无误
