---
name: agent-browser
description: Vercel Agent Browser - AI 优化的无头浏览器自动化 CLI。用于 E2E 测试、网页抓取、自动化任务。
---

# Agent Browser

Vercel Agent Browser 是一个专为 AI 智能体设计的无头浏览器自动化 CLI，基于 Playwright 构建，性能卓越且易用。

## 安装

本技能已包含 agent-browser 依赖，**无需单独安装**。

首次使用时自动安装：
```bash
cd .claude/skills/agent-browser
npm install
npx agent-browser install  # 下载 Chromium
```

## 核心概念：快照 + 引用系统

Agent Browser 使用**快照（Snapshot）** 获取页面可交互元素，然后通过**引用（Refs）** 进行操作，避免脆弱的选择器。

```bash
# 1. 打开页面
agent-browser open https://example.com

# 2. 获取快照（返回带引用的元素）
agent-browser snapshot -i
# 输出示例：
# [ref=e1] button "Submit"
# [ref=e2] input "email"
# [ref=e3] input "password"

# 3. 通过引用操作
agent-browser click @e1          # 点击提交按钮
agent-browser fill @e2 "user@test.com"  # 填充邮箱
```

## 常用命令

### 导航
```bash
agent-browser open <url>         # 打开 URL（别名：goto, navigate）
agent-browser back              # 后退
agent-browser forward           # 前进
agent-browser reload            # 刷新
```

### 交互
```bash
agent-browser click <ref>       # 点击元素
agent-browser dblclick <ref>    # 双击
agent-browser fill <ref> <text> # 清空并填充
agent-browser type <ref> <text> # 输入（保留已有内容）
agent-browser press <key>       # 按键（Enter, Tab, Control+a）
agent-browser hover <ref>       # 悬停
agent-browser select <ref> <val>  # 选择下拉选项
agent-browser check <ref>       # 选中复选框
agent-browser uncheck <ref>     # 取消复选框
```

### 获取信息
```bash
agent-browser get text <ref>       # 获取文本
agent-browser get html <ref>       # 获取 HTML
agent-browser get value <ref>      # 获取输入值
agent-browser get attr <ref> <attr> # 获取属性
agent-browser get title            # 获取页面标题
agent-browser get url              # 获取当前 URL
agent-browser get count <selector> # 计数元素
```

### 等待
```bash
agent-browser wait visible <ref>   # 等待元素可见
agent-browser wait <ms>            # 等待毫秒数
agent-browser wait --text "Welcome"  # 等待文本出现
agent-browser wait --url "**/dash"   # 等待 URL 匹配
agent-browser wait --load networkidle  # 等待加载完成
```

### 截图与快照
```bash
agent-browser screenshot              # 截图（保存到临时目录）
agent-browser screenshot page.png     # 截图到文件
agent-browser screenshot --full       # 全页面截图
agent-browser screenshot --annotate   # 带元素标注的截图
agent-browser snapshot                # 获取可访问性树
agent-browser snapshot -i             # 带引用的快照（AI 优化）
```

### 语义查找
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@test.com"
agent-browser find placeholder "Enter email" type "test"
agent-browser find testid "submit-btn" click
```

### JavaScript
```bash
agent-browser eval "document.title"
agent-browser eval "document.querySelector('.btn').click()"
```

### 浏览器控制
```bash
agent-browser set viewport 1920 1080  # 设置视口大小
agent-browser mouse move 100 200      # 移动鼠标
agent-browser mouse wheel 0 -300      # 滚动
agent-browser scroll down 500         # 滚动
agent-browser close                   # 关闭浏览器
```

## 典型工作流

### 1. 登录流程测试
```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser screenshot dashboard.png
agent-browser get text @welcome
agent-browser close
```

### 2. 表单提交测试
```bash
agent-browser open https://example.com/form
agent-browser fill "#name" "John Doe"
agent-browser fill "#email" "john@example.com"
agent-browser select "#country" "US"
agent-browser click "button[type=submit]"
agent-browser wait --text "Success"
agent-browser get text .message
```

### 3. 侦察模式（调试）
```bash
agent-browser open https://example.com
agent-browser snapshot -i
# 查看元素引用后，选择正确的元素进行操作
agent-browser click @e5
agent-browser screenshot debug.png
```

## 与 e2e-runner 的关系

- **e2e-runner 智能体**：自动执行完整测试流程
- **本技能**：提供直接使用 agent-browser CLI 的能力

使用场景：
- 快速验证页面行为
- 一次性自动化任务
- 调试复杂的 UI 交互
- 需要精细控制浏览器行为时

## 故障排除

### Chromium 未安装
```bash
npx agent-browser install
```

### 权限问题
```bash
# macOS
sudo chown -R $(whoami) ~/.cache
```

### 端口被占用
```bash
# Agent Browser 默认使用端口 9222
lsof -i :9222
```

## 输出示例

```
$ agent-browser open example.com
✓ Opened https://example.com

$ agent-browser snapshot -i
[ref=e1] heading "Example Domain"
[ref=e2] link "More information..."

$ agent-browser get title
Example Domain
```
