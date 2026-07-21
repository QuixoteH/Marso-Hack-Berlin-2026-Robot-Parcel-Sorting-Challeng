# Marso 实验报告：批次 01 DP 基线

- 日期：2026-07-15
- 仓库提交：`6048f33217f26ae39009a812f53c81171517f393`
- 环境：Python 3.10.16，PyTorch 2.6.0+cu126，RTX 3090 24 GB
- 观测与后端：state，GPU PhysX，headless，禁用视频
- 数据：Easy、Medium、Hard 各 200 条示范
- 评估：固定 seeds 5000-5049，共 50 episodes

## 环境准备

- 创建 `experiments/environment_snapshot.txt` 与 `experiments/results.csv`。
- 创建 `conf/eval/server_50.yaml`。
- 为 `eval.py` 增加 `record_video=false` 的 headless 评估路径。
- 六组 state/RGB H5 与 JSON 均为 200 episodes，episode ID 完全一致。
- GPU state 环境 reset/step 验证通过，观测形状为 `(1, 54)`，设备为 `cuda:0`。

## 训练结果

| 难度 | 配置 | 训练耗时 | 训练内最佳 sort accuracy |
|---|---|---:|---:|
| Easy | seed 1，30k，batch 256，horizon 200 | 36m34s | 0.4688 |
| Medium | seed 1，50k，batch 256，horizon 400 | 1h13m37s | 0.1719 |
| Hard | seed 1，60k，batch 256，horizon 550 | 1h44m43s | 0.0833 |

## 固定 50 Seeds 评估

| 难度 | sort accuracy | mean sorted | all placed | mis-sort rate |
|---|---:|---:|---:|---:|
| Easy | 0.170 | 0.34 / 2 | 0.000 | 0.000 |
| Medium | 0.110 | 0.44 / 4 | 0.000 | 0.000 |
| Hard | 0.037 | 0.22 / 6 | 0.000 | 0.013 |

加权分数：

```text
0.2 * 0.170 + 0.3 * 0.110 + 0.5 * 0.037 = 0.0855
```

## Checkpoints

- Easy：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_easy_baseline_s1/checkpoints/best_eval_sort_accuracy.pt`
- Medium：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_medium_baseline_s1/checkpoints/best_eval_sort_accuracy.pt`
- Hard：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_hard_baseline_s1/checkpoints/best_eval_sort_accuracy.pt`

## 发现的问题

1. 指导文档 Task 1 的 `Path.with_suffix()` 会生成错误的数据文件名，实际审计改为在完整 stem 后追加 `.json` 和 `.h5`。
2. 指导文档使用 `flags.seed=1`，但原始 `il/conf/method/dp.yaml` 未声明 `seed`；已添加默认 `seed: 1`。
3. 文档记录的外置 PhysX GPU `.so` 路径不存在，但当前 SAPIEN/ManiSkill 的 GPU PhysX reset/step 正常。
4. 训练内部小样本评估与固定 50-seed 结果差异较大，checkpoint 选择必须以独立固定种子评估为准。

## 结论

Gate A 已通过：三个 checkpoint 均能通过官方 loader 完成无视频 headless 评估，无 renderer 错误。下一批次执行 Task 5 的 longer-training candidates。
