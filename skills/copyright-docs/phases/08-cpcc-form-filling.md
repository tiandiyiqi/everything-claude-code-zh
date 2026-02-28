# Phase 8: CPCC Online Form Filling

使用 agent-browser 自动填写中国版权保护中心官网申请表。

> **工具**: agent-browser (Vercel Labs) - 专为AI代理设计的浏览器自动化工具
> **官网**: https://github.com/vercel-labs/agent-browser

## 前置条件

### 1. 安装 agent-browser

```bash
# 全局安装（推荐，性能最佳）
npm install -g agent-browser
agent-browser install  # 下载Chromium

# 或使用npx（无需安装）
npx agent-browser install
```

### 2. 准备登录凭证

```bash
# 保存登录凭证（加密存储）
echo "your_password" | agent-browser auth save cpcc \
  --url https://register.ccopyright.com.cn \
  --username your_username \
  --password-stdin
```

## CPCC官网信息

| 项目 | 内容 |
|------|------|
| 官网地址 | https://www.ccopyright.com.cn |
| 登记系统 | https://register.ccopyright.com.cn |
| 申请表类型 | 计算机软件著作权登记申请表 |

## 执行流程

```
┌─────────────────────────────────────────────────────────────────┐
│  CPCC官网自动填写流程                                            │
├─────────────────────────────────────────────────────────────────┤
│  1. 打开官网并登录                                                │
│  2. 创建新申请                                                    │
│  3. 填写软件基本信息                                              │
│  4. 填写权利人信息                                                │
│  5. 上传鉴别材料                                                  │
│  6. 确认并提交                                                    │
└─────────────────────────────────────────────────────────────────┘
```

## 自动化脚本

### Step 1: 登录系统

```bash
# 打开登录页面
agent-browser open "https://register.ccopyright.com.cn"

# 等待页面加载
agent-browser wait --load networkidle

# 获取页面快照
agent-browser snapshot -i --json

# 使用保存的凭证登录
agent-browser auth login cpcc

# 或手动填写
# agent-browser fill @e1 "用户名"
# agent-browser fill @e2 "密码"
# agent-browser click @e3  # 登录按钮
```

### Step 2: 创建新申请

```bash
# 等待登录成功
agent-browser wait --text "软件登记"

# 点击"软件登记"菜单
agent-browser find text "软件登记" click

# 点击"计算机软件著作权登记申请"
agent-browser find text "计算机软件著作权登记申请" click

# 点击"新建申请"
agent-browser find text "新建申请" click
```

### Step 3: 填写软件基本信息

```javascript
// 填写函数
async function fillSoftwareInfo(metadata) {
  // 软件名称
  await agentBrowser.fill('@software_name', metadata.software_name);
  
  // 版本号
  await agentBrowser.fill('@version', metadata.version);
  
  // 软件简称（可选）
  if (metadata.short_name) {
    await agentBrowser.fill('@short_name', metadata.short_name);
  }
  
  // 分类号
  await agentBrowser.select('@category', metadata.category_code);
  
  // 开发完成日期
  await agentBrowser.fill('@develop_date', metadata.develop_date);
  
  // 发表状态
  if (metadata.published) {
    await agentBrowser.click('@published_yes');
    await agentBrowser.fill('@publish_date', metadata.publish_date);
  } else {
    await agentBrowser.click('@published_no');
  }
  
  // 开发方式
  await agentBrowser.click('@develop_mode');  // 独立开发/合作开发/委托开发
  
  // 运行环境
  await agentBrowser.fill('@os', metadata.os);
  await agentBrowser.fill('@runtime', metadata.runtime);
  
  // 编程语言
  await agentBrowser.fill('@language', metadata.language);
  
  // 源代码行数
  await agentBrowser.fill('@code_lines', metadata.code_lines);
  
  // 主要功能
  await agentBrowser.fill('@main_functions', metadata.main_functions);
}
```

### Step 4: 填写权利人信息

```javascript
async function fillRightsHolder(metadata) {
  const holder = metadata.rights_holder;
  
  // 权利人类型
  if (holder.type === 'enterprise') {
    await agentBrowser.click('@holder_enterprise');
    
    // 企业信息
    await agentBrowser.fill('@company_name', holder.name);
    await agentBrowser.fill('@credit_code', holder.credit_code);
    await agentBrowser.fill('@address', holder.address);
  } else {
    await agentBrowser.click('@holder_individual');
    
    // 个人信息
    await agentBrowser.fill('@person_name', holder.name);
    await agentBrowser.fill('@id_number', holder.id_number);
    await agentBrowser.fill('@address', holder.address);
  }
  
  // 省市区
  await agentBrowser.select('@province', holder.province);
  await agentBrowser.select('@city', holder.city);
  await agentBrowser.select('@district', holder.district);
}
```

### Step 5: 上传鉴别材料

```javascript
async function uploadDocuments(metadata, outputDir) {
  // 点击上传按钮
  await agentBrowser.click('@upload_doc');
  
  // 上传文档鉴别材料
  const docPath = `${outputDir}/${metadata.software_name}-软件设计说明书.pdf`;
  await agentBrowser.upload('@doc_file', docPath);
  
  // 等待上传完成
  await agentBrowser.wait --text "上传成功";
  
  // 上传程序鉴别材料
  await agentBrowser.click('@upload_code');
  
  const codePath = `${outputDir}/${metadata.software_name}-源程序.pdf`;
  await agentBrowser.upload('@code_file', codePath);
  
  // 等待上传完成
  await agentBrowser.wait --text "上传成功";
}
```

### Step 6: 确认并提交

```javascript
async function submitApplication() {
  // 检查所有必填项
  await agentBrowser.click('@check_all');
  
  // 确认信息无误
  await agentBrowser.click('@confirm');
  
  // 提交申请
  await agentBrowser.click('@submit');
  
  // 等待提交结果
  await agentBrowser.wait --text "提交成功";
  
  // 获取申请号
  const appNumber = await agentBrowser.get text '@application_number';
  
  return appNumber;
}
```

## 完整自动化流程

```bash
#!/bin/bash
# cpcc-submit.sh - CPCC软著申请自动提交脚本

# 配置
METADATA_FILE=".workflow/.scratchpad/copyright-*/project-metadata.json"
OUTPUT_DIR=".workflow/.scratchpad/copyright-*"

# 读取元数据
SOFTWARE_NAME=$(jq -r '.software_name' $METADATA_FILE)
VERSION=$(jq -r '.version' $METADATA_FILE)

echo "## 开始提交软著申请"
echo "软件名称: $SOFTWARE_NAME"
echo "版本号: $VERSION"

# 1. 打开官网
agent-browser open "https://register.ccopyright.com.cn"
agent-browser wait --load networkidle

# 2. 登录
agent-browser auth login cpcc
agent-browser wait --text "软件登记"

# 3. 创建新申请
agent-browser find text "软件登记" click
agent-browser wait --load networkidle
agent-browser find text "新建申请" click
agent-browser wait --load networkidle

# 4. 填写基本信息
agent-browser snapshot -i
# ... 根据snapshot中的ref填写表单

# 5. 上传材料
agent-browser upload '@doc_file' "$OUTPUT_DIR/$SOFTWARE_NAME-软件设计说明书.pdf"
agent-browser upload '@code_file' "$OUTPUT_DIR/$SOFTWARE_NAME-源程序.pdf"

# 6. 提交
agent-browser click '@submit'
agent-browser wait --text "提交成功"

# 7. 获取申请号
agent-browser get text '@application_number'

# 8. 截图保存
agent-browser screenshot "submission-confirmation.png"

# 9. 关闭浏览器
agent-browser close

echo "申请提交完成！"
```

## 表单字段映射

| 表单字段 | 元数据字段 | 说明 |
|----------|------------|------|
| 软件全称 | software_name | 必须与文档一致 |
| 版本号 | version | 格式：V1.0 |
| 软件简称 | short_name | 可选 |
| 分类号 | category_code | 30100(应用软件)/30200(系统软件) |
| 开发完成日期 | develop_date | YYYY-MM-DD |
| 发表状态 | published | 已发表/未发表 |
| 发表日期 | publish_date | YYYY-MM-DD |
| 开发方式 | develop_mode | 独立开发/合作开发/委托开发 |
| 运行平台 | os | Windows/Linux/macOS |
| 运行环境 | runtime | 如：.NET Framework 4.5 |
| 编程语言 | language | 如：C# |
| 源代码行数 | code_lines | 如：50000 |
| 主要功能 | main_functions | 500字以内 |

## 错误处理

```javascript
async function handleErrors() {
  // 检查是否有错误提示
  const errors = await agentBrowser.get text '@error_messages';
  
  if (errors) {
    console.log("发现错误：", errors);
    
    // 截图保存错误信息
    await agentBrowser.screenshot('error-screenshot.png');
    
    // 返回错误信息
    return { success: false, error: errors };
  }
  
  return { success: true };
}
```

## 会话持久化

```bash
# 使用持久化配置文件，保存登录状态
agent-browser --profile ~/.cpcc-profile open "https://register.ccopyright.com.cn"

# 或使用会话名称
agent-browser --session-name cpcc open "https://register.ccopyright.com.cn"
```

## 注意事项

1. **登录验证码**：如果遇到验证码，需要人工处理
2. **网络稳定性**：确保网络连接稳定
3. **材料格式**：确保PDF文件符合要求（≤50MB，无加密）
4. **信息一致性**：确保表单信息与文档材料完全一致
5. **提交确认**：提交前务必检查所有信息

## 输出

```typescript
interface SubmissionResult {
  success: boolean;
  application_number?: string;  // 申请号
  submission_date: string;      // 提交日期
  error?: string;               // 错误信息
  screenshot: string;           // 确认截图
}
```

## 安全建议

1. 使用 `agent-browser auth save` 加密存储凭证
2. 不要在脚本中硬编码密码
3. 使用环境变量存储敏感信息
4. 定期更换密码
