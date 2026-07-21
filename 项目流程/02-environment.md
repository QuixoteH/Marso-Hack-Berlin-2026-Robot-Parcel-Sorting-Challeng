# Environment

The verified state workflow used GPU PhysX in headless mode with rendering disabled. The recorded software stack was Python 3.10.16, PyTorch 2.6.0+cu126, ManiSkill 3.0.1, SAPIEN 3.0.3, Diffusers 0.38.0, and an RTX 3090 with 24 GiB of VRAM.

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
export HDF5_USE_FILE_LOCKING=FALSE
cd /data/coding/berlin-marso-hackathon
```

State reset, step, DP optimisation, EMA, and headless evaluation were smoke-tested. The host exposes CUDA compute but not a Vulkan renderer usable by SAPIEN. State experiments therefore set `render_mode=None` and `render_backend="none"`; RGB evaluation and video replay must be run elsewhere.

The original environment reports are preserved in [实验档案/原始报告](../实验档案/原始报告/).
