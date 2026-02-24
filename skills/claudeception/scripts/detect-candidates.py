#!/usr/bin/env python3
"""
Skill Extraction Candidate Detector

检测 observations.jsonl 中的技能提取候选信号，
写入候选文件供 Claudeception 使用。

这是 v3 与 Claudeception 的松耦合桥接组件。
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def load_config() -> Dict:
    """加载 v3 配置"""
    config_file = Path(__file__).parent.parent / 'config.json'
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_observations(store_path: str, limit: int = 200) -> List[Dict]:
    """
    加载最近的观测数据

    Args:
        store_path: observations.jsonl 路径
        limit: 最多读取的行数

    Returns:
        观测数据列表
    """
    path = Path(store_path).expanduser()
    if not path.exists():
        return []

    observations = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                observations.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    return observations[-limit:]


def detect_error_fix_cycle(observations: List[Dict]) -> Optional[Dict]:
    """
    检测错误-修复循环模式

    信号：同一会话中出现多次错误后成功修复
    """
    error_count = 0
    error_tools = []
    last_session = None

    for obs in observations:
        session = obs.get('session', '')
        if last_session and session != last_session:
            error_count = 0
            error_tools = []
        last_session = session

        output = obs.get('output', '')
        if isinstance(output, str) and obs.get('event') == 'tool_complete':
            error_keywords = ['error', 'Error', 'ERROR', 'failed', 'Failed',
                              'FAILED', 'exception', 'Exception', 'traceback',
                              'TypeError', 'SyntaxError', 'ReferenceError']
            if any(kw in output for kw in error_keywords):
                error_count += 1
                error_tools.append(obs.get('tool', 'unknown'))
            elif error_count >= 3:
                strength = min(0.5 + error_count * 0.1, 0.95)
                return {
                    'signal_type': 'error_fix_cycle',
                    'signal_strength': round(strength, 2),
                    'error_count': error_count,
                    'tools_involved': list(set(error_tools)),
                    'session': session
                }

    return None


def detect_long_investigation(observations: List[Dict]) -> Optional[Dict]:
    """
    检测长时间调查模式

    信号：围绕同一文件/模块的密集工具调用 > 10 次
    """
    file_access_count: Dict[str, int] = {}

    for obs in observations:
        input_data = obs.get('input', '')
        if isinstance(input_data, str):
            for segment in input_data.split():
                if '/' in segment and ('.' in segment.split('/')[-1]):
                    file_path = segment.strip('"').strip("'")
                    file_access_count[file_path] = file_access_count.get(file_path, 0) + 1

    hot_files = {f: c for f, c in file_access_count.items() if c >= 10}
    if hot_files:
        max_file = max(hot_files, key=hot_files.get)
        strength = min(0.5 + hot_files[max_file] * 0.03, 0.95)
        return {
            'signal_type': 'long_investigation',
            'signal_strength': round(strength, 2),
            'hot_files': hot_files,
            'primary_file': max_file
        }

    return None


def detect_non_standard_solution(observations: List[Dict]) -> Optional[Dict]:
    """
    检测非标准解决方案模式

    信号：编辑方向发生转变（先编辑 A 失败，转向编辑 B 成功）
    """
    edit_targets = []

    for obs in observations:
        if obs.get('tool') == 'Edit' and obs.get('event') == 'tool_start':
            input_data = obs.get('input', '')
            if isinstance(input_data, str) and '/' in input_data:
                edit_targets.append(input_data.split()[0] if input_data.split() else '')

    if len(edit_targets) >= 5:
        unique_dirs = set()
        for target in edit_targets:
            parts = target.split('/')
            if len(parts) >= 2:
                unique_dirs.add('/'.join(parts[:-1]))

        if len(unique_dirs) >= 3:
            return {
                'signal_type': 'non_standard_solution',
                'signal_strength': 0.7,
                'edit_targets': edit_targets[-10:],
                'unique_directories': list(unique_dirs)
            }

    return None


def write_candidate(candidate: Dict, candidates_path: str) -> str:
    """
    写入候选文件

    Args:
        candidate: 候选数据
        candidates_path: 候选目录路径

    Returns:
        写入的文件路径
    """
    path = Path(candidates_path).expanduser()
    path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    filename = f"candidate-{timestamp}.json"
    filepath = path / filename

    candidate['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    candidate['suggestion'] = '建议运行 /claudeception 提取为完整技能'

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(candidate, f, ensure_ascii=False, indent=2)

    return str(filepath)


def main():
    """主函数"""
    config = load_config()

    claudeception_config = config.get('claudeception', {})
    if not claudeception_config.get('enabled', False):
        print('Claudeception 桥接未启用，跳过检测')
        return

    min_strength = claudeception_config.get('min_signal_strength', 0.6)
    candidates_path = claudeception_config.get(
        'candidates_path',
        '~/.claude/homunculus/skill-candidates/'
    )

    store_path = config.get('observation', {}).get(
        'store_path',
        '~/.claude/homunculus/observations.jsonl'
    )

    observations = load_observations(store_path)
    if not observations:
        print('无观测数据')
        return

    detectors = [
        detect_error_fix_cycle,
        detect_long_investigation,
        detect_non_standard_solution,
    ]

    candidates_found = 0
    for detector in detectors:
        result = detector(observations)
        if result and result.get('signal_strength', 0) >= min_strength:
            filepath = write_candidate(result, candidates_path)
            candidates_found += 1
            print(f'检测到候选信号: {result["signal_type"]} '
                  f'(强度: {result["signal_strength"]}) → {filepath}')

            if result['signal_strength'] >= claudeception_config.get('auto_remind_threshold', 0.8):
                print(f'\n⚡ 强信号检测！建议立即运行 /claudeception 提取技能')

    if candidates_found == 0:
        print('未检测到技能提取候选信号')
    else:
        print(f'\n共检测到 {candidates_found} 个候选信号')


if __name__ == '__main__':
    main()
