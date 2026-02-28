# Phase 1: Metadata Collection

收集软件元数据，包含版本号格式验证和敏感信息检查。

> **规范参考**: [../specs/cpcc-requirements.md](../specs/cpcc-requirements.md)

## 执行流程

### Step 1: 软件名称与版本号

```javascript
// 1. 收集软件名称
const nameResponse = await AskUserQuestion({
  questions: [{
    question: "请输入软件名称（将显示在文档页眉）：",
    header: "软件名称",
    multiSelect: false,
    options: [
      {label: "自动检测", description: "从 package.json 或项目配置读取"},
      {label: "手动输入", description: "输入自定义名称"}
    ]
  }]
});

// 2. 收集版本号
const versionResponse = await AskUserQuestion({
  questions: [{
    question: "请输入版本号（CPCC要求格式：V1.0 或 V1.0.0）：",
    header: "版本号",
    multiSelect: false,
    options: [
      {label: "自动检测", description: "从 package.json 读取"},
      {label: "手动输入", description: "输入自定义版本号"}
    ]
  }]
});

// 3. 验证版本号格式
const versionValidation = validateVersion(versionResponse.value);
if (!versionValidation.valid) {
  // 提示用户修正
  await AskUserQuestion({
    questions: [{
      question: `版本号格式不符合CPCC要求：${versionValidation.error}\n请选择处理方式：`,
      header: "版本号",
      multiSelect: false,
      options: [
        {label: "自动修正", description: "自动转换为标准格式（如 V1.0.0 → V1.0）"},
        {label: "手动修正", description: "重新输入版本号"},
        {label: "忽略继续", description: "保持当前版本号（可能导致补正）"}
      ]
    }]
  });
}
```

### Step 2: 版本号格式验证

```javascript
function validateVersion(version) {
  // 合法格式: V1.0, V1.0.0, V2.1.0
  const validPattern = /^V\d+\.\d+(\.\d+)?$/;
  
  // 禁止格式检测
  const invalidPatterns = [
    { pattern: /beta/i, error: "版本号不能包含 'beta'" },
    { pattern: /alpha/i, error: "版本号不能包含 'alpha'" },
    { pattern: /test/i, error: "版本号不能包含 'test'" },
    { pattern: /测试/, error: "版本号不能包含 '测试'" },
    { pattern: /正式/, error: "版本号不能包含 '正式'" },
    { pattern: /\.\d+\.\d+\./, error: "版本号层级过多（最多3段）" },
    { pattern: /\d{4}版/, error: "不能使用年份作为版本号" }
  ];
  
  // 检查基本格式
  if (!validPattern.test(version)) {
    // 尝试自动修正
    const corrected = autoCorrectVersion(version);
    if (corrected) {
      return { valid: false, error: "格式不正确", suggestion: corrected };
    }
    return { valid: false, error: "版本号格式不正确，推荐使用 V1.0 或 V1.0.0 格式" };
  }
  
  // 检查禁止格式
  for (const { pattern, error } of invalidPatterns) {
    if (pattern.test(version)) {
      return { valid: false, error };
    }
  }
  
  return { valid: true };
}

function autoCorrectVersion(version) {
  // 尝试自动修正常见格式问题
  let corrected = version;
  
  // 添加 V 前缀
  if (!corrected.startsWith('V') && !corrected.startsWith('v')) {
    corrected = 'V' + corrected;
  }
  
  // 统一大写 V
  corrected = corrected.replace(/^v/, 'V');
  
  // 移除测试标识
  corrected = corrected.replace(/-?beta/i, '');
  corrected = corrected.replace(/-?alpha/i, '');
  corrected = corrected.replace(/-?test/i, '');
  corrected = corrected.replace(/测试版/, '');
  corrected = corrected.replace(/正式版/, '');
  
  // 简化版本号（保留前2段）
  const match = corrected.match(/^V(\d+)\.(\d+)/);
  if (match) {
    corrected = `V${match[1]}.${match[2]}`;
  }
  
  return corrected !== version ? corrected : null;
}
```

### Step 3: 软件类型

```javascript
AskUserQuestion({
  questions: [{
    question: "软件属于哪种类型？",
    header: "软件类型",
    multiSelect: false,
    options: [
      {label: "命令行工具 (CLI)", description: "重点描述命令、参数"},
      {label: "后端服务/API", description: "重点描述端点、协议"},
      {label: "SDK/库", description: "重点描述接口、集成"},
      {label: "数据处理系统", description: "重点描述数据流、转换"},
      {label: "自动化脚本", description: "重点描述工作流、触发器"}
    ]
  }]
})
```

### Step 4: 分析范围

```javascript
AskUserQuestion({
  questions: [{
    question: "分析范围是什么？",
    header: "分析范围",
    multiSelect: false,
    options: [
      {label: "整个项目", description: "分析全部源代码"},
      {label: "指定目录", description: "仅分析 src/ 或其他目录"},
      {label: "自定义路径", description: "手动指定路径"}
    ]
  }]
})
```

### Step 5: 文档类型选择

```javascript
AskUserQuestion({
  questions: [{
    question: "选择要生成的文档类型（CPCC推荐用户手册）：",
    header: "文档类型",
    multiSelect: false,
    options: [
      {label: "用户手册（推荐）", description: "操作流程+界面截图，通过率最高"},
      {label: "设计说明书", description: "架构设计+算法流程，适合技术型软件"},
      {label: "两者都生成", description: "同时生成用户手册和设计说明书"}
    ]
  }]
})
```

### Step 6: 权利人信息

```javascript
AskUserQuestion({
  questions: [{
    question: "权利人类型？",
    header: "权利人",
    multiSelect: false,
    options: [
      {label: "企业", description: "需与营业执照名称一致"},
      {label: "个人", description: "需与身份证姓名一致"}
    ]
  }]
})
```

## 输出

保存元数据到 `project-metadata.json`：

```json
{
  "software_name": "智能数据分析系统",
  "version": "V1.0",
  "category": "后端服务/API",
  "scope_path": "src/",
  "document_type": "user_manual",
  "rights_holder": {
    "type": "enterprise",
    "name": "某某科技有限公司"
  },
  "tech_stack": {
    "language": "TypeScript",
    "runtime": "Node.js 18+",
    "framework": "Express.js",
    "dependencies": ["mongoose", "redis", "bull"]
  },
  "entry_points": ["src/index.ts", "src/cli.ts"],
  "main_modules": ["auth", "data", "api", "worker"],
  "validation": {
    "version_valid": true,
    "version_corrected": false
  }
}
```

## 验证检查清单

在收集完元数据后，执行以下验证：

```javascript
function validateMetadata(metadata) {
  const checks = [];
  
  // 1. 版本号格式验证
  const versionCheck = validateVersion(metadata.version);
  checks.push({
    name: "版本号格式",
    pass: versionCheck.valid,
    error: versionCheck.error,
    suggestion: versionCheck.suggestion
  });
  
  // 2. 软件名称非空
  checks.push({
    name: "软件名称",
    pass: metadata.software_name && metadata.software_name.length > 0,
    error: "软件名称不能为空"
  });
  
  // 3. 权利人名称非空
  checks.push({
    name: "权利人名称",
    pass: metadata.rights_holder?.name && metadata.rights_holder.name.length > 0,
    error: "权利人名称不能为空"
  });
  
  // 4. 分析路径存在
  checks.push({
    name: "分析路径",
    pass: fs.existsSync(metadata.scope_path),
    error: `分析路径不存在: ${metadata.scope_path}`
  });
  
  return {
    valid: checks.every(c => c.pass),
    checks: checks
  };
}
```

## 常见问题处理

| 问题 | 处理方式 |
|------|----------|
| 版本号格式错误 | 提示用户或自动修正 |
| 软件名称包含特殊字符 | 警告用户可能导致问题 |
| 权利人名称不一致 | 提示用户确认与证件一致 |
| 分析路径不存在 | 提示用户重新选择 |
