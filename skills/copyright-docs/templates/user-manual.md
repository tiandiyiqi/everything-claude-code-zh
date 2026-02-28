# User Manual Template

用户手册模板，用于生成符合CPCC规范的用户手册文档。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## CPCC要求

| 项目 | 要求 |
|------|------|
| 文档类型 | 用户手册（推荐） |
| 每页行数 | ≥ 30行文字 |
| 截图要求 | 实际运行界面，清晰完整 |
| 截图说明 | 每张截图需有文字说明 |

## 文档结构

```
1. 封面
2. 目录
3. 软件概述
4. 运行环境
5. 功能模块介绍
6. 操作流程（含截图）
7. 界面说明
8. 常见问题
9. 版权声明
```

## 截图收集

在生成用户手册前，需要用户提供截图：

```javascript
async function collectScreenshots(metadata) {
  const requiredScreenshots = [
    { id: 'startup', name: '启动界面', description: '软件启动后的第一个界面' },
    { id: 'main', name: '主界面', description: '软件主要工作界面' },
    { id: 'function1', name: '核心功能界面1', description: '第一个核心功能的操作界面' },
    { id: 'function2', name: '核心功能界面2', description: '第二个核心功能的操作界面' },
    { id: 'settings', name: '设置界面', description: '软件设置或配置界面' },
    { id: 'about', name: '关于界面', description: '软件版本信息界面' }
  ];
  
  console.log("## 截图收集\n");
  console.log("请提供以下截图（实际运行界面）：\n");
  
  const screenshots = {};
  
  for (const shot of requiredScreenshots) {
    const response = await AskUserQuestion({
      questions: [{
        question: `请提供【${shot.name}】截图\n描述：${shot.description}\n\n截图要求：\n- 桌面端：包含完整窗口（标题栏、菜单栏、边框）\n- 移动端：包含手机状态栏\n- 清晰度：文字清晰可辨\n- 无隐私信息：手机号、账号等需马赛克处理`,
        header: shot.name,
        multiSelect: false,
        options: [
          {label: "提供截图路径", description: "输入截图文件的绝对路径"},
          {label: "跳过此截图", description: "暂不提供此截图"},
          {label: "完成收集", description: "已提供所有截图，开始生成"}
        ]
      }]
    });
    
    if (response === "提供截图路径") {
      // 获取截图路径
      const pathResponse = await getUserInput("请输入截图路径：");
      screenshots[shot.id] = {
        ...shot,
        path: pathResponse
      };
    } else if (response === "完成收集") {
      break;
    }
  }
  
  return screenshots;
}
```

## 用户手册模板

```markdown
<!--
===========================================
封面页
===========================================
-->

<div style="text-align: center; page-break-after: always;">

# {软件名称}

---

## 用户手册

---

**版本号**：{version}

**编写日期**：{date}

</div>

<!--
===========================================
目录页
===========================================
-->

## 目录

1. 软件概述
2. 运行环境
3. 功能模块介绍
4. 操作流程
5. 界面说明
6. 常见问题
7. 版权声明

---

<!-- 页眉：{软件名称} {version}        第1页/共{total_pages}页 -->

## 1. 软件概述

### 1.1 软件简介

{软件名称}是一款{软件类型}软件，主要用于{主要用途}。

本软件具有以下特点：
- 特点1：{描述}
- 特点2：{描述}
- 特点3：{描述}

### 1.2 适用对象

本软件适用于以下用户群体：
- 用户群体1：{描述}
- 用户群体2：{描述}

### 1.3 主要功能

本软件提供以下主要功能：
1. 功能1：{描述}
2. 功能2：{描述}
3. 功能3：{描述}

---

<!-- 页眉：{软件名称} {version}        第2页/共{total_pages}页 -->

## 2. 运行环境

### 2.1 硬件要求

| 项目 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | {要求} | {要求} |
| 内存 | {要求} | {要求} |
| 硬盘 | {要求} | {要求} |
| 显示器 | {要求} | {要求} |

### 2.2 软件要求

| 项目 | 要求 |
|------|------|
| 操作系统 | {系统要求} |
| 运行环境 | {运行时要求} |
| 依赖软件 | {依赖列表} |

### 2.3 安装说明

1. 步骤1：{描述}
2. 步骤2：{描述}
3. 步骤3：{描述}

---

<!-- 页眉：{软件名称} {version}        第3页/共{total_pages}页 -->

## 3. 功能模块介绍

### 3.1 功能模块总览

{软件名称}包含以下功能模块：

| 模块名称 | 功能描述 | 操作入口 |
|----------|----------|----------|
| 模块1 | {描述} | {入口} |
| 模块2 | {描述} | {入口} |
| 模块3 | {描述} | {入口} |

### 3.2 模块详细说明

#### 3.2.1 {模块1名称}

**功能说明**：{详细功能描述}

**使用场景**：{适用场景描述}

**操作入口**：{如何进入该模块}

#### 3.2.2 {模块2名称}

**功能说明**：{详细功能描述}

**使用场景**：{适用场景描述}

**操作入口**：{如何进入该模块}

---

<!-- 页眉：{软件名称} {version}        第N页/共{total_pages}页 -->

## 4. 操作流程

### 4.1 启动软件

**操作步骤**：

1. 双击桌面快捷方式或从开始菜单启动软件
2. 等待软件加载完成
3. 进入软件主界面

**界面截图**：

![启动界面]({screenshot_startup})

**图4-1 软件启动界面**

启动界面显示软件名称、版本号及加载进度，加载完成后自动进入主界面。

---

### 4.2 主界面操作

**操作步骤**：

1. 查看主界面布局
2. 选择需要使用的功能模块
3. 点击相应按钮进入功能界面

**界面截图**：

![主界面]({screenshot_main})

**图4-2 软件主界面**

主界面包含以下区域：
- 菜单栏：提供各项功能入口
- 工具栏：常用操作快捷按钮
- 工作区：主要操作区域
- 状态栏：显示当前状态信息

---

### 4.3 核心功能操作

#### 4.3.1 {功能1名称}

**操作步骤**：

1. 步骤1：{详细操作描述}
2. 步骤2：{详细操作描述}
3. 步骤3：{详细操作描述}
4. 确认操作完成

**界面截图**：

![{功能1名称}]({screenshot_function1})

**图4-3 {功能1名称}界面**

{界面元素说明}

#### 4.3.2 {功能2名称}

**操作步骤**：

1. 步骤1：{详细操作描述}
2. 步骤2：{详细操作描述}
3. 步骤3：{详细操作描述}
4. 确认操作完成

**界面截图**：

![{功能2名称}]({screenshot_function2})

**图4-4 {功能2名称}界面**

{界面元素说明}

---

### 4.4 设置操作

**操作步骤**：

1. 点击菜单栏中的"设置"选项
2. 在设置界面中修改相关参数
3. 点击"保存"按钮保存设置

**界面截图**：

![设置界面]({screenshot_settings})

**图4-5 设置界面**

设置界面包含以下选项：
- 选项1：{说明}
- 选项2：{说明}
- 选项3：{说明}

---

## 5. 界面说明

### 5.1 界面元素说明

#### 5.1.1 菜单栏

| 菜单项 | 功能说明 |
|--------|----------|
| 文件 | {功能描述} |
| 编辑 | {功能描述} |
| 视图 | {功能描述} |
| 帮助 | {功能描述} |

#### 5.1.2 工具栏

| 按钮 | 功能说明 |
|------|----------|
| 按钮1 | {功能描述} |
| 按钮2 | {功能描述} |
| 按钮3 | {功能描述} |

### 5.2 快捷键说明

| 快捷键 | 功能说明 |
|--------|----------|
| Ctrl+N | 新建 |
| Ctrl+O | 打开 |
| Ctrl+S | 保存 |
| Ctrl+Q | 退出 |
| F1 | 帮助 |

---

## 6. 常见问题

### 6.1 安装问题

**问题1：安装过程中提示缺少依赖**

解决方案：请先安装所需的运行环境，然后重新运行安装程序。

**问题2：安装后无法启动**

解决方案：请检查是否满足最低系统要求，并确保已安装所有依赖软件。

### 6.2 使用问题

**问题1：操作无响应**

解决方案：请等待软件处理完成，或重启软件后重试。

**问题2：结果不符合预期**

解决方案：请检查输入参数是否正确，参考操作流程重新操作。

### 6.3 错误处理

| 错误代码 | 错误描述 | 解决方案 |
|----------|----------|----------|
| E001 | {描述} | {解决方案} |
| E002 | {描述} | {解决方案} |
| E003 | {描述} | {解决方案} |

---

## 7. 版权声明

本软件著作权归{权利人}所有，未经授权不得复制、传播或用于商业目的。

**软件信息**：
- 软件名称：{软件名称}
- 版本号：{version}
- 著作权人：{权利人}
- 开发完成日期：{日期}

---

<!-- 文档结束 -->
```

## 生成函数

```javascript
function generateUserManual(metadata, screenshots, outputDir) {
  console.log("## 生成用户手册\n");
  
  // 1. 计算总页数
  const totalPages = estimateUserManualPages(metadata, screenshots);
  
  // 2. 生成封面
  const cover = generateCoverPage(metadata, '用户手册');
  
  // 3. 生成目录
  const toc = generateTOC([
    "软件概述",
    "运行环境",
    "功能模块介绍",
    "操作流程",
    "界面说明",
    "常见问题",
    "版权声明"
  ]);
  
  // 4. 生成正文
  const body = generateUserManualBody(metadata, screenshots, totalPages);
  
  // 5. 组合文档
  const document = `${cover}
${toc}
${body}
`;
  
  // 6. 写入文件
  const outputPath = `${outputDir}/${metadata.software_name}-用户手册.md`;
  Write(outputPath, document);
  
  console.log(`用户手册已生成: ${outputPath}`);
  
  return outputPath;
}

function generateUserManualBody(metadata, screenshots, totalPages) {
  let currentPage = 1;
  let content = '';
  
  // 第1章：软件概述
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateOverviewSection(metadata);
  
  // 第2章：运行环境
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateEnvironmentSection(metadata);
  
  // 第3章：功能模块介绍
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateModulesSection(metadata);
  
  // 第4章：操作流程（含截图）
  content += '\n---\n\n';
  const { content: flowContent, pages: flowPages } = generateOperationFlowSection(metadata, screenshots, currentPage, totalPages);
  content += flowContent;
  currentPage = flowPages;
  
  // 第5章：界面说明
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateInterfaceSection(metadata);
  
  // 第6章：常见问题
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateFAQSection(metadata);
  
  // 第7章：版权声明
  content += '\n---\n\n';
  content += generatePageHeader(metadata, currentPage++, totalPages);
  content += generateCopyrightSection(metadata);
  
  return content;
}
```

## 截图验证

```javascript
function validateScreenshots(screenshots) {
  const issues = [];
  
  for (const [id, shot] of Object.entries(screenshots)) {
    if (!shot.path) {
      issues.push({
        type: "missing_screenshot",
        message: `缺少截图：${shot.name}`,
        severity: "warning"
      });
      continue;
    }
    
    // 检查文件是否存在
    if (!fs.existsSync(shot.path)) {
      issues.push({
        type: "screenshot_not_found",
        message: `截图文件不存在：${shot.path}`,
        severity: "error"
      });
      continue;
    }
    
    // 检查文件格式
    const ext = path.extname(shot.path).toLowerCase();
    if (!['.png', '.jpg', '.jpeg', '.gif'].includes(ext)) {
      issues.push({
        type: "invalid_format",
        message: `截图格式不正确：${shot.path}（支持PNG、JPG、GIF）`,
        severity: "warning"
      });
    }
    
    // 检查文件大小
    const stats = fs.statSync(shot.path);
    const sizeMB = stats.size / (1024 * 1024);
    if (sizeMB > 10) {
      issues.push({
        type: "screenshot_too_large",
        message: `截图文件过大：${shot.path}（${sizeMB.toFixed(2)}MB，建议<5MB）`,
        severity: "warning"
      });
    }
  }
  
  return issues;
}
```

## 输出

```typescript
interface UserManualOutput {
  outputPath: string;       // 输出文件路径
  totalPages: number;       // 总页数
  screenshots: number;      // 截图数量
  warnings: Issue[];        // 警告信息
}
```

## 注意事项

1. **截图真实性**：必须是实际运行界面，禁止使用原型图
2. **截图完整性**：桌面端需包含标题栏，移动端需包含状态栏
3. **隐私保护**：截图中的隐私信息需马赛克处理
4. **图文对应**：每张截图需有对应的文字说明
5. **清晰度**：截图分辨率≥150dpi，文字清晰可辨
