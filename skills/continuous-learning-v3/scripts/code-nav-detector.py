#!/usr/bin/env python3
"""
Code Navigation Pattern Detector

检测用户的代码导航模式:
1. 识别自然语言查询意图
2. 追踪后续工具调用序列
3. 检测隐式确认(Grep → Read → Edit)
"""

import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


# 代码查找意图关键词
CODE_SEARCH_KEYWORDS = [
    # 中文
    "我想修改", "找到", "查找", "在哪", "哪里", "定位", "搜索",
    "看看", "检查", "查看", "打开", "编辑", "更改",
    # 英文
    "find", "locate", "where", "search", "look for", "show me",
    "open", "edit", "modify", "change", "update"
]


def extract_keywords(query: str) -> List[str]:
    """
    从自然语言查询中提取关键词

    Args:
        query: 用户查询字符串

    Returns:
        关键词列表
    """
    # 移除常见停用词
    stopwords = {
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个",
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "should",
        "can", "could", "may", "might", "must", "i", "you", "he", "she", "it",
        "we", "they", "this", "that", "these", "those"
    }

    # 分词(简单实现)
    words = re.findall(r'\w+', query.lower())

    # 过滤停用词和短词
    keywords = [w for w in words if w not in stopwords and len(w) > 1]

    return keywords[:5]  # 最多返回5个关键词


def is_code_search_query(query: str) -> bool:
    """
    判断是否为代码查找查询

    Args:
        query: 用户查询字符串

    Returns:
        是否为代码查找查询
    """
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in CODE_SEARCH_KEYWORDS)


def get_subsequent_tools(
    observations: List[Dict],
    query_index: int,
    window_minutes: int = 5
) -> List[Dict]:
    """
    获取查询后续的工具调用

    Args:
        observations: 观测列表
        query_index: 查询在列表中的索引
        window_minutes: 时间窗口(分钟)

    Returns:
        后续工具调用列表
    """
    if query_index >= len(observations):
        return []

    query_time = datetime.fromisoformat(
        observations[query_index]['timestamp'].replace('Z', '+00:00')
    )
    window_end = query_time + timedelta(minutes=window_minutes)

    subsequent = []
    for obs in observations[query_index + 1:]:
        obs_time = datetime.fromisoformat(
            obs['timestamp'].replace('Z', '+00:00')
        )
        if obs_time > window_end:
            break
        subsequent.append(obs)

    return subsequent


def is_grep_read_edit_sequence(tools: List[Dict]) -> Tuple[bool, Optional[Dict]]:
    """
    检测是否为 Grep → Read → Edit 序列

    Args:
        tools: 工具调用列表

    Returns:
        (是否匹配, 代码位置信息)
    """
    # 查找序列
    grep_idx = None
    read_idx = None
    edit_idx = None

    for i, tool in enumerate(tools):
        tool_name = tool.get('tool', '').lower()

        if 'grep' in tool_name and grep_idx is None:
            grep_idx = i
        elif 'read' in tool_name and grep_idx is not None and read_idx is None:
            read_idx = i
        elif 'edit' in tool_name and read_idx is not None and edit_idx is None:
            edit_idx = i
            break

    # 检查是否找到完整序列
    if grep_idx is not None and read_idx is not None and edit_idx is not None:
        # 提取代码位置
        read_tool = tools[read_idx]
        edit_tool = tools[edit_idx]

        # 从 Read 工具获取文件路径
        file_path = None
        if 'input' in read_tool:
            try:
                input_data = json.loads(read_tool['input']) if isinstance(read_tool['input'], str) else read_tool['input']
                file_path = input_data.get('file_path')
            except:
                pass

        # 从 Edit 工具获取编辑位置
        function_name = None
        if 'input' in edit_tool:
            try:
                input_data = json.loads(edit_tool['input']) if isinstance(edit_tool['input'], str) else edit_tool['input']
                old_string = input_data.get('old_string', '')
                # 尝试提取函数名
                func_match = re.search(r'function\s+(\w+)|def\s+(\w+)|(\w+)\s*\(', old_string)
                if func_match:
                    function_name = next(g for g in func_match.groups() if g)
            except:
                pass

        if file_path:
            return True, {
                'file_path': file_path,
                'function_name': function_name,
                'confirmation_method': 'implicit'
            }

    return False, None


def detect_code_navigation_pattern(observations: List[Dict]) -> List[Dict]:
    """
    检测代码导航模式

    Args:
        observations: 观测列表

    Returns:
        检测到的模式列表
    """
    patterns = []

    for i, obs in enumerate(observations):
        # 跳过非用户查询事件
        if obs.get('event') != 'user_query':
            continue

        query = obs.get('query', '')

        # 检查是否为代码查找查询
        if not is_code_search_query(query):
            continue

        # 提取关键词
        keywords = extract_keywords(query)
        if not keywords:
            continue

        # 获取后续工具调用
        subsequent_tools = get_subsequent_tools(observations, i)

        # 检测 Grep → Read → Edit 序列
        is_sequence, code_location = is_grep_read_edit_sequence(subsequent_tools)

        if is_sequence and code_location:
            patterns.append({
                'natural_language': query,
                'keywords': keywords,
                'code_location': code_location,
                'timestamp': obs['timestamp'],
                'session': obs.get('session', 'unknown'),
                'confidence': 0.5  # 隐式确认的初始置信度
            })

    return patterns


def main():
    """主函数"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: code-nav-detector.py <observations.jsonl>")
        sys.exit(1)

    observations_file = sys.argv[1]

    # 读取观测数据
    observations = []
    with open(observations_file, 'r') as f:
        for line in f:
            if line.strip():
                observations.append(json.loads(line))

    # 检测模式
    patterns = detect_code_navigation_pattern(observations)

    # 输出结果
    print(json.dumps(patterns, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
