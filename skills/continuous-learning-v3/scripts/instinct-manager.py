#!/usr/bin/env python3
"""
Instinct Manager for Code Navigation

管理代码导航 Instincts:
- 更新置信度
- 添加同义词
- 应用衰减规则
- 项目级隔离
"""

import json
import os
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


def load_config() -> Dict:
    """加载配置"""
    config_file = Path(__file__).parent.parent / 'config.json'
    with open(config_file, 'r') as f:
        return json.load(f)


def load_all_instincts(instincts_dir: Path, domain: str = None) -> List[Dict]:
    """
    加载所有 Instincts

    Args:
        instincts_dir: Instincts 目录
        domain: 过滤领域(可选)

    Returns:
        Instinct 列表
    """
    instincts = []

    for yaml_file in instincts_dir.glob('*.yaml'):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 分离 frontmatter 和 body
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue

            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()

            # 过滤领域
            if domain and frontmatter.get('domain') != domain:
                continue

            instincts.append({
                'frontmatter': frontmatter,
                'body': body,
                'file_path': yaml_file
            })
        except Exception as e:
            print(f"Error loading {yaml_file}: {e}")
            continue

    return instincts


def apply_confidence_decay(instincts: List[Dict], config: Dict) -> int:
    """
    应用置信度衰减规则

    Args:
        instincts: Instinct 列表
        config: 配置

    Returns:
        更新的 Instinct 数量
    """
    decay_rules = config['code-navigation']['confidence_decay']
    now = datetime.now()
    updated_count = 0

    for instinct in instincts:
        frontmatter = instinct['frontmatter']

        # 跳过非 code-navigation 领域
        if frontmatter.get('domain') != 'code-navigation':
            continue

        # 获取最后使用时间
        last_used_str = frontmatter.get('last_used')
        if not last_used_str:
            continue

        try:
            last_used = datetime.fromisoformat(last_used_str.replace('Z', '+00:00'))
        except:
            continue

        days_unused = (now - last_used).days

        # 应用衰减规则
        current_confidence = frontmatter.get('confidence', 0.5)
        new_confidence = current_confidence

        if days_unused >= 90:
            # 标记为 stale
            frontmatter['status'] = 'stale'
            updated_count += 1
        elif days_unused >= 60:
            new_confidence = max(0.1, current_confidence + decay_rules['60_days_unused'])
            if new_confidence != current_confidence:
                frontmatter['confidence'] = new_confidence
                updated_count += 1
        elif days_unused >= 30:
            new_confidence = max(0.1, current_confidence + decay_rules['30_days_unused'])
            if new_confidence != current_confidence:
                frontmatter['confidence'] = new_confidence
                updated_count += 1

        # 写回文件
        if updated_count > 0:
            with open(instinct['file_path'], 'w', encoding='utf-8') as f:
                f.write('---\n')
                yaml.dump(frontmatter, f, allow_unicode=True, default_flow_style=False)
                f.write('---\n\n')
                f.write(instinct['body'])

    return updated_count


def get_project_instincts(instincts: List[Dict], project_name: str) -> List[Dict]:
    """
    获取特定项目的 Instincts

    Args:
        instincts: Instinct 列表
        project_name: 项目名称

    Returns:
        过滤后的 Instinct 列表
    """
    return [
        inst for inst in instincts
        if inst['frontmatter'].get('project') == project_name
    ]


def cleanup_low_confidence(instincts: List[Dict], threshold: float = 0.3) -> int:
    """
    清理低置信度 Instincts

    Args:
        instincts: Instinct 列表
        threshold: 置信度阈值

    Returns:
        删除的 Instinct 数量
    """
    deleted_count = 0

    for instinct in instincts:
        frontmatter = instinct['frontmatter']

        # 跳过非 code-navigation 领域
        if frontmatter.get('domain') != 'code-navigation':
            continue

        # 检查置信度
        confidence = frontmatter.get('confidence', 0.5)
        if confidence < threshold:
            try:
                os.remove(instinct['file_path'])
                deleted_count += 1
            except Exception as e:
                print(f"Error deleting {instinct['file_path']}: {e}")

    return deleted_count


def get_statistics(instincts: List[Dict]) -> Dict:
    """
    获取统计信息

    Args:
        instincts: Instinct 列表

    Returns:
        统计字典
    """
    code_nav_instincts = [
        inst for inst in instincts
        if inst['frontmatter'].get('domain') == 'code-navigation'
    ]

    # 按项目分组
    projects = {}
    for inst in code_nav_instincts:
        project = inst['frontmatter'].get('project', 'unknown')
        if project not in projects:
            projects[project] = []
        projects[project].append(inst)

    # 计算统计
    stats = {
        'total': len(code_nav_instincts),
        'projects': len(projects),
        'by_project': {}
    }

    for project, insts in projects.items():
        avg_confidence = sum(
            inst['frontmatter'].get('confidence', 0)
            for inst in insts
        ) / len(insts) if insts else 0

        stats['by_project'][project] = {
            'count': len(insts),
            'avg_confidence': round(avg_confidence, 2)
        }

    return stats


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='Manage code navigation instincts')
    parser.add_argument('command', choices=['decay', 'cleanup', 'stats'],
                        help='Command to execute')
    parser.add_argument('--threshold', type=float, default=0.3,
                        help='Confidence threshold for cleanup')

    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # Instincts 目录
    instincts_dir = Path.home() / '.claude' / 'homunculus' / 'instincts' / 'personal'
    if not instincts_dir.exists():
        print("No instincts directory found")
        return

    # 加载所有 Instincts
    instincts = load_all_instincts(instincts_dir)

    if args.command == 'decay':
        # 应用衰减规则
        updated = apply_confidence_decay(instincts, config)
        print(f"Applied decay to {updated} instincts")

    elif args.command == 'cleanup':
        # 清理低置信度
        deleted = cleanup_low_confidence(instincts, args.threshold)
        print(f"Deleted {deleted} low-confidence instincts")

    elif args.command == 'stats':
        # 显示统计
        stats = get_statistics(instincts)
        print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
