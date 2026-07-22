# 数据与协议

各难度官方数据各有 200 条示范。state 观测维度为 Easy 54、Medium 72、Hard 90，因此每个难度必须单独训练 state checkpoint。额外生成的 state 数据为 Medium 400 条、Hard 600 条；H5 因体积留在本地，JSON manifest 与 SHA-256 保留在 `experiments/datasets/`。

H5 审计发现原始 action 超出环境声明的 `[-1, 1]` Box。训练必须明确采用回归、裁剪、归一化或转换；不能无说明地用 tanh 有界 policy 拟合这些标签。`terminated` 与 `truncated` 也不能直接当作 RL replay 的 bootstrap 规则。

最终评估使用 `conf/eval/server_50.yaml`：50 episodes、seeds `5000-5049`、无视频、官方 policy loader。记录 `sort_accuracy`、`mean_sorted`、`all_placed_rate` 与 `mis_sort_rate`。训练期 4/8/16-episode 指标只能筛选候选，不能替代此协议。最终日志见 [`evidence/evaluations/`](../evidence/evaluations/)。
