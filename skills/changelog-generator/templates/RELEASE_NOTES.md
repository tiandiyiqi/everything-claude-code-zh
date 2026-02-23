# GitHub Release 说明模板

本模板用于生成 GitHub Release 的发布说明。

## 格式规范

### 标题

```
v{版本号}
```

例如：`v2.5.0`

### 正文结构

```markdown
## What's New

{新功能列表}

## Bug Fixes

{修复列表}

## Improvements

{改进列表}

## Breaking Changes

{破坏性变更列表}

## Security

{安全更新列表}

---

**Full Changelog**: https://github.com/{owner}/{repo}/compare/{prev_tag}...{current_tag}
```

## 完整示例

```markdown
## What's New

- **Team Workspaces**: Create separate workspaces for different projects. Invite team members and keep everything organized.
- **Keyboard Shortcuts**: Press ? to see all available shortcuts. Navigate faster without touching your mouse.
- **Dark Mode**: Protect your eyes with a comfortable dark theme for nighttime use.

## Bug Fixes

- Fixed issue where large images couldn't be uploaded
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
- Fixed occasional data sync issues

## Improvements

- **Faster Sync**: Files now sync 2x faster between devices
- **Better Search**: Search now includes file content, not just titles
- **Performance**: Page load speed improved by 50%

## Breaking Changes

⚠️ **API Authentication**: All API endpoints now require Bearer Token authentication.

**Migration Guide**:
1. Add `Authorization: Bearer <token>` header to API requests
2. Obtain token from `/auth/token` endpoint
3. See documentation: https://docs.example.com/auth

## Security

- Fixed path traversal vulnerability in file upload (CVE-2024-1234)
- Strengthened SQL injection protection
- Updated dependencies to fix known vulnerabilities

**We recommend updating to this version immediately.**

---

**Full Changelog**: https://github.com/owner/repo/compare/v2.4.0...v2.5.0
```

## 翻译原则

GitHub Release 说明通常使用英文，但也可以根据项目需求使用中文。

### 英文版本

- 使用简洁的英文
- 避免复杂的技术术语
- 使用主动语态
- 突出用户价值

### 中文版本

如果项目主要面向中文用户，可以使用中文：

```markdown
## 新功能

- **团队工作空间**：为不同项目创建单独的工作空间。邀请团队成员并保持一切井井有条。
- **键盘快捷键**：按 ? 查看所有可用的快捷键。无需触摸鼠标即可更快地导航。

## 修复

- 修复了大图片无法上传的问题
- 解决了预定帖子中的时区混淆

## 改进

- **更快的同步**：文件现在在设备之间的同步速度快 2 倍
- **更好的搜索**：搜索现在包括文件内容，而不仅仅是标题

---

**完整变更日志**: https://github.com/owner/repo/compare/v2.4.0...v2.5.0
```

## 注意事项

1. **保持简洁**：GitHub Release 说明应该简洁明了
2. **突出重点**：使用粗体标记重要功能
3. **分类清晰**：按类别组织，便于查找
4. **提供链接**：包含完整变更日志链接
5. **破坏性变更**：如果有破坏性变更，必须单独列出并提供迁移指南
6. **安全更新**：如果有安全更新，必须单独列出并建议用户更新

## 与 release.yml 集成

当前项目的 `.github/workflows/release.yml` 使用简单的 `git log` 生成发布说明。

**短期方案**：
- 保持 release.yml 不变
- 使用 changelog-generator 手动生成发布说明
- 在创建 GitHub Release 时手动粘贴

**长期方案**（可选）：
- 修改 release.yml 调用 changelog-generator
- 自动生成用户友好的发布说明
- 需要在 CI 环境中安装 Claude Code 或使用脚本

**推荐**：短期方案，避免破坏现有工作流。
