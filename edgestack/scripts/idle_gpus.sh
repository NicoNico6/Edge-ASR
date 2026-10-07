#!/usr/bin/env bash
# 列出利用率持续为 0 的 GPU。用法: idle_gpus.sh [采样次数=6] [间隔秒=10]
# 在每个计算节点上运行（或经 srun/ssh 调用）。空闲的卡要报告，或在授权内使用。
set -euo pipefail
n="${1:-6}"; gap="${2:-10}"
command -v nvidia-smi >/dev/null || { echo "没有 nvidia-smi"; exit 2; }
declare -A busy
for ((i=0; i<n; i++)); do
  while IFS=, read -r idx util mem; do
    idx="${idx// /}"; util="${util// /}"
    if [ "$util" != "0" ]; then busy[$idx]=1; fi
  done < <(nvidia-smi --query-gpu=index,utilization.gpu,memory.used --format=csv,noheader,nounits)
  [ "$i" -lt $((n-1)) ] && sleep "$gap"
done
idle=()
while IFS=, read -r idx _; do idx="${idx// /}"; [ -z "${busy[$idx]:-}" ] && idle+=("$idx"); done \
  < <(nvidia-smi --query-gpu=index --format=csv,noheader)
host="$(hostname)"
if [ "${#idle[@]}" -eq 0 ]; then echo "$host: 没有空闲 GPU"; else echo "$host: 空闲 GPU ${idle[*]}（$((n*gap)) 秒内利用率始终为 0）"; fi
