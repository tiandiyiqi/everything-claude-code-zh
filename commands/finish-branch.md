---
name: finish-branch
description: 完成开发分支——验证测试、呈现合并/PR/保留/丢弃选项，并清理工作树
allowed_tools: ["Bash", "Read", "AskUserQuestion"]
---

# 完成开发分支

调用 `superpowers-finishing-branch` 技能来完成开发工作。

## 使用方法

```bash
/finish-branch
```

## 功能

1. **验证测试** - 运行项目测试套件，确保所有测试通过
2. **确定基础分支** - 检测从哪个分支分离（main/master）
3. **呈现 4 个选项**：
   - 本地合并回基础分支
   - 推送并创建 Pull Request
   - 保持分支原样（稍后处理）
   - 丢弃此工作
4. **执行选择** - 根据用户选择执行相应操作
5. **清理工作树** - 对选项 1、2、4 自动清理工作树

## 示例

```
User: /finish-branch

Agent:
我正在使用 superpowers-finishing-branch 技能来完成这项工作。

[运行测试...]
✅ 所有测试通过（47 个测试，0 个失败）

实现完成。您想做什么？

1. 本地合并回 main
2. 推送并创建 Pull Request
3. 保持分支原样（我稍后处理）
4. 丢弃此工作

选择哪个选项？

User: 2

Agent:
[推送分支...]
[创建 PR...]
✅ Pull Request 已创建：https://github.com/user/repo/pull/123
[清理工作树...]
✅ 工作树已清理
```

## 何时使用

- 功能实现完成
- 所有测试通过
- 准备集成工作
- 需要清理工作树

## 相关

- `/superpowers-plan` - 创建实施计划
- `superpowers-git-worktree` - 创建隔离工作空间
- `superpowers-finishing-branch` - 此命令调用的技能

## 参考

参见 helpers.md#完成分支工作流 了解详细流程
