---
name: everything-assistant
description: Everything Claude Code 智能助手。自动分析用户意图，推荐最匹配的 skill/agent/command。当用户表达困惑、开始新任务、或手动调用 /everything 时激活。
version: "1.2.0"
category: "meta"
---

# Everything 智能助手

此技能是 Everything Claude Code 的"元技能"——它不直接执行任务，而是帮助你找到最合适的工具。

## 何时激活

### 自动触发

- 用户表达"不知道该怎么做"、"有什么工具可以用"、"该用哪个功能"
- 用户开始新任务但未指定工具或 skill
- 用户首次使用 Everything Claude Code

### 手动触发

- `/everything` — 基于当前上下文推荐
- `/everything list` — 列出所有功能
- `/everything search <关键词>` — 搜索特定功能
- `/everything tutorial` — 启动烟花教程

### 不触发

- 用户已明确在使用某个 skill/agent（如已调用 `/plan`、`/tdd`）
- 纯代码编辑操作，无需推荐

---

## 预编译知识摘要

以下是所有 Everything Claude Code 功能的紧凑索引。读取此文件一次即可完成推荐，无需读取其他文件。

### Agents（14 个）

| Agent | 核心用途 | 触发关键词 |
|-------|---------|----------|
| planner | 复杂功能与重构的实施规划 | 新功能、规划、拆解、实现方案 |
| architect | 系统设计与架构决策 | 架构、设计模式、可扩展性、ADR |
| tdd-guide | 测试驱动开发，强制先写测试 | TDD、红绿重构、覆盖率、单元测试 |
| code-reviewer | 代码质量、安全性、可维护性审查 | 代码审查、git diff、质量检查 |
| security-reviewer | 安全漏洞检测与修复 | SQL 注入、XSS、OWASP、密钥泄露 |
| build-error-resolver | TypeScript/构建错误快速修复 | tsc 错误、类型错误、构建失败 |
| error-diagnostician | 系统化错误诊断与根因分析 | 运行时错误、5W2H、根因分析、性能问题 |
| e2e-runner | 端到端测试（Playwright） | E2E、用户旅程、Playwright、截图 |
| refactor-cleaner | 冗余代码清理与合并 | 死代码、未使用导出、knip、重复代码 |
| doc-updater | 文档与代码图谱维护 | 代码图谱、README、文档更新 |
| database-reviewer | PostgreSQL 查询优化与模式设计 | SQL、索引、RLS、Supabase |
| go-build-resolver | Go 构建错误与 vet 问题修复 | go build、go vet、编译错误 |
| go-reviewer | Go 代码审查，地道 Go 模式 | Go 审查、并发、错误处理 |
| python-reviewer | Python 代码审查，PEP 8 合规 | Python 审查、mypy、ruff、类型提示 |

### Skills（36 个）

#### 开发模式 (Patterns)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| coding-standards | 通用编码标准与最佳实践 | 可读性、KISS、DRY、YAGNI |
| frontend-patterns | React/Next.js 前端模式 | 组件、Hook、状态管理、SSR |
| backend-patterns | 后端架构、API 设计、缓存 | API、仓储模式、中间件、缓存 |
| golang-patterns | Go 惯用模式与最佳实践 | Go 接口、并发、错误处理 |
| python-patterns | Python 惯用模式、PEP 8 | 类型提示、装饰器、异常处理 |
| django-patterns | Django 架构、ORM、DRF | 模型、序列化器、视图集、信号 |
| springboot-patterns | Spring Boot 架构、REST API | 控制器、服务层、DTO、异常处理 |
| jpa-patterns | JPA/Hibernate 性能优化 | 实体设计、N+1、事务、索引 |
| java-coding-standards | Java 编码规范（Spring Boot） | 命名、不可变性、Optional、流 |
| project-guidelines-example | 项目特定指南模板 | 架构概览、文件结构、代码模式 |

#### 测试 (Testing)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| tdd-workflow | 测试驱动开发完整工作流 | 红绿重构、覆盖率 80%、先写测试 |
| e2e-testing | E2E 测试最佳实践和模式 | 侦察-然后-行动、关键用户流程、Playwright、Agent Browser、测试金字塔 |
| golang-testing | Go 测试模式、表格驱动测试 | 表格驱动、子测试、基准测试、模糊测试 |
| python-testing | Python 测试、pytest | Fixtures、参数化、Mock、异步测试 |
| django-tdd | Django TDD、pytest-django | 工厂、Mock、覆盖率、集成测试 |
| springboot-tdd | Spring Boot TDD、JUnit 5 | MockMvc、Testcontainers、JaCoCo |
| eval-harness | 评测驱动开发框架 | 评测定义、回归评测、pass@k |

#### 安全 (Security)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| security-review | 安全审查与漏洞检查 | 凭据管理、输入校验、OWASP |
| django-security | Django 安全最佳实践 | CSRF、认证、授权、XSS |
| springboot-security | Spring Boot 安全 | Spring Security、JWT、密钥管理 |

#### 数据库 (Database)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| postgres-patterns | PostgreSQL 查询优化与安全 | 索引、RLS、UPSERT、游标分页 |
| clickhouse-io | ClickHouse 分析模式 | 列式存储、物化视图、分析查询 |

#### 验证 (Verification)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| verification-loop | 全面验证系统（构建+测试+安全） | 构建检查、类型检查、Lint、覆盖率 |
| django-verification | Django 验证循环 | 迁移、测试、安全扫描、部署检查 |
| springboot-verification | Spring Boot 验证循环 | 构建、静态分析、测试、安全扫描 |

#### 并行执行 (Parallel Execution)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| parallel-patterns | 并行子智能体模式（4 种模式） | 并行、扇形研究、并行审查、混合工作流 |

#### 学习 (Learning)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| continuous-learning-v3 | 统一学习管道、沟通风格学习 | 沟通模式、表达库、学习管道 |

#### 项目初始化 (Project Setup)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| create-project-rules | 根据项目信息生成项目规则文件 | 创建规则、项目规范、编码标准、初始化 |

#### 规划与检索 (Planning & Retrieval)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| file-memory | 文件持久化记忆（三文件模式） | 任务计划、发现记录、进度日志 |
| iterative-retrieval | 迭代检索、上下文优化 | 分发、评估、优化、循环 |
| strategic-compact | 策略性上下文压缩 | 压缩建议、阈值检测、逻辑边界 |

#### Superpowers 工作流

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| superpowers-git-worktree | Git 工作树隔离工作空间 | 工作树、隔离、worktree、分支隔离 |
| superpowers-finishing-branch | 完成开发分支（4 个选项） | 完成分支、合并、PR、清理工作树 |
| superpowers-task-planning | 细粒度任务规划（2-5 分钟） | 细粒度、小任务、详细计划、TDD 步骤 |

#### 需求与产品 (Requirements & Product)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| business-analyst | 需求分析、5 Whys、JTBD、SMART | 需求调研、产品发现、根因分析、用户画像 |
| product-manager | PRD 生成、MoSCoW 排序、用户故事 | PRD、需求文档、优先级、验收标准 |

#### 讨论 (Discussion)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| interactive-discussion | 分阶段互动讨论、选择题方式 | 需求讨论、方案细化、多维分析、工作流 |

#### 发布 (Release)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| changelog-generator | 自动生成用户友好的变更日志 | 变更日志、发布说明、版本发布、CHANGELOG |

### Commands（30 个）

| Command | 用途 |
|---------|------|
| /workflow | 分阶段项目工作流（需求→设计→开发→测试→部署） |
| /everything | 智能功能推荐（分析上下文，推荐最匹配的功能） |
| /fireworks-tutorial | 烟花项目新手教程（实践学习 80%+ 功能） |
| /plan | 创建实施计划（调用 planner agent） |
| /tdd | 测试驱动开发工作流 |
| /code-review | 代码审查 |
| /verify | 全面验证（构建+测试+安全） |
| /orchestrate | 多智能体顺序编排 |
| /e2e | 端到端测试 |
| /build-fix | 修复构建错误 |
| /refactor-clean | 冗余代码清理 |
| /learn | 提取可复用模式 |
| /learn-style | 手动记录沟通表达偏好 |
| /evolve | 将直觉演进为技能/命令/智能体 |
| /instinct-status | 查看已学习的直觉 |
| /instinct-export | 导出直觉 |
| /instinct-import | 导入直觉 |
| /eval | 评测驱动开发 |
| /file-memory | 文件持久化记忆 |
| /skill-create | 从 git 历史提取技能 |
| /checkpoint | 创建检查点 |
| /setup-pm | 配置项目管理 |
| /update-codemaps | 更新代码图谱 |
| /update-docs | 更新文档 |
| /test-coverage | 测试覆盖率报告 |
| /growth-report | 个人成长报告（工作概览、习得技能、改进建议） |
| /go-build | Go 构建错误修复 |
| /go-review | Go 代码审查 |
| /go-test | Go TDD |
| /python-review | Python 代码审查 |

### Rules（9 个）

| Rule | 核心要点 |
|------|---------|
| agents | 智能体编排规则、并行执行、多维度分析 |
| coding-style | 不可变性、文件组织、错误处理、输入校验 |
| git-workflow | Conventional Commits、PR 工作流、功能实现流程 |
| helpers | 标准化操作参考中心（工作流模板、报告格式、检查清单、错误处理协议） |
| hooks | 钩子系统、文档拦截器、自动格式化 |
| patterns | API 响应格式、自定义 Hook、仓储模式 |
| performance | 模型选择策略、上下文窗口管理、Ultrathink |
| security | 强制安全检查、凭据管理、安全响应协议 |
| testing | 80% 覆盖率、TDD 工作流、测试失败排查 |

---

## 推荐匹配规则

### 三层匹配逻辑

#### 第一层：任务类型匹配

| 用户意图关键词 | 推荐功能 | 优先级 |
|--------------|---------|-------|
| 新项目、从零开始、完整项目 | /workflow → 分阶段工作流 | P0 |
| 需求分析、产品发现 | business-analyst skill | P0 |
| PRD、需求文档、优先级排序 | product-manager skill | P0 |
| 新功能、实现、开发 | planner agent + /plan + tdd-workflow | P0 |
| 细粒度任务、详细步骤、2-5 分钟 | superpowers-task-planning + /superpowers-plan | P0 |
| 隔离工作空间、工作树、分支隔离 | superpowers-git-worktree | P0 |
| 完成分支、合并、PR、清理 | superpowers-finishing-branch + /finish-branch | P0 |
| Bug、修复、报错 | error-diagnostician + tdd-guide + /verify | P0 |
| 重构、清理、优化 | refactor-cleaner + code-reviewer | P1 |
| 安全、认证、授权 | security-reviewer + security-review skill | P0 |
| 测试、覆盖率 | tdd-workflow + /test-coverage | P1 |
| 架构、设计、选型 | architect agent + interactive-discussion | P1 |
| 文档、README | doc-updater agent + /update-docs | P2 |
| 学习、模式提取 | continuous-learning-v3 + claudeception | P2 |
| 讨论、需求、方案 | interactive-discussion | P1 |
| 部署、CI/CD | verification-loop + /verify | P1 |
| 并行、多维度分析 | parallel-patterns + /orchestrate parallel-review | P1 |
| 项目初始化、创建规则 | create-project-rules + coding-standards | P1 |

#### 第二层：语言/框架匹配

| 技术栈信号 | 推荐功能 |
|-----------|---------|
| .go 文件、Go 项目 | golang-patterns + go-reviewer + golang-testing |
| .py 文件、Python 项目 | python-patterns + python-reviewer + python-testing |
| Django 项目 | django-patterns + django-security + django-tdd + django-verification |
| Spring Boot 项目 | springboot-patterns + springboot-security + springboot-tdd + springboot-verification |
| .ts/.tsx 文件、React | frontend-patterns + coding-standards + tdd-workflow |
| .java 文件 | java-coding-standards + jpa-patterns |
| SQL、数据库 | postgres-patterns / clickhouse-io + database-reviewer |

#### 第三层：工作流阶段匹配

| 当前阶段 | 推荐下一步 |
|---------|----------|
| 刚开始任务 | /plan → interactive-discussion（如需讨论） |
| 规划完成 | /tdd → 开始编码 |
| 编码完成 | code-reviewer + security-review |
| 审查通过 | /verify → 验证循环 |
| 验证通过 | /learn → 提取模式 |
| 上下文过长 | strategic-compact → 策略性压缩 |

### 特殊场景：新项目创建

当用户表达"创建新项目"、"从零开始"、"学习项目"时：

**首选方式：** 使用 `/workflow` 命令，自动编排五阶段工作流：

```
/workflow                    — 启动新项目工作流
/workflow --level 小         — 指定项目规模（小/中/大）
/workflow --phase 3          — 从指定阶段开始（需求已明确时跳过前两阶段）
```

`/workflow` 会自动完成以下编排：

| 阶段 | 名称 | 自动调用 | 产出物 |
|------|------|---------|--------|
| 1 | 需求分析 | business-analyst skill | Doc/BRIEF-{项目名}.md |
| 2 | 设计 | product-manager + architect | Doc/PRD-{项目名}.md + Doc/ARCH-{项目名}.md |
| 3 | 开发 | planner + tdd-guide | Doc/SPRINT-{项目名}.md + 代码 |
| 4 | 测试 | e2e-runner + tdd-guide | 测试报告 |
| 5 | 部署维护 | verification-loop | 验证报告 |

每个阶段之间有建议性门禁检查，用户可选择继续、深入或跳过。

**推荐输出示例：**

```
【Everything 推荐】新项目创建工作流
根据你的需求（学习项目 + 从零开始），建议使用分阶段工作流：

**推荐方式：** /workflow
- 自动编排 5 个阶段（需求分析→设计→开发→测试→部署）
- 每阶段自动调用对应智能体/技能
- 支持中断恢复（/workflow resume）
- 根据项目规模自适应文档深度

**快速启动：**
- 完整流程 → 输入 /workflow
- 需求已明确，直接规划 → 输入 /workflow --phase 3
- 小项目快速启动 → 输入 /workflow --level 小

你想从哪种方式开始？
```

### 推荐输出格式

**核心原则：展示 → 推荐 → 等待确认**

```
【Everything 推荐】
根据你的需求（{需求摘要}），我检索到以下可用的 ECC 功能：

**推荐工作流：**
1. [P0] {功能名} — {为什么推荐}（{简短介绍}）
2. [P1] {功能名} — {为什么推荐}（{简短介绍}）
3. [P2] {功能名} — {为什么推荐}（{简短介绍}）（可选）

**快速启动：**
- {场景 1} → {命令/操作}
- {场景 2} → {命令/操作}

你想从哪一步开始？
```

示例：
```
【Everything 推荐】
根据你的需求（学习项目 + 从零开始 + 可视化时钟），我检索到以下可用的 ECC 功能：

**推荐工作流：**
1. [P0] /workflow — 分阶段项目工作流（自动编排需求分析→设计→开发→测试→部署）
2. [P1] create-project-rules — 确定架构后生成项目规则（编码标准、测试要求、Git 工作流）
3. [P2] interactive-discussion — 需求不明确时先讨论（通过选择题方式澄清细节）

**快速启动：**
- 完整流程 → 输入 /workflow
- 需求已明确，直接规划 → 输入 /workflow --phase 3
- 先讨论需求细节 → 输入 "开启互动讨论模式"

你想从哪一步开始？
```

---

## 详细功能查询

当用户需要某个功能的详细信息时：

1. 先从本文件的预编译摘要中给出概要
2. 如需更多细节，读取对应的 SKILL.md 或 agent .md 文件
3. 引导用户使用 CATALOG.md 按场景查找

## 新手引导

对于首次使用的用户，推荐：

1. 运行 `/everything tutorial` 启动烟花项目教程
2. 教程覆盖 80%+ 的 Everything 功能
3. 通过实践学习，比阅读文档更高效

详见 `TUTORIAL.md`。
