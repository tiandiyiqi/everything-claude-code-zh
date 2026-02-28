# Superpowers 阶段 1 实施计划

## 实施概览

**目标：** 整合 Superpowers 的核心工作流功能到 Everything Claude Code

**时间：** 1-2 周

**范围：**
- 3 个新 Skills
- 2 个新 Commands
- 2 个新 Hooks
- 文档更新

---

## 文件创建清单

### 新增 Skills（3 个）

1. **skills/superpowers-git-worktree/SKILL.md**
   - 功能：Git Worktree 管理
   - 来源：`/superpowers/skills/using-git-worktrees/SKILL.md`
   - 状态：待创建

2. **skills/superpowers-finishing-branch/SKILL.md**
   - 功能：完成开发分支
   - 来源：`/superpowers/skills/finishing-a-development-branch/SKILL.md`
   - 状态：待创建

3. **skills/superpowers-task-planning/SKILL.md**
   - 功能：细粒度任务规划
   - 来源：`/superpowers/skills/writing-plans/SKILL.md`
   - 状态：待创建

### 新增 Commands（2 个）

1. **commands/finish-branch.md**
   - 功能：调用 superpowers-finishing-branch
   - 状态：待创建

2. **commands/superpowers-plan.md**
   - 功能：调用 superpowers-task-planning
   - 状态：待创建

### 新增 Hooks（2 个）

1. **hooks/git-worktree-auto.sh**
   - 功能：自动提示使用 worktree
   - 状态：待创建

2. **hooks/task-completion-check.sh**
   - 功能：任务完成后验证测试
   - 状态：待创建

### 更新文件（3 个）

1. **.claude/rules/helpers.md**
   - 添加：Git Worktree 管理规范
   - 添加：细粒度任务拆解模板
   - 添加：完成分支工作流

2. **skills/everything-assistant/SKILL.md**
   - 添加：3 个新 skills 到索引
   - 添加：推荐规则

3. **README.md**
   - 添加：Superpowers 整合说明

---

## 实施步骤

### 步骤 1：创建 superpowers-git-worktree skill ✓

读取源文件，翻译并改编为中文版本。

### 步骤 2：创建 superpowers-finishing-branch skill

读取源文件，翻译并改编为中文版本。

### 步骤 3：创建 superpowers-task-planning skill

读取源文件，翻译并改编为中文版本。

### 步骤 4：创建 commands

创建 2 个命令文件。

### 步骤 5：创建 hooks

创建 2 个钩子脚本。

### 步骤 6：更新 helpers.md

添加新的标准化操作章节。

### 步骤 7：更新 everything-assistant

添加新功能到索引和推荐规则。

### 步骤 8：更新 README

添加 Superpowers 整合说明。

### 步骤 9：验证

测试所有新功能。

---

## 当前进度

- [x] 探索 Superpowers 源代码
- [x] 设计实施方案
- [x] 创建 Skills
  - [x] superpowers-git-worktree
  - [x] superpowers-finishing-branch
  - [x] superpowers-task-planning
- [x] 创建 Commands
  - [x] finish-branch
  - [x] superpowers-plan
- [ ] 创建 Hooks
- [x] 更新文档
  - [x] helpers.md - 添加 Superpowers 工作流章节
  - [x] everything-assistant - 添加 3 个新 skills 到索引和推荐规则
  - [x] README.md - 添加 Superpowers 整合说明
- [ ] 验证测试

## 下一步

1. 创建 2 个 Hooks（可选，阶段 1 暂不实现）
2. 更新 plugin.json 注册新功能
3. 验证所有新功能
4. 提交变更
