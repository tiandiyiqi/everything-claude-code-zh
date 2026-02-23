# 烟花项目新手教程

通过构建一个纯 HTML/CSS/JS + Canvas 的烟花特效项目，在实践中学习 Everything Claude Code 的核心功能。

**目标：** 15 个步骤，覆盖 80%+ 的 Everything 功能。

---

## 项目概览

**项目名称：** claude-fireworks
**技术栈：** HTML + CSS + JavaScript + Canvas API
**预期时间：** 2-3 小时（完整学习）
**难度：** 初级 → 中级

### 最终效果

一个交互式烟花特效应用，支持：
- 点击屏幕发射烟花
- 自动烟花模式
- 性能监控面板
- 配置调整
- 完整的测试覆盖

---

## 15 个学习步骤

### 步骤 0：需求讨论 (interactive-discussion)

**目标：** 学习如何用 Everything 进行深度需求讨论

**任务：**
1. 调用 `/interactive-discussion`
2. 讨论烟花项目的核心需求：
   - 粒子系统如何设计？
   - 性能优化的优先级？
   - 用户交互方式？
3. 记录决策

**核心功能：** interactive-discussion 选择题式讨论

**预期产出：** 需求文档（可选）

---

### 步骤 1：项目规划 (planner, /plan, file-memory)

**目标：** 学习如何规划复杂功能

**任务：**
1. 调用 `/plan`
2. 创建烟花项目的实施计划：
   - 阶段 1：基础粒子系统
   - 阶段 2：烟花发射器
   - 阶段 3：用户交互
   - 阶段 4：性能优化
   - 阶段 5：测试与文档
3. 使用 `/file-memory` 保存规划

**核心功能：** planner 智能体、/plan 命令、file-memory 技能

**预期产出：** 详细的实施计划

---

### 步骤 2：编码标准 (coding-standards)

**目标：** 学习项目的编码规范

**任务：**
1. 阅读 `coding-standards` 技能
2. 为烟花项目建立编码规范：
   - 文件组织（HTML、CSS、JS 分离）
   - 命名约定（驼峰式、常量大写）
   - 函数大小限制（<50 行）
   - 注释规范
3. 创建 `.claude/rules/coding-style.md`（项目级）

**核心功能：** coding-standards 技能

**预期产出：** 项目编码规范文档

---

### 步骤 3：TDD - 粒子系统 (tdd-workflow, tdd-guide)

**目标：** 学习测试驱动开发

**任务：**
1. 调用 `/tdd`
2. 为粒子系统编写测试（RED）：
   - 粒子初始化测试
   - 粒子更新测试
   - 粒子碰撞检测测试
3. 实现粒子系统代码（GREEN）
4. 重构优化（REFACTOR）
5. 验证覆盖率 ≥ 80%

**核心功能：** tdd-guide 智能体、tdd-workflow 技能

**预期产出：** 粒子系统代码 + 测试（覆盖率 ≥ 80%）

---

### 步骤 4：烟花发射器 (frontend-patterns, code-reviewer)

**目标：** 学习前端模式与代码审查

**任务：**
1. 参考 `frontend-patterns` 技能
2. 实现烟花发射器组件：
   - 发射器类设计
   - 粒子池管理
   - 动画循环
3. 调用 `/code-review`（或 code-reviewer 智能体）
4. 根据审查意见改进代码

**核心功能：** frontend-patterns 技能、code-reviewer 智能体

**预期产出：** 烟花发射器代码 + 审查反馈

---

### 步骤 5：用户交互 (security-review)

**目标：** 学习安全审查

**任务：**
1. 实现用户交互：
   - 鼠标点击事件
   - 触摸事件（移动设备）
   - 键盘快捷键
2. 调用 `/security-review`
3. 检查是否有 XSS、事件注入等安全问题
4. 修复安全问题

**核心功能：** security-review 技能

**预期产出：** 安全的用户交互代码

---

### 步骤 6：性能优化 (architect)

**目标：** 学习架构设计与性能优化

**任务：**
1. 调用 architect 智能体
2. 分析性能瓶颈：
   - Canvas 绘制性能
   - 粒子数量限制
   - 内存管理
3. 实现优化方案：
   - 粒子池复用
   - 批量绘制
   - 帧率控制
4. 添加性能监控面板

**核心功能：** architect 智能体

**预期产出：** 优化后的代码 + 性能报告

---

### 步骤 7：配置面板 (interactive-discussion)

**目标：** 学习交互式讨论设计

**任务：**
1. 调用 `/interactive-discussion`
2. 讨论配置面板的设计：
   - 哪些参数可配置？
   - UI 布局如何设计？
   - 配置如何持久化？
3. 实现配置面板

**核心功能：** interactive-discussion 技能

**预期产出：** 配置面板代码

---

### 步骤 8：E2E 测试 (e2e-runner)

**目标：** 学习端到端测试

**任务：**
1. 调用 `/e2e` 或 e2e-runner 智能体
2. 编写 E2E 测试场景：
   - 页面加载测试
   - 点击发射烟花测试
   - 配置修改测试
   - 自动模式测试
3. 运行测试并捕获截图/视频
4. 验证关键用户流程

**核心功能：** e2e-runner 智能体

**预期产出：** E2E 测试代码 + 测试报告

---

### 步骤 9：代码清理 (refactor-cleaner)

**目标：** 学习冗余代码清理

**任务：**
1. 调用 refactor-cleaner 智能体
2. 扫描项目中的：
   - 未使用的变量
   - 重复代码
   - 死代码
3. 清理并重构
4. 验证功能不变

**核心功能：** refactor-cleaner 智能体

**预期产出：** 清理后的代码

---

### 步骤 10：文档与 Git (doc-updater, git-workflow)

**目标：** 学习文档维护与 Git 工作流

**任务：**
1. 调用 `/update-docs` 或 doc-updater 智能体
2. 创建项目文档：
   - README.md（项目概览）
   - API 文档（类和方法）
   - 使用指南
3. 更新代码图谱（CODEMAPS）
4. 按 Conventional Commits 规范提交代码

**核心功能：** doc-updater 智能体、git-workflow 规则

**预期产出：** 完整的项目文档 + Git 提交历史

---

### 步骤 11：验证循环 (verification-loop, /verify)

**目标：** 学习全面验证

**任务：**
1. 调用 `/verify` 或 verification-loop 技能
2. 执行完整验证：
   - 构建检查（如适用）
   - Lint 检查
   - 测试运行（单元 + E2E）
   - 覆盖率检查（≥ 80%）
   - 安全扫描
3. 修复所有问题

**核心功能：** verification-loop 技能

**预期产出：** 验证报告（所有检查通过）

---

### 步骤 12：新功能编排 (/orchestrate, iterative-retrieval)

**目标：** 学习多智能体编排

**任务：**
1. 添加新功能：例如"烟花录制与回放"
2. 调用 `/orchestrate feature`
3. 系统自动编排：
   - planner 创建规划
   - tdd-guide 指导测试
   - code-reviewer 审查代码
   - verification-loop 验证
4. 使用 iterative-retrieval 优化上下文

**核心功能：** /orchestrate 命令、iterative-retrieval 技能

**预期产出：** 新功能完整实现

---

### 步骤 13：学习管理 (continuous-learning-v2, /learn)

**目标：** 学习如何提取和管理学习成果

**任务：**
1. 调用 `/learn`
2. 提取本项目中学到的模式：
   - Canvas 动画模式
   - 粒子系统设计模式
   - 性能优化技巧
3. 使用 continuous-learning-v2 保存为直觉（instincts）
4. 查看 `/instinct-status`

**核心功能：** continuous-learning-v2 技能、/learn 命令

**预期产出：** 项目学习直觉库

---

### 步骤 14：上下文管理 (strategic-compact, file-memory)

**目标：** 学习上下文压缩与文件记忆

**任务：**
1. 项目完成后，上下文可能很长
2. 调用 `/strategic-compact` 进行策略性压缩
3. 使用 `/file-memory` 保存项目状态快照
4. 验证后续会话可以快速恢复

**核心功能：** strategic-compact 技能、file-memory 技能

**预期产出：** 压缩的上下文 + 项目快照

---

## 学习路径总结

| 步骤 | 功能类型 | 核心学习 | 时间 |
|------|---------|---------|------|
| 0 | 讨论 | 需求分析 | 15 分钟 |
| 1 | 规划 | 项目规划 | 20 分钟 |
| 2 | 标准 | 编码规范 | 10 分钟 |
| 3 | TDD | 测试驱动 | 30 分钟 |
| 4 | 前端 | 代码审查 | 25 分钟 |
| 5 | 安全 | 安全审查 | 15 分钟 |
| 6 | 架构 | 性能优化 | 30 分钟 |
| 7 | 讨论 | 交互设计 | 15 分钟 |
| 8 | E2E | 端到端测试 | 25 分钟 |
| 9 | 清理 | 代码重构 | 15 分钟 |
| 10 | 文档 | 文档维护 | 20 分钟 |
| 11 | 验证 | 全面验证 | 15 分钟 |
| 12 | 编排 | 多智能体 | 30 分钟 |
| 13 | 学习 | 知识管理 | 15 分钟 |
| 14 | 上下文 | 上下文管理 | 10 分钟 |
| **总计** | | | **~4 小时** |

---

## 快速启动

### 从头开始
```bash
/fireworks-tutorial
```

### 跳转到特定步骤
```bash
/fireworks-tutorial 5
```

### 查看进度
```bash
/fireworks-tutorial status
```

---

## 常见问题

**Q: 我可以跳过某些步骤吗？**
A: 可以，但建议按顺序学习。每个步骤都为后续步骤奠定基础。

**Q: 如果我卡住了怎么办？**
A: 调用 `/everything search <关键词>` 查找相关功能，或使用 `/interactive-discussion` 讨论问题。

**Q: 完成后可以做什么？**
A:
- 尝试添加新功能（步骤 12）
- 将学到的模式应用到其他项目
- 导出学习成果（`/instinct-export`）与他人分享

---

## 项目文件结构

完成教程后，你的项目结构应该是：

```
claude-fireworks/
├── index.html           # 主页面
├── styles.css           # 样式
├── js/
│   ├── particle.js      # 粒子类
│   ├── emitter.js       # 发射器类
│   ├── app.js           # 主应用
│   └── config.js        # 配置管理
├── tests/
│   ├── particle.test.js
│   ├── emitter.test.js
│   └── e2e/
│       └── fireworks.spec.js
├── docs/
│   ├── README.md
│   ├── API.md
│   └── CODEMAPS.md
└── .claude/
    └── rules/
        └── coding-style.md
```

---

## 下一步

完成教程后：
1. 尝试 `/everything list` 查看所有功能
2. 在自己的项目中应用学到的模式
3. 使用 `/learn` 提取新的学习成果
4. 加入 Everything Claude Code 社区分享经验

祝你学习愉快！🎆
