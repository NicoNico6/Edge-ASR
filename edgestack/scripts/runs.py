#!/usr/bin/env python3
"""runs.tsv 总账工具。缺字段的行不写入。

  runs.py add runs.tsv --run-id R --metric M --value V --n N --caliber "..." --verdict kept \
      [--spread S] [--device D] [--firmware F] [--seed S] [--data-version V] [--config cfg.yaml] [--note ...]
  runs.py check runs.tsv     检查缺字段、verdict 取值、同一 metric 下口径混用
"""
import argparse, csv, datetime, hashlib, os, subprocess, sys

COLS = ["ts", "run_id", "commit", "config_hash", "data_version", "device", "firmware", "seed",
        "metric", "value", "spread", "n", "caliber", "verdict", "note"]
REQUIRED = ["run_id", "commit", "device", "metric", "value", "n", "caliber", "verdict"]
VERDICTS = {"kept", "reverted", "falsified", "inconclusive", "baseline"}

def git_commit():
    try:
        sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL).decode().strip()
        dirty = subprocess.call(["git", "diff", "--quiet"], stderr=subprocess.DEVNULL) != 0
        return sha + ("-dirty" if dirty else "")
    except Exception:
        return ""

def add(a):
    row = {c: "" for c in COLS}
    row["ts"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row["commit"] = a.commit or git_commit()
    if a.config:
        row["config_hash"] = hashlib.sha256(open(a.config, "rb").read()).hexdigest()[:12]
    for k in ["run_id", "data_version", "device", "firmware", "seed", "metric", "value", "spread", "n", "caliber", "verdict", "note"]:
        v = getattr(a, k.replace("-", "_"), None)
        if v is not None:
            row[k] = str(v).replace("\t", " ").replace("\n", " ")
    miss = [k for k in REQUIRED if not row[k]]
    if miss:
        sys.exit(f"拒绝写入，缺字段: {', '.join(miss)}")
    if row["verdict"] not in VERDICTS:
        sys.exit(f"verdict 必须是 {sorted(VERDICTS)} 之一")
    new = not os.path.exists(a.file) or os.path.getsize(a.file) == 0
    with open(a.file, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, delimiter="\t")
        if new:
            w.writeheader()
        w.writerow(row)
    print(f"已写入 {a.file}: {row['run_id']} {row['metric']}={row['value']} ({row['verdict']})")

def check(a):
    rows = list(csv.DictReader(open(a.file), delimiter="\t"))
    bad = 0
    calibers = {}
    for i, r in enumerate(rows, start=2):
        miss = [k for k in REQUIRED if not r.get(k)]
        if miss:
            print(f"{a.file}:{i}: 缺字段 {', '.join(miss)}"); bad += 1
        if r.get("verdict") and r["verdict"] not in VERDICTS:
            print(f"{a.file}:{i}: verdict 非法 {r['verdict']}"); bad += 1
        if r.get("n") == "1" and not r.get("spread"):
            print(f"{a.file}:{i}: 单次运行，注意噪声底未知")
        calibers.setdefault(r.get("metric"), set()).add(r.get("caliber"))
    for m, cs in calibers.items():
        if len(cs) > 1:
            print(f"注意: 指标 {m} 下有 {len(cs)} 种口径，比较前确认可比")
    print(f"{len(rows)} 行，{bad} 个问题")
    sys.exit(1 if bad else 0)

def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("add"); p.add_argument("file")
    for k in ["run-id", "metric", "value", "n", "caliber", "verdict", "spread", "device", "firmware", "seed", "data-version", "config", "commit", "note"]:
        p.add_argument(f"--{k}")
    c = sp.add_parser("check"); c.add_argument("file")
    a = ap.parse_args()
    add(a) if a.cmd == "add" else check(a)

if __name__ == "__main__":
    main()
