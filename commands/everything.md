---
description: 分析当前上下文，推荐最匹配的 Everything Claude Code 功能。
---

# /everything - 智能功能推荐

分析当前上下文和用户意图，推荐最匹配的 skill、agent 或 command。

## 用法

- `/everything` — 基于当前上下文智能推荐
- `/everything list` — 列出所有可用功能
- `/everything search <关键词>` — 搜索特定功能
- `/everything tutorial` — 启动烟花项目新手教程

## 指令（Instructions）

### 默认模式（无参数或上下文推荐）

1. 读取 `skills/everything-assistant/SKILL.md` 中的预编译知识摘要
2. 分析当前会话上下文：
   - 用户最近的请求内容
   - 当前打开/修改的文件类型
   - 工作流阶段（刚开始？编码中？审查中？）
3. 按三层匹配逻辑（任务类型 → 语言/框架 → 工作流阶段）生成推荐
4. 检查 `~/.claude/homunculus/instincts/personal/` 中的直觉，融合高置信度偏好
5. 输出推荐结果（最多 3 条，按优先级排序）

### `list` 子命令

读取 `skills/everything-assistant/CATALOG.md`，按类型输出所有功能的精简列表：
- Agents（14 个）
- Skills（31 个，按领域分组）
- Commands（28 个）
- Rules（8 个）

### `search <关键词>` 子命令

在预编译知识摘要中搜索关键词，返回匹配的功能及其用途说明。支持中英文关键词。

### `tutorial` 子命令

等同于 `/fireworks-tutorial`，启动烟花项目新手教程。

## 输出格式

```
【Everything 推荐】
根据你的需求，建议使用：
1. [P0] {功能名} — {一句话理由}
2. [P1] {功能名} — {一句话理由}
3. [P2] {功能名} — {一句话理由}（可选）
快速启动：{最相关的命令}
```

## 参数

$ARGUMENTS 可以是：
- （空）— 基于上下文智能推荐
- `list` — 列出所有功能
- `search <关键词>` — 搜索功能
- `tutorial` — 启动新手教程
