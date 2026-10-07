#!/usr/bin/env bash
# 把 edgestack 的 skills 和 agents 链接到 Claude Code 的目录。
# 用法: ./install.sh [--project]
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
if [ "${1:-}" = "--project" ]; then base="$PWD/.claude"; else base="$HOME/.claude"; fi
mkdir -p "$base/skills" "$base/agents"
for d in "$src"/skills/*/; do
  n="$(basename "$d")"
  if [ -e "$base/skills/$n" ] && [ ! -L "$base/skills/$n" ]; then echo "跳过 $n：$base/skills/$n 已存在且不是链接"; continue; fi
  ln -sfn "$d" "$base/skills/$n"
done
for f in "$src"/agents/*.md; do ln -sfn "$f" "$base/agents/$(basename "$f")"; done
echo "已链接到 $base（skills 与 agents）。脚本在 $src/scripts。"
