# Agent Browser Skill

Vercel Agent Browser - AI 优化的无头浏览器自动化 CLI。

## 安装

本技能已包含 agent-browser 作为依赖。

```bash
cd .claude/skills/agent-browser
npm install
npx agent-browser install  # 下载 Chromium
```

## 使用

在 Claude Code 中使用 agent-browser：

```bash
# 打开页面
npx agent-browser open https://example.com

# 获取快照
npx agent-browser snapshot -i

# 交互操作
npx agent-browser click @e1
npx agent-browser fill @e2 "test@example.com"

# 关闭
npx agent-browser close
```

## 详细文档

请参阅 [SKILL.md](./SKILL.md) 获取完整的使用指南。

## 与 e2e-runner 的关系

- **e2e-runner 智能体**：自动化的完整 E2E 测试流程
- **本技能**：直接使用 agent-browser CLI，适合快速验证和一次性任务
