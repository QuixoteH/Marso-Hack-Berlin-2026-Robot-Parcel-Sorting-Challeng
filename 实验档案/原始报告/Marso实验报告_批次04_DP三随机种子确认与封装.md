# Marso 实验报告：批次 04 DP 三随机种子确认与封装

- 完成时间：2026-07-18 03:28 +0800
- 固定评估：seeds 5000-5049，50 episodes，headless state 环境

## 最终 DP 结果

| 难度 | 最高固定评估 sort accuracy |
|---|---:|
| Easy | 0.300 |
| Medium | 0.110 |
| Hard | 0.107 |

DP 加权最高分：`0.1465`。

最终 checkpoint、SHA-256、完整 CSV 与归档位于 `berlin-marso-hackathon/experiments/checkpoints/`、`berlin-marso-hackathon/experiments/results.csv` 和 `berlin-marso-hackathon/experiments/marso_dp_checkpoints.tar.gz`。每个最终 checkpoint 已通过干净的 50-episode loader 复验。
