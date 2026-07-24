# 数据目录、文件格式与训练评估命令

本文说明 WarehouseSort 的示范数据在什么位置、同级文件为何必须成对存在、State DP 与 RGB ACT 分别读取什么数据，以及本项目实际使用的训练和评估命令。除非明确说明，路径均相对于仓库根目录。

## 1. 总体目录关系

```text
warehouse-sort-dp-act/
├── il/
│   ├── demos/                         # 官方 Kaggle 示范的本地工作目录
│   │   ├── easy/
│   │   ├── medium/
│   │   └── hard/
│   ├── train.py                       # Hydra 调度器：选择方法并定位 H5
│   ├── gen_demos.py                   # scripted policy 录制、重放和媒体导出
│   ├── filter_successful_trajectories.py # 只保留成功轨迹并合并数据
│   └── baselines/
│       ├── diffusion_policy/          # State DP 训练实现
│       └── act/                       # RGB ACT 训练实现
├── experiments/
│   ├── datasets/                      # 本项目额外生成的 state 数据的 JSON/hash 记录
│   ├── checkpoints/                   # 最终 DP checkpoint 的 SHA-256 清单
│   └── results.csv                    # 所有 DP 候选的固定 50-seed 结果
├── evidence/                          # 已公开的日志、图和最终评估输出
├── media/                             # MP4/GIF，仅供人查看，不用于训练
└── conf/
    ├── eval/server_50.yaml            # 固定 50-episode 本地评估协议
    └── method/{dp,act_rgb}.yaml       # 两个训练入口的默认参数
```

大体积 H5、checkpoint binary 和视频不会提交到 Git。公开仓库保留其相邻 JSON、SHA-256、训练日志和复跑命令；二进制来源与校验值见 [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md)。

## 2. 官方示范目录与同名文件

官方数据下载后，每个难度目录的逻辑结构如下：

```text
il/demos/easy/
├── trajectory.state.pd_ee_delta_pos.physx_cuda.h5
├── trajectory.state.pd_ee_delta_pos.physx_cuda.json
├── trajectory.rgb.pd_ee_delta_pos.physx_cuda.h5
└── trajectory.rgb.pd_ee_delta_pos.physx_cuda.json
```

Medium 和 Hard 使用相同结构。官方每个难度各有 200 条示范；官方 state 与 RGB 数据的 episode ID 对齐，表示相同专家操作的两种观测版本，而不是两套不同动作标签。

文件名格式为：

```text
trajectory.<观测表示>.<控制模式>.<物理后端>.<文件格式>
```

| 片段 | 含义 |
|---|---|
| `state` 或 `rgb` | 策略可读取的观测表示 |
| `pd_ee_delta_pos` | 末端执行器三维增量位移加夹爪控制，动作维度为 4 |
| `physx_cuda` | 示范生成或重放所用的 GPU PhysX 后端 |
| `.h5` | 按时间步存放的大型数组数据 |
| `.json` | 环境、episode、seed 和成功标记等元数据 |

`.h5` 和同名 `.json` 是一个不可拆分的数据集单元。`il/train.py` 会从 H5 相邻位置读取 JSON，以核对 `control_mode` 并把记录的包裹数、固定/随机位姿和随机化范围带入训练期评估环境。不要只复制 H5，或把 JSON 留在另一目录。

## 3. HDF5 与 JSON 内部内容

一个 H5 中按 episode 保存 `traj_0`、`traj_1` 等 group，逻辑结构如下。具体 `obs` 子键随 raw recording、state replay 或 RGB replay 略有不同，但语义相同。

```text
trajectory.*.h5
├── traj_0/
│   ├── obs/           # 每一步观测
│   ├── actions        # 专家动作，shape 约为 (T, 4)
│   ├── env_states     # 可恢复仿真器的完整状态
│   ├── dones          # 轨迹结束信息
│   └── infos          # 环境记录
├── traj_1/
└── ...
```

观察序列通常有 `T+1` 项，动作序列有 `T` 项：策略在 `obs[t]` 后执行 `actions[t]`，得到 `obs[t+1]`。`env_states` 用于重放和恢复场景，不是 DP 或 ACT 的监督目标；`success`、episode ID 和 seed 位于 JSON 的 `episodes` 中，主要用于审计与筛除失败示范。

JSON 至少保存 `env_info.env_kwargs`、`episodes`、每个 episode 的 `episode_id`、seed 和 `success`。JSON 中的 `episode_id` 对应 H5 中的 `traj_<episode_id>`，因此可以验证“该 H5 group 对应哪个场景和是否成功”。

## 4. raw、state、RGB 与视频之间的关系

生成额外示范时，`il/gen_demos.py` 的流程是：

```text
scripted waypoint policy
  -> RecordEpisode 记录 raw trajectory.h5 + trajectory.json
  -> replay_trajectory 重放相同动作和 env_states
      -> trajectory.state.h5  或  trajectory.rgb.h5
  -> 可选导出 MP4/GIF
```

raw trajectory 的重点是动作与完整 `env_states`；重放阶段用相同的场景和动作重新构造训练所需的观测。state replay 不需要 renderer；RGB replay 必须渲染 scene camera。

`media/*.mp4` 和 `media/*.gif` 是给人检查 scripted policy、演示或失败案例的可视化文件，**不被 DP 或 ACT loader 读取**。ACT 读取的是 RGB H5 内每个时间步的图像 array，而不是 MP4。相机原始图像为 `128x128`；ACT 在训练时 resize 到 `224x224` 以适配 ResNet-18。

## 5. DP 与 ACT 各自使用的数据字段

| 方法 | 读取的 H5 | 输入 | 监督目标 | 不使用的内容 |
|---|---|---|---|---|
| State DP | `trajectory.state...h5` | 低维 privileged state | 未来动作序列 | RGB 图像、MP4/GIF、`env_states` |
| RGB ACT | `trajectory.rgb...h5` | scene RGB 加机器人 proprioception | 未来动作 chunk | 包裹/箱子的 privileged 精确状态、MP4/GIF、`env_states` |

State DP 的 state 包含机器人关节与夹爪状态、TCP 位姿、抓取标记、每个包裹的精确位姿和标签、两个 bin 的精确位置和颜色。其维度为 Easy 54、Medium 72、Hard 90，因此三个难度不能共享 state checkpoint。

RGB ACT 只看到 scene camera RGB 与机器人自身状态；它看不到包裹精确位姿、包裹标签 one-hot 或 bin 精确坐标，必须从像素推断这些信息。

在一个训练样本中：

```text
State DP:  obs[t-1], obs[t] -> actions[t : t+16]
RGB ACT:   rgb[t] + proprioception[t] -> actions[t : t+30]
```

DP 的默认 observation horizon 为 2、prediction horizon 为 16、action horizon 为 8；部署时执行预测序列前 8 步再重新观测。ACT 的 `num_queries=30`，用当前观测监督后续 30 步专家动作。二者学习的动作标签均来自相同的 `pd_ee_delta_pos` action 数据。

## 6. 扩充数据的目录、格式和审计链路

扩充数据仅为 **state** 路线生成，原因是当时服务器没有可用 NVIDIA Vulkan renderer，不能稳定生成 RGB 观测。因此 Medium/Hard 扩充数据可以训练 DP，不能直接补充 ACT 训练。

```text
experiments/datasets/
├── medium_seed2000_n400/
│   ├── trajectory.h5              # 服务器归档中的 400 条 state 成功轨迹
│   └── trajectory.json            # 已保留在 Git：400 条、400 个唯一 seed
├── hard_seed2000_n600/
│   ├── trajectory.h5              # 首轮：576 成功、24 失败
│   └── trajectory.json
├── hard_seed2000_failed24_h900/
│   ├── trajectory.h5              # 将原 24 个失败 seed 延长 horizon 后的诊断批次
│   └── trajectory.json
├── hard_seed2600_n30_replacements/
│   ├── trajectory.h5              # 新 seed 的替代成功轨迹
│   └── trajectory.json
└── hard_seed2000_n600_success/
    ├── trajectory.h5              # 最终 Hard 600 条成功 state 轨迹
    └── trajectory.json            # 已保留在 Git：600 条、600 个唯一 seed
```

H5 binary 位于服务器归档，Git 只保留 JSON manifest 以避免提交数百 MiB 数据。最终 Medium H5 为 77,980,741 bytes，Hard H5 为 212,317,595 bytes；相应 SHA-256 和生成过程见[批次 03 报告](../实验档案/dp训练和评估/Marso实验报告_批次03_扩充示范数据.md)。

Hard 的最终数据集不是直接相信“600 条录制完成”：首轮 seeds `2000-2599` 中只有 576 条成功；对 24 条失败 seed 把 horizon 从 550 提高到 900 后只恢复 2 条，说明问题不只是时间上限。随后使用 seeds `2600-2629` 生成替代轨迹，并用 `il/filter_successful_trajectories.py` 按 JSON `success` 字段复制 H5 的成功 `traj_*` group，最终得到 600 条全成功、seed 唯一的训练集。原始、失败诊断和替代批次均被保留，未覆盖。

扩充数据训练需显式传入完整 H5 路径，并让同名 JSON 位于 H5 旁：

```bash
pixi run python il/train.py method=dp \
  demo_path=/data/coding/berlin-marso-hackathon/experiments/datasets/hard_seed2000_n600_success/trajectory.h5 \
  flags.seed=3 flags.total_iters=100000 flags.batch_size=512 \
  flags.exp_name=dp_hard_aug_b512_s3 flags.capture_video=false
```

## 7. 从安装到训练的命令

环境为 Python 3.10.16、PyTorch 2.6.0+cu126、ManiSkill 3.0.1、SAPIEN 3.0.3。以下命令从仓库根目录执行：

```bash
pixi install
pixi run install
pixi run python il/download_demos.py
```

DP 的记录基线训练命令为：

```bash
# Easy：200 条 state 示范
pixi run python il/train.py method=dp demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=256 \
  flags.exp_name=dp_easy_baseline_s1 flags.capture_video=false

# Medium：200 条 state 示范
pixi run python il/train.py method=dp demo_dir=medium \
  flags.seed=1 flags.total_iters=50000 flags.batch_size=256 \
  flags.exp_name=dp_medium_baseline_s1 flags.capture_video=false

# Hard：200 条 state 示范
pixi run python il/train.py method=dp demo_dir=hard \
  flags.seed=1 flags.total_iters=60000 flags.batch_size=256 \
  flags.exp_name=dp_hard_baseline_s1 flags.capture_video=false
```

DP 训练每 5,000 updates 进行一次 16-episode 训练内评估，用来选择同一次训练的候选 checkpoint；该分数不能作为最终结果。

ACT 的记录复现命令为：

```bash
pixi run python il/train.py method=act_rgb demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=32 \
  flags.lr=1e-4 flags.kl_weight=10 flags.capture_video=false \
  +flags.skip_env_eval=true
```

`+flags.skip_env_eval=true` 会传给 ACT 训练器的 `--skip-env-eval`。它只跳过在线 RGB 环境评估，仍会完成 H5 读取、L1+KL 优化、EMA 与 final checkpoint 保存。该选项是当前没有 Vulkan graphics capability 的服务器完成 ACT 离线训练所必需的，因此不会产生 ACT 的训练内闭环 `sort_accuracy`。

## 8. 固定 50-seed 评估命令

正式本地评估由 `conf/eval/server_50.yaml` 定义：50 episodes、seeds `5000-5049`、GPU PhysX、无视频。`eval.py` 会固定 Torch/CUDA RNG seed 0，并输出 `sort_accuracy`、`mean_sorted`、`all_placed_rate` 和 `mis_sort_rate`。

```bash
# State DP，分别替换 difficulty 与 checkpoint
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=PATH_TO_STATE_DP_CHECKPOINT \
  eval_config=conf/eval/server_50.yaml \
  record_video=false
```

最终封存 checkpoint 的本地目录为 `experiments/checkpoints/state_easy_best.pt`、`state_medium_best.pt`、`state_hard_best.pt`；公开 checkout 不含 binary，恢复后应先执行 `sha256sum -c experiments/checkpoints/SHA256SUMS`。

ACT 的正式评估命令如下，但只有在容器已暴露 NVIDIA graphics/Vulkan capability、`vulkaninfo --summary` 能识别 NVIDIA GPU、且 SAPIEN 能创建 RGB environment 时才能运行：

```bash
pixi run python eval.py difficulty=easy obs_mode=rgb \
  policy=warehouse_sort.act_policy:load_act \
  checkpoint=PATH_TO_ACT_CHECKPOINT \
  eval_config=conf/eval/server_50.yaml \
  record_video=false
```

当前容器不满足这一前置条件。不要使用 CPU llvmpipe fallback 的输出替代该 RGB GPU 评估，也不要将 ACT 离线 loss 作为 `sort_accuracy`。

## 9. 检查清单

```text
[ ] H5 与同名 JSON 同目录，control mode 均为 pd_ee_delta_pos
[ ] state 训练使用与 difficulty 匹配的 H5；不要跨难度加载 state checkpoint
[ ] 扩充 H5 的 JSON 中所有保留 episode 均 success=true，seed 无重复
[ ] 训练内小样本评估只选 checkpoint；最终比较使用 server_50.yaml
[ ] ACT 训练可在无 Vulkan 主机使用 --skip-env-eval；ACT 闭环评估不可
[ ] 恢复公开 binary 后先用 SHA-256 清单校验
```
