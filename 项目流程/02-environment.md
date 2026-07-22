# 环境

## 记录的训练主机

已验证 state workflow 使用 GPU PhysX、headless 运行并关闭渲染。记录环境为 Python 3.10.16、PyTorch 2.6.0+cu126、CUDA 12.6、ManiSkill 3.0.1、SAPIEN 3.0.3、Diffusers 0.38.0，以及 RTX 3090 24 GiB。

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
export HDF5_USE_FILE_LOCKING=FALSE
cd /data/coding/berlin-marso-hackathon
```

上述 Conda 路径属于证据产生服务器；fresh public checkout 请使用 README 中的 Pixi 命令。新主机应记录 package version 与 renderer mode，不能只凭 CUDA 可用即判定 RGB 可评估。

## Smoke check

```bash
pixi install
pixi run install
pixi run python -c "import torch; print(torch.cuda.is_available())"
pixi run python eval.py difficulty=easy \
  policy=examples.random_policy:load_policy \
  checkpoint=ignored \
  eval_config=conf/eval/default.yaml
```

记录主机已验证 state reset/step、DP optimization、EMA load 与 headless evaluation。

## Renderer 限制

该主机有 CUDA compute，却没有 SAPIEN 可用的 NVIDIA Vulkan renderer。ACT 日志包含缺失 Vulkan ICD 和 GLVND ICD 的告警。因此 state 实验使用 `render_mode=None` 与 `render_backend="none"`；ACT 离线训练可运行，但 RGB environment 与 video replay 不能在该机验证。不要用 CPU `llvmpipe` 替代，因为它不能与这里的 CUDA 路径互操作。请将 ACT/RGB 评估迁移至 graphics-capable NVIDIA host。

原始环境记录保留在 [实验档案/原始报告](../实验档案/原始报告/)。
