---
name: growth-report
description: 生成个人成长报告，汇总近期工作概览、习得技能、反复挑战和改进建议
command: true
---

# 成长报告命令（Growth Report Command）

## 概述

`/growth-report` 命令从 continuous-learning v3 系统收集的数据中生成人类可读的成长报告，帮助你：

1. **回顾近期工作成果** - 查看会话数、涉及项目、活跃天数
2. **识别习得的模式** - 发现自动提取的技能和高置信度的直觉
3. **发现反复出现的问题** - 识别需要改进的领域
4. **获得具体的改进建议** - 基于错误模式的可操作建议
5. **确认自己的优势** - 查看高置信度的成功模式

## 实现方式

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v3/scripts/growth-report.py" "$@"
```

## 用法

### 基本用法

```bash
# 默认生成近 7 天的报告
/growth-report

# 生成近 14 天的报告
/growth-report 14

# 生成近 30 天的报告
/growth-report 30
```

### 保存到文件

```bash
# 保存报告到文件
/growth-report 7 --save report.md

# 保存近 30 天的报告
/growth-report 30 --save monthly-report.md
```

### 输出格式

```bash
# 默认文本格式（终端友好）
/growth-report

# Markdown 格式（未来支持）
/growth-report --format markdown

# JSON 格式（未来支持）
/growth-report --format json
```

## 报告内容

报告包含 5 个主要部分：

### 1. 工作概览

- **会话数** - 近期完成的会话数量
- **涉及项目** - 工作过的项目列表
- **活跃天数** - 实际工作的天数
- **完成任务** - 完成的任务数量
- **使用工具** - 使用的 Claude Code 工具列表

**数据源**：`~/.claude/sessions/*-session.tmp`

### 2. 习得的模式与技能

展示近期自动提取的技能和高置信度的直觉：

- **Learned Skills** - 从会话中提取的可复用模式
  - 技能标题
  - 提取日期
  - 上下文摘要
- **Instincts** - 高置信度（>=70%）的行为模式
  - 直觉 ID
  - 触发条件
  - 置信度
  - 领域

**数据源**：
- `~/.claude/skills/learned/*.md`
- `~/.claude/homunculus/instincts/personal/*.yaml`

### 3. 反复出现的挑战

识别在任务执行中反复出现的错误和问题：

- 错误类型
- 出现次数
- 按频率排序（最常见的在前）

**数据源**：
- `.claude/plans/*/progress.md` - 错误日志表
- `.claude/plans/*/task_plan.md` - 错误记录表

### 4. 改进建议

基于反复出现的挑战，使用规则引擎生成可操作的改进建议：

| 错误类型 | 建议 |
|---------|------|
| FileNotFoundError | 在操作文件前先使用 Glob 或 ls 确认文件存在 |
| Timeout | 为长时间运行的操作添加重试逻辑或增加超时时间 |
| ImportError | 检查依赖是否已安装，考虑添加依赖检查脚本 |
| SyntaxError | 在提交前使用 linter 检查代码语法 |
| PermissionError | 检查文件权限，使用 chmod 或 sudo 解决权限问题 |
| 高频错误（>=3次） | 创建专门的错误处理模式 |

### 5. 优势确认

展示高置信度（>=80%）的成功模式，帮助你识别自己的优势：

- 成功模式描述
- 置信度百分比
- 所属领域

**数据源**：`~/.claude/homunculus/instincts/personal/*.yaml`（过滤 confidence >= 0.8）

## 报告示例

```
============================================================
  成长报告 (Growth Report) - 近 7 天
============================================================

## 1. 工作概览
  会话数: 12
  涉及项目: project-a, project-b
  活跃天数: 5 天
  完成任务: 8
  使用工具: Read, Write, Edit, Bash, Grep

## 2. 习得的模式与技能 (3)
  1. Git Worktree 并行开发模式
     提取日期: 2026-02-22
     上下文: 使用 git worktree 实现多分支并行开发...

  2. prefer-functional-over-class (置信度: 85%)
     触发条件: when writing new code
     领域: coding-style

## 3. 反复出现的挑战 (2)
  1. FileNotFoundError (出现 3 次)
  2. ImportError (出现 2 次)

## 4. 改进建议 (2)
  1. 建议：在操作文件前先使用 Glob 或 ls 确认文件存在
  2. 建议：检查依赖是否已安装，考虑添加依赖检查脚本

## 5. 优势确认 (2)
  1. 优先使用函数式模式而非类 (置信度: 85%)
  2. 先写测试，再写实现 (置信度: 90%)

============================================================
  生成时间: 2026-02-23 12:00
============================================================
```

## 参数说明

### 位置参数

- `[天数]` - 统计天数（默认：7 天）
  - 示例：`/growth-report 14` 生成近 14 天的报告

### 可选参数

- `--save FILE` - 保存报告到文件
  - 示例：`/growth-report --save report.md`
  - 默认：输出到终端

- `--format {text,markdown,json}` - 输出格式
  - `text` - 纯文本格式（默认，终端友好）
  - `markdown` - Markdown 格式（未来支持）
  - `json` - JSON 格式（未来支持）

## 数据源详解

| 报告部分 | 数据源 | 提取内容 |
|---------|--------|---------|
| 工作概览 | `~/.claude/sessions/*-session.tmp` | 会话数、项目、活跃天数、任务、工具 |
| 习得模式 | `~/.claude/skills/learned/*.md` | 技能标题、提取日期、上下文 |
| 习得模式 | `~/.claude/homunculus/instincts/personal/*.yaml` | 高置信度直觉（>=0.7） |
| 反复挑战 | `.claude/plans/*/progress.md` | 错误日志表 |
| 反复挑战 | `.claude/plans/*/task_plan.md` | 错误记录表 |
| 改进建议 | 基于挑战的规则引擎 | 3-5 条可操作建议 |
| 优势确认 | `~/.claude/homunculus/instincts/personal/*.yaml` | 高置信度直觉（>=0.8） |

## 与其他命令的关系

### 查看详细直觉

```bash
# 查看所有直觉的详细状态
/instinct-status
```

### 手动提取模式

```bash
# 从当前会话手动提取模式
/learn
```

### 聚类为技能/命令

```bash
# 将直觉聚类为技能、命令或智能体
/evolve
```

### 工作流程

```
会话工作
   ↓
自动观察（hooks）
   ↓
提取直觉（/learn）
   ↓
查看成长报告（/growth-report）
   ↓
聚类为技能（/evolve）
```

## 使用场景

### 1. 每周回顾

```bash
# 每周五生成报告，回顾本周工作
/growth-report 7 --save weekly-report.md
```

### 2. 月度总结

```bash
# 每月底生成报告，总结本月成长
/growth-report 30 --save monthly-report.md
```

### 3. 识别改进点

```bash
# 快速查看近期需要改进的领域
/growth-report 7
```

### 4. 确认学习成果

```bash
# 查看近期习得的技能和模式
/growth-report 14
```

## 技术细节

### 时间过滤

- 使用文件修改时间（mtime）过滤数据
- 只统计在指定天数内修改的文件
- 默认 7 天，可自定义

### 错误聚合

- 从多个数据源提取错误记录
- 按错误类型聚合
- 按出现次数排序

### 规则引擎

- 基于错误类型匹配建议
- 支持关键词匹配（如 "filenotfound", "timeout"）
- 高频错误（>=3次）触发特殊建议

### 零依赖

- 仅使用 Python 标准库
- 无需安装额外依赖
- 兼容 Python 3.7+

## 故障排除

### 报告为空

**原因**：数据源不存在或时间范围内无数据

**解决方案**：
1. 检查数据源目录是否存在
2. 增加天数参数（如 `/growth-report 30`）
3. 确认 continuous-learning v3 系统已启用

### 无法找到会话文件

**原因**：`~/.claude/sessions/` 目录不存在

**解决方案**：
1. 确认 Claude Code 已正确安装
2. 至少完成一次会话以生成会话文件

### 无法找到直觉文件

**原因**：`~/.claude/homunculus/instincts/personal/` 目录不存在

**解决方案**：
1. 确认 continuous-learning v2/v3 已启用
2. 使用 `/learn` 命令手动提取直觉

## 未来扩展

### 支持更多数据源

- 压缩日志（`compaction-log.txt`）
- 工具计数（`/tmp/claude-tool-count-*`）

### 支持更多输出格式

- JSON 格式（用于程序化处理）
- Markdown 格式（用于文档）
- HTML 格式（用于网页展示）

### 支持趋势分析

- 对比不同时间段的报告
- 生成成长曲线图
- 识别改进趋势

### 支持自定义规则

- 允许用户定义错误到建议的映射规则
- 支持从配置文件加载规则
- 支持正则表达式匹配

## 相关文档

- [Continuous Learning v3 文档](../skills/continuous-learning-v3/README.md)
- [Instinct CLI 文档](../skills/continuous-learning-v2/README.md)
- [File-Memory 文档](../docs/file-memory.md)
