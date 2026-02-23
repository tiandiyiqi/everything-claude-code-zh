#!/usr/bin/env python3
"""
Expressions View Generator - Generate a markdown table view of communication instincts.

Reads communication-domain instincts from ~/.claude/homunculus/instincts/
and generates a formatted expressions table at ~/.claude/homunculus/views/expressions.md
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

HOMUNCULUS_DIR = Path.home() / ".claude" / "homunculus"
INSTINCTS_DIR = HOMUNCULUS_DIR / "instincts"
VIEWS_DIR = HOMUNCULUS_DIR / "views"

SUBTYPE_LABELS = {
    "terminology": "术语",
    "phrasing": "句式",
    "project-concept": "项目概念",
}


def parse_instinct_file(content: str) -> list[dict]:
    """Parse YAML-like instinct file format."""
    instincts = []
    current = {}
    in_frontmatter = False
    content_lines = []

    for line in content.split('\n'):
        if line.strip() == '---':
            if in_frontmatter:
                in_frontmatter = False
                if current:
                    current['content'] = '\n'.join(content_lines).strip()
                    instincts.append(current)
                    current = {}
                    content_lines = []
            else:
                in_frontmatter = True
                if current:
                    current['content'] = '\n'.join(content_lines).strip()
                    instincts.append(current)
                current = {}
                content_lines = []
        elif in_frontmatter:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == 'confidence':
                    current[key] = float(value)
                else:
                    current[key] = value
        else:
            content_lines.append(line)

    if current:
        current['content'] = '\n'.join(content_lines).strip()
        instincts.append(current)

    return [i for i in instincts if i.get('id')]


def load_communication_instincts() -> list[dict]:
    """Load all communication-domain instincts."""
    instincts = []

    for directory in [INSTINCTS_DIR / "personal", INSTINCTS_DIR / "inherited"]:
        if not directory.exists():
            continue
        for file in directory.glob("*.yaml"):
            try:
                content = file.read_text()
                parsed = parse_instinct_file(content)
                for inst in parsed:
                    if inst.get('domain') == 'communication':
                        inst['_source_file'] = str(file)
                        instincts.append(inst)
            except Exception as e:
                print(f"Warning: Failed to parse {file}: {e}", file=sys.stderr)

    return instincts


def extract_expression_pair(inst: dict) -> tuple[str, str]:
    """Extract user_term and standard_term from instinct content."""
    content = inst.get('content', '')
    trigger = inst.get('trigger', '')

    # Try to extract from Action section
    action_match = re.search(
        r"Use '(.+?)' instead of '(.+?)'", content
    )
    if action_match:
        return action_match.group(1), action_match.group(2)

    # Try to extract from trigger
    trigger_match = re.search(
        r"when (?:communicating about|user says) '(.+?)'", trigger
    )
    if trigger_match:
        return trigger_match.group(1), ""

    # Fallback: use id
    inst_id = inst.get('id', 'unknown')
    term = inst_id.replace('comm-', '').replace('prefer-term-', '').replace('-', ' ')
    return term, ""


def generate_view(instincts: list[dict]) -> str:
    """Generate markdown table view."""
    lines = [
        "# 表达库（自动生成）",
        "",
        f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> 共 {len(instincts)} 条表达记录",
        "",
        "| 类型 | 你的表达 | 标准/替代表达 | 置信度 | 来源 |",
        "|------|---------|-------------|--------|------|",
    ]

    sorted_instincts = sorted(
        instincts,
        key=lambda x: (-x.get('confidence', 0.5), x.get('subtype', ''))
    )

    for inst in sorted_instincts:
        subtype = inst.get('subtype', 'terminology')
        type_label = SUBTYPE_LABELS.get(subtype, subtype)
        user_term, standard_term = extract_expression_pair(inst)
        confidence = int(inst.get('confidence', 0.5) * 100)
        source = inst.get('source', 'unknown')

        lines.append(
            f"| {type_label} | {user_term} | {standard_term} | {confidence}% | {source} |"
        )

    lines.append("")
    return '\n'.join(lines)


def main():
    instincts = load_communication_instincts()

    if not instincts:
        print("No communication instincts found.")
        print(f"Instinct directories searched:")
        print(f"  {INSTINCTS_DIR / 'personal'}")
        print(f"  {INSTINCTS_DIR / 'inherited'}")
        return 0

    VIEWS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = VIEWS_DIR / "expressions.md"

    view_content = generate_view(instincts)
    output_path.write_text(view_content)

    print(f"Generated expressions view: {output_path}")
    print(f"Total communication instincts: {len(instincts)}")

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
