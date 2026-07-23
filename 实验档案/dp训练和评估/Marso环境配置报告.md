# Marso Hack Berlin 2026 环境配置报告

生成日期：2026-07-15  
项目目录：`/data/coding/berlin-marso-hackathon`  
数据压缩包：`/data/coding/marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip`

## 1. 当前结论

服务器已经具备运行主赛道 state Diffusion Policy 的条件，可以开始 easy、medium、hard 三个难度的训练与无视频评估。

已完成以下端到端验证：

- PyTorch 能在 RTX 3090 上创建和计算 CUDA 张量。
- `WarehouseSort-v1` 能使用 GPU PhysX 创建、reset 并执行 step。
- easy/state 的 200 条轨迹能够被训练脚本完整加载。
- 已执行 1 iteration smoke test，成功完成前向传播、反向传播、参数更新、EMA 和评估。
- 6 个 H5 数据集均可读取，且每个 H5 都与对应 JSON 一致包含 200 条轨迹。

当前主要限制是容器没有挂载 NVIDIA Vulkan 图形驱动能力。state 主赛道通过 headless 模式正常运行；RGB 观测和视频录制暂不可用。

## 2. 服务器硬件与系统

| 项目 | 当前配置 | 状态 |
|---|---|---|
| 操作系统 | Ubuntu 22.04.4 LTS | 符合 |
| GPU | NVIDIA GeForce RTX 3090 | 符合 |
| GPU 显存 | 24 GB | 符合 |
| NVIDIA 驱动 | 550.76 | 符合 CUDA 12.x 计算 |
| CPU | 80 vCPU，Intel Xeon E5-2673 v4 | 充足 |
| 内存 | 377 GiB | 充足 |
| 数据盘 | 120 GB，总剩余约 99 GB | 当前充足 |
| 系统盘 | 30 GB，总剩余约 17 GB | 当前充足 |

`nvidia-smi` 与 PyTorch CUDA 测试均正常。PyTorch 实际识别：

```text
GPU: NVIDIA GeForce RTX 3090
PyTorch: 2.6.0+cu126
Compiled CUDA: 12.6
CUDA available: True
```

## 3. 项目与版本选择

官方仓库：

```text
https://github.com/marso-robotics/berlin-marso-hackathon.git
```

服务器驱动属于 CUDA 12.x 驱动分支，而仓库最新 `pixi.lock` 原本解析到 PyTorch 2.12 和 CUDA 13 运行库。为避免 CUDA 13 与驱动不兼容，项目配置调整为：

```text
torch       2.6.0
torchvision 0.21.0
mani-skill  3.0.1
sapien      3.0.3
diffusers   0.38.0
gymnasium   1.3.0
hydra-core  1.3.3
omegaconf   2.3.1
```

最终实际使用的是独立 Conda 环境：

```text
环境名: marso-rl
路径: /data/miniconda/envs/marso-rl
Python: 3.10.16
```

项目 `pyproject.toml` 要求 Python `>=3.10`，因此该环境满足项目声明。独立环境由服务器预装且已验证 CUDA 可用的 `torch` 环境克隆，然后补装项目依赖，不会污染原始环境。

激活方式：

```bash
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon
```

依赖一致性检查结果：

```text
No broken requirements found.
```

## 4. 镜像源配置

### pip

系统级配置文件：`/etc/pip.conf`

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

### Conda

配置文件：`/data/miniconda/.condarc`

已配置：

- 清华 `defaults` 镜像
- 清华 `conda-forge` 镜像
- `channel_priority: strict`
- 显示实际下载 channel URL

### Pixi

Pixi 版本：`0.72.2`

全局配置：`/root/.pixi/config.toml`

```toml
[mirrors]
"https://conda.anaconda.org/conda-forge" = ["https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge"]

[pypi-config]
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
```

项目 `pixi.toml` 也显式设置了清华 PyPI 地址，重新生成的 `pixi.lock` 中 PyPI 下载地址已指向清华镜像。

### npm

```text
https://registry.npmmirror.com
```

Node.js 和 npm 仅用于 Codex CLI，本机器人学习项目本身当前不需要 npm 依赖。

### GitHub

Git 全局配置会把 GitHub HTTPS 地址自动改写到代理：

```text
https://github.com/...
  -> https://gh-proxy.com/https://github.com/...
```

普通 `git clone`、`git fetch` 和 `git pull` 命令无需手工修改 URL。

## 5. SAPIEN 与 PhysX 配置

SAPIEN 3.0.3 首次启用 GPU PhysX 时需要额外的预编译库：

```text
/root/.sapien/physx/105.1-physx-5.3.1.patch0/libPhysXGpu_64.so
```

文件大小：`236,705,440` 字节。

GitHub Release 单连接下载速度过低，最终通过 `gh-proxy.com` 和 `aria2c` 多连接下载，并通过 ZIP 完整性测试后解压安装。

系统另外安装了：

```text
libvulkan1
mesa-vulkan-drivers
vulkan-tools
aria2
```

Mesa Vulkan 只能提供 CPU `llvmpipe`，不能替代未挂载的 NVIDIA Vulkan 图形驱动。state 模式不需要 renderer，因此通过 `render_backend="none"` 运行。

## 6. 比赛数据

数据通过服务器已有的 `bypy 1.8.9` 从百度网盘下载。

远端文件：

```text
marso-hack-berlin-2026-robot-parcel-sorting-challenge.zip
```

下载结果：

```text
大小: 407,539,396 bytes
本地 MD5: bbeaaf828fb82dcc2057c47254d86fdf
ZIP 完整性: 通过
```

解压目录：

```text
/data/coding/berlin-marso-hackathon/il/demos/easy
/data/coding/berlin-marso-hackathon/il/demos/medium
/data/coding/berlin-marso-hackathon/il/demos/hard
```

每个难度均包含：

```text
trajectory.state.pd_ee_delta_pos.physx_cuda.h5
trajectory.state.pd_ee_delta_pos.physx_cuda.json
trajectory.rgb.pd_ee_delta_pos.physx_cuda.h5
trajectory.rgb.pd_ee_delta_pos.physx_cuda.json
```

验证结果：

| 难度 | state | RGB |
|---|---:|---:|
| easy | 200 条 | 200 条 |
| medium | 200 条 | 200 条 |
| hard | 200 条 | 200 条 |

仓库原有 easy RGB JSON 只有 50 条记录，已使用比赛包中与 H5 匹配的 200 条版本更新。

## 7. Headless 兼容修改

由于租用平台只向容器暴露 NVIDIA compute 能力，没有暴露 graphics/Vulkan 能力，默认环境初始化会在创建 renderer 时失败。

已做以下兼容修改：

- `warehouse_sort/env.py`
  - 无 renderer 时跳过灯光、材质和视觉几何。
  - 保留全部碰撞几何、机器人、物理状态、state 观测、奖励与成功判断。
- `warehouse_sort/utils.py`
  - state 且不录制视频时自动使用 `render_backend="none"`。
- `il/baselines/diffusion_policy/diffusion_policy/make_env.py`
  - state 训练的无视频评估自动使用 headless renderer 配置。
- `.gitignore`
  - 忽略训练 `runs/`、H5 和下载生成的 demo JSON，避免误提交大文件及本地数据。

这些修改不会改变有正常 NVIDIA Vulkan 驱动时的 RGB/视频路径。

## 8. 已完成的验证

### GPU state 环境

验证参数：

```text
env_id: WarehouseSort-v1
difficulty: easy
obs_mode: state
control_mode: pd_ee_delta_pos
sim_backend: physx_cuda
render_backend: none
num_envs: 1
```

结果：

```text
observation shape: (1, 54)
observation device: cuda:0
reset: success
step: success
```

### Diffusion Policy 冒烟测试

测试内容：

- 加载 easy/state 200 条轨迹。
- 共读取 23,000 transitions。
- 创建约 4.48M 参数的策略网络和 EMA 网络。
- 完成 1 iteration 训练。
- 完成 1 episode、2 steps 的 GPU headless 评估。

结果：

```text
loss: 约 1.31
process exit code: 0
```

该测试仅用于验证训练链路，不代表策略性能。

## 9. 当前限制

### 可正常执行

- state 数据训练
- GPU PhysX 并行仿真
- 无视频 state 评估
- easy、medium、hard 独立模型训练
- TensorBoard 日志与 checkpoint 保存

### 暂不可执行

- RGB 观测训练
- NVIDIA GPU Vulkan 渲染
- 评估视频录制
- RGB 示范 replay

原因是当前容器没有挂载 NVIDIA Vulkan/graphics 驱动库，而不是 Python 环境缺包。若要启用这些功能，需要租用平台以类似以下能力重新创建容器：

```text
NVIDIA_DRIVER_CAPABILITIES=compute,utility,graphics,video
```

或直接设置：

```text
NVIDIA_DRIVER_CAPABILITIES=all
```

## 10. 后续实验入口

进入环境：

```bash
conda activate marso-rl
cd /data/coding/berlin-marso-hackathon
```

建议首先训练 easy/state：

```bash
python il/train.py \
  method=dp \
  demo_dir=easy \
  flags.capture_video=false
```

medium 和 hard 需要分别训练独立模型，并为每个实验使用不同的 `flags.exp_name`。

当前未启动正式训练，等待进一步实验指令。
