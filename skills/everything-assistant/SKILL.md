---
name: everything-assistant
description: Everything Claude Code 智能助手。自动分析用户意图，推荐最匹配的 skill/agent/command。当用户表达困惑、开始新任务、或手动调用 /everything 时激活。
version: "1.0.0"
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

### Skills（31 个）

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

#### 学习 (Learning)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| continuous-learning | 会话模式自动提取为技能 | 模式检测、技能提取、学习 |
| continuous-learning-v2 | 直觉系统、置信度评分、演进 | 直觉、观测、演进、置信度 |
| continuous-learning-v3 | 统一学习管道、沟通风格学习 | 沟通模式、表达库、学习管道 |

#### 规划与检索 (Planning & Retrieval)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| file-memory | 文件持久化记忆（三文件模式） | 任务计划、发现记录、进度日志 |
| iterative-retrieval | 迭代检索、上下文优化 | 分发、评估、优化、循环 |
| strategic-compact | 策略性上下文压缩 | 压缩建议、阈值检测、逻辑边界 |

#### 讨论 (Discussion)

| Skill | 核心用途 | 触发关键词 |
|-------|---------|----------|
| interactive-discussion | 互动讨论模式、选择题方式 | 需求讨论、方案细化、多维分析 |

### Commands（26 个）

| Command | 用途 |
|---------|------|
| /plan | 创建实施计划（调用 planner agent） |
| /tdd | 测试驱动开发工作流 |
| /code-review | 代码审查 |
| /verify | 全面验证（构建+测试+安全） |
| /orchestrate | 多智能体顺序编排 |
| /e2e | 端到端测试 |
| /build-fix | 修复构建错误 |
| /refactor-clean | 冗余代码清理 |
| /learn | 提取可复用模式 |
| /learn-style | 学习沟通风格 |
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
| /go-build | Go 构建错误修复 |
| /go-review | Go 代码审查 |
| /go-test | Go TDD |
| /python-review | Python 代码审查 |

### Rules（8 个）

| Rule | 核心要点 |
|------|---------|
| agents | 智能体编排规则、并行执行、多维度分析 |
| coding-style | 不可变性、文件组织、错误处理、输入校验 |
| git-workflow | Conventional Commits、PR 工作流、功能实现流程 |
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
| 新功能、实现、开发 | planner agent + /plan + tdd-workflow | P0 |
| Bug、修复、报错 | error-diagnostician + tdd-guide + /verify | P0 |
| 重构、清理、优化 | refactor-cleaner + code-reviewer | P1 |
| 安全、认证、授权 | security-reviewer + security-review skill | P0 |
| 测试、覆盖率 | tdd-workflow + /test-coverage | P1 |
| 架构、设计、选型 | architect agent + interactive-discussion | P1 |
| 文档、README | doc-updater agent + /update-docs | P2 |
| 学习、模式提取 | continuous-learning-v2 + /learn | P2 |
| 讨论、需求、方案 | interactive-discussion | P1 |
| 部署、CI/CD | verification-loop + /verify | P1 |

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

### 推荐输出格式

```
【Everything 推荐】
根据你的需求，建议使用：
1. [P0] {功能名} — {一句话理由}
2. [P1] {功能名} — {一句话理由}
3. [P2] {功能名} — {一句话理由}（可选）
快速启动：{最相关的命令}
```

示例：
```
【Everything 推荐】
根据你的需求，建议使用：
1. [P0] planner agent — 任务较复杂，建议先规划
2. [P1] tdd-workflow skill — 新功能应先写测试
3. [P2] interactive-discussion — 需求不明确时可先讨论
快速启动：/plan
```

---

## Continuous-Learning 集成

### 直觉增强推荐

当 continuous-learning-v2 系统已积累直觉时，推荐引擎会：

1. 读取 `~/.claude/homunculus/instincts/personal/` 中的直觉文件
2. 筛选 confidence >= 0.5 的直觉
3. 将直觉的 domain/trigger 与推荐映射交叉匹配
4. 高置信度直觉可提升对应功能的推荐优先级（+0.2 权重）

### 示例

如果存在直觉：
```json
{
  "domain": "testing",
  "trigger": "新功能实现",
  "confidence": 0.8,
  "content": "用户偏好先写集成测试再写单元测试"
}
```

则推荐输出会调整为：
```
【Everything 推荐】（已融合学习直觉）
根据你的需求和历史偏好，建议使用：
1. [P0] tdd-workflow — 你偏好先写集成测试，此 skill 支持自定义测试顺序
...
```

### 无直觉时的行为

如果 `~/.claude/homunculus/instincts/personal/` 不存在或为空，推荐引擎正常工作，不显示直觉增强标记。

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
