#!/usr/bin/env python3
"""
项目规则生成器

根据项目信息生成项目规则文件，复用 ECC 现有规则模板。
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class ProjectRulesGenerator:
    """项目规则生成器"""

    def __init__(self):
        self.script_dir = Path(__file__).parent.parent
        self.config = self._load_config()
        self.templates_dir = self.script_dir / self.config['templates_dir']
        self.ecc_rules_dir = Path(self.config['ecc_rules_dir'])

    def _load_config(self) -> dict:
        """加载配置文件"""
        config_file = self.script_dir / 'config.json'
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_language_template(self, language: str) -> str:
        """加载语言特定模板"""
        template_file = self.templates_dir / f"{language}.md"
        if template_file.exists():
            return template_file.read_text(encoding='utf-8')
        return ""

    def load_ecc_rules(self) -> Dict[str, str]:
        """加载 ECC 现有规则"""
        rules = {}
        if not self.ecc_rules_dir.exists():
            return rules

        for rule_file in self.ecc_rules_dir.glob("*.md"):
            rule_name = rule_file.stem
            if rule_name in self.config['rule_sections']:
                rules[rule_name] = rule_file.read_text(encoding='utf-8')

        return rules

    def generate_header(self, project_info: dict) -> str:
        """生成规则文件头部"""
        tech_stack_str = ', '.join(project_info.get('tech_stack', []))

        header = f"""# {project_info['name']} 项目规则

## 版本信息

- **版本**：1.0.0
- **创建时间**：{datetime.now().strftime('%Y-%m-%d')}
- **项目类型**：{project_info.get('type', 'N/A')}
- **编程语言**：{project_info.get('language', 'N/A')}
- **技术栈**：{tech_stack_str or 'N/A'}
- **架构设计**：{project_info.get('architecture', 'N/A')}
- **团队规模**：{project_info.get('team_size', 'N/A')}

## 规则说明

本规则文件由 Everything Claude Code 的 `create-project-rules` 技能自动生成。

规则分为两部分：
1. **语言特定规范** - 针对 {project_info.get('language', 'N/A')} 的最佳实践
2. **通用规则** - 继承自 ECC 的核心规则

---

"""
        return header

    def generate_language_section(self, language: str) -> str:
        """生成语言特定规范部分"""
        template = self.load_language_template(language.lower())

        if not template:
            return f"""## 语言特定规范

暂无 {language} 的特定规范模板。

请参考以下资源：
- 官方文档
- 社区最佳实践
- 团队约定

"""

        return template + "\n\n---\n\n"

    def generate_ecc_rules_section(self, ecc_rules: Dict[str, str]) -> str:
        """生成 ECC 通用规则部分"""
        if not ecc_rules:
            return """## 通用规则

暂无 ECC 通用规则。请手动添加项目规则。

"""

        section = "## 通用规则（继承自 ECC）\n\n"
        section += "以下规则继承自 Everything Claude Code 的核心规则，适用于所有项目。\n\n"
        section += "---\n\n"

        # 按优先级排序规则
        priority_order = [
            'coding-style',
            'testing',
            'git-workflow',
            'security',
            'performance',
            'patterns',
            'hooks',
            'agents'
        ]

        for rule_name in priority_order:
            if rule_name in ecc_rules:
                section += ecc_rules[rule_name] + "\n\n---\n\n"

        return section

    def generate_footer(self) -> str:
        """生成规则文件尾部"""
        footer = f"""## 规则维护

### 更新规则

当项目需求变化时，请更新本规则文件：

1. 修改对应章节的内容
2. 更新版本号
3. 记录变更日志
4. 通知团队成员

### 规则执行

- 代码审查时参考本规则
- 使用 ECC 的智能体自动检查规则遵循情况
- 定期回顾和优化规则

### 相关命令

- `/code-review` - 代码审查
- `/security-review` - 安全审查
- `/tdd` - 测试驱动开发

---

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**生成工具**：Everything Claude Code - create-project-rules
"""
        return footer

    def generate(self, project_info: dict) -> str:
        """生成完整的项目规则文件"""
        # 1. 生成头部
        content = self.generate_header(project_info)

        # 2. 生成语言特定规范
        language = project_info.get('language', '').lower()
        if language:
            content += self.generate_language_section(language)

        # 3. 生成 ECC 通用规则
        ecc_rules = self.load_ecc_rules()
        content += self.generate_ecc_rules_section(ecc_rules)

        # 4. 生成尾部
        content += self.generate_footer()

        return content

    def save(self, content: str, output_path: Optional[Path] = None) -> Path:
        """保存规则文件"""
        if output_path is None:
            output_path = Path(self.config['output_dir']) / 'project-rules.md'

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')

        return output_path


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("Usage: python generate-rules.py '<project_info_json>'")
        print("\nExample:")
        print('python generate-rules.py \'{"name": "my-app", "language": "typescript", "type": "web-application"}\'')
        sys.exit(1)

    try:
        # 解析项目信息
        project_info = json.loads(sys.argv[1])

        # 验证必需字段
        required_fields = ['name', 'language']
        for field in required_fields:
            if field not in project_info:
                print(f"Error: Missing required field '{field}'")
                sys.exit(1)

        # 生成规则
        generator = ProjectRulesGenerator()
        content = generator.generate(project_info)

        # 保存规则
        output_path = generator.save(content)

        print(f"✅ 项目规则已生成：{output_path}")
        print(f"\n项目信息：")
        print(f"  - 名称：{project_info['name']}")
        print(f"  - 语言：{project_info['language']}")
        print(f"  - 类型：{project_info.get('type', 'N/A')}")

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
