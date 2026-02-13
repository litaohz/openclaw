---
name: ai-daily-filter
description: |
  筛选和排序 AI 日报推文。从 X/Twitter 推文链接中，筛选出适合 AI 日报的内容并按优先级排序。
  触发条件：用户提到"AI日报"、"X版日报"、"筛选推文"、"推文排序"、"日报筛选"，或给出包含推文链接的飞书文档。
---

# AI 日报推文筛选与排序

## 完整工作流

```
1. 筛选推文 → 本 skill
2. 内容提取 → extract-from-x-url skill
3. 截图 → playwright-screenshot skill
4. 生成 HTML → md-to-html skill
5. 上传 OSS → oss-image-uploader skill（可选）
```

---

## 第一步：筛选逻辑

### 判断优先级（按重要性排序）

**第一优先级：发布者/公司**
→ OpenAI 的一句话 > 小公司的详细长文

**第二优先级：内容类型**
→ 新模型 > 新产品 > 新功能 > 观点

**第三优先级：同等条件下的加分项**
→ 正式发布 > 预览 | 附带视频 > 纯文字 | 首创 > 跟进

### 公司梯队

| 梯队 | 公司 |
|------|------|
| 第一 | OpenAI ≥ Google = Anthropic |
| 第二 | Microsoft, Meta, Amazon, Apple |
| 特例 | OpenClaw（近期较火，放第二梯队第1位）|
| 第二偏后 | NVIDIA（芯片公司，模型优先级较低）|
| 第三 | Cursor > Perplexity > Langchain = Mistral = Midjourney = HuggingFace |

### 入选条件

- 新模型/新产品/新功能发布
- 新技术/重大突破
- 重要行业数据
- 真金白银的投资/并购
- 头部大佬观点或公开访谈

### 不入选条件

- 老新闻/前几天已写过
- 私人互怼/与网友交锋
- 纯社交互动
- 快速变动的排名截图
- 中国公司（放中国板块）
- 敏感政治内容

---

## 第二步：内容提取

**引用 skill**: [extract-from-x-url](../extract-from-x-url/SKILL.md)

该 skill 包含：
- 内容提取原则（推文即新闻）
- Markdown 格式规范
- 时间处理规则
- 示例输出

---

## 第三步：截图

**引用 skill**: [playwright-screenshot](../playwright-screenshot/SKILL.md)

```bash
python tweet_screenshot.py "https://x.com/xxx" "output.png"
```

---

## 输出文件路径规则

**目录结构：**
```
ai-news/
├── raw/                    # 原始筛选结果
├── processed/              # 最终 markdown
├── screenshots/YYYY-MM-DD/ # 截图
└── processed/output/       # HTML 输出
```

**图片路径：**
- `processed/xxx.md` 引用截图：`../screenshots/YYYY-MM-DD/xx.png`
- `processed/output/xxx.html` 引用截图：`../../screenshots/YYYY-MM-DD/xx.png`

---

## 弹性机制

**消息少时放宽**：边缘内容可补选
**消息多时收紧**：只选最重要的

---

## 参考文档

- 筛选原则详解：[references/principles.md](references/principles.md)
- 筛选案例：[references/examples.md](references/examples.md)
