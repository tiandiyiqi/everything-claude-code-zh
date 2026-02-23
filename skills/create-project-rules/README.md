# Create Project Rules（创建项目规则）

根据项目信息自动生成项目规则文件，整合语言特定规范和 ECC 通用规则。

## 快速开始

### 方式 1: 通过 Claude 调用技能

```
请为我的项目创建规则
```

Claude 会通过交互式问答收集项目信息，然后自动生成规则文件。

### 方式 2: 直接运行脚本

```bash
python3 skills/create-project-rules/scripts/generate-rules.py '{
  "name": "my-app",
  "language": "typescript",
  "type": "web-application",
  "tech_stack": ["react", "next.js"],
  "architecture": "frontend-backend-separation",
  "team_size": "small-team"
}'
```

## 支持的语言

- ✅ JavaScript (ES2020+)
- ✅ TypeScript
- ✅ Python (PEP 8)
- 🚧 Go (待添加)
- 🚧 Java (待添加)
- 🚧 Rust (待添加)

## 生成的规则文件

规则文件保存在 `.claude/rules/project-rules.md`，包含：

1. **语言特定规范** - 来自 `templates/{language}.md`
   - 代码风格
   - 最佳实践
   - 工具配置
   - 代码示例

2. **通用规则** - 继承自 ECC 的核心规则
   - coding-style
   - testing
   - git-workflow
   - security
   - performance
   - patterns
   - hooks
   - agents

## 与 ECC 命令集成

生成的规则会自动被以下命令使用：

- `/code-review` - 代码审查
- `/security-review` - 安全审查
- `/tdd` - 测试驱动开发

## 配置

编辑 `config.json` 可以自定义：

```json
{
  "supported_languages": ["javascript", "typescript", "python", ...],
  "rule_sections": ["coding-style", "testing", ...],
  "templates_dir": "templates/",
  "ecc_rules_dir": ".claude/rules/",
  "output_dir": ".claude/rules/"
}
```

## 添加新语言支持

1. 在 `templates/` 目录创建 `{language}.md` 文件
2. 参考现有模板格式（typescript.md, python.md）
3. 包含语言特定的最佳实践和代码示例
4. 更新 `config.json` 中的 `supported_languages`

## 示例

### TypeScript 项目

```bash
python3 skills/create-project-rules/scripts/generate-rules.py '{
  "name": "my-app",
  "language": "typescript",
  "type": "web-application",
  "tech_stack": ["react", "next.js"],
  "architecture": "frontend-backend-separation",
  "team_size": "small-team"
}'
```

### Python 项目

```bash
python3 skills/create-project-rules/scripts/generate-rules.py '{
  "name": "api-service",
  "language": "python",
  "type": "backend-service",
  "tech_stack": ["django", "postgresql"],
  "architecture": "microservices",
  "team_size": "medium-team"
}'
```

## 故障排除

### 问题：生成的规则文件为空

**解决：** 检查模板和 ECC 规则目录是否存在

```bash
ls skills/create-project-rules/templates/
ls .claude/rules/
```

### 问题：Python 脚本执行失败

**解决：** 确保使用 Python 3.7+

```bash
python3 --version
```

## 未来计划

- [ ] 添加 Go, Java, Rust 语言支持
- [ ] 支持规则版本管理
- [ ] 支持规则导入/导出
- [ ] 集成 continuous-learning v2
- [ ] 支持规则自动演进

## 相关文档

- [SKILL.md](./SKILL.md) - 完整技能文档
- [ECC 规则系统](../../.claude/rules/) - ECC 通用规则
