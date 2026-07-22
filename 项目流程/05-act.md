# RGB ACT Offline Reproduction

## Purpose And Boundary

This branch reproduces the Easy RGB ACT training configuration from the public leaderboard worktree, then records exactly what can and cannot be verified on the available host. ACT receives the scene camera image plus robot proprioception; unlike DP, it does not receive the privileged state vector. The completed result is **offline optimization and checkpoint-load verification**, not a closed-loop task score.

The source is vendored under [`il/baselines/act/`](../il/baselines/act/). The submission-compatible loader is `warehouse_sort.act_policy:load_act`. The compact report and original retained log are in [实验档案/ACT离线复现](../实验档案/ACT离线复现/); the copy supplied with the key-artifact archive is under [`evidence/act/`](../evidence/act/).

## Recorded Training Configuration

| Item | Recorded value |
|---|---|
| Difficulty and input | Easy, scene RGB plus proprioception |
| Demonstrations | 200 successful trajectories, 23,000 transitions |
| Backbone and policy | ResNet-18, DETR/CVAE, EMA |
| Objective | L1 plus KL, KL weight 10 |
| Optimizer settings | learning rate `1e-4`, batch size 32, seed 1 |
| Action chunking | 30 action queries with temporal aggregation enabled for training |
| Training duration | 30,000 updates |
| Runtime deviation | `--skip-env-eval` skips only Vulkan-dependent online evaluation |

The public configuration is [`il/conf/method/act_rgb.yaml`](../il/conf/method/act_rgb.yaml). To reproduce the offline run on a host with the RGB dataset:

```bash
pixi run python il/train.py method=act_rgb demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=32 \
  flags.lr=1e-4 flags.kl_weight=10 \
  flags.exp_name=act_easy_rank1_offline_30k
```

## Offline Training Evidence

![ACT Easy offline training loss](../evidence/figures/act_easy_loss.png)

The plot is generated from the copied terminal log, not TensorBoard. It records loss falling from `88.055382` at update 0 to `0.012345` at update 29,000, with all 30,000 updates completed. The source is [`evidence/act/act_easy_training.log`](../evidence/act/act_easy_training.log); regenerate the figure with `python scripts/generate_evidence_figures.py`.

The final checkpoint passed an independent load/inference check: output shape `(2, 4)`, finite values, and sample action range `[-0.211787, 0.621868]`. Its expected SHA-256 is `9654561175bc7e9c6d289fa7a74e235c20aa8a63cdc3aaca0795ca0ff6dc43fe`.

## Why A Closed-Loop ACT Score Is Absent

SAPIEN could not initialise a compatible NVIDIA Vulkan renderer on the training host. The captured log reports missing Vulkan ICD and GLVND ICD files. CUDA compute was available, which is enough to train the model, but CUDA alone is insufficient to create the RGB simulation environment. The project therefore does not label the missing score as zero and does not present the ACT curve as manipulation success.

To obtain a reportable ACT score, move the restored checkpoint and this worktree to a host with a functional NVIDIA graphics/Vulkan driver, then run the official 50-episode protocol:

```bash
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.act_policy:load_act \
  checkpoint=PATH_TO_ACT_CHECKPOINT \
  eval_config=conf/eval/server_50.yaml
```

Record the exact driver, renderer initialization, seeds, `sort_accuracy`, mean sorted parcels, and video policy with the result. Until that run exists, the only defensible ACT claim is the offline reproduction described above.
