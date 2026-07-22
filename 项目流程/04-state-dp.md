# 状态 Diffusion Policy

## 目标与范围

state DP 是本档案中已完成且可提交的主路径。它将 privileged 低维 state 观测映射为末端执行器动作序列。Easy、Medium、Hard 的 state 维度不同，不能共享 checkpoint。本文记录实际训练与评估，不将 state DP 与 RGB ACT 作为公平算法排名。

训练入口为 `il/train.py method=dp`，配置位于 [`il/conf/method/dp.yaml`](../il/conf/method/dp.yaml)，提交 loader 为 `warehouse_sort.il_policy:load_dp`，三个 checkpoint 路径在 [`submission.yaml`](../submission.yaml)。

## 训练候选

```bash
pixi run python il/train.py method=dp demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=256 \
  flags.exp_name=dp_easy_baseline_s1

pixi run python il/train.py method=dp demo_dir=hard \
  flags.seed=3 flags.total_iters=100000 flags.batch_size=512 \
  flags.exp_name=dp_hard_aug_b512_s3
```

默认设置为 observation horizon 2、action horizon 8、prediction horizon 16。训练期 16-episode 指标仅用于筛选，最终选择必须遵循 [03-data-and-protocol.md](03-data-and-protocol.md) 的 50-episode 协议。

## 候选证据

![State DP 固定 50-episode 候选成绩](../evidence/figures/dp_candidate_scores.png)

该图由 [`experiments/results.csv`](../experiments/results.csv) 生成，记录 phase、难度、seed、示范数、迭代数、batch size、checkpoint 与 `sort_accuracy`。证据显示：更长训练并非普遍改进；Medium 的 400-demo 候选低于 200-demo baseline；Hard 的 600-demo 与 batch 512 路径得到保留。该图是 CSV 派生图，不是 TensorBoard 输出。

## 最终 checkpoint 与复验

选定 checkpoint 使用官方 loader 在 clean shell 复验：Torch/CUDA RNG seed 0、50 diffusion inference steps、50 episodes、seeds `5000-5049`、关闭视频。Easy 的第二次运行一致；原始日志公开在 [`evidence/evaluations/`](../evidence/evaluations/)。

| 难度 | checkpoint | `sort_accuracy` | 平均正确分拣 |
|---|---|---:|---:|
| Easy | `state_easy_best.pt` | 0.390 | 0.78 / 2 |
| Medium | `state_medium_best.pt` | 0.090 | 0.36 / 4 |
| Hard | `state_hard_best.pt` | 0.103 | 0.62 / 6 |

```bash
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=experiments/checkpoints/state_easy_best.pt \
  eval_config=conf/eval/server_50.yaml
```

恢复二进制后先以 [`experiments/checkpoints/SHA256SUMS`](../experiments/checkpoints/SHA256SUMS) 核验。上述结果仅证明本地固定协议，且三个最终日志中的 `all_placed_rate` 都为零；不得称为 held-out leaderboard 成绩或完整 episode 成功率。
