# 评估与选择

训练期指标使用的 episode 数较少，与固定 50-seed 评估存在明显偏差。例如 DP Easy baseline 的训练期数值显著高于首次独立本地评估。

使用 `conf/eval/server_50.yaml`，关闭视频，保留精确 seed，并同时记录 `sort_accuracy` 与 `mean_sorted`。不得把本地加权值写成 Kaggle leaderboard 成绩；Easy/Medium/Hard 权重固定为 `0.20/0.30/0.50`。
