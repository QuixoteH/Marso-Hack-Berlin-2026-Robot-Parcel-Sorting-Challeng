# 发布与提交

公开 state 提交使用 [`submission.yaml`](../submission.yaml) 与 `warehouse_sort.il_policy:load_dp`。仓库包含源码、配置、manifest、结果 CSV、紧凑日志、派生图和 SHA-256；不含 checkpoint、原始 H5 与 submission tarball。

195 MiB submission archive 与 133 MiB ACT checkpoint 超出 GitHub 100 MiB 单文件限制。DP checkpoint 虽为 35–38 MiB，也有意不进入普通 Git，以保持 clone 可用；所有获取位置与完整性锚点见 [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md)。

提交前：恢复三个 DP checkpoint；用 `sha256sum -c experiments/checkpoints/SHA256SUMS` 核验；确认 `submission.yaml` 路径与 loader import；在 clean environment 运行 Easy/Medium/Hard 的官方评估并保存日志。发布独立仓库或 fork，不要直接推送至上游挑战仓库。
