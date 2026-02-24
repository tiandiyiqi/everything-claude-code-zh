# 编排（Orchestrate）命令

用于复杂任务的智能体（Agent）工作流，支持顺序、并行和混合模式。

## 用法

`/orchestrate [workflow-type] [task-description]`

## 顺序工作流类型

### feature
完整功能实现工作流：
```
planner -> tdd-guide -> code-reviewer -> security-reviewer
```

### bugfix
Bug 调查与修复工作流：
```
explorer -> tdd-guide -> code-reviewer
```

### refactor
安全重构工作流：
```
architect -> code-reviewer -> tdd-guide
```

### security
侧重安全的评审：
```
security-reviewer -> code-reviewer -> architect
```

## 并行工作流类型

### parallel-review
多维度并行代码审查（完全独立，无依赖）：
```
同时启动：
├→ code-reviewer（代码质量）
├→ security-reviewer（安全性）
└→ architect（架构合理性）
↓ 合成统一审查报告
```

### parallel-plan
复杂功能的多角度并行规划：
```
同时启动：
├→ planner（实施规划）
├→ architect（架构设计）
└→ security-reviewer（安全分析）
↓ 合成综合规划文档
```

### parallel-diagnose
复杂问题的多假设并行诊断：
```
同时启动：
├→ error-diagnostician（根因分析）
├→ build-error-resolver（构建层面排查）
└→ security-reviewer（安全层面排查）
↓ 合成诊断报告
```

## 混合工作流类型

### hybrid-feature
结合顺序和并行的完整功能开发流程：
```
阶段 1（顺序）：planner → 生成实施计划
                    ↓
阶段 2（并行）：tdd-guide + architect
                    ↓
阶段 3（并行）：code-reviewer + security-reviewer
                    ↓
阶段 4（顺序）：合成最终报告
```

### hybrid-refactor
安全重构的混合工作流：
```
阶段 1（顺序）：architect → 设计重构方案
                    ↓
阶段 2（并行）：code-reviewer + security-reviewer（审查方案）
                    ↓
阶段 3（顺序）：tdd-guide → 实施重构
                    ↓
阶段 4（并行）：code-reviewer + security-reviewer（审查结果）
```

## 执行模式

对于工作流中的每个智能体（Agent）：

1. **调用智能体**：携带来自上一个智能体的上下文。
2. **收集输出**：将其作为结构化的交接（Handoff）文档。
3. **传递**：交给链条中的下一个智能体。
4. **汇总结果**：生成最终报告。

## 交接（Handoff）文档格式

在智能体之间创建交接文档：

```markdown
## HANDOFF: [previous-agent] -> [next-agent]

### Context
[工作总结]

### Findings
[关键发现或决策]

### Files Modified
[涉及的文件列表]

### Open Questions
[留给下一个智能体的未解决事项]

### Recommendations
[建议的后续步骤]
```

## 示例：功能开发工作流（Feature Workflow）

```
/orchestrate feature "添加用户认证功能"
```

执行流程：

1. **规划智能体（Planner Agent）**
   - 分析需求
   - 创建实现计划
   - 识别依赖项
   - 输出：`HANDOFF: planner -> tdd-guide`

2. **TDD 指导智能体（TDD Guide Agent）**
   - 读取规划智能体（Planner）的交接文档
   - 测试先行（先编写测试）
   - 编写实现代码以通过测试
   - 输出：`HANDOFF: tdd-guide -> code-reviewer`

3. **代码评审智能体（Code Reviewer Agent）**
   - 评审实现代码
   - 检查潜在问题
   - 提出改进建议
   - 输出：`HANDOFF: code-reviewer -> security-reviewer`

4. **安全评审智能体（Security Reviewer Agent）**
   - 安全审计
   - 漏洞检查
   - 最终批准
   - 输出：最终报告

## 最终报告格式

```
ORCHESTRATION REPORT
====================
Workflow: feature
Task: 添加用户认证功能
Agents: planner -> tdd-guide -> code-reviewer -> security-reviewer

SUMMARY
-------
[一段话总结]

AGENT OUTPUTS
-------------
Planner: [摘要]
TDD Guide: [摘要]
Code Reviewer: [摘要]
Security Reviewer: [摘要]

FILES CHANGED
-------------
[列出所有修改的文件]

TEST RESULTS
------------
[测试通过/失败摘要]

SECURITY STATUS
---------------
[安全发现项]

RECOMMENDATION
--------------
[SHIP / NEEDS WORK / BLOCKED]
```

## 并行执行机制

并行工作流通过 `Task` 工具的 `run_in_background=true` 实现：

1. **写入共享上下文**：将任务描述和相关信息写入 `.claude/plans/parallel-context.md`
2. **启动并行智能体**：每个智能体读取共享上下文，独立执行
3. **收集结果**：通过 `TaskOutput` 工具收集各智能体输出
4. **合成报告**：主上下文将所有输出合并为统一报告

### 分阶段依赖管理

混合工作流中，使用分阶段执行处理依赖：

```
阶段 1（并行）：无依赖的任务同时执行
                    ↓ 等待所有完成
阶段 2（并行）：依赖阶段 1 结果的任务同时执行
                    ↓ 等待所有完成
阶段 3（顺序）：最终合成
```

### 并行 vs 顺序决策

| 场景 | 推荐 | 原因 |
|------|------|------|
| 审查 + 安全检查 | 并行 | 完全独立 |
| 规划 → 编码 | 顺序 | 编码依赖规划 |
| 多维度分析 | 并行 | 各维度独立 |
| 编码 → 测试 | 顺序 | 测试依赖代码 |

详细并行模式参见 `skills/parallel-patterns/SKILL.md`。

## 参数

$ARGUMENTS:
- `feature <description>` - 完整功能实现工作流（顺序）
- `bugfix <description>` - Bug 修复工作流（顺序）
- `refactor <description>` - 重构工作流（顺序）
- `security <description>` - 安全评审工作流（顺序）
- `parallel-review <description>` - 多维度并行审查
- `parallel-plan <description>` - 多角度并行规划
- `parallel-diagnose <description>` - 多假设并行诊断
- `hybrid-feature <description>` - 混合功能开发（顺序+并行）
- `hybrid-refactor <description>` - 混合重构（顺序+并行）
- `custom <agents> <description>` - 自定义智能体序列

## 自定义工作流示例

```
/orchestrate custom "architect,tdd-guide,code-reviewer" "重构缓存层"
```

## 技巧

1. **从规划开始**：对于复杂功能，优先使用规划智能体（Planner）。
2. **始终包含代码评审**：在合并前，务必包含代码评审智能体（Code Reviewer）。
3. **涉及敏感操作使用安全评审**：在处理鉴权、支付或敏感信息（PII）时，请使用安全评审智能体（Security Reviewer）。
4. **保持交接文档简洁**：专注于下一个智能体所需的信息。
5. **在环节间运行验证**：如有必要，在智能体交接间运行验证（Verification）。
