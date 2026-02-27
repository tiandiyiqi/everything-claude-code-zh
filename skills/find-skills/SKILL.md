---
name: find-skills
description: 帮助用户发现和安装智能体技能。当用户询问"如何做X"、"查找X技能"、"有能做X的技能吗"时使用。
---

# Find Skills

这个技能帮助你从开放的智能体技能生态系统中发现和安装技能。

## 何时使用此技能

当用户满足以下条件时使用此技能：

- 询问"如何做X"，其中X可能是已有技能的常见任务
- 说"查找X技能"或"有X的技能吗"
- 询问"你能做X吗"，其中X是专业能力
- 表示有兴趣扩展智能体能力
- 想要搜索工具、模板或工作流
- 提到希望有特定领域（设计、测试、部署等）的帮助

## 什么是 Skills CLI？

Skills CLI（`npx skills`）是开放智能体技能生态系统的包管理器。技能是模块化包，用专业知识、工作流和工具扩展智能体能力。

**关键命令：**

- `npx skills find [query]` - 交互式搜索或按关键词搜索技能
- `npx skills add <package>` - 从 GitHub 或其他来源安装技能
- `npx skills check` - 检查技能更新
- `npx skills update` - 更新所有已安装的技能

**浏览技能：** https://skills.sh/

## 如何帮助用户找到技能

### 第 1 步：了解他们需要什么

当用户请求帮助时，确定：

1. 领域（如 React、测试、设计、部署）
2. 具体任务（如写测试、创建动画、审查 PR）
3. 这是否是一个足够常见的任务，可能已有技能

### 第 2 步：搜索技能

使用相关查询运行查找命令：

```bash
npx skills find [query]
```

例如：

- 用户问"如何让 React 应用更快？" → `npx skills find react performance`
- 用户问"你能帮我审查 PR 吗？" → `npx skills find pr review`
- 用户说"我需要创建变更日志" → `npx skills find changelog`

命令会返回如下结果：

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 第 3 步：向用户展示选项

找到相关技能时，向用户展示：

1. 技能名称及其功能
2. 他们可以运行的安装命令
3. 在 skills.sh 上了解更多信息的链接

示例回复：

```
我找到一个可能有帮助的技能！"vercel-react-best-practices" 技能提供
来自 Vercel Engineering 的 React 和 Next.js 性能优化指南。

安装方法：
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

了解更多：https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 第 4 步：提供安装

如果用户想继续，你可以为他们安装技能：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 标志全局安装（用户级别），`-y` 跳过确认提示。

## 常见技能类别

搜索时考虑这些常见类别：

| 类别 | 示例查询 |
|------|---------|
| Web 开发 | react, nextjs, typescript, css, tailwind |
| 测试 | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| 文档 | docs, readme, changelog, api-docs |
| 代码质量 | review, lint, refactor, best-practices |
| 设计 | ui, ux, design-system, accessibility |
| 生产力 | workflow, automation, git |

## 有效搜索的技巧

1. **使用具体关键词**："react testing" 比单独 "testing" 更好
2. **尝试替代术语**：如果 "deploy" 不行，试试 "deployment" 或 "ci-cd"
3. **检查热门来源**：许多技能来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 未找到技能时

如果没有找到相关技能：

1. 承认没有找到现有技能
2. 提供直接使用你的通用能力帮助他们完成任务的选项
3. 建议用户可以使用 `npx skills init` 创建自己的技能

示例：

```
我搜索了与"xyz"相关的技能，但没有找到匹配结果。
我仍然可以直接帮助你完成这个任务！你想让我继续吗？

如果这是你经常做的事情，你可以创建自己的技能：
npx skills init my-xyz-skill
```
