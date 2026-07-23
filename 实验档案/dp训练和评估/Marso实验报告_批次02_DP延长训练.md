# Marso 实验报告：批次 02 DP 延长训练

- 日期：2026-07-15 至 2026-07-16
- 仓库提交：`6048f33217f26ae39009a812f53c81171517f393`
- 环境：Python 3.10.16，PyTorch 2.6.0+cu126，RTX 3090 24 GB
- 观测与后端：state，GPU PhysX，headless，禁用视频
- 数据：Easy、Medium、Hard 各使用原始 200 条示范
- 评估：固定 seeds 5000-5049，共 50 episodes

## 训练配置与耗时

| 难度 | seed | iterations | batch | horizon | 训练耗时 | 训练内最佳 sort accuracy |
|---|---:|---:|---:|---:|---:|---:|
| Easy | 1 | 50,000 | 256 | 200 | 1h02m17s | 0.5625 |
| Medium | 1 | 75,000 | 256 | 400 | 1h54m27s | 0.2500 |
| Hard | 1 | 100,000 | 256 | 550 | 2h53m16s | 0.0938 |

训练内评估只有 16 episodes，不能代替固定 50-seed 独立评估。

## 固定 50 Seeds 评估

| 难度 | long sort accuracy | baseline | mean sorted | all placed | mis-sort rate | 决策 |
|---|---:|---:|---:|---:|---:|---|
| Easy | 0.170 | 0.170 | 0.34 / 2 | 0.060 | 0.000 | 未严格提高，保留 baseline |
| Medium | 0.080 | 0.110 | 0.32 / 4 | 0.000 | 0.000 | 下降，保留 baseline |
| Hard | 0.040 | 0.037 | 0.24 / 6 | 0.000 | 0.003 | 严格提高，保留 long |

按 Task 5 keep rule，候选配置暂定为：Easy baseline、Medium baseline、Hard long。后续 Task 6-7 的扩充数据候选仍需与这些结果比较。

## Checkpoints

- Easy long：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_easy_long_s1/checkpoints/best_eval_sort_accuracy.pt`
- Medium long：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_medium_long_s1/checkpoints/best_eval_sort_accuracy.pt`
- Hard long：`/data/coding/berlin-marso-hackathon/il/baselines/diffusion_policy/runs/dp_hard_long_s1/checkpoints/best_eval_sort_accuracy.pt`

## 文档与实验注意事项

1. 训练内部小样本评估与固定 50-seed 结果仍有明显偏差；候选保留严格以固定评估为准。
2. Hard 固定评估按指导使用 `num_envs=4`，50 episodes 实际耗时约 35 分钟，是换用更强 GPU 后仍难完全消除的环境仿真开销。
3. Task 5 命令本身可执行，未发现新的阻断性错误。

## 结论

Task 5 已完成。Hard 延长训练取得轻微但严格的提升（0.037 → 0.040）；Easy 持平、Medium 下降。下一批次继续生成并验证 Medium 400 条、Hard 600 条成功示范。
