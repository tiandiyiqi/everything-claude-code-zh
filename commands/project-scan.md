# 项目状态扫描（Project Scan）命令

扫描当前项目的实际状态，生成项目状态快照。供 `/workflow`、`interactive-discussion` 等技能感知项目当前所处阶段。

## 用法

```
/project-scan              — 扫描并输出项目状态快照
/project-scan --save       — 扫描并写入 file-memory（task_plan.md 的"项目状态快照"区域）
/project-scan --phase      — 扫描并推荐 workflow 起始阶段
```

## 指令（Instructions）

### 扫描流程

按以下顺序执行扫描，每一步都是实际的文件系统/命令探测，不是猜测：

#### 1. 技术栈检测

检测项目根目录下的配置文件，确定技术栈：

| 检测文件 | 推断结果 |
|----------|----------|
| `package.json` | Node.js / JavaScript / TypeScript |
| `tsconfig.json` | TypeScript |
| `go.mod` | Go |
| `requirements.txt` / `pyproject.toml` / `setup.py` | Python |
| `Cargo.toml` | Rust |
| `pom.xml` / `build.gradle` | Java / Spring Boot |
| `next.config.*` | Next.js |
| `nuxt.config.*` | Nuxt.js |
| `vite.config.*` | Vite |

从 `package.json` 或对应配置文件中提取框架和关键依赖。

#### 2. 项目结构扫描

检测以下目录和文件是否存在：

```
源代码:     src/ | app/ | lib/ | cmd/ | pkg/
测试:       tests/ | __tests__/ | test/ | *_test.go | *.test.ts
文档:       Doc/ | docs/ | README.md
需求文档:   Doc/BRIEF-* | Doc/PRD-* | specs/
架构文档:   Doc/ARCH-* | docs/CODEMAPS/
计划文件:   Doc/SPRINT-* | .claude/plans/
CI/CD:      .github/workflows/ | .gitlab-ci.yml | Dockerfile
配置:       .env.example | .env.local
```

统计源代码文件数量和大致行数（使用 `wc -l` 或 `find | wc`）。

#### 3. 已有产物检测

检测 workflow 五阶段对应的产物是否已存在：

| 阶段 | 检测目标 | 检测方法 |
|------|----------|----------|
| 阶段 1（需求） | `Doc/BRIEF-*.md` | Glob 匹配 |
| 阶段 2（设计） | `Doc/PRD-*.md` + `Doc/ARCH-*.md` | Glob 匹配 |
| 阶段 3（开发） | `src/` 下有实际代码文件 | 文件计数 > 0 |
| 阶段 4（测试） | 测试文件存在 + 覆盖率报告 | Glob + `coverage/` 目录 |
| 阶段 5（部署） | CI/CD 配置 + Dockerfile | Glob 匹配 |

#### 4. 代码健康度快速检查（可选，`--full` 时执行）

- 运行 `git status` 查看工作区状态
- 运行 `git log --oneline -5` 查看最近提交
- 如果有 `package.json`，检查是否有 `test`、`build`、`lint` 脚本
- 如果有测试脚本，尝试运行 `npm test -- --coverage --passWithNoTests 2>&1 | tail -5` 获取覆盖率

#### 5. 阶段推荐（`--phase` 时执行）

根据已有产物推荐 workflow 起始阶段：

```
决策树：
  无任何产物 → 阶段 1（需求分析）
  有 BRIEF 但无 PRD → 阶段 2（设计）
  有 PRD + ARCH 但无代码 → 阶段 3（开发）
  有代码但无测试/覆盖率不足 → 阶段 4（测试）
  有代码 + 测试通过 → 阶段 5（部署验证）
  全部就绪 → 提示"项目已完成所有阶段"
```

## 输出格式

### 项目状态快照

```markdown
## 项目状态快照
<!-- 由 /project-scan 于 YYYY-MM-DD HH:MM 生成 -->

### 技术栈
- 语言: TypeScript
- 框架: Next.js 15
- 包管理: pnpm
- 关键依赖: React 19, Tailwind CSS, Supabase

### 项目规模
- 源文件数: 42
- 代码行数: ~3,200
- 测试文件数: 8
- 分级: 中

### 五阶段产物检测
| 阶段 | 产物 | 状态 |
|------|------|------|
| 1 需求分析 | Doc/BRIEF-myapp.md | ✅ 已存在 |
| 2 设计 | Doc/PRD-myapp.md | ✅ 已存在 |
| 2 设计 | Doc/ARCH-myapp.md | ❌ 缺失 |
| 3 开发 | src/ (42 文件) | ✅ 已存在 |
| 4 测试 | tests/ (8 文件) | ⚠️ 存在但覆盖率未知 |
| 5 部署 | .github/workflows/ | ❌ 缺失 |

### 推荐起始阶段
基于以上状态，建议从 **阶段 2（设计）** 继续——补充架构文档。

### Git 状态
- 分支: feature/auth
- 未提交变更: 3 文件
- 最近提交: feat: 添加用户登录页面
```

## `--save` 行为

当使用 `--save` 参数时：
1. 检查 `.claude/plans/` 下是否有活跃的 task_plan.md
2. 如果有：将快照追加/更新到 task_plan.md 的"项目状态快照"区域
3. 如果没有：提示用户先运行 `/file-memory init`，或自动初始化

## 与其他技能的集成

```
/workflow 启动时：
  → 自动调用 /project-scan --phase --save
  → 根据推荐阶段跳过已完成的阶段
  → 将快照写入 workflow 的 file-memory

interactive-discussion 启动时：
  → 自动调用 /project-scan
  → 根据项目状态调整讨论维度和问题
  → 避免讨论已经完成的阶段

/plan 启动时：
  → 可选调用 /project-scan
  → 帮助 planner 了解项目现状

手动使用：
  → /project-scan 随时查看项目状态
```

## 注意事项

- 扫描是只读操作，不修改任何项目文件
- 扫描结果基于文件系统的实际状态，不依赖对话历史
- 覆盖率检查可能需要运行测试命令，耗时较长，默认跳过（`--full` 时执行）
- 产物检测使用 Glob 模式匹配，支持自定义项目的文档命名约定
