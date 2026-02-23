#!/usr/bin/env python3
"""
Growth Report Generator - Generate personal growth reports from continuous learning data.

Aggregates data from:
- Session files (~/.claude/sessions/*.tmp)
- Learned Skills (~/.claude/skills/learned/*.md)
- Instincts (~/.claude/homunculus/instincts/personal/*.yaml)
- File-Memory (.claude/plans/*/progress.md, task_plan.md)

Usage:
  growth-report.py [days]              # Default 7 days
  growth-report.py 14                  # Last 14 days
  growth-report.py 30 --save report.md # Save to file
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

SESSIONS_DIR = Path.home() / ".claude" / "sessions"
LEARNED_SKILLS_DIR = Path.home() / ".claude" / "skills" / "learned"
INSTINCTS_DIR = Path.home() / ".claude" / "homunculus" / "instincts" / "personal"


# ─────────────────────────────────────────────
# Core Generator Class
# ─────────────────────────────────────────────

class GrowthReportGenerator:
    def __init__(self, days: int = 7):
        self.days = days
        self.cutoff_date = datetime.now() - timedelta(days=days)

    def _is_recent(self, file_path: Path) -> bool:
        """Check if file was modified within the time window."""
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            return mtime >= self.cutoff_date
        except Exception:
            return False

    # ─────────────────────────────────────────────
    # Work Overview Extraction
    # ─────────────────────────────────────────────

    def _parse_session_file(self, file_path: Path) -> Optional[Dict]:
        """Parse a session file to extract metadata."""
        try:
            content = file_path.read_text()

            # Extract date from filename: YYYY-MM-DD-project-session.tmp
            filename = file_path.stem
            date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
            date = date_match.group(1) if date_match else "unknown"

            # Extract project from filename
            project = filename.replace(date + "-", "").replace("-session", "") if date != "unknown" else "unknown"

            # Extract tasks from content
            tasks = []
            tasks_section = re.search(r'### Tasks\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
            if tasks_section:
                task_lines = tasks_section.group(1).strip().split('\n')
                tasks = [line.strip('- ').strip() for line in task_lines if line.strip().startswith('-')]

            # Extract tools from content
            tools = []
            tools_section = re.search(r'### Tools Used\s*\n(.*?)(?=\n###|\Z)', content, re.DOTALL)
            if tools_section:
                tools_text = tools_section.group(1).strip()
                tools = [t.strip() for t in tools_text.split(',') if t.strip()]

            return {
                'date': date,
                'project': project,
                'tasks': tasks,
                'tools': tools,
                'file': str(file_path)
            }
        except Exception as e:
            print(f"Warning: Failed to parse session file {file_path}: {e}", file=sys.stderr)
            return None

    def extract_work_overview(self) -> Dict:
        """Extract work overview from session files."""
        if not SESSIONS_DIR.exists():
            return {
                'session_count': 0,
                'projects': [],
                'active_days': 0,
                'tasks': [],
                'tools': []
            }

        sessions = []
        for file in SESSIONS_DIR.glob("*.tmp"):
            if self._is_recent(file):
                parsed = self._parse_session_file(file)
                if parsed:
                    sessions.append(parsed)

        # Aggregate data
        projects = list(set(s['project'] for s in sessions if s['project'] != 'unknown'))
        active_days = len(set(s['date'] for s in sessions if s['date'] != 'unknown'))
        all_tasks = [task for s in sessions for task in s['tasks']]
        all_tools = [tool for s in sessions for tool in s['tools']]
        tool_counts = Counter(all_tools)

        return {
            'session_count': len(sessions),
            'projects': projects,
            'active_days': active_days,
            'tasks': all_tasks,
            'tools': list(tool_counts.keys()),
            'tool_counts': tool_counts
        }

    # ─────────────────────────────────────────────
    # Learned Patterns Extraction
    # ─────────────────────────────────────────────

    def _parse_learned_skill(self, file_path: Path) -> Optional[Dict]:
        """Parse a learned skill file."""
        try:
            content = file_path.read_text()

            # Extract title (first # heading)
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else file_path.stem

            # Extract date (look for both Chinese and English)
            date_match = re.search(r'\*\*(?:提取日期|Extracted):\*\*\s*(.+?)(?:\n|$)', content)
            date = date_match.group(1).strip() if date_match else "unknown"

            # Extract context (look for both Chinese and English)
            context_match = re.search(r'\*\*(?:上下文|Context):\*\*\s*(.+?)(?:\n\n|\n##|\Z)', content, re.DOTALL)
            context = context_match.group(1).strip() if context_match else ""

            return {
                'title': title,
                'date': date,
                'context': context[:200] + "..." if len(context) > 200 else context,
                'file': str(file_path)
            }
        except Exception as e:
            print(f"Warning: Failed to parse learned skill {file_path}: {e}", file=sys.stderr)
            return None

    def _parse_instinct_file(self, content: str) -> List[Dict]:
        """Parse YAML-like instinct file format (reused from instinct-cli.py)."""
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

    def _parse_instincts(self, file_path: Path) -> List[Dict]:
        """Parse instincts from a YAML file."""
        try:
            content = file_path.read_text()
            instincts = self._parse_instinct_file(content)
            # Filter high-confidence instincts (>=0.7)
            return [i for i in instincts if i.get('confidence', 0) >= 0.7]
        except Exception as e:
            print(f"Warning: Failed to parse instinct file {file_path}: {e}", file=sys.stderr)
            return []

    def extract_learned_patterns(self) -> List[Dict]:
        """Extract learned patterns from Learned Skills and Instincts."""
        patterns = []

        # Extract from Learned Skills
        if LEARNED_SKILLS_DIR.exists():
            for file in LEARNED_SKILLS_DIR.glob("*.md"):
                if self._is_recent(file):
                    parsed = self._parse_learned_skill(file)
                    if parsed:
                        parsed['type'] = 'skill'
                        patterns.append(parsed)

        # Extract from Instincts
        if INSTINCTS_DIR.exists():
            for file in INSTINCTS_DIR.glob("*.yaml"):
                if self._is_recent(file):
                    instincts = self._parse_instincts(file)
                    for inst in instincts:
                        patterns.append({
                            'type': 'instinct',
                            'title': inst.get('id', 'unknown'),
                            'trigger': inst.get('trigger', ''),
                            'confidence': inst.get('confidence', 0.5),
                            'domain': inst.get('domain', 'general'),
                            'file': str(file)
                        })

        return patterns

    # ─────────────────────────────────────────────
    # Recurring Challenges Extraction
    # ─────────────────────────────────────────────

    def _extract_errors_from_progress(self, file_path: Path) -> List[Dict]:
        """Extract errors from progress.md file."""
        try:
            content = file_path.read_text()
            errors = []

            # Look for error log table: ## 错误日志
            error_section = re.search(r'##\s*错误日志\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            if error_section:
                table_content = error_section.group(1)
                # Parse table rows: | 时间戳 | 错误 | 尝试次数 | 解决方案 |
                rows = re.findall(r'\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|', table_content)
                for row in rows:
                    if row[0].strip() and not row[0].strip().startswith('-'):
                        error_type = row[1].strip()
                        if error_type and error_type != '错误':
                            errors.append({
                                'error': error_type,
                                'attempts': row[2].strip(),
                                'solution': row[3].strip()
                            })

            return errors
        except Exception as e:
            print(f"Warning: Failed to parse progress file {file_path}: {e}", file=sys.stderr)
            return []

    def _extract_errors_from_plan(self, file_path: Path) -> List[Dict]:
        """Extract errors from task_plan.md file."""
        try:
            content = file_path.read_text()
            errors = []

            # Look for error record table
            error_section = re.search(r'##\s*错误记录\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            if error_section:
                table_content = error_section.group(1)
                rows = re.findall(r'\|([^|]+)\|([^|]+)\|([^|]+)\|', table_content)
                for row in rows:
                    if row[0].strip() and not row[0].strip().startswith('-'):
                        error_type = row[0].strip()
                        if error_type and error_type != '错误类型':
                            errors.append({
                                'error': error_type,
                                'count': row[1].strip(),
                                'solution': row[2].strip()
                            })

            return errors
        except Exception as e:
            print(f"Warning: Failed to parse plan file {file_path}: {e}", file=sys.stderr)
            return []

    def extract_recurring_challenges(self) -> List[Dict]:
        """Extract recurring challenges from File-Memory."""
        all_errors = []

        # Search for .claude/plans/*/progress.md and task_plan.md
        cwd = Path.cwd()
        plans_dir = cwd / ".claude" / "plans"

        if plans_dir.exists():
            for plan_dir in plans_dir.iterdir():
                if plan_dir.is_dir():
                    # Check progress.md
                    progress_file = plan_dir / "progress.md"
                    if progress_file.exists() and self._is_recent(progress_file):
                        all_errors.extend(self._extract_errors_from_progress(progress_file))

                    # Check task_plan.md
                    plan_file = plan_dir / "task_plan.md"
                    if plan_file.exists() and self._is_recent(plan_file):
                        all_errors.extend(self._extract_errors_from_plan(plan_file))

        # Aggregate errors by type
        error_counts = Counter(e['error'] for e in all_errors)

        # Return top errors
        return [
            {'error': error, 'count': count}
            for error, count in error_counts.most_common(10)
        ]

    # ─────────────────────────────────────────────
    # Improvement Suggestions
    # ─────────────────────────────────────────────

    def _map_error_to_suggestion(self, error_type: str, count: int) -> str:
        """Map error type to actionable suggestion (rule engine)."""
        error_lower = error_type.lower()

        # File-related errors
        if 'filenotfound' in error_lower or 'no such file' in error_lower:
            return "建议：在操作文件前先使用 Glob 或 ls 确认文件存在"

        # Timeout errors
        if 'timeout' in error_lower or 'timed out' in error_lower:
            return "建议：为长时间运行的操作添加重试逻辑或增加超时时间"

        # Import errors
        if 'import' in error_lower or 'module' in error_lower:
            return "建议：检查依赖是否已安装，考虑添加依赖检查脚本"

        # Syntax errors
        if 'syntax' in error_lower:
            return "建议：在提交前使用 linter 检查代码语法"

        # Permission errors
        if 'permission' in error_lower:
            return "建议：检查文件权限，使用 chmod 或 sudo 解决权限问题"

        # Network errors
        if 'network' in error_lower or 'connection' in error_lower:
            return "建议：添加网络错误重试机制，检查网络连接"

        # High frequency errors
        if count >= 3:
            return f"建议：{error_type} 出现 {count} 次，考虑创建专门的错误处理模式"

        # Generic suggestion
        return f"建议：分析 {error_type} 的根本原因，建立预防机制"

    def generate_improvement_suggestions(self, challenges: List[Dict]) -> List[str]:
        """Generate improvement suggestions based on challenges."""
        suggestions = []

        for challenge in challenges[:5]:  # Top 5 challenges
            error_type = challenge['error']
            count = challenge['count']
            suggestion = self._map_error_to_suggestion(error_type, count)
            suggestions.append(suggestion)

        return suggestions

    # ─────────────────────────────────────────────
    # Strengths Extraction
    # ─────────────────────────────────────────────

    def extract_strengths(self) -> List[Dict]:
        """Extract strengths from high-confidence instincts (>=0.8)."""
        strengths = []

        if not INSTINCTS_DIR.exists():
            return strengths

        for file in INSTINCTS_DIR.glob("*.yaml"):
            if self._is_recent(file):
                instincts = self._parse_instincts(file)
                for inst in instincts:
                    if inst.get('confidence', 0) >= 0.8:
                        strengths.append({
                            'pattern': inst.get('trigger', inst.get('id', 'unknown')),
                            'confidence': inst.get('confidence', 0.8),
                            'domain': inst.get('domain', 'general')
                        })

        return strengths

    # ─────────────────────────────────────────────
    # Report Generation
    # ─────────────────────────────────────────────

    def generate_report(self) -> str:
        """Generate the complete growth report."""
        lines = []

        # Header
        lines.append("=" * 60)
        lines.append(f"  成长报告 (Growth Report) - 近 {self.days} 天")
        lines.append("=" * 60)
        lines.append("")

        # 1. Work Overview
        overview = self.extract_work_overview()
        lines.append("## 1. 工作概览")
        lines.append(f"  会话数: {overview['session_count']}")
        if overview['projects']:
            lines.append(f"  涉及项目: {', '.join(overview['projects'][:5])}")
        lines.append(f"  活跃天数: {overview['active_days']} 天")
        lines.append(f"  完成任务: {len(overview['tasks'])}")
        if overview['tools']:
            lines.append(f"  使用工具: {', '.join(overview['tools'][:10])}")
        lines.append("")

        # 2. Learned Patterns
        patterns = self.extract_learned_patterns()
        lines.append(f"## 2. 习得的模式与技能 ({len(patterns)})")
        if patterns:
            for i, pattern in enumerate(patterns[:10], 1):
                if pattern['type'] == 'skill':
                    lines.append(f"  {i}. {pattern['title']}")
                    lines.append(f"     提取日期: {pattern['date']}")
                    if pattern['context']:
                        lines.append(f"     上下文: {pattern['context']}")
                else:  # instinct
                    lines.append(f"  {i}. {pattern['title']} (置信度: {int(pattern['confidence']*100)}%)")
                    lines.append(f"     触发条件: {pattern['trigger']}")
                    lines.append(f"     领域: {pattern['domain']}")
                lines.append("")
        else:
            lines.append("  暂无新习得的模式")
            lines.append("")

        # 3. Recurring Challenges
        challenges = self.extract_recurring_challenges()
        lines.append(f"## 3. 反复出现的挑战 ({len(challenges)})")
        if challenges:
            for i, challenge in enumerate(challenges[:10], 1):
                lines.append(f"  {i}. {challenge['error']} (出现 {challenge['count']} 次)")
        else:
            lines.append("  暂无记录的挑战")
        lines.append("")

        # 4. Improvement Suggestions
        suggestions = self.generate_improvement_suggestions(challenges)
        lines.append(f"## 4. 改进建议 ({len(suggestions)})")
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                lines.append(f"  {i}. {suggestion}")
        else:
            lines.append("  继续保持当前的工作模式")
        lines.append("")

        # 5. Strengths
        strengths = self.extract_strengths()
        lines.append(f"## 5. 优势确认 ({len(strengths)})")
        if strengths:
            for i, strength in enumerate(strengths[:10], 1):
                lines.append(f"  {i}. {strength['pattern']} (置信度: {int(strength['confidence']*100)}%)")
        else:
            lines.append("  暂无高置信度的优势模式")
        lines.append("")

        # Footer
        lines.append("=" * 60)
        lines.append(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append("=" * 60)

        return '\n'.join(lines)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Generate personal growth report from continuous learning data'
    )
    parser.add_argument(
        'days',
        type=int,
        nargs='?',
        default=7,
        help='Number of days to analyze (default: 7)'
    )
    parser.add_argument(
        '--save',
        type=str,
        help='Save report to file instead of printing to stdout'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'markdown', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    # Generate report
    generator = GrowthReportGenerator(days=args.days)
    report = generator.generate_report()

    # Output
    if args.save:
        output_path = Path(args.save)
        output_path.write_text(report)
        print(f"Report saved to: {output_path}")
    else:
        print(report)

    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
