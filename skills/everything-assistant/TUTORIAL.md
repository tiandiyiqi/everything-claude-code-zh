# 烟花项目新手教程

通过构建一个纯 HTML/CSS/JS + Canvas 的烟花特效项目，在实践中学习 Everything Claude Code 的核心功能。

**目标：** 15 个步骤，覆盖 80%+ 的 Everything 功能。

---

## 📖 如何使用本教程

### 教程设计理念

这是一个**用户学习指南**，而不是 AI 任务清单。每个步骤都会教你：

1. **命令是什么** - 功能和作用
2. **如何使用** - 具体输入方式
3. **会发生什么** - AI 的工作过程
4. **结果在哪里** - 文件位置和查看方法
5. **为什么这样做** - 背后的原理和价值

### 学习方式

**推荐：边学边做**
- 跟随每个步骤的指引
- 实际输入命令，观察 AI 的反应
- 查看生成的文件，理解结果
- 完成"验证学习成果"清单

**不推荐：让 AI 自动完成**
- ❌ 直接说"帮我完成步骤 1-5"
- ❌ 让 AI 一次性执行所有命令
- ✅ 一步一步跟随，理解每个命令的作用

### 教程结构

每个步骤包含：
- **学习目标** - 你将掌握什么技能
- **命令介绍** - 工具的作用和原理
- **实战演练** - 具体操作步骤
- **文件位置** - 结果保存在哪里
- **验证清单** - 检查是否真正理解
- **实际练习** - 额外的练习建议

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

**学习目标：** 掌握使用交互式讨论模式进行需求分析

#### 0.1 什么是 `/interactive-discussion`？

这是一个**选择题式讨论工具**，通过多轮问答帮助你：
- 明确模糊的需求
- 在多个方案中做选择
- 深入思考产品细节

**与普通对话的区别：**
- 普通对话：你问 AI 答，容易遗漏关键问题
- 交互式讨论：AI 主动提问，引导你思考

#### 0.2 如何使用？

**步骤 1：启动讨论**

输入：
```
/interactive-discussion 我想做一个烟花特效项目，帮我讨论一下核心需求
```

**步骤 2：回答 AI 的选择题**

AI 会提出一系列选择题，例如：

```
【问题 1】粒子系统的设计重点是什么？
A. 视觉效果优先（更多粒子、更炫的效果）
B. 性能优先（流畅运行、低资源占用）
C. 平衡两者（适度的效果 + 可接受的性能）

请选择：
```

你回答后，AI 会根据你的选择继续提问：

```
【问题 2】用户交互方式？
A. 仅鼠标点击
B. 鼠标 + 触摸屏（移动设备）
C. 鼠标 + 触摸 + 键盘快捷键

请选择：
```

**步骤 3：查看讨论总结**

完成所有问题后，AI 会生成需求文档：

```markdown
# 烟花项目需求总结

## 核心决策
1. 设计重点：平衡视觉效果与性能
2. 交互方式：支持鼠标、触摸和键盘
3. 目标设备：桌面 + 移动端

## 技术约束
- 粒子数量上限：1000
- 目标帧率：60 FPS
- 浏览器兼容：Chrome/Safari/Firefox 最新版

## 下一步
- 创建技术方案
- 设计粒子系统架构
```

#### 0.3 为什么要用交互式讨论？

**场景 1：需求模糊**
```
用户："我想做一个好看的烟花"
问题：什么叫"好看"？多少粒子？什么颜色？
```

**场景 2：技术选型**
```
用户："我想优化性能"
问题：优化什么？Canvas 还是 WebGL？粒子池还是按需创建？
```

交互式讨论通过**结构化提问**，帮你把模糊需求变成清晰的技术方案。

#### 0.4 讨论结果保存在哪里？

AI 可以选择：
1. 仅在对话中展示（临时讨论）
2. 保存到 `.claude/discussions/` 目录（重要决策）

你可以要求：
```
请将讨论结果保存到文件
```

#### 0.5 验证学习成果

完成本步骤后，你应该能够：
- [ ] 理解交互式讨论的价值（结构化需求分析）
- [ ] 知道如何启动讨论模式
- [ ] 能够通过选择题明确需求
- [ ] 理解讨论结果如何指导后续开发

**实际练习：**
尝试用 `/interactive-discussion` 讨论一个"在线聊天室"的需求，观察 AI 会问哪些问题。

---

### 步骤 1：项目规划 (planner, /plan, file-memory)

**学习目标：** 掌握使用 `/plan` 命令进行复杂功能规划的方法

#### 1.1 什么是 `/plan` 命令？

`/plan` 是 Everything Claude Code 的规划命令，它会：
- 自动调用 **planner 智能体**（专门负责架构设计和任务拆解）
- 分析需求并识别技术风险
- 生成分阶段的实施计划
- 将计划保存到 `.claude/plans/` 目录

#### 1.2 如何使用？

**步骤 1：输入命令**

在 Claude Code 中输入：
```
/plan 创建一个烟花特效项目，包含粒子系统、发射器、用户交互、性能优化和测试
```

**步骤 2：观察 AI 的工作过程**

你会看到：
1. AI 进入"计划模式"（Plan Mode）
2. 分析需求并提出问题（如果需要澄清）
3. 生成多阶段实施计划
4. 询问你是否批准计划

**步骤 3：审查计划**

AI 会生成类似这样的计划：
```
阶段 1：基础粒子系统
  - 创建 Particle 类
  - 实现粒子物理（重力、速度、生命周期）
  - 编写单元测试

阶段 2：烟花发射器
  - 创建 Emitter 类
  - 实现粒子池管理
  - 添加动画循环

...
```

**步骤 4：批准或修改**

- 如果满意，回复 "批准" 或 "开始实施"
- 如果需要调整，直接说明修改意见

#### 1.3 计划文件在哪里？

打开文件浏览器，查看：
```
.claude/plans/[随机名称].md
```

例如：`.claude/plans/lively-sleeping-blanket.md`

#### 1.4 使用 `/file-memory` 保存规划

**为什么需要 file-memory？**

`/file-memory` 技能可以将重要信息持久化到文件系统，避免上下文丢失。它会创建三个文件：
- `task_plan.md` - 任务计划
- `findings.md` - 发现和决策
- `progress.md` - 进度跟踪

**如何使用？**

输入：
```
请使用 /file-memory 保存当前的烟花项目规划
```

AI 会自动创建文件到 `.claude/memory/` 目录。

#### 1.5 验证学习成果

完成本步骤后，你应该能够：
- [ ] 理解 `/plan` 命令的作用
- [ ] 知道如何输入规划需求
- [ ] 能够找到并查看生成的计划文件
- [ ] 理解 file-memory 的持久化作用

**实际练习：**
尝试用 `/plan` 规划一个简单的待办事项应用，观察 AI 如何拆解任务。

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

**学习目标：** 掌握测试驱动开发（TDD）的完整流程

#### 3.1 什么是 `/tdd` 命令?

`/tdd` 命令会：
- 调用 **tdd-guide 智能体**（强制执行"先写测试"原则）
- 引导你完成 RED → GREEN → REFACTOR 循环
- 确保测试覆盖率达到 80% 以上

#### 3.2 TDD 三步循环

```
RED（红灯）   → 先写测试，运行失败（因为功能还没实现）
GREEN（绿灯） → 编写最简代码，让测试通过
REFACTOR（重构）→ 优化代码，保持测试通过
```

#### 3.3 实战演练：粒子系统

**步骤 1：启动 TDD 模式**

输入：
```
/tdd 实现粒子系统，包含粒子初始化、更新和碰撞检测
```

**步骤 2：观察 AI 的工作流程**

AI 会按以下顺序工作：

**阶段 1：RED（写测试）**
```javascript
// AI 会先创建测试文件 tests/particle.test.js
describe('Particle', () => {
  test('should initialize with position and velocity', () => {
    const particle = new Particle(100, 200, 5, -10)
    expect(particle.x).toBe(100)
    expect(particle.y).toBe(200)
    expect(particle.vx).toBe(5)
    expect(particle.vy).toBe(-10)
  })
})
```

AI 会运行测试，显示失败（因为 Particle 类还不存在）。

**阶段 2：GREEN（实现功能）**
```javascript
// AI 创建 js/particle.js
class Particle {
  constructor(x, y, vx, vy) {
    this.x = x
    this.y = y
    this.vx = vx
    this.vy = vy
  }
}
```

AI 再次运行测试，显示通过。

**阶段 3：REFACTOR（重构优化）**

AI 会检查代码质量，可能添加：
- 输入验证
- 默认值
- 注释

**步骤 3：查看测试覆盖率**

AI 会运行覆盖率检查：
```bash
npm test -- --coverage
```

你会看到类似输出：
```
File           | % Stmts | % Branch | % Funcs | % Lines |
---------------|---------|----------|---------|---------|
particle.js    |   95.2  |   88.9   |  100.0  |   95.2  |
```

#### 3.4 为什么要先写测试？

**传统方式的问题：**
```
写代码 → 手动测试 → 发现 Bug → 修复 → 再测试 → ...
```

**TDD 的优势：**
```
写测试 → 写代码 → 自动验证 → 重构 → 自动验证 → 完成
```

- ✅ 测试即文档（说明代码应该做什么）
- ✅ 防止回归（修改代码后立即发现问题）
- ✅ 更好的设计（先思考接口，再实现）

#### 3.5 如何查看测试文件？

打开项目目录：
```
tests/
  ├── particle.test.js      # 粒子测试
  ├── emitter.test.js       # 发射器测试
  └── e2e/                  # E2E 测试（后续步骤）
```

#### 3.6 验证学习成果

完成本步骤后，你应该能够：
- [ ] 理解 TDD 的 RED-GREEN-REFACTOR 循环
- [ ] 知道如何使用 `/tdd` 命令
- [ ] 能够查看测试文件和覆盖率报告
- [ ] 理解"先写测试"的价值

**实际练习：**
尝试用 `/tdd` 实现一个简单的计数器类，观察 AI 如何先写测试。

---

### 步骤 4：烟花发射器 (frontend-patterns, code-reviewer)

**学习目标：** 掌握代码审查流程和前端开发模式

#### 4.1 什么是 code-reviewer 智能体？

**code-reviewer** 是一个专门的代码审查智能体，它会：
- 检查代码质量（命名、结构、复杂度）
- 发现潜在 Bug（边界条件、错误处理）
- 评估性能问题（不必要的循环、内存泄漏）
- 提供改进建议（重构、优化）

**审查等级：**
- 🔴 CRITICAL - 必须修复（会导致崩溃或严重 Bug）
- 🟠 HIGH - 强烈建议修复（影响功能或性能）
- 🟡 MEDIUM - 建议修复（代码质量问题）
- 🟢 LOW - 可选优化（风格或微优化）

#### 4.2 实战演练：发射器实现 + 审查

**步骤 1：实现发射器**

先让 AI 实现基础功能：
```
请实现烟花发射器类，包含：
1. 粒子池管理（复用粒子对象）
2. 发射逻辑（根据点击位置发射）
3. 动画循环（requestAnimationFrame）
```

AI 会创建 `js/emitter.js`：
```javascript
class Emitter {
  constructor(canvas) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    this.particles = []
  }

  emit(x, y) {
    for (let i = 0; i < 50; i++) {
      this.particles.push(new Particle(x, y))
    }
  }

  update() {
    this.particles.forEach(p => p.update())
    this.particles = this.particles.filter(p => p.isAlive())
  }

  render() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)
    this.particles.forEach(p => p.render(this.ctx))
    requestAnimationFrame(() => this.render())
  }
}
```

**步骤 2：调用代码审查**

输入：
```
请使用 code-reviewer 审查 js/emitter.js
```

**步骤 3：查看审查报告**

AI 会返回类似报告：

```markdown
# 代码审查报告：js/emitter.js

## 🔴 CRITICAL 问题

无

## 🟠 HIGH 问题

1. **内存泄漏风险** (第 8 行)
   - 问题：每次 emit() 都创建新粒子，从不释放
   - 影响：长时间运行会导致内存溢出
   - 建议：实现粒子池复用机制

2. **无限递归风险** (第 18 行)
   - 问题：render() 无条件调用自身
   - 影响：无法停止动画循环
   - 建议：添加 stop() 方法和状态标志

## 🟡 MEDIUM 问题

1. **魔法数字** (第 8 行)
   - 问题：硬编码 50 个粒子
   - 建议：提取为配置常量

## 改进建议

```javascript
class Emitter {
  constructor(canvas, config = {}) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    this.particles = []
    this.particlePool = []  // 粒子池
    this.isRunning = false
    this.config = {
      particlesPerEmit: 50,
      maxParticles: 1000,
      ...config
    }
  }

  emit(x, y) {
    const count = Math.min(
      this.config.particlesPerEmit,
      this.config.maxParticles - this.particles.length
    )

    for (let i = 0; i < count; i++) {
      const particle = this.getParticle()  // 从池中获取
      particle.reset(x, y)
      this.particles.push(particle)
    }
  }

  getParticle() {
    return this.particlePool.pop() || new Particle()
  }

  recycleParticle(particle) {
    this.particlePool.push(particle)
  }

  start() {
    this.isRunning = true
    this.render()
  }

  stop() {
    this.isRunning = false
  }

  render() {
    if (!this.isRunning) return

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height)

    // 更新并回收死亡粒子
    this.particles = this.particles.filter(p => {
      p.update()
      if (!p.isAlive()) {
        this.recycleParticle(p)
        return false
      }
      p.render(this.ctx)
      return true
    })

    requestAnimationFrame(() => this.render())
  }
}
```
```

**步骤 4：应用改进**

告诉 AI：
```
请应用审查建议，修复 HIGH 和 MEDIUM 问题
```

AI 会更新代码并再次运行审查，直到没有严重问题。

#### 4.3 frontend-patterns 技能

在实现过程中，AI 会参考 `frontend-patterns` 技能，它包含：
- Canvas 动画最佳实践
- 对象池模式（Object Pool Pattern）
- 性能优化技巧
- 事件处理模式

你可以查看：
```
~/.claude/skills/frontend-patterns/SKILL.md
```

#### 4.4 为什么要代码审查？

**场景：没有审查**
```
写代码 → 看起来能用 → 提交 → 生产环境崩溃 😱
```

**场景：有审查**
```
写代码 → 审查发现问题 → 修复 → 再审查 → 提交 ✅
```

代码审查的价值：
- 🐛 提前发现 Bug
- 📈 提升代码质量
- 🎓 学习最佳实践
- 🔒 避免安全漏洞

#### 4.5 验证学习成果

完成本步骤后，你应该能够：
- [ ] 理解 code-reviewer 的审查等级
- [ ] 知道如何触发代码审查
- [ ] 能够读懂审查报告
- [ ] 理解对象池等前端模式
- [ ] 知道如何应用改进建议

**实际练习：**
实现一个简单的计时器组件，然后用 code-reviewer 审查，看看会发现什么问题。

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

**学习目标：** 掌握全面验证流程，确保代码质量

#### 11.1 什么是验证循环？

**verification-loop** 是一个自动化验证系统，它会依次执行：

```
1. 构建检查 → 2. Lint 检查 → 3. 测试运行 → 4. 覆盖率检查 → 5. 安全扫描
```

**为什么需要验证循环？**

手动验证的问题：
```
开发者："我觉得代码没问题"
→ 忘记运行测试
→ 忘记检查覆盖率
→ 忘记 Lint
→ 提交后 CI 失败 😱
```

自动验证的优势：
```
/verify
→ 自动运行所有检查
→ 发现问题立即报告
→ 修复后再次验证
→ 全部通过才提交 ✅
```

#### 11.2 如何使用？

**步骤 1：触发验证**

输入：
```
/verify
```

或者：
```
请运行完整的验证循环
```

**步骤 2：观察验证过程**

AI 会依次执行：

**阶段 1：构建检查**
```bash
# 如果是 TypeScript 项目
npm run build

# 如果是纯 JS 项目，跳过此步骤
```

输出示例：
```
✅ Build successful
   - 0 errors
   - 0 warnings
```

**阶段 2：Lint 检查**
```bash
npm run lint
# 或
eslint js/**/*.js
```

输出示例：
```
✅ Lint passed
   - 0 errors
   - 2 warnings (可接受)
```

**阶段 3：测试运行**
```bash
npm test
```

输出示例：
```
✅ Tests passed
   - 15 tests passed
   - 0 tests failed
   - Duration: 2.3s
```

**阶段 4：覆盖率检查**
```bash
npm test -- --coverage
```

输出示例：
```
✅ Coverage meets threshold (80%)
   - Statements: 92.5%
   - Branches: 88.3%
   - Functions: 95.0%
   - Lines: 92.1%
```

**阶段 5：安全扫描**
```bash
npm audit
```

输出示例：
```
✅ No security vulnerabilities found
   - 0 vulnerabilities
```

**步骤 3：查看验证报告**

AI 会生成汇总报告：

```markdown
# 验证报告

## ✅ 所有检查通过

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 构建 | ✅ | 无错误 |
| Lint | ✅ | 2 个警告（可接受）|
| 测试 | ✅ | 15/15 通过 |
| 覆盖率 | ✅ | 92.5% (>80%) |
| 安全 | ✅ | 无漏洞 |

## 可以安全提交代码
```

**步骤 4：如果有失败项**

假设测试失败：

```markdown
# 验证报告

## ❌ 发现问题

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 构建 | ✅ | 无错误 |
| Lint | ✅ | 无问题 |
| 测试 | ❌ | 2/15 失败 |
| 覆盖率 | ⏸️ | 跳过（测试未通过）|
| 安全 | ⏸️ | 跳过（测试未通过）|

## 失败的测试

1. **Emitter.emit() 应该限制粒子数量**
   - 预期：1000
   - 实际：1050
   - 位置：tests/emitter.test.js:42

2. **Particle.update() 应该应用重力**
   - 预期：vy = 10
   - 实际：vy = 0
   - 位置：tests/particle.test.js:28

## 下一步

修复失败的测试，然后重新运行 /verify
```

AI 会自动修复问题，然后再次运行验证。

#### 11.3 验证循环的配置

验证循环会读取项目配置：

**package.json**
```json
{
  "scripts": {
    "build": "tsc",
    "lint": "eslint js/**/*.js",
    "test": "jest",
    "test:coverage": "jest --coverage"
  }
}
```

**jest.config.js**
```javascript
module.exports = {
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 80,
      functions: 80,
      lines: 80
    }
  }
}
```

#### 11.4 何时使用验证循环？

**必须使用的场景：**
- ✅ 提交代码前
- ✅ 创建 PR 前
- ✅ 合并到主分支前
- ✅ 发布新版本前

**可选使用的场景：**
- 完成一个功能模块后
- 重构代码后
- 修复 Bug 后

#### 11.5 验证循环 vs 手动检查

| 对比项 | 手动检查 | 验证循环 |
|--------|---------|---------|
| 速度 | 慢（逐个运行）| 快（自动化）|
| 遗漏风险 | 高（容易忘记）| 低（强制执行）|
| 一致性 | 低（每次不同）| 高（标准流程）|
| 报告 | 无 | 详细报告 |

#### 11.6 验证学习成果

完成本步骤后，你应该能够：
- [ ] 理解验证循环的 5 个阶段
- [ ] 知道如何触发验证
- [ ] 能够读懂验证报告
- [ ] 理解何时必须运行验证
- [ ] 知道如何配置验证阈值

**实际练习：**
故意在代码中引入一个 Bug（例如删除一个测试），然后运行 `/verify`，观察验证循环如何发现问题。

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

### 步骤 13：学习管理 (continuous-learning-v3, claudeception)

**目标：** 学习如何提取和管理学习成果

**任务：**
1. 调用 `/claudeception`
2. 提取本项目中学到的模式：
   - Canvas 动画模式
   - 粒子系统设计模式
   - 性能优化技巧

**核心功能：** continuous-learning-v3 技能、claudeception 命令

**预期产出：** 项目技能库

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

---

## 📝 教程设计说明（给维护者）

### 为什么要重新设计教程？

**原教程的问题：**
- 面向 AI 的任务清单，而非用户学习指南
- 缺少命令使用方法和预期交互过程
- 没有说明结果文件的位置
- "预期产出"是任务结果，而非学习成果

**新教程的改进：**
- 每个步骤都是完整的学习单元
- 包含命令介绍、使用方法、预期过程、文件位置
- 强调"为什么"（原理和价值）
- 提供验证清单和实际练习

### 教程编写原则

1. **用户视角**
   - 假设用户第一次使用命令
   - 解释每个命令的作用和原理
   - 展示完整的交互过程

2. **可验证性**
   - 每个步骤都有明确的验证清单
   - 用户可以自我检查是否真正理解
   - 提供额外的练习建议

3. **文件可见性**
   - 明确说明生成的文件位置
   - 引导用户打开文件查看
   - 解释文件内容的意义

4. **渐进式学习**
   - 从简单到复杂
   - 每个步骤都基于前面的知识
   - 避免一次性引入太多概念

### 如何扩展教程

如果要添加新步骤，请遵循以下模板：

```markdown
### 步骤 X：[功能名称] ([相关技能/智能体])

**学习目标：** 掌握 [具体技能]

#### X.1 什么是 [命令/工具]？

[解释功能、作用、与其他工具的区别]

#### X.2 如何使用？

**步骤 1：[操作名称]**
[具体输入内容]

**步骤 2：观察 AI 的工作过程**
[描述 AI 会做什么，用户会看到什么]

**步骤 3：查看结果**
[文件位置、如何打开、内容解释]

#### X.3 为什么要用 [工具]？

[场景对比、价值说明]

#### X.4 [结果/文件] 在哪里？

[具体路径、查看方法]

#### X.5 验证学习成果

完成本步骤后，你应该能够：
- [ ] [技能点 1]
- [ ] [技能点 2]
- [ ] [技能点 3]

**实际练习：**
[额外的练习建议]
```

### 维护建议

1. **定期更新**
   - 当命令行为变化时，更新相应步骤
   - 添加用户反馈的常见问题
   - 补充实际使用中的最佳实践

2. **收集反馈**
   - 哪些步骤用户容易卡住？
   - 哪些概念需要更详细的解释？
   - 哪些练习最有帮助？

3. **保持一致性**
   - 所有步骤使用相同的结构
   - 术语使用保持一致
   - 代码示例风格统一
