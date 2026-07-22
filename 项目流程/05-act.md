# RGB ACT 离线复现

## 目的与边界

本分支复现公开 leaderboard worktree 的 Easy RGB ACT 训练配置，并记录可验证与不可验证的内容。ACT 使用 scene RGB 和 robot proprioception，不使用 privileged state。完成结果是离线优化与 checkpoint-load 验证，**不是**闭环任务成绩。

源码位于 [`il/baselines/act/`](../il/baselines/act/)，提交 loader 为 `warehouse_sort.act_policy:load_act`；报告与日志见 [实验档案/ACT离线复现](../实验档案/ACT离线复现/) 和 [`evidence/act/`](../evidence/act/)。

## 记录的训练配置

| 项目 | 值 |
|---|---|
| 数据 | Easy，200 条 successful trajectories，23,000 transitions |
| 模型 | ResNet-18、DETR/CVAE、EMA |
| 目标 | L1 + KL，KL weight 10 |
| 优化 | learning rate `1e-4`、batch size 32、seed 1 |
| chunking | 30 action queries，训练期启用 temporal aggregation |
| 训练量 | 30,000 updates |
| 唯一运行时差异 | `--skip-env-eval` 跳过 Vulkan 依赖的在线评估 |

```bash
pixi run python il/train.py method=act_rgb demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=32 \
  flags.lr=1e-4 flags.kl_weight=10
```

## 离线证据与缺口

![ACT Easy 离线训练 loss](../evidence/figures/act_easy_loss.png)

该图由 [`evidence/act/act_easy_training.log`](../evidence/act/act_easy_training.log) 生成，不是 TensorBoard；它记录 loss 从 update 0 的 `88.055382` 下降至 update 29,000 的 `0.012345`，并完成 30,000 updates。checkpoint 独立加载后输出 shape 为 `(2, 4)`、数值有限，预期 SHA-256 为 `9654561175bc7e9c6d289fa7a74e235c20aa8a63cdc3aaca0795ca0ff6dc43fe`。

训练主机的 CUDA 可用，但 SAPIEN 无法初始化兼容的 NVIDIA Vulkan renderer，日志记录了缺失 Vulkan ICD 与 GLVND ICD。因此不能给出 RGB closed-loop 分数，也不得把缺失成绩写为零分。要得到可报告结果，应在具备 NVIDIA graphics/Vulkan driver 的主机恢复 checkpoint 后运行官方 50-episode 协议。
