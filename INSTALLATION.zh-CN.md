# 安装指南

## 方法一：通过 Claude Code 插件系统安装（推荐）

### 1. 添加插件市场

```bash
/plugin marketplace add tiandiyiqi/everything-claude-code-zh
```

### 2. 安装插件

```bash
/plugin install everything-claude-code-zh@everything-claude-code-zh
```

### 3. 手动安装规则（必需）

> ⚠️ **重要提示：** Claude Code 插件系统无法自动分发 `rules` 目录，需要手动安装。

```bash
# 克隆仓库
git clone https://github.com/tiandiyiqi/everything-claude-code-zh.git

# 复制规则到全局配置目录（应用于所有项目）
cp -r everything-claude-code-zh/rules/* ~/.claude/rules/
```

### 4. 验证安装

```bash
# 查看已安装的插件
/plugin list everything-claude-code-zh@everything-claude-code-zh

# 尝试使用一个命令
/plan "添加用户认证功能"
```

---

## 方法二：手动安装

如果你想手动安装或只安装部分组件：

### 1. 克隆仓库

```bash
git clone https://github.com/tiandiyiqi/everything-claude-code-zh.git
cd everything-claude-code-zh
```

### 2. 安装 Agents（智能体）

```bash
# 复制所有 agents 到全局目录
cp -r agents/* ~/.claude/agents/

# 或者只复制你需要的 agents
cp agents/code-reviewer.md ~/.claude/agents/
cp agents/tdd-guide.md ~/.claude/agents/
```

### 3. 安装 Skills（技能）

```bash
# 复制所有 skills
cp -r skills/* ~/.claude/skills/

# 或者只复制特定的 skills
cp -r skills/everything-assistant ~/.claude/skills/
cp -r skills/continuous-learning-v3 ~/.claude/skills/
```

### 4. 安装 Commands（命令）

```bash
# 复制所有 commands
cp -r commands/* ~/.claude/commands/
```

### 5. 安装 Rules（规则）

```bash
# 复制规则（应用于所有项目）
cp -r rules/* ~/.claude/rules/
```

### 6. 安装 Hooks（钩子）

```bash
# 查看 hooks 示例
cat hooks/hooks.json

# 手动将需要的 hooks 添加到 ~/.claude/settings.json
```

---

## 验证安装

### 检查 Agents

```bash
ls ~/.claude/agents/
```

应该看到：
- architect.md
- code-reviewer.md
- tdd-guide.md
- security-reviewer.md
- 等等...

### 检查 Skills

```bash
ls ~/.claude/skills/
```

应该看到：
- everything-assistant/
- continuous-learning-v3/
- interactive-discussion/
- 等等...

### 检查 Rules

```bash
ls ~/.claude/rules/
```

应该看到：
- agents.md
- coding-style.md
- git-workflow.md
- testing.md
- 等等...

---

## 更新插件

### 通过插件系统更新

```bash
# 更新到最新版本
/plugin update everything-claude-code-zh@everything-claude-code-zh
```

### 手动更新

```bash
cd everything-claude-code-zh
git pull origin main

# 重新复制需要更新的组件
cp -r rules/* ~/.claude/rules/
cp -r agents/* ~/.claude/agents/
cp -r skills/* ~/.claude/skills/
```

---

## 卸载

### 通过插件系统卸载

```bash
/plugin uninstall everything-claude-code-zh@everything-claude-code-zh
```

### 手动卸载

```bash
# 删除 agents
rm ~/.claude/agents/architect.md
rm ~/.claude/agents/code-reviewer.md
# ... 删除其他 agents

# 删除 skills
rm -rf ~/.claude/skills/everything-assistant
rm -rf ~/.claude/skills/continuous-learning-v3
# ... 删除其他 skills

# 删除 rules
rm ~/.claude/rules/agents.md
rm ~/.claude/rules/coding-style.md
# ... 删除其他 rules
```

---

## 常见问题

### Q: 为什么需要手动安装 rules？

A: Claude Code 的插件系统目前不支持自动分发 `rules` 目录。这是 Claude Code 的限制，不是插件的问题。

### Q: 可以只安装部分组件吗？

A: 可以！你可以选择性地复制需要的 agents、skills 或 commands。但建议至少安装 rules，因为它们定义了核心工作流。

### Q: 如何知道哪些 skills 可用？

A: 在 Claude Code 中运行：
```bash
/plugin list everything-claude-code-zh@everything-claude-code-zh
```

### Q: 安装后如何使用？

A: 查看 [README.zh-CN.md](README.zh-CN.md) 中的"快速开始"部分，或者直接尝试：
```bash
/plan "你的任务描述"
/everything
```

---

## 技术支持

如果遇到问题：

1. 查看 [GitHub Issues](https://github.com/tiandiyiqi/everything-claude-code-zh/issues)
2. 提交新的 Issue
3. 参考原版文档：[affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)
