# Experiment Archive

This directory preserves the small, reviewable DP and ACT material that was originally scattered under `/data/coding`. Files retain their original names where possible so report links, commands, and hashes remain auditable.

| Directory | Contents |
|---|---|
| [原始报告](原始报告/) | Environment records and DP batch reports |
| [ACT离线复现](ACT离线复现/) | Easy ACT 30k offline training report and final training log |

Large files are intentionally absent from this directory and from Git: H5 datasets, checkpoint binaries, TensorBoard event files, generated run folders, and tar archives. Use [RELEASE_MANIFEST.md](../RELEASE_MANIFEST.md) for their local source paths and integrity data.

The DP result table and final interpretation are [experiments/results.csv](../experiments/results.csv) and [experiments/final_report.md](../experiments/final_report.md).
