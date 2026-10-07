### Authoring a skill（写 skill）

**你拥有 skill 的措辞。agent 读到的每句话都会变成它的行为。**

1. 用 skill 编写工具（Claude Code 里是 skill-creator），或按 Agent Skills 格式手写。
2. frontmatter 有 `name`（和目录名一致）和 `description`（写清什么时候用）。
3. 只留能改变决定的句子。告诉它做什么，规则不解释就会被误解时才写理由。
4. 能结构化的规则写成脚本或检查，不写成文字（**principle-encode-lessons-in-structure**）。
5. 引用其他 skill 用名字或相对路径，不复述它们的内容。
6. 运行 `scripts/check-skills.py` 检查链接和格式。
7. 结构性改动用 **Eval** playbook 测过再推广。

**回复：** skill 摘要、关键设计决定、检查结果。
