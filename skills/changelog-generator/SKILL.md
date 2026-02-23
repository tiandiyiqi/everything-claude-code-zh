---
name: changelog-generator
description: 通过分析 Git 提交历史、分类更改并将技术提交转换为清晰、用户友好的发布说明，自动创建面向用户的变更日志。将数小时的手动变更日志编写转变为几分钟的自动生成。
---

# 变更日志生成器

这个技能将技术性的 Git 提交转换为经过精心打磨、用户友好的变更日志，让您的客户和用户能够真正理解并欣赏。

## 何时使用此技能

- 为新版本准备发布说明
- 创建 GitHub Release 说明
- 生成每周或每月的产品更新摘要
- 为客户记录更改
- 维护 CHANGELOG.md 文件
- 准备产品更新公告
- 创建内部发布文档

## 此技能的功能

1. **扫描 Git 历史**：分析特定时间段或版本之间的提交
2. **智能分类**：将提交分组为逻辑类别（✨ 新功能、🐛 修复、🔧 改进、⚠️ 破坏性变更、🔒 安全）
3. **翻译技术→用户友好**：将开发者提交转换为用户语言，移除技术术语
4. **专业格式化**：创建清晰、结构化的 Markdown 变更日志
5. **过滤噪音**：排除内部提交（test, chore, ci, build, refactor）
6. **遵循项目规范**：基于项目的 Conventional Commits 配置（commitlint.config.js）

## 如何使用

### 手动触发

从项目仓库根目录：

```
生成变更日志
```

```
从 v2.4.0 到 HEAD 的变更日志
```

```
为版本 2.5.0 创建发布说明
```

### 自动触发场景

- 用户说"我要发布新版本"（通过 everything-assistant 推荐）
- 用户说"生成变更日志"
- 用户说"创建发布说明"

### 使用特定日期范围

```
为 2024-03-01 至 2024-03-15 之间的所有提交创建变更日志
```

### 使用自定义模板

```
使用 templates/RELEASE_NOTES.md 模板生成 GitHub Release 说明
```

## 工作流程

1. **分析 Git 历史**
   - 使用 `git log` 获取指定范围的提交
   - 解析 Conventional Commits 格式（feat:, fix:, perf: 等）
   - 识别破坏性变更（BREAKING CHANGE）

2. **解析提交**
   - 提取提交类型（type）
   - 提取作用域（scope）
   - 提取描述（description）
   - 检测破坏性变更标记

3. **过滤噪音**
   - 排除 test, chore, ci, build, refactor 类型
   - 保留 feat, fix, perf 等用户相关提交
   - 特殊处理安全相关提交

4. **翻译与分类**
   - 将技术描述转换为用户友好语言
   - 按类别分组（新功能、修复、改进、破坏性变更、安全）
   - 添加 emoji 标识

5. **格式化输出**
   - 生成 Markdown 格式变更日志
   - 按优先级排序（破坏性变更 > 新功能 > 改进 > 修复）
   - 添加版本号和日期

## 示例

**用户**："生成从 v2.4.0 到 HEAD 的变更日志"

**输出**：
```markdown
# v2.5.0 - 2024-03-15

## ⚠️ 破坏性变更

- **API 认证**：所有 API 端点现在需要 Bearer Token 认证。请更新您的客户端代码以包含 Authorization 头。

## ✨ 新功能

- **团队工作空间**：为不同项目创建单独的工作空间。邀请团队成员并保持一切井井有条。
- **键盘快捷键**：按 ? 查看所有可用的快捷键。无需触摸鼠标即可更快地导航。

## 🔧 改进

- **更快的同步**：文件现在在设备之间的同步速度快 2 倍
- **更好的搜索**：搜索现在包括文件内容，而不仅仅是标题

## 🐛 修复

- 修复了大图片无法上传的问题
- 解决了预定帖子中的时区混淆
- 更正了通知徽章计数

## 🔒 安全

- 修复了文件上传中的路径遍历漏洞（CVE-2024-1234）
```

## 与项目集成

### 与 Conventional Commits 集成

本技能基于项目的 `commitlint.config.js` 配置：

- **feat**: ✨ 新功能（用户可见）
- **fix**: 🐛 修复（用户可见）
- **perf**: 🔧 改进（用户可见）
- **docs**: 📝 文档（通常过滤）
- **style**: 💄 样式（通常过滤）
- **refactor**: ♻️ 重构（过滤）
- **test**: ✅ 测试（过滤）
- **chore**: 🔧 杂项（过滤）
- **ci**: 👷 CI（过滤）
- **build**: 📦 构建（过滤）

### 与 release.yml 的关系

- **短期**：changelog-generator 作为手动工具用于维护 CHANGELOG.md
- **长期**：可选择性修改 release.yml 调用 changelog-generator
- **推荐**：保持 release.yml 不变，避免破坏现有工作流

### 与 everything-assistant 集成

当用户说"我要发布新版本"时，everything-assistant 会推荐使用 changelog-generator。

## 配置

技能配置位于 `skills/changelog-generator/config.json`：

- 提交类型映射（type → label + emoji）
- 过滤规则（哪些类型包含/排除）
- 输出格式（markdown, github_release, plain_text）
- 特殊标签（破坏性变更、安全）

## 模板

- `templates/CHANGELOG_STYLE.md`：默认变更日志风格指南
- `templates/RELEASE_NOTES.md`：GitHub Release 专用模板

## 提示

- 从 Git 仓库根目录运行
- 指定版本范围以获得专注的变更日志（如 `v2.4.0..HEAD`）
- 使用模板进行一致的格式化
- 在发布之前审查和调整生成的变更日志
- 将输出直接保存到 CHANGELOG.md

## 翻译原则

### 技术 → 用户友好

- **技术**："feat: add JWT authentication middleware"
- **用户友好**："新增安全登录功能，保护您的账户安全"

- **技术**："fix: resolve race condition in cache invalidation"
- **用户友好**："修复了偶尔出现的数据不同步问题"

- **技术**："perf: optimize database queries with indexing"
- **用户友好**："页面加载速度提升 50%"

### 突出业务价值

- 不说"添加了 Redis 缓存"
- 而说"响应速度提升 3 倍"

- 不说"实现了 WebSocket 连接"
- 而说"实时更新，无需刷新页面"

### 用户视角

- 使用"您"而非"用户"
- 使用主动语态
- 避免技术术语（API、SDK、ORM、middleware 等）
- 关注用户能感知到的变化

## 破坏性变更处理

对于包含 `BREAKING CHANGE` 的提交：

1. 单独列出在最顶部（⚠️ 破坏性变更）
2. 清楚说明影响范围
3. 提供迁移指南或解决方案
4. 使用警告语气

示例：
```markdown
## ⚠️ 破坏性变更

- **API 认证**：所有 API 端点现在需要 Bearer Token 认证。

  **迁移指南**：
  1. 在 API 请求中添加 `Authorization: Bearer <token>` 头
  2. 从 `/auth/token` 端点获取 token
  3. 详见文档：https://docs.example.com/auth
```

## 安全更新处理

对于安全相关的提交：

1. 单独列出（🔒 安全）
2. 如果有 CVE 编号，包含它
3. 说明修复的漏洞类型（但不泄露细节）
4. 建议用户尽快更新

示例：
```markdown
## 🔒 安全

- 修复了文件上传中的路径遍历漏洞（CVE-2024-1234）
- 加强了 SQL 注入防护
- 更新了依赖项以修复已知漏洞

**建议立即更新到此版本。**
```

## 相关用例

- 创建 GitHub Release 说明
- 维护 CHANGELOG.md 文件
- 编写产品更新邮件
- 生成周报/月报
- 创建社交媒体公告帖子

## 参考

- 详细配置：`skills/changelog-generator/config.json`
- 风格指南：`skills/changelog-generator/templates/CHANGELOG_STYLE.md`
- 最佳实践：`skills/changelog-generator/reference.md`
