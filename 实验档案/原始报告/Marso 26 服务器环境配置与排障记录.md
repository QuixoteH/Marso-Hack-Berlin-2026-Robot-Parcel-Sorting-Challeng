---
title: Marso 26 服务器环境配置与排障记录
aliases:
  - Marso服务器环境配置
  - WarehouseSort服务器环境
tags:
  - Marso26
  - ManiSkill
  - 强化学习
  - 环境配置
  - RTX3090
date: 2026-07-15
status: 已验证
---

# Marso 26 服务器环境配置与排障记录

> [!success] 当前状态
> 服务器已经能够在 RTX 3090 上运行 `WarehouseSort-v1` 的 GPU PhysX、加载 easy/medium/hard 的 state 数据，并完成 State Diffusion Policy 的前向、反向、参数更新、EMA 和 headless 评估。当前容器缺少 NVIDIA graphics/Vulkan 能力，因此只使用 state 主赛道，不运行 RGB、视频录制或 RGB replay。

## 1. 目标与最终目录

- 官方仓库：[marso-robotics/berlin-marso-hackathon](https://github.com/marso-robotics/berlin-marso-hackathon)
- 项目目录：`/data/coding/berlin-marso-hackathon`
- 数据压缩包：`/data/coding/marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip`
- Conda 环境：`/data/miniconda/envs/marso-rl`
- Conda 环境名：`marso-rl`
- 项目目标：完成 state DP 主赛道，并保留 RGB ACT 离线复现记录。

每次重新登录服务器后执行：

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon
export HDF5_USE_FILE_LOCKING=FALSE
```

## 2. 最终硬件与软件版本

| 项目 | 已验证配置 |
|---|---|
| 系统 | Ubuntu 22.04.4 LTS |
| GPU | NVIDIA GeForce RTX 3090 24 GB |
| 驱动 | 550.76 |
| CPU | 80 vCPU，Intel Xeon E5-2673 v4 |
| 内存 | 377 GiB |
| 数据盘 | 120 GB，配置完成时剩余约 99 GB |
| Python | 3.10.16 |
| PyTorch | 2.6.0+cu126 |
| TorchVision | 0.21.0 |
| ManiSkill | 3.0.1 |
| SAPIEN | 3.0.3 |
| Diffusers | 0.38.0 |
| Gymnasium | 1.3.0 |
| Hydra Core | 1.3.3 |
| OmegaConf | 2.3.1 |
| Pixi | 0.72.2 |

基础检查：

```bash
nvidia-smi
cat /etc/os-release
df -h / /data
free -h
```

PyTorch GPU 检查：

```bash
python - <<'PY'
import torch

print("PyTorch:", torch.__version__)
print("Compiled CUDA:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("GPU:", torch.cuda.get_device_name(0))
x = torch.randn(1024, 1024, device="cuda")
print("GPU matmul:", (x @ x).mean().item())
PY
```

## 3. 克隆官方仓库

服务器访问 GitHub 时优先使用代理：

```bash
mkdir -p /data/coding
cd /data/coding

git clone \
  https://ghproxy.net/https://github.com/marso-robotics/berlin-marso-hackathon.git

cd berlin-marso-hackathon
git rev-parse HEAD
git status --short --branch
```

也可以设置全局 URL 改写：

```bash
git config --global url."https://gh-proxy.com/https://github.com/".insteadOf \
  "https://github.com/"
```

> [!warning]
> 不要对已经包含 headless 修改的工作区执行 `git reset --hard` 或 `git checkout -- <file>`。

## 4. 镜像源配置

### 4.1 pip 清华镜像

服务器以 root 运行，直接写系统配置：

```bash
python -m pip config set global.index-url \
  https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip config set global.trusted-host \
  pypi.tuna.tsinghua.edu.cn
python -m pip config list
```

最终配置位于 `/etc/pip.conf`：

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

### 4.2 Conda 清华镜像

配置文件：`/data/miniconda/.condarc`

```yaml
channels:
  - defaults
show_channel_urls: true
channel_priority: strict
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
```

检查实际配置：

```bash
conda config --show-sources
conda config --show channels
```

### 4.3 Pixi 镜像

Pixi 全局配置：`/root/.pixi/config.toml`

```toml
[mirrors]
"https://conda.anaconda.org/conda-forge" = ["https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge"]

[pypi-config]
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

验证：

```bash
pixi --version
pixi config list
```

### 4.4 npm 镜像（仅供 Codex CLI）

```bash
npm config set registry https://registry.npmmirror.com
npm config get registry
```

## 5. 为什么没有直接使用官方 Pixi 锁定环境

官方仓库当前 `pixi.toml` 选择 Python 3.12，最新 `pixi.lock` 曾解析到 PyTorch 2.12 和 CUDA 13 运行库。服务器驱动 550.76 属于 CUDA 12.x 驱动分支，直接采用该组合存在 CUDA 13 运行库不兼容风险。

最终方案是克隆服务器预装且已验证 CUDA 可用的 `torch` Conda 环境，再安装项目依赖：

```bash
source /data/miniconda/etc/profile.d/conda.sh

conda create --name marso-rl --clone torch -y
conda activate marso-rl

python --version
python -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available())"
```

安装与服务器 CUDA 组合匹配的依赖：

```bash
python -m pip install \
  "torch==2.6.0" \
  "torchvision==0.21.0" \
  "mani-skill==3.0.1" \
  "sapien==3.0.3" \
  "diffusers==0.38.0" \
  "gymnasium==1.3.0" \
  "hydra-core==1.3.3" \
  "omegaconf==2.3.1" \
  "transforms3d==0.4.2" \
  tyro matplotlib tensorboard \
  -i https://pypi.tuna.tsinghua.edu.cn/simple

cd /data/coding/berlin-marso-hackathon
python -m pip install -e . \
  -i https://pypi.tuna.tsinghua.edu.cn/simple

python -m pip check
```

预期：

```text
No broken requirements found.
```

> [!note]
> 项目 `pyproject.toml` 声明 `requires-python = ">=3.10"`，因此 Python 3.10.16 满足项目最低要求。服务器环境的目标是稳定运行，不强制复现官方 Pixi 中的 Python 3.12。

## 6. SAPIEN GPU PhysX 预编译库

SAPIEN 3.0.3 第一次启用 GPU PhysX 时需要：

```text
/root/.sapien/physx/105.1-physx-5.3.1.patch0/libPhysXGpu_64.so
```

安装下载工具：

```bash
apt-get update
apt-get install -y aria2 unzip
```

通过代理多连接下载：

```bash
mkdir -p /data/downloads/physx
cd /data/downloads/physx

aria2c -x 16 -s 16 -k 1M \
  -o linux-so.zip \
  "https://gh-proxy.com/https://github.com/sapien-sim/physx-precompiled/releases/download/105.1-physx-5.3.1.patch0/linux-so.zip"

unzip -t linux-so.zip
mkdir -p /root/.sapien/physx/105.1-physx-5.3.1.patch0
unzip -o linux-so.zip \
  -d /root/.sapien/physx/105.1-physx-5.3.1.patch0

find /root/.sapien/physx/105.1-physx-5.3.1.patch0 \
  -name 'libPhysXGpu_64.so' -ls
```

最终 `libPhysXGpu_64.so` 大小约 `236,705,440` 字节。

如果 ZIP 内还有一层目录，将文件移动到 SAPIEN 期望位置：

```bash
find /root/.sapien/physx/105.1-physx-5.3.1.patch0 \
  -type f -name 'libPhysXGpu_64.so'
```

确保最终路径正好是：

```text
/root/.sapien/physx/105.1-physx-5.3.1.patch0/libPhysXGpu_64.so
```

## 7. Vulkan 限制与 headless 方案

系统安装了 Vulkan 基础包：

```bash
apt-get update
apt-get install -y libvulkan1 mesa-vulkan-drivers vulkan-tools
vulkaninfo --summary
```

当前容器只能看到 Mesa `llvmpipe`，没有 NVIDIA Vulkan graphics capability。这意味着：

| 功能 | 状态 |
|---|---|
| PyTorch CUDA | 可用 |
| GPU PhysX | 可用 |
| state 观测 | 可用 |
| State DP 训练 | 可用 |
| headless state 评估 | 可用 |
| RGB 观测 | 不可用 |
| RGB replay | 不可用 |
| GPU 视频渲染 | 不可用 |

如果重新创建容器，需要平台暴露：

```text
NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics,video
```

或者：

```text
NVIDIA_DRIVER_CAPABILITIES=all
```

当前服务器为兼容 headless state 路径修改了：

- `warehouse_sort/env.py`
  - 无 renderer 时跳过灯光、材质和视觉几何。
  - 保留碰撞几何、机器人、state 观测、奖励和成功判定。
- `warehouse_sort/utils.py`
  - state 且不录制视频时使用 `render_backend="none"`。
- `il/baselines/diffusion_policy/diffusion_policy/make_env.py`
  - state 训练的无视频评估使用 headless renderer 配置。

检查这些修改是否仍在：

```bash
git status --short
git diff -- \
  warehouse_sort/env.py \
  warehouse_sort/utils.py \
  il/baselines/diffusion_policy/diffusion_policy/make_env.py
```

## 8. 比赛数据部署与校验

压缩包：

```text
/data/coding/marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip
```

已验证信息：

```text
大小：407,539,396 bytes
MD5：bbeaaf828fb82dcc2057c47254d86fdf
ZIP 完整性：通过
```

校验并解压：

```bash
cd /data/coding

md5sum marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip
unzip -t marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip

cd /data/coding/berlin-marso-hackathon
mkdir -p il/demos
unzip -o ../marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip \
  -d il/demos
```

每个难度目录都应包含：

```text
trajectory.state.pd_ee_delta_pos.physx_cuda.h5
trajectory.state.pd_ee_delta_pos.physx_cuda.json
trajectory.rgb.pd_ee_delta_pos.physx_cuda.h5
trajectory.rgb.pd_ee_delta_pos.physx_cuda.json
```

检查文件：

```bash
find il/demos -maxdepth 2 -type f -printf '%p %s bytes\n' | sort
```

验证 H5 和 JSON episode 数量一致：

```bash
python - <<'PY'
import glob
import json
import h5py

for json_path in sorted(glob.glob("il/demos/*/*.json")):
    h5_path = json_path[:-5] + ".h5"
    with open(json_path, encoding="utf-8") as f:
        metadata = json.load(f)
    with h5py.File(h5_path, "r") as h5:
        h5_ids = {int(k.split("_")[-1]) for k in h5.keys()}
    json_ids = {ep["episode_id"] for ep in metadata["episodes"]}
    print(json_path, len(json_ids), len(h5_ids), json_ids == h5_ids)
PY
```

预期：easy、medium、hard 的 state 和 RGB 均为 `200 200 True`。

> [!important]
> 仓库原有 easy RGB JSON 曾只有 50 条记录。必须使用比赛压缩包中与 H5 匹配的 200 条 JSON，避免 H5/JSON episode ID 不一致。

## 9. GPU PhysX state 环境验证

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon

python - <<'PY'
import gymnasium as gym
import torch
import warehouse_sort

env = gym.make(
    "WarehouseSort-v1",
    difficulty="easy",
    num_parcels=2,
    fixed_poses=True,
    num_envs=1,
    obs_mode="state",
    control_mode="pd_ee_delta_pos",
    sim_backend="physx_cuda",
    render_backend="none",
    render_mode=None,
)

obs, info = env.reset(seed=1000)
print("observation shape:", obs.shape)
print("observation device:", obs.device)

action = torch.zeros((1, 4), device=obs.device)
obs, reward, terminated, truncated, info = env.step(action)
print("reset: success")
print("step: success")
env.close()
PY
```

预期：

```text
observation shape: (1, 54)
observation device: cuda:0
reset: success
step: success
```

## 10. State Diffusion Policy smoke test

仅验证链路，不代表策略性能：

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon

export HDF5_USE_FILE_LOCKING=FALSE
export WANDB_MODE=disabled

python il/train.py \
  method=dp \
  demo_dir=easy \
  max_episode_steps=2 \
  flags.total_iters=1 \
  flags.eval_freq=1 \
  flags.log_freq=1 \
  flags.save_freq=1 \
  flags.num_eval_envs=1 \
  flags.num_eval_episodes=1 \
  flags.capture_video=false \
  flags.exp_name=smoke_easy_state
```

成功标准：

- easy/state 200 条轨迹被加载。
- 输出约 23,000 transitions。
- 创建约 4.48M 参数的网络和 EMA 网络。
- 完成一次 forward、backward、optimizer step 和 EMA。
- 完成一次 GPU headless 评估。
- 进程退出码为 0。

## 11. 正式训练入口

完成 smoke test 后，先运行 Easy baseline：

```bash
source /data/miniconda/etc/profile.d/conda.sh
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon

export HDF5_USE_FILE_LOCKING=FALSE
export WANDB_MODE=disabled

python il/train.py \
  method=dp \
  demo_dir=easy \
  flags.total_iters=30000 \
  flags.capture_video=false \
  flags.exp_name=dp_easy_baseline
```

正式实验流程见 [项目流程索引](../../项目流程/workflow.md)。

## 12. 常见故障与判断顺序

### `torch.cuda.is_available()` 为 False

1. 运行 `nvidia-smi`。
2. 检查是否激活 `marso-rl`。
3. 检查 `torch.__version__` 是否为 `2.6.0+cu126`。
4. 不要直接安装解析到 CUDA 13 的最新 PyTorch。

### 找不到 `libPhysXGpu_64.so`

检查：

```bash
ls -lh /root/.sapien/physx/105.1-physx-5.3.1.patch0/libPhysXGpu_64.so
```

若不存在，重新执行第 6 节的下载、ZIP 校验和解压步骤。

### Vulkan 只显示 `llvmpipe`

这是租用平台没有向容器挂载 NVIDIA graphics 驱动，不是 Python 包缺失。继续使用 state + `render_backend="none"`；安装更多 Mesa 包不能替代 NVIDIA Vulkan。

### RGB 或视频初始化失败

当前服务器不支持该路径。确认：

```text
obs_mode=state
render_backend=none
flags.capture_video=false
```

### H5/JSON episode 数量不一致

不要修改 H5。重新从比赛 ZIP 提取与 H5 同名的 JSON，再运行第 8 节的校验脚本。

### 系统盘空间不足

训练数据、checkpoint 和缓存放在 `/data`。定期检查：

```bash
df -h / /data
du -sh /root/.cache /data/coding/berlin-marso-hackathon/il/baselines/*/runs 2>/dev/null
```

## 13. 配置完成验收清单

- [x] Ubuntu 22.04 和 RTX 3090 可识别。
- [x] PyTorch 2.6.0+cu126 可以进行 CUDA 计算。
- [x] `marso-rl` 使用 Python 3.10.16。
- [x] ManiSkill 3.0.1 与 SAPIEN 3.0.3 可导入。
- [x] SAPIEN GPU PhysX 预编译库安装完成。
- [x] 比赛 ZIP MD5 与完整性验证通过。
- [x] 6 个 H5 与对应 JSON 均为 200 episodes。
- [x] `WarehouseSort-v1` 可以 GPU reset 和 step。
- [x] easy/state DP 1 iteration smoke test 通过。
- [x] Headless state 训练与评估可用。
- [ ] RGB、视频和 RGB replay：当前容器能力不支持，未纳入本服务器实验范围。

## 14. 相关资料

- [比赛页面](https://www.kaggle.com/competitions/marso-hack-berlin-2026-robot-parcel-sorting-challenge)
- [官方仓库](https://github.com/marso-robotics/berlin-marso-hackathon)
- [ManiSkill 文档](https://maniskill.readthedocs.io/)
