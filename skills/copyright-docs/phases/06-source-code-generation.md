# Phase 6: Source Code Material Generation

生成符合CPCC规范的源程序鉴别材料（前30页+后30页）。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## CPCC要求

| 项目 | 要求 |
|------|------|
| 提交方式 | 前30页 + 后30页，共60页 |
| 不足60页 | 提交全部源程序 |
| 每页行数 | ≥ 50行有效代码 |
| 连续性 | 前30页从开头连续，后30页从结尾连续 |
| 页眉格式 | `软件名称 V1.0        第X页/共Y页` |

## 执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│  源程序材料生成流程                                              │
├─────────────────────────────────────────────────────────────────┤
│  1. 扫描源代码文件                                               │
│  2. 按入口文件排序                                               │
│  3. 提取前30页代码                                               │
│  4. 提取后30页代码                                               │
│  5. 添加页眉页码                                                 │
│  6. 敏感信息检查                                                 │
│  7. 生成最终文件                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 源代码扫描

```javascript
function scanSourceFiles(scopePath, entryPoints) {
  // 支持的源代码文件扩展名
  const codeExtensions = [
    '.ts', '.tsx', '.js', '.jsx',  // JavaScript/TypeScript
    '.py',                          // Python
    '.java',                        // Java
    '.go',                          // Go
    '.rs',                          // Rust
    '.c', '.cpp', '.h',             // C/C++
    '.cs',                          // C#
    '.php',                         // PHP
    '.rb',                          // Ruby
    '.swift',                       // Swift
    '.kt',                          // Kotlin
    '.vue', '.svelte'               // Frontend frameworks
  ];
  
  // 排除目录
  const excludeDirs = [
    'node_modules', 'dist', 'build', 'out',
    '.git', '.svn', '__pycache__', 'venv',
    'vendor', 'target', 'bin', 'obj'
  ];
  
  // 扫描所有源代码文件
  const files = [];
  
  function scan(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        if (!excludeDirs.includes(entry.name)) {
          scan(fullPath);
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name);
        if (codeExtensions.includes(ext)) {
          files.push(fullPath);
        }
      }
    }
  }
  
  scan(scopePath);
  
  // 按入口文件排序
  return sortByEntryPoints(files, entryPoints);
}

function sortByEntryPoints(files, entryPoints) {
  // 入口文件排在前面
  const entryFiles = [];
  const otherFiles = [];
  
  for (const file of files) {
    const isEntry = entryPoints.some(ep => file.includes(ep));
    if (isEntry) {
      entryFiles.push(file);
    } else {
      otherFiles.push(file);
    }
  }
  
  // 入口文件按指定顺序，其他文件按字母顺序
  entryFiles.sort((a, b) => {
    const indexA = entryPoints.findIndex(ep => a.includes(ep));
    const indexB = entryPoints.findIndex(ep => b.includes(ep));
    return indexA - indexB;
  });
  
  otherFiles.sort();
  
  return [...entryFiles, ...otherFiles];
}
```

## 代码提取

```javascript
function extractSourceCode(files, metadata) {
  // 读取所有代码内容
  let allCode = '';
  const fileBoundaries = [];
  
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    const startLine = allCode.split('\n').length;
    
    // 添加文件分隔注释
    allCode += `// ========== 文件: ${file} ==========\n`;
    allCode += content + '\n';
    
    const endLine = allCode.split('\n').length;
    fileBoundaries.push({ file, startLine, endLine });
  }
  
  // 计算有效代码行数
  const lines = allCode.split('\n');
  const effectiveLines = lines.filter(line => {
    const trimmed = line.trim();
    return trimmed.length > 0 && 
           !trimmed.startsWith('//') && 
           !trimmed.startsWith('#') &&
           !trimmed.startsWith('/*') &&
           !trimmed.startsWith('*') &&
           !trimmed.match(/^\/\/ =+ 文件:/);
  });
  
  // 计算总页数（每页约60行有效代码）
  const totalPages = Math.ceil(effectiveLines.length / 60);
  
  // 判断是否需要分页
  if (totalPages <= 60) {
    // 不足60页，返回全部
    return {
      type: 'full',
      code: allCode,
      totalPages,
      fileBoundaries
    };
  }
  
  // 提取前30页和后30页
  const linesPerPage = 60;
  const frontLines = linesPerPage * 30;
  const backLines = linesPerPage * 30;
  
  // 前30页
  const frontCode = extractPages(lines, 0, frontLines);
  
  // 后30页
  const backCode = extractPages(lines, lines.length - backLines, lines.length);
  
  return {
    type: 'split',
    frontCode,
    backCode,
    totalPages: 60,
    totalLines: lines.length,
    fileBoundaries
  };
}

function extractPages(lines, start, end) {
  let code = '';
  let currentFile = '';
  
  for (let i = start; i < end && i < lines.length; i++) {
    const line = lines[i];
    
    // 检测文件分隔符
    const fileMatch = line.match(/^\/\/ =+ 文件: (.+) =+/);
    if (fileMatch) {
      currentFile = fileMatch[1];
    }
    
    code += line + '\n';
  }
  
  return code;
}
```

## 页眉页码生成

```javascript
function generateSourceCodeDocument(code, metadata, totalPages, startPage = 1) {
  const lines = code.split('\n');
  const linesPerPage = 60;
  const pages = [];
  
  for (let i = 0; i < lines.length; i += linesPerPage) {
    const pageLines = lines.slice(i, i + linesPerPage);
    const pageNum = startPage + Math.floor(i / linesPerPage);
    
    // 页眉
    const header = `${metadata.software_name} ${metadata.version}        第${pageNum}页/共${totalPages}页`;
    
    // 页面内容
    const pageContent = `${header}\n\n${pageLines.join('\n')}`;
    pages.push(pageContent);
  }
  
  return pages.join('\n\n' + '-'.repeat(80) + '\n\n');
}
```

## 敏感信息处理

```javascript
function sanitizeCode(code, metadata) {
  let sanitized = code;
  
  // 敏感信息模式
  const patterns = [
    // 密码
    {
      pattern: /(password\s*[:=]\s*['"])[^'"]+(['"])/gi,
      replacement: '$1******$2'
    },
    // API密钥
    {
      pattern: /(api[_-]?key\s*[:=]\s*['"])[^'"]+(['"])/gi,
      replacement: '$1******$2'
    },
    // Token
    {
      pattern: /(token\s*[:=]\s*['"])[a-zA-Z0-9]{16,}(['"])/gi,
      replacement: '$1******$2'
    },
    // 手机号
    {
      pattern: /1[3-9]\d{9}/g,
      replacement: match => match.substring(0, 3) + '****' + match.substring(7)
    },
    // 身份证号
    {
      pattern: /\d{17}[\dXx]/g,
      replacement: match => match.substring(0, 6) + '********' + match.substring(14)
    },
    // 他人版权声明
    {
      pattern: new RegExp(`Copyright\\s+©?\\s*(?!${escapeRegex(metadata.rights_holder?.name || '')})[\\w\\s]+`, 'gi'),
      replacement: `Copyright © ${metadata.rights_holder?.name || '权利人'}`
    }
  ];
  
  for (const { pattern, replacement } of patterns) {
    sanitized = sanitized.replace(pattern, replacement);
  }
  
  return sanitized;
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
```

## 完整生成流程

```javascript
async function generateSourceCodeMaterial(metadata, outputDir) {
  console.log("## Phase 6: 源程序材料生成\n");
  
  // 1. 扫描源代码文件
  console.log("1. 扫描源代码文件...");
  const files = scanSourceFiles(metadata.scope_path, metadata.entry_points);
  console.log(`   找到 ${files.length} 个源代码文件`);
  
  // 2. 提取代码
  console.log("2. 提取源代码...");
  const extraction = extractSourceCode(files, metadata);
  
  // 3. 敏感信息处理
  console.log("3. 检查并处理敏感信息...");
  
  let finalCode;
  let totalPages;
  
  if (extraction.type === 'full') {
    finalCode = sanitizeCode(extraction.code, metadata);
    totalPages = extraction.totalPages;
  } else {
    const frontSanitized = sanitizeCode(extraction.frontCode, metadata);
    const backSanitized = sanitizeCode(extraction.backCode, metadata);
    
    finalCode = `/* ========== 前30页 ========== */\n\n${frontSanitized}\n\n/* ========== 后30页 ========== */\n\n${backSanitized}`;
    totalPages = 60;
  }
  
  // 4. 生成文档
  console.log("4. 生成源程序文档...");
  const document = generateSourceCodeDocument(finalCode, metadata, totalPages);
  
  // 5. 验证
  console.log("5. 验证文档...");
  const validation = validateSourceCodeDocument(document, metadata);
  
  if (!validation.valid) {
    console.log("   警告:");
    for (const warning of validation.warnings) {
      console.log(`   - ${warning.message}`);
    }
  }
  
  // 6. 写入文件
  const outputPath = `${outputDir}/${metadata.software_name}-源程序.md`;
  Write(outputPath, document);
  console.log(`\n源程序材料已生成: ${outputPath}`);
  
  return {
    outputPath,
    totalPages,
    totalFiles: files.length,
    warnings: validation.warnings
  };
}
```

## 验证函数

```javascript
function validateSourceCodeDocument(document, metadata) {
  const warnings = [];
  
  // 检查页眉
  const headerPattern = /第\d+页\/共\d+页/g;
  const headers = document.match(headerPattern) || [];
  
  if (headers.length === 0) {
    warnings.push({
      type: "missing_header",
      message: "缺少页眉页码"
    });
  }
  
  // 检查每页行数
  const pages = document.split(/第\d+页\/共\d+页/).slice(1);
  
  for (let i = 0; i < pages.length; i++) {
    const lines = pages[i].split('\n').filter(l => {
      const trimmed = l.trim();
      return trimmed.length > 0 && 
             !trimmed.startsWith('//') && 
             !trimmed.startsWith('#') &&
             !trimmed.startsWith('/*');
    });
    
    if (lines.length < 50) {
      warnings.push({
        type: "low_line_count",
        message: `第${i + 1}页有效代码行数不足: ${lines.length}行（要求≥50行）`,
        page: i + 1
      });
    }
  }
  
  // 检查敏感信息
  const sensitivePatterns = [
    { name: "密码", pattern: /password\s*[:=]\s*['"][^'"]+['"]/gi },
    { name: "API密钥", pattern: /api[_-]?key\s*[:=]\s*['"][^'"]+['"]/gi },
    { name: "手机号", pattern: /1[3-9]\d{9}/g },
    { name: "身份证号", pattern: /\d{17}[\dXx]/g }
  ];
  
  for (const { name, pattern } of sensitivePatterns) {
    const matches = document.match(pattern);
    if (matches && matches.length > 0) {
      warnings.push({
        type: "sensitive_info",
        message: `检测到${name}，共${matches.length}处`,
        severity: "warning"
      });
    }
  }
  
  return {
    valid: warnings.filter(w => w.severity === 'error').length === 0,
    warnings
  };
}
```

## 输出

```typescript
interface SourceCodeOutput {
  outputPath: string;       // 输出文件路径
  totalPages: number;       // 总页数
  totalFiles: number;       // 源文件数量
  warnings: Issue[];        // 警告信息
}
```

## 输出文件示例

```markdown
软件名称 V1.0        第1页/共60页

// ========== 文件: src/index.ts ==========
import express from 'express';
import { config } from './config';
...

--------------------------------------------------------------------------------

软件名称 V1.0        第2页/共60页

// ========== 文件: src/auth.ts ==========
export function authenticate(token: string) {
  ...
}
...

--------------------------------------------------------------------------------
```

## 注意事项

1. **代码连续性**：确保代码从开头连续选取，不能跳跃
2. **有效行数**：空行和注释不计入有效行数
3. **敏感信息**：必须脱敏处理
4. **页眉格式**：必须与文档材料一致
5. **总页数**：必须标注正确的总页数
