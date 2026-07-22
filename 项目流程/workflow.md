# WarehouseSort Experiment Workflow

This index presents the work in execution order. It distinguishes reproducible facts from historical conclusions; full primary reports remain in [实验档案](../实验档案/README.md). For a compact public proof bundle, start with [evidence](../evidence/README.md), then use the stage documents below to reproduce or audit each decision.

| Stage | Document | Outcome |
|---|---|---|
| 1 | [01-task-and-evaluation.md](01-task-and-evaluation.md) | Task contract, metrics, and fair-comparison boundary |
| 2 | [02-environment.md](02-environment.md) | Headless state environment verified; RGB renderer unavailable |
| 3 | [03-data-and-protocol.md](03-data-and-protocol.md) | Demo audit, fixed 50-seed evaluation, data handling rules |
| 4 | [04-state-dp.md](04-state-dp.md) | Three-difficulty state DP selection and independent recheck |
| 5 | [05-act.md](05-act.md) | ACT offline reproduction and evaluation boundary |
| 6 | [07-release-and-submission.md](07-release-and-submission.md) | Submission packaging and GitHub release boundary |

Start with the task contract, then use the method documents for exact commands, selected configurations, result boundaries, and preserved evidence. The published DP figures are derived from `experiments/results.csv`; the ACT curve is derived from the captured training log, not TensorBoard exports.
