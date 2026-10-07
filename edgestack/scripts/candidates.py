#!/usr/bin/env python3
"""候选谱系工具，记录在 candidates.jsonl。思路来自 NVlabs/kda 的 candidates.jsonl。

  candidates.py add  FILE NAME [--parent P] [--desc "..."] [--evidence path]
  candidates.py set  FILE NAME {promoted,rejected,revised,testing} [--reason "..."] [--evidence path]
  candidates.py tree FILE        按父子关系打印谱系和状态
  candidates.py check FILE       拒绝或修改的候选必须有原因，父节点必须存在
"""
import argparse, datetime, json, os, sys

STATUSES = {"testing", "promoted", "rejected", "revised"}

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load(f):
    if not os.path.exists(f):
        return []
    return [json.loads(l) for l in open(f) if l.strip()]

def state(events):
    c = {}
    for e in events:
        if e["op"] == "add":
            c[e["name"]] = {"parent": e.get("parent"), "desc": e.get("desc", ""), "status": "testing", "reason": "", "evidence": e.get("evidence", "")}
        elif e["op"] == "set" and e["name"] in c:
            c[e["name"]].update({k: e[k] for k in ("status", "reason", "evidence") if e.get(k)})
    return c

def append(f, e):
    e["ts"] = now()
    with open(f, "a") as h:
        h.write(json.dumps(e, ensure_ascii=False) + "\n")

def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("add"); a.add_argument("file"); a.add_argument("name"); a.add_argument("--parent"); a.add_argument("--desc", default=""); a.add_argument("--evidence", default="")
    s = sp.add_parser("set"); s.add_argument("file"); s.add_argument("name"); s.add_argument("status", choices=sorted(STATUSES)); s.add_argument("--reason", default=""); s.add_argument("--evidence", default="")
    for n in ("tree", "check"):
        p = sp.add_parser(n); p.add_argument("file")
    x = ap.parse_args()
    c = state(load(x.file))
    if x.cmd == "add":
        if x.name in c: sys.exit(f"候选 {x.name} 已存在")
        if x.parent and x.parent not in c: sys.exit(f"父候选 {x.parent} 不存在")
        append(x.file, {"op": "add", "name": x.name, "parent": x.parent, "desc": x.desc, "evidence": x.evidence})
        print(f"已添加 {x.name}（父：{x.parent or '无'}）")
    elif x.cmd == "set":
        if x.name not in c: sys.exit(f"候选 {x.name} 不存在")
        if x.status in ("rejected", "revised") and not x.reason: sys.exit("拒绝或修改必须给 --reason")
        if x.status == "promoted" and not x.evidence: sys.exit("晋升必须给 --evidence（验证与评测结果的路径）")
        append(x.file, {"op": "set", "name": x.name, "status": x.status, "reason": x.reason, "evidence": x.evidence})
        print(f"{x.name} → {x.status}")
    elif x.cmd == "tree":
        kids = {}
        for n, v in c.items(): kids.setdefault(v["parent"], []).append(n)
        def walk(p, d):
            for n in kids.get(p, []):
                v = c[n]; r = f"  原因：{v['reason']}" if v["reason"] else ""
                print("  " * d + f"- {n} [{v['status']}] {v['desc']}{r}")
                walk(n, d + 1)
        walk(None, 0)
    else:
        bad = 0
        for n, v in c.items():
            if v["status"] in ("rejected", "revised") and not v["reason"]: print(f"{n}: {v['status']} 但没有原因"); bad += 1
            if v["parent"] and v["parent"] not in c: print(f"{n}: 父候选 {v['parent']} 不存在"); bad += 1
            if v["status"] == "promoted" and not v["evidence"]: print(f"{n}: 晋升但没有证据"); bad += 1
        print(f"{len(c)} 个候选，{bad} 个问题"); sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
