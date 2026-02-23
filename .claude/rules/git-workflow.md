# Git 工作流 (Git Workflow)

## 提交信息格式 (Commit Message Format)

```
<type>: <description>

<optional body>
```

类型 (Types): feat, fix, refactor, docs, test, chore, perf, ci

注意：归属归因 (Attribution) 已通过 `~/.claude/settings.json` 全局禁用。

## 拉取请求工作流 (Pull Request Workflow)

创建 PR 时：
1. 分析完整的提交历史（不仅是最近一次提交）
2. 使用 `git diff [base-branch]...HEAD` 查看所有变更
3. 起草详尽的 PR 摘要
4. 包含带有 TODO 的测试计划
5. 如果是新分支，使用 `-u` 参数推送

## 功能实现工作流 (Feature Implementation Workflow)

1. **规划先行 (Plan First)**
   - 使用 **planner** 智能体 (Agent) 创建实现计划
   - 识别依赖关系与风险
   - 拆分为多个阶段

2. **测试驱动开发 (TDD Approach)**
   - 使用 **tdd-guide** 智能体 (Agent)
   - 先编写测试 (RED)
   - 实现功能以通过测试 (GREEN)
   - 重构 (IMPROVE)
   - 验证 80% 以上的覆盖率

3. **代码评审 (Code Review)**
   - 在编写代码后立即使用 **code-reviewer** 智能体 (Agent)
   - 解决严重 (CRITICAL) 和高 (HIGH) 等级的问题
   - 尽可能修复中 (MEDIUM) 等级的问题

4. **提交与推送 (Commit & Push)**
   - 详细的提交信息
   - 遵循约定式提交 (Conventional Commits) 格式

## 发布工作流 (Release Workflow)

### 版本发布流程

1. **准备发布**
   - 确保所有功能已合并到主分支
   - 运行完整测试套件
   - 确保构建通过

2. **生成变更日志**
   - 使用 **changelog-generator** 技能
   - 命令：`/changelog` 或 `/changelog v2.4.0..HEAD`
   - 审查并调整生成的变更日志
   - 更新 CHANGELOG.md

3. **创建版本标签**
   ```bash
   git tag -a v2.5.0 -m "Release v2.5.0"
   git push origin v2.5.0
   ```

4. **自动发布**
   - GitHub Actions 自动触发（.github/workflows/release.yml）
   - 创建 GitHub Release
   - 附加变更日志

### 何时使用 changelog-generator

- ✅ 版本发布前
- ✅ 创建 GitHub Release
- ✅ 准备产品更新公告
- ✅ 生成周报/月报
- ❌ 日常提交（使用标准提交信息即可）
- ❌ PR 创建（已有 PR 工作流）

### 变更日志最佳实践

1. **提交信息质量**
   - 使用清晰的 Conventional Commits 格式
   - 在提交正文中提供上下文
   - 标记破坏性变更（`BREAKING CHANGE:` 或 `!`）

2. **定期维护**
   - 每次版本发布时更新 CHANGELOG.md
   - 审查生成的内容，确保用户友好
   - 添加迁移指南（如有破坏性变更）

3. **用户视角**
   - 使用用户能理解的语言
   - 突出业务价值，而非技术实现
   - 关注用户能感知到的变化
