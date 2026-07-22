# WarehouseSort 实验流程

本索引按执行顺序组织工作，区分可复现事实与历史结论；完整原始报告保留在 [实验档案](../实验档案/README.md)。先阅读 [evidence](../evidence/README.md) 的公开证据，再通过下列阶段文档复现或审阅每个决定。

| 阶段 | 文档 | 结果 |
|---|---|---|
| 1 | [01-task-and-evaluation.md](01-task-and-evaluation.md) | Task contract, metrics, and fair-comparison boundary |
| 2 | [02-environment.md](02-environment.md) | Headless state environment verified; RGB renderer unavailable |
| 3 | [03-data-and-protocol.md](03-data-and-protocol.md) | Demo audit, fixed 50-seed evaluation, data handling rules |
| 4 | [04-state-dp.md](04-state-dp.md) | Three-difficulty state DP selection and independent recheck |
| 5 | [05-act.md](05-act.md) | ACT offline reproduction and evaluation boundary |
| 6 | [07-release-and-submission.md](07-release-and-submission.md) | Submission packaging and GitHub release boundary |

从任务约定开始，再使用方法文档获取准确命令、选定配置、结果边界与保留证据。公开 DP 图由 `experiments/results.csv` 生成；ACT 曲线来自保存的训练日志，不是 TensorBoard 导出。
