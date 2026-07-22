# 发布清单

本仓库面向普通 GitHub Git 托管，而非 Git LFS。已包含的材料足以审阅代码改动、配置、结果、报告方法与紧凑审计证据。

## Git 中包含

- Challenge source modifications, DP/ACT scripts, and policy loaders.
- `experiments/results.csv`, `experiments/final_report.md`, selected shell tooling, JSON manifests, and SHA-256 lists.
- The original DP reports and compact ACT offline-reproduction material under `实验档案/`.
- Four final DP evaluation logs, one ACT training log, and two source-labelled figures under `evidence/`.
- Media that documents the task, configuration files, and the selected `submission.yaml`.

## 有意仅保留在本地

| 产物类别 | 本地位置 | 原因 |
|---|---|---|
| Selected DP checkpoints | `experiments/checkpoints/*.pt` | 35-38 MiB each; release separately to keep clone size practical |
| DP submission archive | `experiments/marso_final_submission.tar.gz` | about 195 MiB; exceeds GitHub's per-file limit |
| Generated H5 datasets | `experiments/datasets/**/trajectory.h5` | 20-219 MiB per file; several exceed GitHub's limit |
| Original demonstration H5 | `il/demos/**/trajectory.*.h5` | competition data, large and not for normal Git history |
| Training logs and event files | `experiments/logs/`, `il/baselines/*/runs/`, `outputs/` | generated artifacts; compact final logs are copied into `evidence/`, but TensorBoard event files were not present in the supplied archive |
| ACT checkpoint | `/data/coding/ACT榜一复现实验_2026-07-19/checkpoints/act_easy_rank1_offline_30k_final.pt` | 133 MiB; exceeds GitHub's per-file limit |
| Original archives and dataset zip | `/data/coding/*.tar.gz`, `/data/coding/*challenge*.zip` | source delivery artifacts, up to 408 MiB |

## 完整性锚点

| Artifact | SHA-256 |
|---|---|
| State DP Easy | `118895f645c1852f94cb94f3e9563172626fa641b35e98fa66f241d5b82250ab` |
| State DP Medium | `a3e6791d9485c90d1c501b362277baa4fe0cf7a4624abd30360daea1b3544246` |
| State DP Hard | `4019d3599ee9f5dd4e74711c95c347bf40edea8349235cd6e578674ed485bb00` |
| Final DP submission archive | `86246a605503d42ccb7d8fe02ab29d2a1f3a538fd3604739af8191e80440d0ab` |
| ACT Easy offline 30k checkpoint | `9654561175bc7e9c6d289fa7a74e235c20aa8a63cdc3aaca0795ca0ff6dc43fe` |

通过 GitHub Release 或 LFS 发布产物前，请重新计算 checksum，并与本清单和 `experiments/checkpoints/SHA256SUMS` 比较。
