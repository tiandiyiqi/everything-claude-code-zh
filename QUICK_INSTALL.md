# 快速安装指南

## 🚀 2 分钟快速安装

### 步骤 1：添加插件市场

在 Claude Code 中运行：

```bash
/plugin marketplace add tiandiyiqi/everything-claude-code-zh
```

### 步骤 2：安装插件

```bash
/plugin install everything-claude-code-zh@everything-claude-code-zh
```

### 步骤 3：手动安装规则（必需）

```bash
# 克隆仓库
git clone https://github.com/tiandiyiqi/everything-claude-code-zh.git

# 复制规则
cp -r everything-claude-code-zh/rules/* ~/.claude/rules/
```

### 步骤 4：开始使用

```bash
# 尝试一个命令
/plan "添加用户认证"

# 或使用智能助手
/everything
```

---

## ✅ 验证安装

运行以下命令检查安装是否成功：

```bash
/plugin list everything-claude-code-zh@everything-claude-code-zh
```

你应该看到可用的 skills、agents 和 commands 列表。

---

## 📚 下一步

- 阅读 [README.zh-CN.md](README.zh-CN.md) 了解完整功能
- 查看 [INSTALLATION.zh-CN.md](INSTALLATION.zh-CN.md) 了解详细安装选项
- 尝试使用 `/everything` 命令获取智能推荐

---

## ⚠️ 重要提示

**为什么需要手动安装 rules？**

Claude Code 的插件系统目前不支持自动分发 `rules` 目录。这是平台限制，所有插件都需要手动安装 rules。

**Windows 用户：**

使用 PowerShell 或 Git Bash：

```powershell
# PowerShell
Copy-Item -Recurse everything-claude-code-zh\rules\* $env:USERPROFILE\.claude\rules\

# Git Bash
cp -r everything-claude-code-zh/rules/* ~/.claude/rules/
```

---

## 🆘 遇到问题？

1. 确保你使用的是最新版本的 Claude Code
2. 检查 [GitHub Issues](https://github.com/tiandiyiqi/everything-claude-code-zh/issues)
3. 提交新的 Issue 寻求帮助
