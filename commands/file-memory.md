---
description: 管理文件持久化记忆系统。初始化、查看状态、恢复或归档任务的三文件规划系统（task_plan.md、findings.md、progress.md）。
---

# File Memory 命令

管理基于文件的持久化记忆系统，用于复杂任务的上下文管理。

## 子命令

### `/file-memory init [任务名]`

初始化三文件规划系统：

1. 在 `.claude/plans/` 下创建三个文件：
   - `task_plan.md` — 任务计划（阶段、决策、错误表）
   - `findings.md` — 发现记录（研究、技术决策）
   - `progress.md` — 进度日志（会话记录、测试结果）

2. 使用 `skills/file-memory/templates/` 下的模板

3. 如果提供了任务名，用它替换模板中的占位符

### `/file-memory status`

查看当前活跃任务的状态：

1. 扫描 `.claude/plans/` 下的 `task_plan.md` 文件
2. 报告每个任务的：
   - 目标
   - 当前阶段
   - 各阶段完成状态
   - 错误数量

### `/file-memory resume`

恢复中断的任务：

1. 读取 `.claude/plans/` 下的三文件
2. 执行 5 问题重启测试：
   - 我在哪里？→ task_plan.md 当前阶段
   - 我要去哪里？→ 剩余阶段
   - 目标是什么？→ 目标陈述
   - 我学到了什么？→ findings.md
   - 我做了什么？→ progress.md
3. 输出上下文摘要，准备继续工作

### `/file-memory archive`

归档已完成的任务：

1. 检查所有阶段是否已完成
2. 将三文件移动到 `.claude/plans/archive/` 目录
3. 文件名添加日期前缀（如 `2026-02-23-task_plan.md`）

## 何时使用

- 开始复杂任务前：`/file-memory init 用户通知系统`
- 新会话恢复工作：`/file-memory resume`
- 检查进度：`/file-memory status`
- 任务完成后清理：`/file-memory archive`

## 与 /plan 的关系

- `/plan` = 规划能力（调用 planner 智能体生成方案）
- `/file-memory` = 持久化能力（将方案和过程写入文件）

推荐工作流：
1. `/plan` 生成实施方案
2. `/file-memory init` 创建持久化文件
3. 将方案写入 `task_plan.md`
4. 实施过程中持续更新三文件
5. 完成后 `/file-memory archive`

## 相关技能

此命令使用 `skills/file-memory/` 技能：
- `SKILL.md` — 核心规则和工作流
- `reference.md` — Manus 上下文工程原理
- `templates/` — 三文件模板
