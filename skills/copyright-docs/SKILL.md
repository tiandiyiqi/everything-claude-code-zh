---
name: copyright-docs
description: Generate software copyright design specification documents compliant with China Copyright Protection Center (CPCC) standards. Creates complete design documents with Mermaid diagrams based on source code analysis. Use for software copyright registration, generating design specification, creating CPCC-compliant documents, or documenting software for intellectual property protection. Triggers on "软件著作权", "设计说明书", "版权登记", "CPCC", "软著申请".
allowed-tools: Task, AskUserQuestion, Read, Bash, Glob, Grep, Write
---

# Software Copyright Documentation Skill

Generate CPCC-compliant software copyright registration materials through multi-phase code analysis.

> **依据**：中国版权保护中心《计算机软件著作权登记办法》及官方审查标准

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│  CPCC软著材料生成流程                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: 元数据收集      → project-metadata.json               │
│           ↓                                                      │
│  Phase 2: 深度代码分析    → sections/section-N.md               │
│           (6个并行Agent)                                         │
│           ↓                                                      │
│  Phase 2.5: 整合分析      → cross-module-summary.md             │
│           ↓                                                      │
│  Phase 4: 文档组装        → 设计说明书.md                        │
│           ↓                                                      │
│  Phase 5: 合规审查        → 验证 + 迭代修复                      │
│           ↓                                                      │
│  Phase 6: 源程序生成      → 源程序.md                            │
│           ↓                                                      │
│  Phase 7: PDF输出         → 最终PDF文件                          │
│           ↓                                                      │
│  Phase 8: CPCC官网填写    → 自动提交申请                          │
│                                                                  │
│  可选：用户手册生成                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Features

### ✅ 符合CPCC官方规范

| 功能 | 状态 | 说明 |
|------|------|------|
| 页眉格式 | ✅ | `软件名称 V1.0        第X页/共Y页` |
| 封面设计 | ✅ | 包含软件名称、版本号、文档类型 |
| 版本号验证 | ✅ | 自动验证V1.0格式，禁止beta/test等 |
| 行数验证 | ✅ | 文档≥30行/页，源代码≥50行/页 |
| 敏感信息检查 | ✅ | 检测密码、密钥、手机号、身份证等 |
| 源程序生成 | ✅ | 前30页+后30页，自动脱敏 |
| PDF输出 | ✅ | A4纵向，无加密，字体嵌入 |
| 用户手册 | ✅ | 含截图收集和验证 |
| CPCC官网填写 | ✅ | 使用agent-browser自动提交申请 |

## Document Sections (7 Required)

| Section | Title | Diagram | Agent |
|---------|-------|---------|-------|
| 1 | 软件概述 | - | Phase 4 生成 |
| 2 | 系统架构图 | graph TD | architecture |
| 3 | 功能模块设计 | flowchart TD | functions |
| 4 | 核心算法与流程 | flowchart TD | algorithms |
| 5 | 数据结构设计 | classDiagram | data_structures |
| 6 | 接口设计 | sequenceDiagram | interfaces |
| 7 | 异常处理设计 | flowchart TD | exceptions |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  Phase 1: Metadata Collection                                    │
│  → 收集软件名称、版本号、类型、范围                                │
│  → 验证版本号格式                                                 │
│  → 选择文档类型（设计说明书/用户手册）                             │
│  → Output: project-metadata.json                                 │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2: Deep Code Analysis (6 Parallel Agents)                 │
│  → 分析代码架构、功能、算法、数据结构、接口、异常                   │
│  → 直接写入 sections/section-N.md                                │
│  → Output: 6个章节文件                                            │
├─────────────────────────────────────────────────────────────────┤
│  Phase 2.5: Consolidation                                        │
│  → 跨章节一致性检查                                               │
│  → Output: cross-module-summary.md                               │
├─────────────────────────────────────────────────────────────────┤
│  Phase 4: Document Assembly                                      │
│  → 生成封面、目录、页眉页码                                        │
│  → 合并章节内容                                                   │
│  → Output: {软件名称}-软件设计说明书.md                            │
├─────────────────────────────────────────────────────────────────┤
│  Phase 5: Compliance Review & Refinement                         │
│  → 结构验证、格式验证、内容验证、安全验证                          │
│  → 发现问题则迭代修复                                             │
│  → Output: 验证报告                                               │
├─────────────────────────────────────────────────────────────────┤
│  Phase 6: Source Code Generation                                 │
│  → 扫描源代码文件                                                 │
│  → 提取前30页+后30页                                              │
│  → 敏感信息脱敏                                                   │
│  → Output: {软件名称}-源程序.md                                    │
├─────────────────────────────────────────────────────────────────┤
│  Phase 7: PDF Output                                             │
│  → Markdown转PDF                                                 │
│  → 添加页眉页脚                                                   │
│  → 验证PDF格式                                                    │
│  → Output: 最终PDF文件                                            │
└─────────────────────────────────────────────────────────────────┘
```

## Output Structure

```
.workflow/.scratchpad/copyright-{timestamp}/
├── project-metadata.json          # 元数据
├── sections/                      # 各章节MD文件
│   ├── section-2-architecture.md
│   ├── section-3-functions.md
│   ├── section-4-algorithms.md
│   ├── section-5-data-structures.md
│   ├── section-6-interfaces.md
│   └── section-7-exceptions.md
├── cross-module-summary.md        # 跨模块总结
├── {软件名称}-软件设计说明书.md     # 设计说明书
├── {软件名称}-用户手册.md          # 用户手册（可选）
├── {软件名称}-源程序.md            # 源程序材料
└── {软件名称}-*.pdf               # 最终PDF文件
```

## Directory Setup

```javascript
// 生成时间戳目录名
const timestamp = new Date().toISOString().slice(0,19).replace(/[-:T]/g, '');
const dir = `.workflow/.scratchpad/copyright-${timestamp}`;

// 创建目录结构
Bash(`mkdir -p "${dir}/sections" "${dir}/iterations"`);
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| [phases/01-metadata-collection.md](phases/01-metadata-collection.md) | 元数据收集与验证 |
| [phases/02-deep-analysis.md](phases/02-deep-analysis.md) | 6-agent并行分析 |
| [phases/02.5-consolidation.md](phases/02.5-consolidation.md) | 跨模块整合 |
| [phases/04-document-assembly.md](phases/04-document-assembly.md) | 文档组装 |
| [phases/05-compliance-refinement.md](phases/05-compliance-refinement.md) | 合规审查 |
| [phases/06-source-code-generation.md](phases/06-source-code-generation.md) | 源程序生成 |
| [phases/07-pdf-output.md](phases/07-pdf-output.md) | PDF输出 |
| [phases/08-cpcc-form-filling.md](phases/08-cpcc-form-filling.md) | CPCC官网填写 |
| [specs/cpcc-requirements.md](specs/cpcc-requirements.md) | CPCC规范要求 |
| [templates/agent-base.md](templates/agent-base.md) | Agent模板 |
| [templates/user-manual.md](templates/user-manual.md) | 用户手册模板 |

## CPCC Compliance Checklist

### 文档鉴别材料

- [ ] 封面包含软件名称、版本号
- [ ] 页眉格式正确：`软件名称 V1.0        第X页/共Y页`
- [ ] 页码连续，包含总页数
- [ ] 每页文字行数 ≥ 30行
- [ ] 无敏感信息（密码、密钥、手机号等）
- [ ] 无他人版权声明
- [ ] 图表编号正确

### 程序鉴别材料

- [ ] 前30页 + 后30页源代码
- [ ] 每页有效代码行数 ≥ 50行
- [ ] 代码连续，无跳跃
- [ ] 无敏感信息
- [ ] 无他人版权声明

### PDF格式

- [ ] 文件大小 ≤ 50MB
- [ ] 无加密、无密码保护
- [ ] 无水印
- [ ] 字体嵌入PDF
- [ ] A4纵向排版

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v2.1 | 2025-01-28 | 添加CPCC官网自动填写功能（agent-browser） |
| v2.0 | 2025-01-28 | 添加源程序生成、PDF输出、用户手册功能 |
| v1.0 | 2025-01-27 | 初始版本，支持设计说明书生成 |
