#!/bin/bash
# Continuous Learning v2 - Observation Hook
#
# Captures tool use events for pattern analysis.
# Claude Code passes hook data via stdin as JSON.
#
# Hook config (in ~/.claude/settings.json):
#
# If installed as a plugin, use ${CLAUDE_PLUGIN_ROOT}:
# {
#   "hooks": {
#     "PreToolUse": [{
#       "matcher": "*",
#       "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh pre" }]
#     }],
#     "PostToolUse": [{
#       "matcher": "*",
#       "hooks": [{ "type": "command", "command": "${CLAUDE_PLUGIN_ROOT}/skills/continuous-learning-v2/hooks/observe.sh post" }]
#     }]
#   }
# }
#
# If installed manually to ~/.claude/skills:
# {
#   "hooks": {
#     "PreToolUse": [{
#       "matcher": "*",
#       "hooks": [{ "type": "command", "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh pre" }]
#     }],
#     "PostToolUse": [{
#       "matcher": "*",
#       "hooks": [{ "type": "command", "command": "~/.claude/skills/continuous-learning-v2/hooks/observe.sh post" }]
#     }]
#   }
# }

set -e

CONFIG_DIR="${HOME}/.claude/homunculus"
OBSERVATIONS_FILE="${CONFIG_DIR}/observations.jsonl"
MAX_FILE_SIZE_MB=10

# Ensure directory exists
mkdir -p "$CONFIG_DIR"

# Skip if disabled
if [ -f "$CONFIG_DIR/disabled" ]; then
  exit 0
fi

# Read JSON from stdin (Claude Code hook format)
INPUT_JSON=$(cat)

# Exit if no input
if [ -z "$INPUT_JSON" ]; then
  exit 0
fi

# Parse using python (more reliable than jq for complex JSON)
PARSED=$(echo "$INPUT_JSON" | python3 << 'EOF'
import json
import sys
import re

try:
    # 从 stdin 读取 JSON，避免注入风险
    data = json.load(sys.stdin)

    # Extract fields - Claude Code hook format
    hook_type = data.get('hook_type', 'unknown')  # PreToolUse or PostToolUse
    tool_name = data.get('tool_name', data.get('tool', 'unknown'))
    tool_input = data.get('tool_input', data.get('input', {}))
    tool_output = data.get('tool_output', data.get('output', ''))
    session_id = data.get('session_id', 'unknown')
    user_message = data.get('user_message', '')

    # Truncate large inputs/outputs
    if isinstance(tool_input, dict):
        tool_input_str = json.dumps(tool_input)[:5000]
    else:
        tool_input_str = str(tool_input)[:5000]

    if isinstance(tool_output, dict):
        tool_output_str = json.dumps(tool_output)[:5000]
    else:
        tool_output_str = str(tool_output)[:5000]

    # Determine event type
    event = 'tool_start' if 'Pre' in hook_type else 'tool_complete'

    result = {
        'parsed': True,
        'event': event,
        'tool': tool_name,
        'input': tool_input_str if event == 'tool_start' else None,
        'output': tool_output_str if event == 'tool_complete' else None,
        'session': session_id
    }

    # Code navigation: detect user query intent
    if user_message and 'Pre' in hook_type:
        code_search_keywords = [
            '我想修改', '找到', '查找', '在哪', '哪里', '定位', '搜索',
            '看看', '检查', '查看', '打开', '编辑', '更改',
            'find', 'locate', 'where', 'search', 'look for', 'show me',
            'open', 'edit', 'modify', 'change', 'update'
        ]

        user_message_lower = user_message.lower()
        if any(keyword in user_message_lower for keyword in code_search_keywords):
            result['user_query_event'] = {
                'event': 'user_query',
                'query': user_message,
                'intent': 'code_search',
                'session': session_id
            }

    print(json.dumps(result))
except Exception as e:
    print(json.dumps({'parsed': False, 'error': str(e)}), file=sys.stderr)
    print(json.dumps({'parsed': False, 'error': str(e)}))
EOF
)

# Check if parsing succeeded
PARSED_OK=$(echo "$PARSED" | python3 -c "import json,sys; print(json.load(sys.stdin).get('parsed', False))")

if [ "$PARSED_OK" != "True" ]; then
  # Fallback: log raw input for debugging
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  echo "{\"timestamp\":\"$timestamp\",\"event\":\"parse_error\",\"raw\":$(echo "$INPUT_JSON" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()[:1000]))')}" >> "$OBSERVATIONS_FILE"
  exit 0
fi

# Archive if file too large
if [ -f "$OBSERVATIONS_FILE" ]; then
  # 使用跨平台的方式获取文件大小
  if command -v stat >/dev/null 2>&1; then
    # macOS 和 BSD
    file_size_bytes=$(stat -f%z "$OBSERVATIONS_FILE" 2>/dev/null || stat -c%s "$OBSERVATIONS_FILE" 2>/dev/null)
  else
    # 回退到 du
    file_size_bytes=$(du -b "$OBSERVATIONS_FILE" 2>/dev/null | cut -f1)
  fi

  file_size_mb=$((${file_size_bytes:-0} / 1024 / 1024))

  if [ "${file_size_mb:-0}" -ge "$MAX_FILE_SIZE_MB" ]; then
    archive_dir="${CONFIG_DIR}/observations.archive"

    # 创建归档目录，失败则退出
    if ! mkdir -p "$archive_dir"; then
      echo "Error: Failed to create archive directory: $archive_dir" >&2
      exit 1
    fi

    archive_file="$archive_dir/observations-$(date +%Y%m%d-%H%M%S).jsonl"

    # 移动文件，失败则报错
    if mv "$OBSERVATIONS_FILE" "$archive_file"; then
      echo "Archived observations to: $archive_file" >&2
    else
      echo "Error: Failed to archive observations file" >&2
      exit 1
    fi
  fi
fi

# Build and write observation
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

python3 << EOF
import json

parsed = json.loads('''$PARSED''')
observation = {
    'timestamp': '$timestamp',
    'event': parsed['event'],
    'tool': parsed['tool'],
    'session': parsed['session']
}

if parsed['input']:
    observation['input'] = parsed['input']
if parsed['output']:
    observation['output'] = parsed['output']

with open('$OBSERVATIONS_FILE', 'a') as f:
    f.write(json.dumps(observation) + '\n')

# Write user query event if detected
if 'user_query_event' in parsed:
    query_event = parsed['user_query_event']
    query_event['timestamp'] = '$timestamp'
    f.write(json.dumps(query_event) + '\n')
EOF

# Signal observer if running
OBSERVER_PID_FILE="${CONFIG_DIR}/.observer.pid"
if [ -f "$OBSERVER_PID_FILE" ]; then
  observer_pid=$(cat "$OBSERVER_PID_FILE")
  if kill -0 "$observer_pid" 2>/dev/null; then
    kill -USR1 "$observer_pid" 2>/dev/null || true
  fi
fi

exit 0
