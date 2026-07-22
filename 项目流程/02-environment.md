# Environment

## Recorded Training Host

The verified state workflow used GPU PhysX in headless mode with rendering disabled. This is the recorded experiment stack, not a general minimum requirement:

| Component | Recorded version / setting |
|---|---|
| Python | 3.10.16 |
| PyTorch | 2.6.0+cu126 |
| CUDA | 12.6 |
| ManiSkill | 3.0.1 |
| SAPIEN | 3.0.3 |
| Diffusers | 0.38.0 |
| GPU | RTX 3090, 24 GiB |
| Simulator mode | GPU PhysX, headless state evaluation |

Start a shell with the recorded environment variables:

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
export HDF5_USE_FILE_LOCKING=FALSE
cd /data/coding/berlin-marso-hackathon
```

For a fresh public checkout, use the project-local Pixi workflow shown in the top-level README instead. The server-specific Conda path above is retained because it describes the evidence-producing environment.

## Smoke Checks

Before committing a long run, check the smallest relevant surface:

```bash
pixi install
pixi run install
pixi run python -c "import torch; print(torch.cuda.is_available())"
pixi run python eval.py difficulty=easy \
  policy=examples.random_policy:load_policy \
  eval_config=conf/eval/default.yaml
```

The recorded host completed state reset/step, DP optimization, EMA loading, and headless evaluation. Record the exact package versions and renderer mode for any new host; CUDA availability alone does not establish that RGB evaluation will work.

## Renderer Limitation

The host exposes CUDA compute but did not expose an NVIDIA Vulkan renderer usable by SAPIEN. The ACT evidence log includes warnings for missing Vulkan ICD and GLVND ICD files. State experiments therefore use `render_mode=None` and `render_backend="none"`; no result in this archive relies on a video-rendered state rollout.

| Workflow | Recorded host status | Appropriate claim |
|---|---|---|
| State DP training and headless evaluation | verified | local 50-episode metrics are available |
| ACT offline training and checkpoint loading | verified | optimization and serialization completed |
| ACT RGB environment / video replay | blocked by Vulkan renderer | no closed-loop score is available |

Move the ACT checkpoint to a machine with a functional NVIDIA graphics driver and Vulkan ICD before running RGB evaluation. Do not bypass a renderer failure by treating the absence of a score as score zero. The original environment reports are preserved in [实验档案/原始报告](../实验档案/原始报告/).
