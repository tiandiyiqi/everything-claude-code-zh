---
name: continuous-learning-v3
description: 统一学习管道——在 v2 直觉架构上新增 communication 领域，支持术语偏好、句式习惯和项目概念的自动学习与表达库视图。
version: 3.0.0
---

# 持续学习 v3 — 统一学习管道

v3 = v2 全部能力 + communication 领域 + 表达库视图。

## 版本演进

| 版本 | 观测方式 | 学习粒度 | 新增能力 |
|------|---------|---------|---------|
| v1 | Stop 钩子 | 完整技能 | — |
| v2 | PreToolUse/PostToolUse | 原子化直觉 + 置信度 | 导出/导入 |
| v3 | 复用 v2 钩子 | v2 + communication 领域 | 表达库 |

## 与 v2 的关系

v3 是 v2 的**完全独立版本**：

- 包含完整的观测基础设施（`hooks/observe.sh`）
- 包含完整的智能体定义（`agents/observer.md`、`agents/start-observer.sh`）
- 包含完整的脚本工具（`scripts/instinct-cli.py` 等）
- 新增 communication 和 code-navigation 领域支持
- 不再依赖 v2 的任何文件（已移除 config.json 中的 extends）

## communication 领域

### 三种子类型

| 子类型 | 说明 | 示例 |
|--------|------|------|
| `terminology` | 术语偏好 | "用户画像" → "用户档案" |
| `phrasing` | 句式习惯 | "帮我..." → "请帮我..." |
| `project-concept` | 项目概念 | "磨刀石" → 当前项目代号 |

### 自动检测

observer 智能体会在以下场景自动创建 communication 直觉：

- 用户反复使用特定术语代替标准术语（≥2 次）
- 用户纠正 Claude 的措辞（"不要说 X，说 Y"）
- 用户使用项目特定的缩写或代号
- 用户的句式偏好

**置信度规则：**
- 自动检测（1-2 次）: 0.4
- 自动检测（3+ 次）: 0.6
- 用户明确纠正: 0.7

## 表达库视图

运行 `expressions-view.py` 生成表达库表格：

```bash
python3 ~/.claude/skills/continuous-learning-v3/scripts/expressions-view.py
```

输出到 `~/.claude/homunculus/views/expressions.md`：

```markdown
| 类型 | 你的表达 | 标准/替代表达 | 置信度 | 来源 |
|------|---------|-------------|--------|------|
| 术语 | 用户画像 | 用户档案 | 70% | session-observation |
| 句式 | 帮我... | 请帮我... | 85% | session-observation |
```

## 双库系统

- **全局表达库**：`~/.claude/homunculus/instincts/personal/comm-*.yaml` — 跨项目通用的表达偏好
- **项目级表达库**：`.claude/communication/` — 项目特定的术语和概念

## 数据流

```
用户对话
  │
  │ observe.sh 捕获（复用 v2，不变）
  ▼
observations.jsonl（不变）
  │
  │ observer 智能体分析（扩展：+communication_patterns）
  ▼
instincts/personal/
  ├── prefer-functional.yaml      (domain: code-style)     ← 不变
  ├── always-test-first.yaml      (domain: testing)        ← 不变
  ├── comm-user-portrait.yaml     (domain: communication)  ← 新增
  └── comm-help-phrasing.yaml     (domain: communication)  ← 新增
  │
  │ expressions-view.py 生成视图（新增）
  ▼
views/expressions.md  ← 表达库表格视图（新增）
```

## 命令

| 命令 | 描述 |
|------|------|
| `/instinct-status` | 显示所有直觉（含 communication 领域的表格视图） |
| `/evolve` | 聚类直觉（自然支持 communication 领域） |

## 文件结构

```
skills/continuous-learning-v3/
├── SKILL.md                              ← 技能文档
├── config.json                           ← 完整独立配置（已移除 extends）
├── hooks/
│   └── observe.sh                        ← 观测钩子（从 v2 复制）
├── agents/
│   ├── observer.md                       ← 通用观测者（含 communication 扩展）
│   ├── start-observer.sh                 ← 启动脚本（从 v2 复制）
│   └── communication-observer.md         ← communication 专属规范
├── scripts/
│   ├── instinct-cli.py                   ← 直觉管理 CLI（从 v2 复制）
│   ├── expressions-view.py               ← 表达库视图生成器
│   ├── growth-report.py                  ← 成长报告生成器
│   ├── instinct-generator.py             ← 直觉生成器
│   └── instinct-manager.py               ← 直觉管理器
└── templates/
    ├── code-navigation-instinct.yaml     ← 代码导航模板
    └── communication-instinct.yaml       ← 沟通直觉模板
```

---

*统一学习管道：编程直觉 + 沟通风格，一套架构全覆盖。*
