# Phase 7: PDF Output

将Markdown文档转换为符合CPCC规范的PDF格式。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## CPCC要求

| 项目 | 要求 |
|------|------|
| 文件格式 | PDF |
| 文件大小 | ≤ 50MB |
| 加密 | 无加密、无密码保护 |
| 水印 | 无水印 |
| 字体 | 字体嵌入PDF |
| 排版 | A4纵向，文字从左至右 |

## 技术方案

使用 Markdown 转 PDF 工具链：

```
Markdown → HTML → PDF
```

推荐工具：
- **md-to-pdf** - 简单直接的MD转PDF工具
- **markdown-pdf** - 支持自定义样式
- **puppeteer** - 高质量PDF输出（备选）

## 执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│  PDF生成流程                                                     │
├─────────────────────────────────────────────────────────────────┤
│  1. 检查依赖                                                     │
│  2. 准备样式模板                                                 │
│  3. 转换Markdown为PDF                                            │
│  4. 验证PDF格式                                                  │
│  5. 输出最终文件                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 依赖检查

```javascript
async function checkDependencies() {
  const requiredPackages = ['md-to-pdf', 'marked'];
  const missing = [];
  
  for (const pkg of requiredPackages) {
    try {
      require.resolve(pkg);
    } catch (e) {
      missing.push(pkg);
    }
  }
  
  if (missing.length > 0) {
    console.log(`缺少依赖包: ${missing.join(', ')}`);
    console.log('正在安装...');
    
    await RunCommand({
      command: `cnpm install ${missing.join(' ')} --save-dev`,
      cwd: process.cwd()
    });
  }
  
  return true;
}
```

## 样式模板

```css
/* cpcc-style.css - CPCC规范PDF样式 */

@page {
  size: A4 portrait;
  margin: 25mm 20mm 20mm 20mm;
}

body {
  font-family: "SimSun", "宋体", serif;
  font-size: 12pt;
  line-height: 1.6;
  color: #000;
}

/* 页眉 */
@page {
  @top-center {
    content: element(header);
  }
}

#header {
  position: running(header);
  text-align: center;
  font-size: 10pt;
  border-bottom: 1px solid #000;
  padding-bottom: 5px;
}

/* 封面 */
.cover-page {
  page-break-after: always;
  text-align: center;
  padding-top: 200px;
}

.cover-page h1 {
  font-size: 22pt;
  font-weight: bold;
  margin-bottom: 40px;
}

.cover-page h2 {
  font-size: 18pt;
  font-weight: normal;
  margin-bottom: 60px;
}

.cover-page .info {
  font-size: 14pt;
  margin-top: 20px;
}

/* 目录 */
.toc-page {
  page-break-after: always;
}

.toc-page h2 {
  font-size: 16pt;
  text-align: center;
  margin-bottom: 30px;
}

.toc-page ul {
  list-style: none;
  padding-left: 0;
}

.toc-page li {
  margin-bottom: 10px;
  font-size: 12pt;
}

/* 正文 */
h1 {
  font-size: 16pt;
  font-weight: bold;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
}

h2 {
  font-size: 14pt;
  font-weight: bold;
  margin-top: 15px;
  margin-bottom: 10px;
}

h3 {
  font-size: 12pt;
  font-weight: bold;
  margin-top: 10px;
  margin-bottom: 8px;
}

p {
  text-indent: 2em;
  margin-bottom: 10px;
  text-align: justify;
}

/* 表格 */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 15px 0;
  font-size: 10pt;
}

th, td {
  border: 1px solid #000;
  padding: 6px 10px;
  text-align: left;
}

th {
  background-color: #f0f0f0;
  font-weight: bold;
}

/* 代码块 */
pre, code {
  font-family: "Courier New", Consolas, monospace;
  font-size: 9pt;
  background-color: #f5f5f5;
  padding: 2px 5px;
}

pre {
  padding: 10px;
  overflow-x: auto;
  border: 1px solid #ddd;
}

/* 图片 */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 15px auto;
}

/* Mermaid图表 */
.mermaid {
  text-align: center;
  margin: 15px 0;
}

/* 分页符 */
.page-break {
  page-break-after: always;
}

/* 页码 */
@page {
  @bottom-right {
    content: "第" counter(page) "页/共" counter(pages) "页";
    font-size: 10pt;
  }
}
```

## PDF生成函数

```javascript
const { mdToPdf } = require('md-to-pdf');
const fs = require('fs');
const path = require('path');

async function generatePDF(markdownPath, metadata, outputDir) {
  console.log("## Phase 7: PDF输出\n");
  
  // 1. 检查依赖
  console.log("1. 检查依赖...");
  await checkDependencies();
  
  // 2. 读取Markdown内容
  console.log("2. 读取Markdown内容...");
  const markdown = fs.readFileSync(markdownPath, 'utf-8');
  
  // 3. 预处理Markdown
  console.log("3. 预处理Markdown...");
  const processedMd = preprocessMarkdown(markdown, metadata);
  
  // 4. 配置PDF选项
  const pdfOptions = {
    dest: path.join(outputDir, `${metadata.software_name}-软件设计说明书.pdf`),
    pdf_options: {
      format: 'A4',
      margin: {
        top: '25mm',
        right: '20mm',
        bottom: '20mm',
        left: '20mm'
      },
      printBackground: true,
      preferCSSPageSize: true
    },
    stylesheet: [path.join(__dirname, 'cpcc-style.css')],
    body_class: 'cpcc-document',
    css: getInlineCSS(metadata),
    pdf_options: {
      headerTemplate: getHeaderTemplate(metadata),
      footerTemplate: getFooterTemplate(),
      displayHeaderFooter: true,
      margin: {
        top: '35mm',
        bottom: '25mm',
        right: '20mm',
        left: '20mm'
      }
    }
  };
  
  // 5. 生成PDF
  console.log("4. 生成PDF...");
  const pdf = await mdToPdf({ content: processedMd }, pdfOptions);
  
  if (pdf) {
    fs.writeFileSync(pdfOptions.dest, pdf.content);
    console.log(`\nPDF已生成: ${pdfOptions.dest}`);
    
    // 6. 验证PDF
    console.log("5. 验证PDF...");
    const validation = await validatePDF(pdfOptions.dest);
    
    return {
      success: true,
      outputPath: pdfOptions.dest,
      fileSize: fs.statSync(pdfOptions.dest).size,
      validation
    };
  }
  
  return { success: false, error: "PDF生成失败" };
}
```

## Markdown预处理

```javascript
function preprocessMarkdown(markdown, metadata) {
  let processed = markdown;
  
  // 1. 处理封面页
  processed = processed.replace(
    /<div style="text-align: center[^"]*">[\s\S]*?<\/div>/,
    match => {
      return `<div class="cover-page">
${match.replace(/<div[^>]*>|<\/div>/g, '')}
</div>`;
    }
  );
  
  // 2. 处理目录页
  if (processed.includes('## 目录')) {
    processed = processed.replace(
      /## 目录[\s\S]*?(?=\n---|\n##)/,
      match => `<div class="toc-page">\n${match}\n</div>`
    );
  }
  
  // 3. 处理分页符
  processed = processed.replace(/\n---\n/g, '\n<div class="page-break"></div>\n');
  
  // 4. 处理页眉注释（转换为HTML注释）
  processed = processed.replace(
    /<!-- 页眉：(.+?) 第(\d+)页\/共(\d+)页 -->/g,
    ''
  );
  
  // 5. 确保Mermaid图表正确渲染
  processed = processed.replace(
    /```mermaid\n([\s\S]*?)```/g,
    '<div class="mermaid">$1</div>'
  );
  
  return processed;
}
```

## 页眉页脚模板

```javascript
function getHeaderTemplate(metadata) {
  return `
    <style>
      .header {
        width: 100%;
        text-align: center;
        font-size: 10pt;
        font-family: "SimSun", serif;
        border-bottom: 1px solid #000;
        padding-bottom: 5px;
      }
    </style>
    <div class="header">
      ${metadata.software_name} ${metadata.version}
    </div>
  `;
}

function getFooterTemplate() {
  return `
    <style>
      .footer {
        width: 100%;
        text-align: right;
        font-size: 10pt;
        font-family: "SimSun", serif;
      }
    </style>
    <div class="footer">
      第<span class="pageNumber"></span>页/共<span class="totalPages"></span>页
    </div>
  `;
}
```

## 内联CSS

```javascript
function getInlineCSS(metadata) {
  return `
    @page {
      size: A4 portrait;
      margin: 35mm 20mm 25mm 20mm;
    }
    
    body {
      font-family: "SimSun", "宋体", serif;
      font-size: 12pt;
      line-height: 1.8;
    }
    
    .cover-page {
      page-break-after: always;
      text-align: center;
      padding-top: 200px;
    }
    
    .cover-page h1 {
      font-size: 22pt;
      margin-bottom: 40px;
    }
    
    .toc-page {
      page-break-after: always;
    }
    
    h1 { font-size: 16pt; text-align: center; }
    h2 { font-size: 14pt; }
    h3 { font-size: 12pt; }
    
    p { text-indent: 2em; text-align: justify; }
    
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 15px 0;
    }
    
    th, td {
      border: 1px solid #000;
      padding: 6px 10px;
    }
    
    pre {
      font-family: "Courier New", monospace;
      font-size: 9pt;
      background: #f5f5f5;
      padding: 10px;
    }
    
    .page-break {
      page-break-after: always;
    }
  `;
}
```

## PDF验证

```javascript
async function validatePDF(pdfPath) {
  const stats = fs.statSync(pdfPath);
  const fileSizeMB = stats.size / (1024 * 1024);
  
  const checks = [];
  
  // 1. 文件大小检查
  checks.push({
    name: "文件大小",
    pass: fileSizeMB <= 50,
    value: `${fileSizeMB.toFixed(2)}MB`,
    limit: "≤50MB"
  });
  
  // 2. 文件格式检查
  const buffer = fs.readFileSync(pdfPath);
  const isPDF = buffer.slice(0, 4).toString() === '%PDF';
  checks.push({
    name: "文件格式",
    pass: isPDF,
    value: isPDF ? "PDF" : "非PDF"
  });
  
  // 3. 加密检查（简单检测）
  const isEncrypted = buffer.includes('/Encrypt');
  checks.push({
    name: "无加密",
    pass: !isEncrypted,
    value: isEncrypted ? "已加密" : "未加密"
  });
  
  return {
    valid: checks.every(c => c.pass),
    checks,
    fileSize: fileSizeMB
  };
}
```

## 批量转换

```javascript
async function convertAllToPDF(outputDir, metadata) {
  const mdFiles = [
    { name: '设计说明书', file: `${metadata.software_name}-软件设计说明书.md` },
    { name: '源程序', file: `${metadata.software_name}-源程序.md` },
    { name: '用户手册', file: `${metadata.software_name}-用户手册.md` }
  ];
  
  const results = [];
  
  for (const { name, file } of mdFiles) {
    const mdPath = path.join(outputDir, file);
    
    if (fs.existsSync(mdPath)) {
      console.log(`\n转换: ${name}`);
      const result = await generatePDF(mdPath, metadata, outputDir);
      results.push({ name, ...result });
    }
  }
  
  return results;
}
```

## 输出

```typescript
interface PDFOutput {
  success: boolean;
  outputPath: string;       // PDF文件路径
  fileSize: number;         // 文件大小（MB）
  validation: {
    valid: boolean;
    checks: ValidationCheck[];
  };
}
```

## 注意事项

1. **字体嵌入**：确保中文字体嵌入PDF
2. **页眉页脚**：使用Puppeteer的headerTemplate/footerTemplate
3. **分页控制**：使用CSS的page-break-after属性
4. **图片质量**：确保截图分辨率≥150dpi
5. **文件大小**：压缩图片，控制PDF大小≤50MB

## 备选方案

如果md-to-pdf效果不理想，可使用Puppeteer直接生成：

```javascript
const puppeteer = require('puppeteer');

async function generatePDFWithPuppeteer(html, outputPath, metadata) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: getHeaderTemplate(metadata),
    footerTemplate: getFooterTemplate(),
    margin: {
      top: '35mm',
      bottom: '25mm',
      right: '20mm',
      left: '20mm'
    }
  });
  
  await browser.close();
}
```
