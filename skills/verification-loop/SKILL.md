# 验证循环技能（Verification Loop Skill）

一个用于 Claude Code 会话的全面验证系统。

## 何时使用

在以下场景调用此技能（Skill）：
- 完成功能开发或重大代码变更后
- 创建 PR 之前
- 当你想确保质量门禁（Quality Gates）通过时
- 代码重构之后

## 验证阶段（Verification Phases）

参见 helpers.md#通用验证六阶段

## 输出格式（Output Format）

参见 helpers.md#验证报告模板

## 持续模式（Continuous Mode）

对于长时间的会话（Session），每 15 分钟或在重大变更后运行一次验证：

```markdown
设置心理检查点：
- 完成每个函数后
- 完成一个组件后
- 在开始下一个任务之前

运行：/verify
```

## 与钩子（Hooks）集成

此技能（Skill）是对 `PostToolUse` 钩子（Hooks）的补充，但提供了更深层次的验证。
钩子可以立即发现问题；此技能则提供全面的审查。
