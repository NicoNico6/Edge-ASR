#!/usr/bin/env python3
"""Validate a folder of Agent Skills.

Checks every SKILL.md and playbook under a root:
  - frontmatter exists with `name` and `description`
  - `name` matches the directory name
  - every relative markdown link resolves to a file
  - every **bold** reference to a `principle-*` or other skill names a dir that exists
  - no long dash, curly quote, or mid-sentence colon in prose (the reply style)

Usage: check-skills.py <root> [--strict]
Exit 1 when any problem is found. Prints `file:line: message`.
"""
import os
import re
import sys

LINK = re.compile(r"\]\(([^)#]+)(#[^)]*)?\)")
BOLD = re.compile(r"\*\*([a-z0-9][a-z0-9-]*)\*\*")
DASH = re.compile("[–—]")
CURLY = re.compile("[‘’“”]")
COLON = re.compile(r"(?<!\S): \S")


def frontmatter(lines):
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = {}
            for raw in lines[1:i]:
                if ":" in raw:
                    k, v = raw.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"')
            return fm, i + 1
    return None, 0


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    root = os.path.abspath(sys.argv[1])
    strict = "--strict" in sys.argv
    skills_root = os.path.join(root, "skills")
    skill_dirs = set()
    if os.path.isdir(skills_root):
        skill_dirs = {d for d in os.listdir(skills_root) if os.path.isdir(os.path.join(skills_root, d))}

    problems = []
    files = []
    for dp, _, fns in os.walk(root):
        if ".git" in dp:
            continue
        for fn in fns:
            if fn.endswith(".md"):
                files.append(os.path.join(dp, fn))

    for path in sorted(files):
        rel = os.path.relpath(path, root)
        with open(path, encoding="utf-8") as f:
            text = f.read()
        lines = text.split("\n")
        is_skill = os.path.basename(path) == "SKILL.md"
        fm, body_start = frontmatter(lines)
        if is_skill:
            if fm is None:
                problems.append(f"{rel}:1: no frontmatter")
            else:
                for key in ("name", "description"):
                    if not fm.get(key):
                        problems.append(f"{rel}:1: frontmatter missing `{key}`")
                dirname = os.path.basename(os.path.dirname(path))
                if fm.get("name") and fm["name"] != dirname:
                    problems.append(f"{rel}:1: name `{fm['name']}` != dir `{dirname}`")
        fence = False
        for i, line in enumerate(lines[body_start:], start=body_start + 1):
            if line.startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            for m in LINK.finditer(line):
                target = m.group(1).strip()
                if re.match(r"^[a-z]+://", target) or target.startswith("mailto:"):
                    continue
                full = os.path.normpath(os.path.join(os.path.dirname(path), target))
                if not os.path.exists(full):
                    problems.append(f"{rel}:{i}: broken link {target}")
            for m in BOLD.finditer(line):
                name = m.group(1)
                if name.startswith("principle-") and name not in skill_dirs:
                    problems.append(f"{rel}:{i}: bold reference to missing skill **{name}**")
            prose = re.sub(r"`[^`]*`", "`", line)
            if DASH.search(prose):
                problems.append(f"{rel}:{i}: long dash")
            if CURLY.search(prose):
                problems.append(f"{rel}:{i}: curly quote")
            if strict and COLON.search(prose) and not prose.rstrip().endswith(":"):
                problems.append(f"{rel}:{i}: mid-sentence colon")

    for p in problems:
        print(p)
    print(f"{len(files)} files, {len(problems)} problems")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
