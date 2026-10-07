#!/usr/bin/env python3
"""Roofline estimate for batch-1 edge inference.

Answers the question every edge port starts with: on this device, at this
frame or token rate, is the model bandwidth-bound or compute-bound, does it
fit in memory, and how far is the measured number from the ceiling.

Usage:
  roofline.py --bw 60 --tops 30 --mem 8 \
      --part llm:9e9:3 --part tts:1e9:16 --part enc:0.6e9:16 \
      --rate 12.5 [--eff 0.6] [--measured-ms 87.7] [--json]

  --part NAME:PARAMS:BITS   one weight group. PARAMS as a float (9e9), BITS per
                            weight (3, 4, 8, 16). Repeat for each component.
  --flops-per-param N       multiply-adds per parameter per step (default 2,
                            one MAC per weight for a dense decode step).
  --kv-mb MB                extra bytes read per step (KV cache, activations).
  --rate HZ                 steps per second the product needs (frames/s or
                            tokens/s). Budget per step is 1000/rate ms.
  --eff F                   fraction of peak bandwidth batch-1 decode achieves
                            in practice (default 0.6; measure it on the board).
  --measured-ms MS          per-step time you measured, to report the gap.

Every number printed is an estimate from the inputs. Put the measured number
next to it before you trust either.
"""
import argparse
import json
import sys


def parse_part(spec: str):
    try:
        name, params, bits = spec.split(":")
        return name, float(params), float(bits)
    except ValueError:
        sys.exit(f"bad --part {spec!r}, want NAME:PARAMS:BITS")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bw", type=float, required=True, help="device memory bandwidth, GB/s")
    ap.add_argument("--tops", type=float, required=True, help="peak compute at the precision you run, TOPS (or TFLOPS)")
    ap.add_argument("--mem", type=float, required=True, help="memory available to the model, GB")
    ap.add_argument("--part", action="append", default=[], help="NAME:PARAMS:BITS, repeatable")
    ap.add_argument("--flops-per-param", type=float, default=2.0)
    ap.add_argument("--kv-mb", type=float, default=0.0, help="extra MB read per step")
    ap.add_argument("--rate", type=float, required=True, help="required steps per second")
    ap.add_argument("--eff", type=float, default=0.6, help="achieved fraction of peak bandwidth")
    ap.add_argument("--measured-ms", type=float, default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    parts = [parse_part(p) for p in a.part]
    if not parts:
        sys.exit("give at least one --part")

    weight_bytes = sum(n * b / 8 for _, n, b in parts)
    step_bytes = weight_bytes + a.kv_mb * 1e6
    step_flops = sum(n for _, n, _ in parts) * a.flops_per_param
    budget_ms = 1000.0 / a.rate

    bw_ms_peak = step_bytes / (a.bw * 1e9) * 1000
    bw_ms = bw_ms_peak / a.eff
    compute_ms = step_flops / (a.tops * 1e12) * 1000
    bound = "bandwidth" if bw_ms >= compute_ms else "compute"
    est_ms = max(bw_ms, compute_ms)
    rtf = est_ms / budget_ms
    need_bw = step_bytes * a.rate / a.eff / 1e9

    out = {
        "parts": [{"name": n, "params": p, "bits": b, "bytes": p * b / 8} for n, p, b in parts],
        "weight_gb": weight_bytes / 1e9,
        "fits_memory": weight_bytes / 1e9 < a.mem,
        "bytes_per_step": step_bytes,
        "flops_per_step": step_flops,
        "budget_ms": budget_ms,
        "bandwidth_ms_at_peak": bw_ms_peak,
        "bandwidth_ms_at_eff": bw_ms,
        "compute_ms_at_peak": compute_ms,
        "bound": bound,
        "estimated_step_ms": est_ms,
        "estimated_rtf": rtf,
        "bandwidth_needed_gbs": need_bw,
        "headroom_x": a.bw / need_bw if need_bw else None,
    }
    if a.measured_ms is not None:
        out["measured_ms"] = a.measured_ms
        out["measured_vs_estimate"] = a.measured_ms / est_ms if est_ms else None
        out["implied_eff"] = (step_bytes / (a.bw * 1e9) * 1000) / a.measured_ms if a.measured_ms else None

    if a.json:
        print(json.dumps(out, indent=2))
        return

    print(f"weights        {out['weight_gb']:.2f} GB  ({'fits' if out['fits_memory'] else 'DOES NOT FIT'} in {a.mem} GB)")
    for p in out["parts"]:
        print(f"  {p['name']:<8} {p['params']/1e9:6.2f}B x {p['bits']:>2.0f} bit = {p['bytes']/1e9:5.2f} GB")
    print(f"per step       {step_bytes/1e9:.2f} GB read, {step_flops/1e9:.1f} GFLOP")
    print(f"budget         {budget_ms:.1f} ms per step at {a.rate} steps/s")
    print(f"bandwidth      {bw_ms_peak:.1f} ms at peak, {bw_ms:.1f} ms at eff={a.eff}")
    print(f"compute        {compute_ms:.1f} ms at peak {a.tops} TOPS")
    print(f"bound by       {bound}")
    print(f"estimate       {est_ms:.1f} ms per step, RTF {rtf:.2f}  ({'real time' if rtf <= 1 else 'SLOWER than real time'})")
    print(f"needs          {need_bw:.1f} GB/s sustained, device has {a.bw} GB/s ({out['headroom_x']:.2f}x headroom)")
    if a.measured_ms is not None:
        print(f"measured       {a.measured_ms:.1f} ms = {out['measured_vs_estimate']:.2f}x the estimate, implied bandwidth efficiency {out['implied_eff']:.2f}")
        if out["measured_vs_estimate"] > 1.5:
            print("               gap > 1.5x: the limiter is not the weights. Profile per stage before quantizing further.")


if __name__ == "__main__":
    main()
