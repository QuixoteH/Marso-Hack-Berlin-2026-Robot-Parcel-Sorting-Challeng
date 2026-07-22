# WarehouseSort: DP and ACT Experiment Archive

This repository is a reproducible public record of a [WarehouseSort](https://github.com/marso-robotics/berlin-marso-hackathon) colour-matching pick-and-place project. A Franka Panda must grasp each parcel and release it in the bin with the matching colour tag. It contains the runnable task integration, selected State Diffusion Policy (DP) path, an ACT offline reproduction, commands, configurations, small primary evidence, and an explicit boundary around results that were not verified.

The repository follows the public-project style of [JereoZero/so101-real](https://github.com/JereoZero/so101-real): begin with the top-level result and task preview, then follow an ordered procedure, evidence index, and release manifest. It is an experiment archive, not an algorithm leaderboard: DP consumes privileged state, while ACT consumes RGB plus proprioception.

## Verified Result Summary

Every DP score below was produced by the official loader in a clean shell with fixed evaluation seeds `5000-5049`, 50 episodes, no video, and `sort_accuracy` as the primary metric. These are local fixed-seed evaluations, not Kaggle held-out leaderboard results.

| Track | Observation | Completed scope | Verifiable outcome | Evidence |
|---|---|---|---|---|
| State DP | low-dimensional privileged state | Easy, Medium, Hard | `0.390 / 0.090 / 0.103` | [50-episode logs](evidence/evaluations/), [candidate CSV](experiments/results.csv) |
| RGB ACT | scene RGB plus robot proprioception | Easy, 30,000 offline updates | checkpoint loads; no closed-loop score | [training log](evidence/act/act_easy_training.log), [loss plot](evidence/figures/act_easy_loss.png) |

The challenge weights are Easy/Medium/Hard = `0.20/0.30/0.50`, so the documented DP scores give a local weighted aggregate of `0.1565` (`0.2*0.390 + 0.3*0.090 + 0.5*0.103`). This is a descriptive local aggregate only. The 195 MiB submission archive exceeds GitHub's 100 MiB per-file limit; binary artifacts remain local and are identified by SHA-256 in [RELEASE_MANIFEST.md](RELEASE_MANIFEST.md).

## Evidence At A Glance

| DP candidate selection | ACT offline optimization |
|:---:|:---:|
| ![Fixed 50-episode DP candidate scores](evidence/figures/dp_candidate_scores.png) | ![ACT Easy offline training loss](evidence/figures/act_easy_loss.png) |

The figures are generated from versioned CSV/log files, not TensorBoard exports. The supplied training-artifact archive has no TensorBoard event files. See [evidence/README.md](evidence/README.md) for source paths and interpretation limits.

## Task Preview

| Easy: 2 parcels | Medium: 4 parcels | Hard: 6 parcels, bins may swap |
|:---:|:---:|:---:|
| ![Easy scripted demonstration](media/easy_demo.gif) | ![Medium scripted demonstration](media/medium_demo.gif) | ![Hard scripted demonstration](media/hard_demo.gif) |

The scripted policy shown above only generated demonstrations. Submitted policies must be learned observation-to-action mappings.

## What Is In This Repository

```text
.
├── README.md                       Project entry point, outcome and evidence overview
├── 项目流程/                        Followable procedure from task contract to release
├── evidence/                       Public 50-episode logs, ACT log, and derived figures
├── 实验档案/                        Historical source reports retained for auditability
├── experiments/                    Candidate table, final report, manifests and hashes
├── il/                             Demonstration tooling plus DP and ACT baselines
├── warehouse_sort/                 Environment and submission policy loaders
├── conf/                           Difficulty and fixed-evaluation configurations
├── submission.yaml                 Selected three-level DP submission manifest
└── RELEASE_MANIFEST.md             Included and deliberately local-only artifacts
```

## Reproduce The State DP Evaluation

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

The supplied public checkout does not contain selected checkpoint binaries. Restore the exact checkpoint from the artifact archive or a future release, verify its SHA-256, then run the evaluation command above. The exact three-level manifest is [submission.yaml](submission.yaml); the evaluation contract is [项目流程/03-data-and-protocol.md](项目流程/03-data-and-protocol.md).

## Follow The Project Procedure

| Step | Read this | You will learn |
|---|---|---|
| 1 | [Task and evaluation](项目流程/01-task-and-evaluation.md) | What counts as a sorted parcel and what the score means |
| 2 | [Environment](项目流程/02-environment.md) | Headless state setup and the Vulkan limitation |
| 3 | [Data and protocol](项目流程/03-data-and-protocol.md) | Dataset audit, action handling, seeds, and final-evaluation rules |
| 4 | [State DP](项目流程/04-state-dp.md) | DP configuration, candidate selection, final verification and artifacts |
| 5 | [RGB ACT](项目流程/05-act.md) | Offline reproduction parameters and why it has no closed-loop score |
| 6 | [Release and submission](项目流程/07-release-and-submission.md) | How to restore, validate, package and publish artifacts |

For raw historical source material, use [实验档案/README.md](实验档案/README.md). For evidence copied from the supplied artifact archive, use [evidence/README.md](evidence/README.md).

## Evidence Boundaries

- DP consumes privileged state; ACT consumes RGB plus proprioception. Their results are not an algorithm ranking.
- ACT training and checkpoint loading succeeded offline. No RGB environment could be initialized on this host, so absence of a score does not mean score zero.
- Original demonstrations, generated H5 datasets, run outputs, large checkpoints, and submission tarballs stay local. Their locations and SHA-256 values are documented rather than silently omitted.
- The final DP logs prove only the stated local 50-episode condition. They do not prove a competition-held-out score.
- The ACT loss curve proves offline optimization progressed to 30,000 updates. It does not prove grasping, placement, or sorting performance.

## Navigation

- [Workflow index](项目流程/workflow.md)
- [Pitfall index](踩坑记录/pitfalls.md)
- [Final DP report](experiments/final_report.md)
- [All DP candidates](experiments/results.csv)
- [Public evidence index](evidence/README.md)
- [ACT offline reproduction report](实验档案/ACT离线复现/复现报告.md)
- [Release manifest](RELEASE_MANIFEST.md)

## Upstream and Credits

This work extends the official [marso-robotics/berlin-marso-hackathon](https://github.com/marso-robotics/berlin-marso-hackathon) repository at commit `6048f33217f26ae39009a812f53c81171517f393`. The ACT reproduction follows the public leaderboard branch recorded in the archived report. Keep the original challenge's submission rules and licence obligations when publishing or submitting a fork.
