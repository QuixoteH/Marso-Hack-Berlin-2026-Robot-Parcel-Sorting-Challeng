# WarehouseSort: DP and ACT Experiment Archive

This repository records a reproducible investigation of the [WarehouseSort](https://github.com/marso-robotics/berlin-marso-hackathon) colour-matching pick-and-place challenge. A Franka Panda must move parcels into the bin whose colour matches the parcel tag.

The project keeps the runnable challenge code, the selected State Diffusion Policy (DP) submission path, and an offline ACT reproduction. It is an experiment archive, not a direct algorithm comparison: DP uses privileged state, while ACT uses RGB plus proprioception.

## Results at a Glance

All scores below are independently evaluated local results using the official loader, fixed seeds `5000-5049`, 50 episodes, and `sort_accuracy`. They are not Kaggle held-out leaderboard scores.

| Method | Input | Completed scope | Best verifiable result | Status |
|---|---|---|---|---|
| State DP | low-dimensional state | Easy, Medium, Hard | `0.390 / 0.090 / 0.103` | Deliverable state policy |
| RGB ACT | RGB plus proprioception | Easy offline training, 30k updates | no closed-loop score | Needs Vulkan-capable evaluation host |

Using the challenge weights Easy/Medium/Hard = `0.20/0.30/0.50`, the DP fixed-seed aggregate is `0.1565`. The 195 MiB submission archive exceeds GitHub's 100 MiB file limit; checkpoints are also kept outside normal Git history to keep ordinary clones practical. See [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md).

## Task Preview

| Easy: 2 parcels | Medium: 4 parcels | Hard: 6 parcels, bins may swap |
|:---:|:---:|:---:|
| ![Easy scripted demonstration](media/easy_demo.gif) | ![Medium scripted demonstration](media/medium_demo.gif) | ![Hard scripted demonstration](media/hard_demo.gif) |

The scripted policy shown above only generated demonstrations. Submitted policies must be learned observation-to-action mappings.

## Repository Layout

```text
.
├── README.md                       Project entry point and verified result summary
├── 项目流程/                        End-to-end workflow, by experiment stage
├── 踩坑记录/                        Environment, data, evaluation, and RL pitfalls
├── 实验档案/                        Preserved source reports and small audit evidence
├── experiments/                    Result CSV, final report, scripts, and hashes
├── il/                             Demo tooling and DP / ACT baselines
├── warehouse_sort/                 Environment and policy loader entry points
├── conf/                           Difficulty and evaluation configuration
├── submission.yaml                 Selected DP submission manifest
└── RELEASE_MANIFEST.md             Included files and local-only artifact inventory
```

The structure follows the public-project style of [JereoZero/so101-real](https://github.com/JereoZero/so101-real): a focused top-level README, a stage-by-stage workflow, a separately indexed problem record, and a preserved evidence archive.

## Quick Start

The verified state-track environment used Python 3.10.16, PyTorch 2.6.0+cu126, ManiSkill 3.0.1, and SAPIEN 3.0.3 on an RTX 3090. RGB evaluation additionally requires an NVIDIA Vulkan graphics driver; CUDA compute alone is insufficient.

```bash
pixi install
pixi run install

# Download the official demonstrations after joining the Kaggle competition.
pixi run python il/download_demos.py

# Train a State Diffusion Policy candidate.
pixi run python il/train.py method=dp demo_dir=easy

# Evaluate through the official loader without video rendering.
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=PATH_TO_CHECKPOINT \
  eval_config=conf/eval/server_50.yaml
```

For the operational sequence and exact experimental boundaries, start at [项目流程/workflow.md](项目流程/workflow.md). For historical source material and hashes, use [实验档案/README.md](实验档案/README.md).

## Important Boundaries

- DP consumes privileged state; ACT consumes RGB plus proprioception. Their results are not an algorithm ranking.
- ACT training and checkpoint loading succeeded offline. No RGB environment could be initialized on this host, so absence of a score does not mean score zero.
- Original demonstrations, generated H5 datasets, run outputs, large checkpoints, and submission tarballs stay local. Their locations and SHA-256 values are documented rather than silently omitted.

## Navigation

- [Workflow index](项目流程/workflow.md)
- [Pitfall index](踩坑记录/pitfalls.md)
- [Final DP report](experiments/final_report.md)
- [All DP candidates](experiments/results.csv)
- [ACT offline reproduction report](实验档案/ACT离线复现/复现报告.md)
- [Release manifest](RELEASE_MANIFEST.md)

## Upstream and Credits

This work extends the official [marso-robotics/berlin-marso-hackathon](https://github.com/marso-robotics/berlin-marso-hackathon) repository at commit `6048f33217f26ae39009a812f53c81171517f393`. The ACT reproduction follows the public leaderboard branch recorded in the archived report. Keep the original challenge's submission rules and licence obligations when publishing or submitting a fork.
