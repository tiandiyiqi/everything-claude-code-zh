# Phase 4: Document Assembly

生成符合CPCC规范的完整文档，包含封面、页眉页码、正文内容。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## 设计原则

1. **CPCC 合规**：严格遵循软著申请规范要求
2. **封面设计**：包含软件名称、版本号、文档类型
3. **页眉页码**：符合官方格式要求
4. **独立可读**：各章节文件可单独阅读

## 输入

```typescript
interface AssemblyInput {
  output_dir: string;
  metadata: ProjectMetadata;
  consolidation: {
    synthesis: string;           // 跨章节综合分析
    section_summaries: Array<{
      file: string;
      title: string;
      summary: string;
    }>;
    issues: { errors: Issue[], warnings: Issue[], info: Issue[] };
    stats: { total_sections: number, total_diagrams: number };
  };
  document_type: 'design' | 'user_manual';  // 文档类型
}
```

## 执行流程

```javascript
// 1. 检查是否有阻塞性问题
if (consolidation.issues.errors.length > 0) {
  const response = await AskUserQuestion({
    questions: [{
      question: `发现 ${consolidation.issues.errors.length} 个严重问题，如何处理？`,
      header: "阻塞问题",
      multiSelect: false,
      options: [
        {label: "查看并修复", description: "显示问题列表，手动修复后重试"},
        {label: "忽略继续", description: "跳过问题检查，继续装配"},
        {label: "终止", description: "停止文档生成"}
      ]
    }]
  });

  if (response === "查看并修复") {
    return { action: "fix_required", errors: consolidation.issues.errors };
  }
  if (response === "终止") {
    return { action: "abort" };
  }
}

// 2. 生成完整文档（包含封面、页眉页码）
const doc = generateCompleteDocument(metadata, consolidation);

// 3. 写入最终文件
Write(`${outputDir}/${metadata.software_name}-软件设计说明书.md`, doc);
```

## 文档模板

```markdown
<!--
===========================================
封面页（无页眉页码）
===========================================
-->

# {软件名称}

## 软件设计说明书

**版本号**：{version}

**文档类型**：设计文档

---

<!--
===========================================
目录页（可选，罗马数字页码）
===========================================
-->

## 目录

1. 软件概述
2. 系统架构图
3. 功能模块设计
4. 核心算法与流程
5. 数据结构设计
6. 接口设计
7. 异常处理设计

---

<!--
===========================================
正文开始（从第1页连续编号）
===========================================
-->

<!-- 页眉：{软件名称} {version}        第1页/共{total_pages}页 -->

## 1. 软件概述

### 1.1 软件背景与用途

[从 metadata 生成的软件背景描述]

### 1.2 开发目标与特点

[从 metadata 生成的目标和特点]

### 1.3 运行环境与技术架构

[从 metadata.tech_stack 生成]

---

<!-- 页眉：{软件名称} {version}        第2页/共{total_pages}页 -->

## 2. 系统架构图

[引用 sections/section-2-architecture.md 内容]

---

<!-- 页眉：{软件名称} {version}        第N页/共{total_pages}页 -->

## 附录

- [跨模块分析报告](./cross-module-summary.md)
- [章节文件目录](./sections/)

---

<!-- 文档结束 -->
```

## 生成函数

```javascript
function generateCompleteDocument(metadata, consolidation) {
  const date = new Date().toLocaleDateString('zh-CN');
  
  // 计算总页数（估算）
  const estimatedPages = estimateTotalPages(consolidation);
  
  // 生成封面
  const coverPage = generateCoverPage(metadata, date);
  
  // 生成目录
  const tocPage = generateTOC(consolidation.section_summaries);
  
  // 生成正文（带页眉页码）
  const bodyPages = generateBodyPages(metadata, consolidation, estimatedPages);
  
  return `${coverPage}

${tocPage}

${bodyPages}
`;
}

function generateCoverPage(metadata, date) {
  const docType = metadata.document_type === 'user_manual' ? '用户手册' : '软件设计说明书';
  
  return `
<div style="text-align: center; page-break-after: always;">

# ${metadata.software_name}

---

## ${docType}

---

**版本号**：${metadata.version}

**生成日期**：${date}

</div>
`;
}

function generateTOC(sectionSummaries) {
  return `
## 目录

${sectionSummaries.map((s, i) => `${i + 2}. ${s.title}`).join('\n')}

---
`;
}

function generateBodyPages(metadata, consolidation, totalPages) {
  let currentPage = 1;
  let content = '';
  
  // 第1章：软件概述
  content += generatePageHeader(metadata, currentPage, totalPages);
  content += generateSection1(metadata);
  currentPage++;
  
  // 第2-7章：引用章节文件
  for (const section of consolidation.section_summaries) {
    content += '\n---\n\n';
    content += generatePageHeader(metadata, currentPage, totalPages);
    content += `## ${section.title}\n\n`;
    content += `详见：[${section.title}](./sections/${section.file})\n\n`;
    content += section.summary;
    currentPage++;
  }
  
  // 附录
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage, totalPages);
  content += `## 附录\n\n`;
  content += `- [跨模块分析报告](./cross-module-summary.md)\n`;
  content += `- [章节文件目录](./sections/)\n`;
  
  return content;
}

function generatePageHeader(metadata, pageNum, totalPages) {
  // 官方规范格式：软件全称 版本号        第X页/共Y页
  return `<!-- 页眉：${metadata.software_name} ${metadata.version}        第${pageNum}页/共${totalPages}页 -->\n\n`;
}

function estimateTotalPages(consolidation) {
  // 估算：封面1页 + 目录1页 + 软件概述2页 + 6个章节各3页 + 附录1页
  return 1 + 1 + 2 + (consolidation.section_summaries.length * 3) + 1;
}

function generateSection1(metadata) {
  const categoryDescriptions = {
    "命令行工具 (CLI)": "提供命令行界面，用户通过终端命令与系统交互",
    "后端服务/API": "提供 RESTful/GraphQL API 接口，支持前端或其他服务调用",
    "SDK/库": "提供可复用的代码库，供其他项目集成使用",
    "数据处理系统": "处理数据导入、转换、分析和导出",
    "自动化脚本": "自动执行重复性任务，提高工作效率"
  };

  return `## 1. 软件概述

### 1.1 软件背景与用途

${metadata.software_name}是一款${metadata.category}软件。${categoryDescriptions[metadata.category] || ''}

本软件基于${metadata.tech_stack.language}语言开发，运行于${metadata.tech_stack.runtime}环境，采用${metadata.tech_stack.framework || '原生'}框架实现核心功能。

### 1.2 开发目标与特点

本软件旨在${metadata.purpose || '解决特定领域的技术问题'}。

主要技术特点包括${metadata.tech_stack.framework ? `采用 ${metadata.tech_stack.framework} 框架` : '模块化设计'}，具备良好的可扩展性和可维护性。

### 1.3 运行环境与技术架构

**运行环境**

- 操作系统：${metadata.os || 'Windows/Linux/macOS'}
- 运行时：${metadata.tech_stack.runtime}
- 依赖环境：${metadata.tech_stack.dependencies?.join(', ') || '无特殊依赖'}

**技术架构**

- 架构模式：${metadata.architecture_pattern || '分层架构'}
- 核心框架：${metadata.tech_stack.framework || '原生实现'}
- 主要模块：详见第2章系统架构设计
`;
}
```

## 页眉格式规范

根据CPCC官方要求，页眉格式必须为：

```
软件全称 版本号        第X页/共Y页
```

**示例**：
```
物托邦图书管理系统 V1.0        第1页/共60页
```

**注意事项**：
1. 软件名称和版本号之间用**空格**分隔
2. 版本号和页码之间用**8个空格**或**制表符**分隔
3. 页码必须包含**总页数**
4. 封面页**不设页眉页码**

## 输出结构

```
.workflow/.scratchpad/copyright-{timestamp}/
├── sections/                           # 独立章节（Phase 2 产出）
│   ├── section-2-architecture.md
│   ├── section-3-functions.md
│   └── ...
├── cross-module-summary.md             # 跨模块报告（Phase 2.5 产出）
└── {软件名称}-软件设计说明书.md         # 完整文档（本阶段产出）
```

## 与 Phase 2.5 的协作

Phase 2.5 consolidation agent 需要提供：

```typescript
interface ConsolidationOutput {
  synthesis: string;           // 设计思路综述（2-3 段落）
  section_summaries: Array<{
    file: string;              // 文件名
    title: string;             // 章节标题（如"2. 系统架构设计"）
    summary: string;           // 一句话说明
  }>;
  issues: {...};
  stats: {...};
}
```

## 关键变更

| 原设计 | 新设计 |
|--------|--------|
| 无封面 | 添加封面页（软件名称、版本号、文档类型） |
| 页眉格式错误 | 符合官方规范：`软件名称 V1.0        第X页/共Y页` |
| 无总页数 | 添加总页数估算和显示 |
| 引用章节 | 合并章节内容到主文档 |
