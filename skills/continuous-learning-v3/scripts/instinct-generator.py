#!/usr/bin/env python3
"""
Instinct Generator for Code Navigation

生成和更新代码导航 Instincts
"""

import json
import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def slugify(text: str) -> str:
    """
    将文本转换为 slug 格式

    Args:
        text: 输入文本

    Returns:
        slug 字符串
    """
    # 转小写
    text = text.lower()
    # 移除特殊字符
    text = re.sub(r'[^\w\s-]', '', text)
    # 空格转连字符
    text = re.sub(r'[\s_]+', '-', text)
    # 移除多余连字符
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def get_project_name() -> str:
    """
    获取当前项目名称

    Returns:
        项目名称
    """
    try:
        # 尝试从 git 获取
        import subprocess
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            check=True
        )
        project_path = result.stdout.strip()
        return os.path.basename(project_path)
    except:
        # 回退到当前目录名
        return os.path.basename(os.getcwd())


def get_git_commit() -> str:
    """
    获取当前 git commit

    Returns:
        commit hash
    """
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except:
        return 'unknown'


def load_existing_instinct(instinct_id: str, instincts_dir: Path) -> Optional[Dict]:
    """
    加载已存在的 Instinct

    Args:
        instinct_id: Instinct ID
        instincts_dir: Instincts 目录

    Returns:
        Instinct 数据或 None
    """
    instinct_file = instincts_dir / f"{instinct_id}.yaml"
    if not instinct_file.exists():
        return None

    with open(instinct_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 分离 frontmatter 和 body
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    frontmatter = yaml.safe_load(parts[1])
    body = parts[2].strip()

    return {
        'frontmatter': frontmatter,
        'body': body,
        'file_path': instinct_file
    }


def extract_synonyms(body: str) -> List[str]:
    """
    从 Instinct body 中提取同义词

    Args:
        body: Instinct body 文本

    Returns:
        同义词列表
    """
    synonyms = []
    in_synonyms_section = False

    for line in body.split('\n'):
        if '## Synonyms' in line:
            in_synonyms_section = True
            continue
        if in_synonyms_section:
            if line.startswith('##'):
                break
            if line.strip().startswith('-'):
                synonym = line.strip()[1:].strip()
                if synonym:
                    synonyms.append(synonym)

    return synonyms


def update_instinct_body(body: str, updates: Dict) -> str:
    """
    更新 Instinct body

    Args:
        body: 原始 body
        updates: 更新字典

    Returns:
        更新后的 body
    """
    lines = body.split('\n')
    new_lines = []
    in_evidence_section = False
    in_synonyms_section = False

    for line in lines:
        if '## Evidence' in line:
            in_evidence_section = True
            in_synonyms_section = False
            new_lines.append(line)
            continue

        if '## Synonyms' in line:
            in_synonyms_section = True
            in_evidence_section = False
            new_lines.append(line)
            # 添加更新的同义词
            if 'synonyms' in updates:
                for synonym in updates['synonyms']:
                    new_lines.append(f"- {synonym}")
            continue

        if line.startswith('##'):
            in_evidence_section = False
            in_synonyms_section = False

        if in_evidence_section and 'evidence' in updates:
            # 跳过旧的 evidence 行
            if line.strip().startswith('-'):
                continue
            # 添加新的 evidence
            if line.strip() == '':
                for evidence_line in updates['evidence']:
                    new_lines.append(f"- {evidence_line}")
                new_lines.append(line)
                in_evidence_section = False
                continue

        if in_synonyms_section and line.strip().startswith('-'):
            # 跳过旧的同义词(已在上面添加)
            continue

        new_lines.append(line)

    return '\n'.join(new_lines)


def create_code_navigation_instinct(
    pattern: Dict,
    instincts_dir: Path,
    config: Dict
) -> str:
    """
    创建或更新代码导航 Instinct

    Args:
        pattern: 检测到的模式
        instincts_dir: Instincts 目录
        config: 配置

    Returns:
        Instinct ID
    """
    # 生成 ID
    keywords = pattern['keywords']
    keyword_slug = slugify('-'.join(keywords[:2]))  # 使用前2个关键词
    instinct_id = f"code-nav-{keyword_slug}"

    # 检查是否已存在
    existing = load_existing_instinct(instinct_id, instincts_dir)

    project_name = get_project_name()
    git_commit = get_git_commit()
    natural_language = pattern['natural_language']
    code_location = pattern['code_location']
    timestamp = pattern['timestamp']

    if existing:
        # 更新已存在的 Instinct
        frontmatter = existing['frontmatter']
        body = existing['body']

        # 增加置信度
        current_confidence = frontmatter.get('confidence', 0.5)
        growth = config['code-navigation']['confidence_growth']['implicit_confirmation']
        new_confidence = min(
            current_confidence + growth,
            config['code-navigation']['confidence_max']
        )
        frontmatter['confidence'] = new_confidence

        # 提取现有同义词
        existing_synonyms = extract_synonyms(body)

        # 添加新同义词(如果不同)
        if natural_language not in existing_synonyms:
            existing_synonyms.append(natural_language)

        # 限制同义词数量
        max_synonyms = config['code-navigation']['max_synonyms_per_mapping']
        existing_synonyms = existing_synonyms[:max_synonyms]

        # 更新 evidence
        evidence_lines = [
            f"User confirmed this mapping on {timestamp}",
            f"Usage count: {frontmatter.get('usage_count', 0) + 1}",
            f"Last used: {timestamp}",
            f"Confirmation method: {code_location['confirmation_method']}"
        ]

        frontmatter['usage_count'] = frontmatter.get('usage_count', 0) + 1
        frontmatter['last_used'] = timestamp

        # 更新 body
        body = update_instinct_body(body, {
            'synonyms': existing_synonyms,
            'evidence': evidence_lines
        })

        # 写入文件
        with open(existing['file_path'], 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
            f.write('---\n\n')
            f.write(body)

        return instinct_id

    else:
        # 创建新 Instinct
        file_path = code_location['file_path']
        function_name = code_location.get('function_name', 'unknown')
        line_number = code_location.get('line_number', 'unknown')

        frontmatter = {
            'id': instinct_id,
            'trigger': f"when user says '{natural_language}' or similar phrases",
            'domain': 'code-navigation',
            'subtype': 'semantic-mapping',
            'confidence': pattern['confidence'],
            'source': 'session-observation',
            'project': project_name,
            'usage_count': 1,
            'last_used': timestamp
        }

        body = f"""# 代码导航：{natural_language}

## Action
Navigate to: {file_path}:{function_name}()

## Context
- File: {file_path}
- Function: {function_name}
- Line: {line_number}

## Synonyms
- {natural_language}

## Evidence
- User confirmed this mapping on {timestamp}
- Usage count: 1
- Last used: {timestamp}
- Confirmation method: {code_location['confirmation_method']}

## Metadata
- Project: {project_name}
- Codebase version: {git_commit}
"""

        # 写入文件
        instinct_file = instincts_dir / f"{instinct_id}.yaml"
        with open(instinct_file, 'w', encoding='utf-8') as f:
            f.write('---\n')
            yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
            f.write('---\n\n')
            f.write(body)

        return instinct_id


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: instinct-generator.py <patterns.json>")
        sys.exit(1)

    patterns_file = sys.argv[1]

    # 读取模式
    with open(patterns_file, 'r') as f:
        patterns = json.load(f)

    # 读取配置
    config_file = Path(__file__).parent.parent / 'config.json'
    with open(config_file, 'r') as f:
        config = json.load(f)

    # Instincts 目录
    instincts_dir = Path.home() / '.claude' / 'homunculus' / 'instincts' / 'personal'
    instincts_dir.mkdir(parents=True, exist_ok=True)

    # 生成 Instincts
    created_ids = []
    for pattern in patterns:
        instinct_id = create_code_navigation_instinct(pattern, instincts_dir, config)
        created_ids.append(instinct_id)

    print(json.dumps({
        'created': len(created_ids),
        'ids': created_ids
    }, indent=2))


if __name__ == '__main__':
    main()
