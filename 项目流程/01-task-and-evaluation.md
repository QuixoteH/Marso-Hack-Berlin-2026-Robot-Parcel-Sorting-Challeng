# 任务与评估

WarehouseSort 要求 Franka Panda 将每个包裹放入颜色匹配的箱子。控制模式为 `pd_ee_delta_pos`：三个末端执行器 Δ位置分量加一个夹爪分量。

| 难度 | 包裹 | horizon | 泛化压力 |
|---|---:|---:|---|
| Easy | 2 | 200 | 固定布局 |
| Medium | 4 | 400 | 包裹 XY 扰动 |
| Hard | 6 | 550 | XY/yaw 扰动与箱子侧边互换 |

`sort_accuracy` 为最终正确放入匹配箱子的包裹比例。抓住包裹、停在箱子上方、掉落或放入错误颜色箱子都不算成功。辅助指标包括 `mean_sorted/episode`、`all_placed_rate` 与 `mis_sort_rate`。

state 赛道使用 privileged 低维几何/颜色信息；RGB ACT 需从图像与 proprioception 推断它们，不可作为纯算法比较。挑战加权为 `0.20 * Easy + 0.30 * Medium + 0.50 * Hard`。本仓库报告使用官方 loader、seeds `5000-5049`、50 episodes、无视频；它们是本地证据，不是 held-out Kaggle 结果。
