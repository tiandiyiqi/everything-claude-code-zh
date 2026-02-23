---
description: 启动烟花项目新手教程，在实践中学习 Everything Claude Code 80%+ 的功能。
---

# /fireworks-tutorial - 烟花项目新手教程

通过构建一个纯 HTML/CSS/JS + Canvas 的烟花特效项目，在实践中学习 Everything Claude Code 的核心功能。

## 用法

`/fireworks-tutorial [step]`

## 指令（Instructions）

1. 读取 `skills/everything-assistant/TUTORIAL.md`
2. 如果提供了 `step` 参数，跳转到对应步骤
3. 如果没有参数，从步骤 0 开始
4. 每个步骤完成后，询问用户是否继续下一步

## 教程概览

15 个步骤，覆盖 80%+ 的 Everything 功能：

| 步骤 | 内容 | 核心功能 |
|------|------|---------|
| 0 | 需求讨论 | interactive-discussion |
| 1 | 项目规划 | planner, /plan, file-memory |
| 2 | 编码标准 | coding-standards |
| 3 | TDD：粒子系统 | tdd-workflow, tdd-guide |
| 4 | 烟花发射器 | frontend-patterns, code-reviewer |
| 5 | 用户交互 | security-review |
| 6 | 性能优化 | architect |
| 7 | 配置面板 | interactive-discussion |
| 8 | E2E 测试 | e2e-runner |
| 9 | 重构清理 | refactor-cleaner |
| 10 | 文档与 Git | doc-updater, git-workflow |
| 11 | 验证循环 | verification-loop, /verify |
| 12 | 新功能编排 | /orchestrate, iterative-retrieval |
| 13 | 学习管理 | continuous-learning-v2, /learn |
| 14 | 上下文管理 | strategic-compact, file-memory |

## 参数

$ARGUMENTS 可以是：
- （空）— 从步骤 0 开始
- `0`-`14` — 跳转到指定步骤
- `status` — 查看当前进度
