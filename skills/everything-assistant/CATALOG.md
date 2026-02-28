# Everything Claude Code 功能目录

精简版功能索引。每个功能一行，快速查找。

---

## 按场景索引（我想做什么？）

### 我要开始一个新功能
```
interactive-discussion → /plan → /tdd → code-reviewer → /verify
```

### 我要修复一个 Bug
```
error-diagnostician → /tdd → code-reviewer → /verify
```

### 我要重构代码
```
architect → refactor-cleaner → code-reviewer → /verify
```

### 我要做安全审查
```
security-reviewer → security-review skill → /verify pre-pr
```

### 我要写测试
```
/tdd → tdd-workflow → /test-coverage → /verify
```

### 我要测试关键用户流程
```
e2e-testing skill → /e2e → e2e-runner agent
```

### 我要做架构设计
```
interactive-discussion → architect → /plan
```

### 我要优化数据库
```
database-reviewer → postgres-patterns / clickhouse-io
```

### 我要更新文档
```
doc-updater → /update-docs → /update-codemaps
```

### 我要学习和提取模式
```
/learn → /instinct-status → /evolve → /skill-create
```

### 我要部署前检查
```
/verify pre-pr → security-reviewer → /orchestrate security
```

### 我要编排多智能体协作
```
/orchestrate feature|bugfix|refactor|security
```

### 我的构建失败了
```
build-error-resolver（TS）/ go-build-resolver（Go）
```

### 我的上下文太长了
```
strategic-compact → 策略性压缩
```

### 我想讨论需求/方案
```
interactive-discussion → 选择题式深度讨论
```

### 我要发布新版本
```
changelog-generator → 生成变更日志 → 更新 CHANGELOG.md → 创建 GitHub Release
```

---

## 按类型索引

### Agents（14 个）

| Agent | 用途 | 调用方式 |
|-------|------|---------|
| planner | 实施规划 | /plan |
| architect | 架构设计 | 自动/手动 |
| tdd-guide | TDD 指导 | /tdd |
| code-reviewer | 代码审查 | /code-review |
| security-reviewer | 安全审查 | 自动/手动 |
| build-error-resolver | TS 构建修复 | /build-fix |
| error-diagnostician | 错误诊断 | 自动/手动 |
| e2e-runner | E2E 测试 | /e2e |
| refactor-cleaner | 代码清理 | /refactor-clean |
| doc-updater | 文档更新 | /update-docs |
| database-reviewer | 数据库审查 | 自动/手动 |
| go-build-resolver | Go 构建修复 | /go-build |
| go-reviewer | Go 审查 | /go-review |
| python-reviewer | Python 审查 | /python-review |

### Skills（32 个）

#### 开发模式
coding-standards · frontend-patterns · backend-patterns · golang-patterns · python-patterns · django-patterns · springboot-patterns · jpa-patterns · java-coding-standards · project-guidelines-example

#### 测试
tdd-workflow · e2e-testing · golang-testing · python-testing · django-tdd · springboot-tdd · eval-harness

#### 安全
security-review · django-security · springboot-security

#### 数据库
postgres-patterns · clickhouse-io

#### 验证
verification-loop · django-verification · springboot-verification

#### 学习
continuous-learning-v3

#### 规划与检索
file-memory · iterative-retrieval · strategic-compact

#### 讨论
interactive-discussion

#### 发布
changelog-generator

### Commands（28 个）

| 命令 | 用途 |
|------|------|
| /everything | 智能功能推荐 |
| /fireworks-tutorial | 烟花项目新手教程 |
| /plan | 创建实施计划 |
| /tdd | TDD 工作流 |
| /code-review | 代码审查 |
| /verify | 全面验证 |
| /orchestrate | 多智能体编排 |
| /e2e | E2E 测试 |
| /build-fix | 构建修复 |
| /refactor-clean | 代码清理 |
| /learn | 提取模式 |
| /learn-style | 学习沟通风格 |
| /evolve | 直觉演进 |
| /instinct-status | 查看直觉 |
| /instinct-export | 导出直觉 |
| /instinct-import | 导入直觉 |
| /eval | 评测开发 |
| /file-memory | 文件记忆 |
| /skill-create | 提取技能 |
| /checkpoint | 创建检查点 |
| /setup-pm | 配置项目管理 |
| /update-codemaps | 更新代码图谱 |
| /update-docs | 更新文档 |
| /test-coverage | 覆盖率报告 |
| /go-build | Go 构建修复 |
| /go-review | Go 审查 |
| /go-test | Go TDD |
| /python-review | Python 审查 |

### Rules（8 个）

| Rule | 核心要点 |
|------|---------|
| agents | 智能体编排、并行执行、多维度分析 |
| coding-style | 不可变性、文件组织（<800 行）、错误处理 |
| git-workflow | Conventional Commits、PR 流程、TDD |
| hooks | 钩子系统、文档拦截器、自动格式化 |
| patterns | API 响应格式、仓储模式、骨架项目 |
| performance | 模型选择、上下文管理、Ultrathink |
| security | 安全检查清单、凭据管理、响应协议 |
| testing | 80% 覆盖率、TDD 强制流程、测试排查 |
