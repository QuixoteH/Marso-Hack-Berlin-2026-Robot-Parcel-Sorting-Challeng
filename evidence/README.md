# 公开证据索引

此目录保存从 `warehouse-sort-dp-act-key-artifacts-2026-07-21.zip` 提取的紧凑、可审阅证据；不包含其中体积较大的 checkpoint 二进制文件。

| 项目 | 压缩包内来源 | 用途 |
|---|---|---|
| `evaluations/` | `dp/evaluation_logs/` | 最终 DP 的 clean-shell、50-episode 评估 |
| `act/act_easy_training.log` | `act/training/训练日志_final.log` | ACT Easy 离线优化日志 |
| `figures/dp_candidate_scores.png` | `experiments/results.csv` | 从版本化 CSV 生成的 DP 候选成绩图 |
| `figures/act_easy_loss.png` | `act/act_easy_training.log` | 从复制的终端日志生成的 ACT loss 图 |

压缩包不含 `events.out.tfevents.*`，因此两张图都不是 TensorBoard 导出，且已明确标注为 CSV/日志派生。输入变化后可重新生成：

```bash
python scripts/generate_evidence_figures.py
```

## 解读规则

- DP 图中的 `sort_accuracy` 来自固定本地 50-episode 运行，不是 Kaggle leaderboard 分数。
- ACT 曲线只证明记录的 30,000 次离线优化完成，不能证明闭环抓取或分拣成功。
- 对应 checkpoint 的 SHA-256 位于 [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md)；二进制仍不进 Git，原因是 ACT 文件为 133 MiB，DP 文件为 35–38 MiB。
