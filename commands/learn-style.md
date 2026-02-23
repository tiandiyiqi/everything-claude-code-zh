---
name: learn-style
description: 手动记录用户的沟通表达偏好，创建 communication 领域的直觉
allowed-tools: Read, Write, Bash, Glob
---

# /learn-style 命令

手动记录沟通表达偏好，保存为 communication 领域的直觉。

## 用法

```
/learn-style "用户表达" = "标准表达"
/learn-style --type terminology "画像" = "档案"
/learn-style --type phrasing "帮我..." = "请帮我..."
/learn-style --project "磨刀石" = "当前项目代号"
```

## 参数

- 第一个引号内容：用户偏好的表达
- `=` 后的引号内容：标准/替代表达
- `--type`：子类型（terminology | phrasing | project-concept），默认 terminology
- `--project`：标记为项目级概念，存储到 `.claude/communication/`

## 实现步骤

1. 解析用户输入，提取表达对和子类型
2. 生成直觉 ID：`comm-{normalized_user_term}`
3. 检查是否已存在同 ID 的直觉，如存在则更新置信度（+0.1）
4. 创建直觉文件，使用模板：

```yaml
---
id: comm-{normalized_term}
trigger: "when communicating about '{standard_term}'"
confidence: 0.7
domain: "communication"
source: "user-explicit"
subtype: "{type}"
---

# 术语偏好：{user_term}

## Action
Use '{user_term}' instead of '{standard_term}' when communicating with user.

## Evidence
- User explicitly recorded via /learn-style
- Date: {current_date}
```

5. 保存位置：
   - 默认：`~/.claude/homunculus/instincts/personal/comm-{term}.yaml`
   - `--project`：`.claude/communication/comm-{term}.yaml`

6. 运行 `expressions-view.py` 更新表达库视图

7. 输出确认信息：
   ```
   ✅ 已记录表达偏好：
      类型：{subtype}
      你的表达：{user_term}
      标准表达：{standard_term}
      置信度：70%
      存储位置：{file_path}
   ```

## 初始置信度

用户通过 `/learn-style` 明确记录的表达，初始置信度为 0.7（高于自动检测的 0.5），因为这是用户的明确意图。
