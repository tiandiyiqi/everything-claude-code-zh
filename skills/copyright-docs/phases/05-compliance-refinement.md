# Phase 5: Compliance Review & Iterative Refinement

合规审查与迭代完善，确保文档完全符合CPCC规范要求。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## 执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│  合规审查流程                                                    │
├─────────────────────────────────────────────────────────────────┤
│  1. 结构验证 → 检查章节完整性                                     │
│  2. 格式验证 → 检查页眉页码                                       │
│  3. 内容验证 → 检查行数、图表                                     │
│  4. 安全验证 → 检查敏感信息                                       │
│  5. 用户确认 → 发现问题则迭代修复                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 验证函数

### 1. 完整合规验证

```javascript
function validateCPCCCompliance(document, metadata, analyses) {
  const results = {
    passed: 0,
    total: 0,
    errors: [],
    warnings: [],
    info: []
  };
  
  // 1. 结构验证
  const structureChecks = validateStructure(document);
  results.errors.push(...structureChecks.errors);
  results.warnings.push(...structureChecks.warnings);
  
  // 2. 格式验证
  const formatChecks = validateFormat(document, metadata);
  results.errors.push(...formatChecks.errors);
  results.warnings.push(...formatChecks.warnings);
  
  // 3. 内容验证
  const contentChecks = validateContent(document);
  results.errors.push(...contentChecks.errors);
  results.warnings.push(...contentChecks.warnings);
  
  // 4. 安全验证
  const securityChecks = validateSecurity(document, metadata);
  results.errors.push(...securityChecks.errors);
  results.warnings.push(...securityChecks.warnings);
  
  // 统计
  results.total = results.errors.length + results.warnings.length + results.info.length;
  results.passed = results.total - results.errors.length;
  
  return results;
}
```

### 2. 结构验证

```javascript
function validateStructure(document) {
  const errors = [];
  const warnings = [];
  
  // 必需章节检查
  const requiredSections = [
    { pattern: /## 1\. 软件概述/, name: "软件概述" },
    { pattern: /## 2\. 系统架构图/, name: "系统架构图" },
    { pattern: /## 3\. 功能模块设计/, name: "功能模块设计" },
    { pattern: /## 4\. 核心算法与流程/, name: "核心算法与流程" },
    { pattern: /## 5\. 数据结构设计/, name: "数据结构设计" },
    { pattern: /## 6\. 接口设计/, name: "接口设计" },
    { pattern: /## 7\. 异常处理设计/, name: "异常处理设计" }
  ];
  
  for (const section of requiredSections) {
    if (!section.pattern.test(document)) {
      errors.push({
        type: "missing_section",
        message: `缺少必需章节: ${section.name}`,
        severity: "error"
      });
    }
  }
  
  // 封面检查
  if (!document.includes("# ") || !document.includes("版本号")) {
    warnings.push({
      type: "missing_cover",
      message: "文档可能缺少封面页",
      severity: "warning"
    });
  }
  
  return { errors, warnings };
}
```

### 3. 格式验证

```javascript
function validateFormat(document, metadata) {
  const errors = [];
  const warnings = [];
  
  // 页眉格式检查
  const headerPattern = /<!-- 页眉：(.+?) 第(\d+)页\/共(\d+)页 -->/g;
  const headers = document.match(headerPattern) || [];
  
  if (headers.length === 0) {
    errors.push({
      type: "missing_header",
      message: "文档缺少页眉",
      severity: "error"
    });
  } else {
    // 检查页眉格式是否正确
    for (const header of headers) {
      const match = header.match(/<!-- 页眉：(.+?) 第(\d+)页\/共(\d+)页 -->/);
      if (match) {
        const headerText = match[1].trim();
        const expectedHeader = `${metadata.software_name} ${metadata.version}`;
        
        if (!headerText.includes(metadata.software_name)) {
          errors.push({
            type: "header_name_mismatch",
            message: `页眉软件名称不匹配: 期望包含 "${metadata.software_name}"`,
            severity: "error"
          });
        }
        
        if (!headerText.includes(metadata.version)) {
          errors.push({
            type: "header_version_mismatch",
            message: `页眉版本号不匹配: 期望包含 "${metadata.version}"`,
            severity: "error"
          });
        }
      }
    }
    
    // 检查页码连续性
    const pageNums = headers.map(h => {
      const match = h.match(/第(\d+)页/);
      return match ? parseInt(match[1]) : 0;
    });
    
    const sorted = [...pageNums].sort((a, b) => a - b);
    for (let i = 1; i < sorted.length; i++) {
      if (sorted[i] - sorted[i-1] > 1) {
        warnings.push({
          type: "page_number_gap",
          message: `页码不连续: 从第${sorted[i-1]}页跳到第${sorted[i]}页`,
          severity: "warning"
        });
      }
    }
  }
  
  // 图表编号检查
  const figurePattern = /\*\*图(\d+)-(\d+)/g;
  const figures = document.match(figurePattern) || [];
  
  const expectedFigures = {
    2: ["图2-1"],
    3: ["图3-1"],
    4: ["图4-1"],
    5: ["图5-1"],
    6: ["图6-1"],
    7: ["图7-1"]
  };
  
  for (const [chapter, expected] of Object.entries(expectedFigures)) {
    const hasFigure = figures.some(f => f.includes(`图${chapter}-`));
    if (!hasFigure) {
      warnings.push({
        type: "missing_figure",
        message: `第${chapter}章缺少图表`,
        severity: "warning"
      });
    }
  }
  
  return { errors, warnings };
}
```

### 4. 内容验证（行数验证）

```javascript
function validateContent(document) {
  const errors = [];
  const warnings = [];
  
  // 按页分割（假设 --- 为分页符）
  const pages = document.split(/\n---\n/);
  
  for (let i = 0; i < pages.length; i++) {
    const page = pages[i];
    
    // 排除封面页和目录页
    if (page.includes("封面") || page.includes("目录") || page.includes("# ")) {
      continue;
    }
    
    // 计算有效文字行数
    const lines = page.split('\n');
    const textLines = lines.filter(line => {
      const trimmed = line.trim();
      // 排除空行、纯图表行、纯代码块、页眉注释
      return trimmed.length > 0 && 
             !trimmed.startsWith('```') &&
             !trimmed.startsWith('<!--') &&
             !trimmed.match(/^!\[.*\]\(.*\)$/) &&
             !trimmed.match(/^#{1,2}\s/); // 标题行也算
    });
    
    // 检查每页行数
    if (textLines.length > 0 && textLines.length < 30) {
      warnings.push({
        type: "low_line_count",
        message: `第${i + 1}页文字行数不足: ${textLines.length}行（要求≥30行）`,
        severity: "warning",
        page: i + 1,
        lineCount: textLines.length
      });
    }
  }
  
  // Mermaid 图表语法检查
  const mermaidPattern = /```mermaid\n([\s\S]*?)```/g;
  const mermaidBlocks = document.match(mermaidPattern) || [];
  
  for (const block of mermaidBlocks) {
    // 基本语法检查
    if (!block.includes('graph') && !block.includes('flowchart') && 
        !block.includes('sequenceDiagram') && !block.includes('classDiagram')) {
      errors.push({
        type: "invalid_mermaid",
        message: "Mermaid 图表语法可能不正确",
        severity: "error",
        snippet: block.substring(0, 100)
      });
    }
  }
  
  return { errors, warnings };
}
```

### 5. 安全验证（敏感信息检查）

```javascript
function validateSecurity(document, metadata) {
  const errors = [];
  const warnings = [];
  
  const selfCompany = metadata.rights_holder?.name || "";
  
  // 敏感信息检测模式
  const sensitivePatterns = [
    { 
      name: "密码", 
      pattern: /password\s*[:=]\s*['"][^'"]+['"]/gi, 
      severity: "error",
      message: "检测到硬编码密码"
    },
    { 
      name: "API密钥", 
      pattern: /(api[_-]?key|secret[_-]?key|apikey)\s*[:=]\s*['"][^'"]+['"]/gi, 
      severity: "error",
      message: "检测到API密钥"
    },
    { 
      name: "Token", 
      pattern: /(token|auth[_-]?token)\s*[:=]\s*['"][a-zA-Z0-9]{16,}['"]/gi, 
      severity: "error",
      message: "检测到认证Token"
    },
    { 
      name: "手机号", 
      pattern: /1[3-9]\d{9}/g, 
      severity: "warning",
      message: "检测到手机号码"
    },
    { 
      name: "身份证号", 
      pattern: /\d{17}[\dXx]/g, 
      severity: "error",
      message: "检测到身份证号"
    },
    { 
      name: "邮箱", 
      pattern: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, 
      severity: "warning",
      message: "检测到邮箱地址"
    },
    { 
      name: "他人版权", 
      pattern: new RegExp(`Copyright\\s+©?\\s*(?!${escapeRegex(selfCompany)})[\\w\\s]+`, 'gi'), 
      severity: "error",
      message: "检测到他人版权声明"
    }
  ];
  
  for (const { name, pattern, severity, message } of sensitivePatterns) {
    const matches = document.match(pattern);
    if (matches && matches.length > 0) {
      const finding = {
        type: "sensitive_info",
        name: name,
        message: `${message}，共${matches.length}处`,
        severity: severity,
        count: matches.length,
        examples: matches.slice(0, 3).map(m => maskSensitive(m))
      };
      
      if (severity === "error") {
        errors.push(finding);
      } else {
        warnings.push(finding);
      }
    }
  }
  
  return { errors, warnings };
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function maskSensitive(text) {
  // 脱敏处理
  if (text.length <= 8) {
    return text.substring(0, 2) + '***';
  }
  return text.substring(0, 4) + '***' + text.substring(text.length - 2);
}
```

## 迭代修复流程

```javascript
async function iterativeRefinement(document, metadata, maxIterations = 3) {
  let currentDoc = document;
  let iteration = 0;
  
  while (iteration < maxIterations) {
    iteration++;
    
    // 验证当前文档
    const validation = validateCPCCCompliance(currentDoc, metadata, {});
    
    // 没有错误则通过
    if (validation.errors.length === 0) {
      return {
        success: true,
        document: currentDoc,
        iterations: iteration,
        warnings: validation.warnings
      };
    }
    
    // 显示问题并询问用户
    const errorList = validation.errors.map(e => `- ${e.message}`).join('\n');
    
    const response = await AskUserQuestion({
      questions: [{
        question: `发现以下问题（第${iteration}次检查）：\n${errorList}\n\n如何处理？`,
        header: "合规问题",
        multiSelect: false,
        options: [
          {label: "自动修复", description: "尝试自动修复可修复的问题"},
          {label: "手动修复", description: "显示详细问题，手动修改"},
          {label: "忽略继续", description: "忽略问题，继续生成（可能导致补正）"},
          {label: "终止", description: "停止文档生成"}
        ]
      }]
    });
    
    if (response === "终止") {
      return { success: false, reason: "user_aborted" };
    }
    
    if (response === "忽略继续") {
      return {
        success: true,
        document: currentDoc,
        iterations: iteration,
        warnings: [...validation.warnings, ...validation.errors]
      };
    }
    
    if (response === "自动修复") {
      currentDoc = autoFix(currentDoc, validation.errors, metadata);
    } else {
      // 手动修复：显示详细问题
      console.log("详细问题列表：");
      for (const error of validation.errors) {
        console.log(`- [${error.type}] ${error.message}`);
        if (error.snippet) {
          console.log(`  示例: ${error.snippet}`);
        }
      }
      // 等待用户手动修复后重新验证
      await waitForUserFix();
    }
  }
  
  return {
    success: false,
    reason: "max_iterations_reached",
    document: currentDoc
  };
}
```

### 自动修复函数

```javascript
function autoFix(document, errors, metadata) {
  let fixed = document;
  
  for (const error of errors) {
    switch (error.type) {
      case "missing_header":
        // 添加页眉（需要更复杂的处理）
        break;
        
      case "header_name_mismatch":
      case "header_version_mismatch":
        // 修正页眉
        fixed = fixed.replace(
          /<!-- 页眉：.+? 第(\d+)页\/共(\d+)页 -->/g,
          `<!-- 页眉：${metadata.software_name} ${metadata.version}        第$1页/共$2页 -->`
        );
        break;
        
      case "sensitive_info":
        // 敏感信息脱敏
        if (error.name === "手机号") {
          fixed = fixed.replace(/1[3-9]\d{9}/g, match => 
            match.substring(0, 3) + '****' + match.substring(7)
          );
        }
        if (error.name === "身份证号") {
          fixed = fixed.replace(/\d{17}[\dXx]/g, match => 
            match.substring(0, 6) + '********' + match.substring(14)
          );
        }
        if (error.name === "他人版权") {
          fixed = fixed.replace(/Copyright\s+©?\s+(?!${metadata.rights_holder?.name})[\w\s]+/gi, 
            `Copyright © ${metadata.rights_holder?.name || '权利人'}`
          );
        }
        break;
    }
  }
  
  return fixed;
}
```

## 验证报告生成

```javascript
function generateValidationReport(validation, metadata) {
  const report = {
    title: "CPCC合规验证报告",
    software: metadata.software_name,
    version: metadata.version,
    timestamp: new Date().toISOString(),
    summary: {
      total_checks: validation.total,
      passed: validation.passed,
      errors: validation.errors.length,
      warnings: validation.warnings.length
    },
    details: {
      errors: validation.errors,
      warnings: validation.warnings
    },
    recommendation: validation.errors.length === 0 
      ? "文档符合CPCC规范要求，可以提交申请"
      : "请修复上述问题后重新验证"
  };
  
  return report;
}
```

## 输出

```typescript
interface RefinementOutput {
  success: boolean;
  document: string;           // 修复后的文档
  iterations: number;         // 迭代次数
  warnings: Issue[];          // 警告信息
  report: ValidationReport;   // 验证报告
}
```

## 检查清单

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
