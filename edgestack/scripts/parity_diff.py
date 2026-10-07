#!/usr/bin/env python3
"""逐张量比较两个 dump 目录，报告第一个发散点。

用法: parity_diff.py <参考目录> <候选目录> [--cos-min 0.999] [--sort name|mtime]

两个目录里同名的 .npy 文件（或 .bin，需 --dtype 和 --shape-from-ref）逐个比较，
输出 max abs、mean abs、cosine、相关系数。按 --sort 的顺序找第一个 cosine 低于阈值的张量。
文件名建议带层序号（例如 012_encoder.layer3.out.npy），这样按名字排序就是执行顺序。
"""
import argparse, os, sys
import numpy as np

def load(path, dtype):
    if path.endswith(".npy"):
        return np.load(path).astype(np.float64).ravel()
    return np.fromfile(path, dtype=dtype).astype(np.float64).ravel()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref"); ap.add_argument("cand")
    ap.add_argument("--cos-min", type=float, default=0.999)
    ap.add_argument("--sort", choices=["name", "mtime"], default="name")
    ap.add_argument("--dtype", default="float32")
    a = ap.parse_args()
    names = [n for n in os.listdir(a.ref) if n.endswith((".npy", ".bin")) and os.path.exists(os.path.join(a.cand, n))]
    if a.sort == "mtime":
        names.sort(key=lambda n: os.path.getmtime(os.path.join(a.ref, n)))
    else:
        names.sort()
    missing = [n for n in os.listdir(a.ref) if n.endswith((".npy", ".bin")) and n not in names]
    first = None
    print(f"{'tensor':<48} {'n':>10} {'max_abs':>10} {'mean_abs':>10} {'cos':>9} {'corr':>9}")
    for n in names:
        r = load(os.path.join(a.ref, n), a.dtype); c = load(os.path.join(a.cand, n), a.dtype)
        if r.size != c.size:
            print(f"{n:<48} SIZE MISMATCH {r.size} vs {c.size}")
            first = first or n
            continue
        d = np.abs(r - c)
        cos = float(r @ c / (np.linalg.norm(r) * np.linalg.norm(c) + 1e-30))
        corr = float(np.corrcoef(r, c)[0, 1]) if r.std() > 0 and c.std() > 0 else float("nan")
        flag = " <" if cos < a.cos_min else ""
        print(f"{n:<48} {r.size:>10} {d.max():>10.4g} {d.mean():>10.4g} {cos:>9.6f} {corr:>9.6f}{flag}")
        if cos < a.cos_min and first is None:
            first = n
    if missing:
        print(f"\n候选目录缺少 {len(missing)} 个张量: {', '.join(missing[:5])}{' ...' if len(missing) > 5 else ''}")
    print(f"\n第一个发散点: {first or '无（全部高于阈值）'}  (cos-min={a.cos_min})")
    sys.exit(1 if first else 0)

if __name__ == "__main__":
    main()
