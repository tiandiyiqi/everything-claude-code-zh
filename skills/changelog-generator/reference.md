# 变更日志生成器参考文档

本文档提供变更日志生成器的最佳实践、使用场景、常见问题和技术实现细节。

## 最佳实践

### 1. 发布工作流

**推荐的发布流程**：

1. **准备发布**
   - 确保所有功能已合并到主分支
   - 运行完整测试套件
   - 确保构建通过

2. **生成变更日志**
   - 使用 changelog-generator 生成变更日志
   - 审查并调整生成的内容
   - 更新 CHANGELOG.md

3. **创建版本标签**
   ```bash
   git tag -a v2.5.0 -m "Release v2.5.0"
   git push origin v2.5.0
   ```

4. **自动发布**
   - GitHub Actions 自动触发
   - 创建 GitHub Release
   - 附加变更日志

### 2. 提交信息质量

变更日志的质量取决于提交信息的质量。

**好的提交信息**：
```
feat(auth): add two-factor authentication

Users can now enable 2FA for enhanced account security.
Supports TOTP apps like Google Authenticator.
```

**不好的提交信息**：
```
fix stuff
update code
wip
```

**改进提交质量的方法**：
- 使用 commitlint 强制规范
- 在 PR 审查时检查提交信息
- 提供提交信息模板
- 团队培训和文档

### 3. 定期维护 CHANGELOG.md

**推荐频率**：
- 每次版本发布时更新
- 每周或每月生成一次（用于内部跟踪）
- 重大功能发布时单独更新

**维护方法**：
```bash
# 生成从上次标签到 HEAD 的变更日志
git describe --tags --abbrev=0  # 获取上次标签
# 然后使用 changelog-generator 生成变更日志
```

## 使用场景

### 场景 1：版本发布

**目标**：为新版本创建发布说明

**步骤**：
1. 确定版本范围（如 `v2.4.0..HEAD`）
2. 生成变更日志
3. 审查并调整
4. 更新 CHANGELOG.md
5. 创建 GitHub Release

**命令**：
```
生成从 v2.4.0 到 HEAD 的变更日志
```

### 场景 2：周报/月报

**目标**：生成产品更新摘要

**步骤**：
1. 确定时间范围（如过去 7 天）
2. 生成变更日志
3. 转换为用户友好的更新公告
4. 发送给用户或团队

**命令**：
```
生成过去 7 天的变更日志
```

### 场景 3：GitHub Release

**目标**：创建 GitHub Release 说明

**步骤**：
1. 生成变更日志
2. 使用 RELEASE_NOTES.md 模板
3. 复制到 GitHub Release
4. 添加完整变更日志链接

**命令**：
```
使用 templates/RELEASE_NOTES.md 模板生成 GitHub Release 说明
```

### 场景 4：产品更新公告

**目标**：为用户创建产品更新邮件

**步骤**：
1. 生成变更日志
2. 选择最重要的功能
3. 添加截图或 GIF
4. 转换为邮件格式

**命令**：
```
生成从 v2.4.0 到 v2.5.0 的变更日志，突出新功能
```

## 常见问题

### Q1: 如何处理多语言变更日志？

**A**: 有两种方法：

**方法 1：生成后翻译**
1. 使用 changelog-generator 生成英文变更日志
2. 使用翻译工具或 LLM 翻译为其他语言
3. 维护多个 CHANGELOG 文件（如 CHANGELOG.md, CHANGELOG.zh-CN.md）

**方法 2：自定义配置**
1. 修改 `config.json` 中的标签为目标语言
2. 在翻译规则中添加目标语言的替换
3. 生成时直接输出目标语言

### Q2: 如何自定义 emoji？

**A**: 修改 `config.json`：

```json
{
  "commit_types": {
    "feat": {
      "label": "🎉 新功能",  // 修改这里
      "include": true,
      "user_facing": true
    }
  }
}
```

### Q3: 如何过滤特定作用域（scope）？

**A**: 修改 `config.json`：

```json
{
  "filtering": {
    "exclude_scopes": ["internal", "test", "dev"],
    "exclude_authors": ["bot@example.com"],
    "min_commit_length": 10
  }
}
```

### Q4: 如何处理不符合 Conventional Commits 的提交？

**A**: changelog-generator 会智能降级：

1. **尝试解析**：首先尝试解析为 Conventional Commits
2. **降级处理**：如果解析失败，使用原始提交信息
3. **人工审查**：生成后提示用户审查和调整
4. **渐进改进**：通过 commitlint 逐步提高提交质量

### Q5: 如何与现有 release.yml 集成？

**A**: 有两种方案：

**短期方案**（推荐）：
- 保持 release.yml 不变
- changelog-generator 作为手动工具
- 用于维护 CHANGELOG.md

**长期方案**（可选）：
- 修改 release.yml 调用 changelog-generator
- 需要在 CI 环境中安装 Claude Code
- 或者编写脚本调用 changelog-generator

### Q6: 如何处理破坏性变更？

**A**: changelog-generator 会自动检测：

1. **检测方式**：
   - 提交信息包含 `BREAKING CHANGE:`
   - 提交信息包含 `!`（如 `feat!: ...`）

2. **处理方式**：
   - 单独列出在最顶部
   - 使用 ⚠️ emoji
   - 提示用户添加迁移指南

3. **示例**：
   ```
   feat(api)!: require authentication for all endpoints

   BREAKING CHANGE: All API endpoints now require Bearer Token authentication.
   ```

## 技术实现细节

### Git 命令

changelog-generator 使用以下 Git 命令：

```bash
# 获取提交历史
git log --pretty=format:"%H|%s|%b|%an|%ae|%ad" v2.4.0..HEAD

# 获取上一个标签
git describe --tags --abbrev=0 HEAD^

# 获取所有标签
git tag -l --sort=-version:refname
```

### 提交解析正则

```regex
# Conventional Commits 格式
^(?<type>\w+)(\((?<scope>[\w-]+)\))?(?<breaking>!)?: (?<description>.+)$

# 破坏性变更检测
BREAKING CHANGE:|^feat!:|^fix!:|^perf!:
```

### 破坏性变更检测

1. **提交类型后的 `!`**：
   ```
   feat!: require authentication
   ```

2. **提交正文中的 `BREAKING CHANGE:`**：
   ```
   feat: add authentication

   BREAKING CHANGE: All endpoints now require auth.
   ```

### 安全更新检测

1. **提交类型为 `security`**（如果配置）
2. **提交信息包含 `CVE-`**
3. **提交信息包含 `security`, `vulnerability`, `exploit`**

### 翻译流程

1. **提取关键信息**：
   - 提交类型（type）
   - 作用域（scope）
   - 描述（description）

2. **应用翻译规则**：
   - 移除技术术语
   - 使用用户友好替换
   - 突出业务价值

3. **格式化输出**：
   - 添加 emoji
   - 分类组织
   - Markdown 格式

## 配置文件详解

### commit_types

定义提交类型的映射和过滤规则。

```json
{
  "feat": {
    "label": "✨ 新功能",      // 显示标签
    "include": true,           // 是否包含在变更日志中
    "user_facing": true,       // 是否面向用户
    "description": "新增功能或特性"  // 描述
  }
}
```

### special_labels

定义特殊标签（破坏性变更、安全）。

```json
{
  "breaking": {
    "label": "⚠️ 破坏性变更",
    "priority": 1,             // 优先级（越小越靠前）
    "description": "不兼容的 API 变更"
  }
}
```

### category_order

定义变更日志中类别的显示顺序。

```json
{
  "category_order": [
    "breaking",   // 破坏性变更
    "security",   // 安全
    "feat",       // 新功能
    "perf",       // 改进
    "fix",        // 修复
    "revert"      // 回退
  ]
}
```

### translation_rules

定义翻译规则。

```json
{
  "remove_technical_terms": [
    "API", "SDK", "ORM", "middleware"
  ],
  "user_friendly_replacements": {
    "add JWT authentication": "新增安全登录功能",
    "optimize database queries": "提升页面加载速度"
  }
}
```

### filtering

定义过滤规则。

```json
{
  "exclude_scopes": [],           // 排除的作用域
  "exclude_authors": [],          // 排除的作者
  "min_commit_length": 10         // 最小提交信息长度
}
```

## 扩展和自定义

### 添加新的提交类型

1. 修改 `config.json`：
   ```json
   {
     "commit_types": {
       "security": {
         "label": "🔒 安全",
         "include": true,
         "user_facing": true,
         "description": "安全相关"
       }
     }
   }
   ```

2. 更新 `commitlint.config.js`：
   ```javascript
   'type-enum': [2, 'always', [
     'feat', 'fix', 'docs', 'style', 'refactor',
     'perf', 'test', 'chore', 'ci', 'build', 'revert',
     'security'  // 添加新类型
   ]]
   ```

### 自定义模板

1. 创建新模板文件：
   ```bash
   touch skills/changelog-generator/templates/CUSTOM_TEMPLATE.md
   ```

2. 定义模板格式：
   ```markdown
   # 自定义模板

   ## 格式规范
   ...
   ```

3. 使用模板：
   ```
   使用 templates/CUSTOM_TEMPLATE.md 模板生成变更日志
   ```

## 相关资源

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [commitlint](https://commitlint.js.org/)
- [GitHub Release Notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
