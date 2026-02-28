---
name: superpowers-plan
description: 创建细粒度实施计划——将多步骤任务分解为 2-5 分钟的小块任务，包含完整代码和测试步骤
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob", "AskUserQuestion"]
---

# Superpowers 细粒度规划

调用 `superpowers-task-planning` 技能来创建详细的实施计划。

## 使用方法

```bash
/superpowers-plan "功能描述"
```

## 功能

1. **细粒度拆解** - 将任务分解为 2-5 分钟的小步骤
2. **完整代码** - 每个步骤包含完整的代码实现
3. **TDD 流程** - 强制红-绿-重构循环
4. **精确路径** - 指定确切的文件路径和行号
5. **验证步骤** - 每个步骤包含测试命令和预期输出
6. **提交信息** - 为每个任务提供提交信息模板

## 计划结构

生成的计划包含：

```markdown
# [功能名称] 实施计划

**目标：** [一句话描述]
**架构：** [2-3 句话]
**技术栈：** [关键技术]

---

### 任务 1：[组件名称]

**文件：**
- 创建：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 测试：`tests/exact/path/to/test.py`

**步骤 1：编写失败的测试**
[完整代码]

**步骤 2：运行测试验证失败**
运行：`pytest tests/path/test.py::test_name -v`
预期：FAIL

**步骤 3：编写最小实现**
[完整代码]

**步骤 4：运行测试验证通过**
运行：`pytest tests/path/test.py::test_name -v`
预期：PASS

**步骤 5：提交**
```bash
git add ...
git commit -m "feat: ..."
```
```

## 示例

```
User: /superpowers-plan "Add user authentication with JWT"

Agent:
我正在使用 superpowers-task-planning 技能来创建实施计划。

[分析需求...]
[探索代码库...]
[设计架构...]

计划完成并保存到 `docs/plans/2025-02-28-user-authentication.md`

两个执行选项：

1. 子智能体驱动（此会话）- 我为每个任务分派新的子智能体，任务之间审查，快速迭代

2. 并行会话（单独）- 使用 executing-plans 打开新会话，带检查点的批量执行

选择哪种方法？

User: 1

Agent:
[启动子智能体驱动执行...]
```

## 何时使用

- 开始新功能实现
- 需要详细的实施步骤
- 团队协作需要清晰计划
- 复杂任务需要分解
- 需要强制 TDD 流程

## 与 /plan 的区别

| 特性 | /plan | /superpowers-plan |
|------|-------|-------------------|
| 粒度 | 高层次阶段 | 2-5 分钟小任务 |
| 代码 | 概述 | 完整代码 |
| TDD | 推荐 | 强制 |
| 验证 | 手动 | 每步自动 |
| 适用 | 架构规划 | 实施执行 |

## 相关

- `/plan` - 高层次架构规划
- `/finish-branch` - 完成开发分支
- `superpowers-git-worktree` - 创建隔离工作空间
- `superpowers-task-planning` - 此命令调用的技能

## 参考

参见 helpers.md#细粒度任务拆解模板 了解任务结构
参见 helpers.md#TDD 工作流 了解测试驱动开发流程
