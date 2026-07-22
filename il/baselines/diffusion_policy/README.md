# Diffusion Policy

本目录包含基于论文 [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion](https://arxiv.org/abs/2303.04137v4) 的实现，改编自[原始代码](https://github.com/real-stanford/diffusion_policy)。

## 安装

```bash
conda create -n diffusion-policy-ms python=3.9
conda activate diffusion-policy-ms
pip install -e .
```

## 使用说明

ManiSkill imitation learning 的数据、预处理和评估说明见[官方文档](https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html)。WarehouseSort 的实际训练命令、参数和最终证据见 [项目流程/04-state-dp.md](../../../项目流程/04-state-dp.md)。

示范速度较慢时，请通过 `--max-episode-steps` 增大 episode 上限；通常设为训练示范平均长度的约两倍。RGB+Depth 路径在本仓库中未完成调优或验证；公开完成的主路径是 state DP。

## 引用

使用该 baseline 时请引用原论文：Chi et al., *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*, RSS 2023。
