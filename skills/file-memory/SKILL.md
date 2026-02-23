---
name: file-memory
description: 文件系统作为外部记忆——Manus 风格的三文件持久化规划系统。自动为复杂任务创建 task_plan.md、findings.md、progress.md，解决上下文丢失问题。
version: "1.0.0"
category: "planning"
---

# File Memory — 文件持久化记忆系统

> 上下文窗口 = RAM（易失，有限）
> 文件系统 = 磁盘（持久，无限）
> 任何重要信息都写入磁盘。

## 何时激活

自动激活条件（满足任一即可）：
- 任务需要 3 个以上步骤
- 任务涉及研究或探索
- 任务需要跨多个文件操作
- 用户明确请求：`/file-memory init`

不激活的场景：
- 简单问答
- 单文件小修改（<10 行）
- 快速查询

## 三文件模式

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| `task_plan.md` | 阶段跟踪、进度、决策、错误表 | 每个阶段完成后 |
| `findings.md` | 研究发现、技术决策、知识存储 | 任何发现后立即更新 |
| `progress.md` | 会话日志、测试结果、5 问题重启检查 | 整个会话过程中 |

文件位置：`.claude/plans/` 目录下（已在 doc-blocker 白名单中）。

## 与 planner 智能体的协调

```
planner 智能体（规划能力）
    │
    ▼
file-memory 技能（持久化层）
    │
    ├── task_plan.md  ← planner 输出 + 阶段状态 + 错误表
    ├── findings.md   ← 实施过程中的发现 + 智能体审查结果
    └── progress.md   ← 会话日志 + 验证结果 + 5 问题重启检查
```

工作流：
1. planner 智能体生成实施方案
2. file-memory 将方案持久化到 `task_plan.md`
3. 实施过程中，发现写入 `findings.md`，进度写入 `progress.md`
4. 会话恢复时，读取三文件恢复上下文

## 6 条核心规则

### 规则 1：先创建计划

永远不要在没有 `task_plan.md` 的情况下开始复杂任务。

```
开始任务 → 检查 .claude/plans/ 下是否有活跃计划
  → 有：读取恢复上下文
  → 无：创建三文件
```

### 规则 2：2 操作规则

> 每进行 2 次查看/浏览/搜索操作后，立即将关键发现保存到 `findings.md`。

这防止多模态信息（图片、PDF、浏览器截图）在上下文重置时丢失。

### 规则 3：决策前读取

在做出重大决策前，读取 `task_plan.md`。这利用了注意力操纵（Attention Manipulation）原理——将目标推入模型的近期注意力窗口。

```
上下文开头: [原始目标 — 距离远，已被遗忘]
...大量工具调用...
上下文末尾: [刚读取的 task_plan.md — 获得注意力！]
```

### 规则 4：行动后更新

完成任何阶段后：
- 更新阶段状态：`in_progress` → `complete`
- 记录遇到的错误到 `task_plan.md` 错误表
- 记录创建/修改的文件到 `progress.md`

### 规则 5：记录所有错误

每个错误都记录在 `task_plan.md` 的错误表中。这建立知识库并防止重复犯错。

```markdown
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | 创建默认配置 |
| API timeout | 2 | 添加重试逻辑 |
```

### 规则 6：3 次错误协议

```
尝试 1：诊断并修复
  → 仔细阅读错误信息
  → 识别根本原因
  → 应用针对性修复

尝试 2：替代方案
  → 同样错误？尝试不同方法
  → 不同工具？不同库？
  → 永远不要重复完全相同的失败操作

尝试 3：更广泛的重新思考
  → 质疑假设
  → 搜索解决方案
  → 考虑更新计划

3 次失败后：升级给用户
  → 解释尝试了什么
  → 分享具体错误
  → 请求指导
```

## 读写决策矩阵

| 情况 | 操作 | 原因 |
|------|------|------|
| 刚写入文件 | 不读取 | 内容仍在上下文中 |
| 查看图片/PDF | 立即写入发现 | 多模态→文本，防止丢失 |
| 浏览器返回数据 | 写入文件 | 截图不持久 |
| 开始新阶段 | 读取计划/发现 | 上下文可能过时 |
| 发生错误 | 读取相关文件 | 需要当前状态来修复 |
| 间隔后恢复 | 读取所有规划文件 | 恢复状态 |

## 5 问题重启测试

会话恢复时，如果能回答这 5 个问题，说明上下文管理良好：

| 问题 | 答案来源 |
|------|----------|
| 我在哪里？ | `task_plan.md` 中的当前阶段 |
| 我要去哪里？ | 剩余阶段 |
| 目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | `findings.md` |
| 我做了什么？ | `progress.md` |

## 与其他系统的定位差异

| 系统 | 定位 | 生命周期 |
|------|------|----------|
| `file-memory` (findings.md) | 任务级短期记忆 | 单次任务，完成后归档 |
| `continuous-learning` (直觉) | 跨任务长期模式 | 永久习得的行为偏好 |
| `interactive-discussion` (discussion_context.md) | 讨论上下文 | 单次讨论会话 |

## 反模式

| 不要 | 应该 |
|------|------|
| 只用 TodoWrite 持久化 | 创建 task_plan.md 文件 |
| 陈述目标后忘记 | 决策前重新读取计划 |
| 隐藏错误并静默重试 | 将错误记录到计划文件 |
| 把所有内容塞入上下文 | 将大内容存储到文件 |
| 立即开始执行 | 首先创建计划文件 |
| 重复失败的操作 | 跟踪尝试，改变方法 |
| 在技能目录创建文件 | 在 .claude/plans/ 创建文件 |

## 命令

- `/file-memory init [任务名]` — 初始化三文件
- `/file-memory status` — 查看当前任务状态
- `/file-memory resume` — 恢复中断的任务
- `/file-memory archive` — 归档已完成的任务

## 模板

- [templates/task_plan.md](templates/task_plan.md) — 任务计划模板
- [templates/findings.md](templates/findings.md) — 发现记录模板
- [templates/progress.md](templates/progress.md) — 进度日志模板

## 参考资料

- [reference.md](reference.md) — Manus 上下文工程原理精要

---

**版本**: 1.0.0
**基于**: [Planning with Files](https://github.com/OthmanAdi/planning-with-files) v2.15.0
**灵感来源**: [Manus AI Context Engineering](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
