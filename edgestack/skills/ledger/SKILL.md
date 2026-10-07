---
name: ledger
description: "实验总账：每次运行一行 runs.tsv，加上总账、对照、底稿、回归四种文档体裁。用于 /ledger，记录任何实验结果（保留和证伪都记）。"
disable-model-invocation: true
---

# Ledger

## runs.tsv

一次运行一行，用 `scripts/runs.py add` 追加，它会拒绝缺字段的行。表头：

`ts  run_id  commit  config_hash  data_version  device  firmware  seed  metric  value  spread  n  caliber  verdict  note`

- `verdict`：kept、reverted、falsified、inconclusive、baseline。
- `spread`：范围或标准差，单次运行写 `n=1`。
- `caliber`：口径行（见 `../edge-mode/references/caliber-block.md`）。

`scripts/runs.py check runs.tsv` 检查缺字段和口径混用。

## 文档体裁

模板在 `../../templates/`。

- **总账**（`ledger-doc.md`）：一个项目阶段的全貌。结论速览、帕累托前沿表、杠杆表、已证伪表、配方修正表、差距归属表、未完成、这份记录的限度。
- **对照**（`comparison-doc.md`）：两到四个配置的并排比较。口径行、并排产物、数据表、看什么、为什么和早先读数不同。
- **底稿**（`port-draft.md`）：移植或对接的状态。现状、执行版图、偏差清单、可用包络、实测开销、待对方解决的问题、文件导航。
- **回归**（`regression-doc.md`）：一次改动在多个数据集上的判决。守门线、每个集上的前后数字、是否越线、非独立集标注。

## 规则

只追加，不改历史。错误的行用新行更正。每张表后写「看什么」和「口径」。
