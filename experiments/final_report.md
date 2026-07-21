# Marso Final Experiment Report

完成时间：2026-07-18T04:09:14+08:00

## Final Policy

三个难度均选择 State Diffusion Policy（DP）。最终封存结果以官方 loader、固定 50 episodes 和无视频 headless 环境为准。

## Final Verification

最终 DP checkpoint 使用官方 loader 在无训练进程的干净 shell 中完成固定 50-episode、无视频复验：Easy 0.390、Medium 0.090、Hard 0.103。评估显式固定 Torch/CUDA RNG seed 为 0，并重复 Easy 得到相同分数。按计划权重 0.50 / 0.30 / 0.20 计算，加权分数为 0.2421。

| Level | Method | Source checkpoint | Final checkpoint | Fixed-50 score | SHA-256 |
|---|---|---|---|---:|---|
| Easy | DP | `il/baselines/diffusion_policy/runs/dp_easy_baseline_s3/checkpoints/best_eval_sort_accuracy.pt` | `experiments/checkpoints/state_easy_best.pt` | 0.390 | `118895f645c1852f94cb94f3e9563172626fa641b35e98fa66f241d5b82250ab` |
| Medium | DP | `il/baselines/diffusion_policy/runs/dp_medium_baseline_s1/checkpoints/best_eval_sort_accuracy.pt` | `experiments/checkpoints/state_medium_best.pt` | 0.090 | `a3e6791d9485c90d1c501b362277baa4fe0cf7a4624abd30360daea1b3544246` |
| Hard | DP | `il/baselines/diffusion_policy/runs/dp_hard_aug_b512_s3/checkpoints/best_eval_sort_accuracy.pt` | `experiments/checkpoints/state_hard_best.pt` | 0.103 | `4019d3599ee9f5dd4e74711c95c347bf40edea8349235cd6e578674ed485bb00` |

完整逐次训练和评估记录在 `experiments/results.csv`；最终确定性加载复验日志在 `experiments/logs/eval_dp_*_best_deterministic.log`；哈希清单在 `experiments/checkpoints/SHA256SUMS`。

## Reproducibility

- Official base commit: `6048f33217f26ae39009a812f53c81171517f393`。
- Environment: Python 3.10.16, PyTorch 2.6.0+cu126, CUDA 12.6, ManiSkill 3.0.1, SAPIEN 3.0.3, RTX 3090 24 GiB.
- Demonstration datasets: Easy 200, Medium 400, Hard 600 successful state trajectories.
- Submission archive: `experiments/marso_final_submission.tar.gz`; its SHA-256 is stored alongside it in `experiments/marso_final_submission.tar.gz.sha256`.
- Local copy command: `scp root@SERVER_IP:/data/coding/berlin-marso-hackathon/experiments/marso_final_submission.tar.gz /home/quixoteh/desktop/`

## Limitations

服务器缺少可用的 NVIDIA Vulkan graphics 配置，实验和提交均使用 state/headless 路径；未声明或依赖 RGB 渲染能力。工作树包含本实验所需的未提交环境和训练代码改动，详情见 `git status --short`。
