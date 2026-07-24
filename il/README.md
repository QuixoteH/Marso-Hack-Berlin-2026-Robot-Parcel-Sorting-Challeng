# 模仿学习——WarehouseSort

主赛道为 state。IL 流程为：**demos → 训练 state Diffusion Policy → 用 `eval.py` 评估**。state DP 可端到端运行；另提供更困难但尚未解决任务的 RGB 模板（`method=dp_rgb`、`load_dp_rgb`）。

## 第一步：示范数据

无需自行录制。每个难度提供 200 个 episode 的 `state` 和 `rgb` 数据，来自 [Kaggle competition data](https://www.kaggle.com/competitions/marso-hack-berlin-2026-robot-parcel-sorting-challenge/data)。Kaggle 中数据自动挂载在 `/kaggle/input/`；其他环境先加入竞赛并配置 Kaggle API token，再执行：

```bash
pixi run python il/download_demos.py
```

文件会进入 `il/demos/<level>/`。每份数据都由 `.h5` 和同名 `.json` 组成，二者必须放在同一目录；trainer 会在 `.h5` 旁寻找 control-mode metadata。示范由 `examples/scripted_policy.py` 生成，只能用于收集数据；提交 scripted、hard-coded 或读取 privileged simulator state 的控制器会被取消资格。

H5 内部的 `traj_*`、JSON 与 H5 的对应关系、state/RGB replay、MP4/GIF 的非训练用途、扩充 state 数据的审计链路，以及 DP/ACT 的完整训练和评估命令见[数据目录、文件格式与训练评估命令](../项目流程/06-data-layout-and-commands.md)。

### 可选：生成更多示范

```bash
pixi run python il/gen_demos.py --difficulty easy --num-episodes 200
pixi run python il/gen_demos.py --difficulty medium --num-episodes 200
pixi run python il/gen_demos.py --difficulty hard --num-episodes 200
```

流程为 **record → replay → media**：`RecordEpisode` 保存 raw trajectory 与 env state；`replay_trajectory` 重放动作并渲染 RGB，得到训练用 H5；随后保存 `media/<level>_demo.mp4` 和 GIF。`--no-replay` 只保留 raw demo，`--no-media` 跳过视频，`--base-seed` 改变 seed 区间。

## 第二步：训练

```bash
pixi run python il/train.py method=dp demo_dir=easy
pixi run python il/train.py method=dp demo_dir=medium
pixi run python il/train.py method=dp demo_dir=hard
```

state 维度随难度变化，因此每个难度独立训练并提交 checkpoint。可通过 CLI 覆盖参数：

```bash
pixi run python il/train.py method=dp flags.total_iters=50000 flags.pred_horizon=32
```

checkpoint 位于 `il/baselines/diffusion_policy/runs/<exp_name>/checkpoints/`。自定义数据可传入完整 `demo_path=`，并保留同目录 `.json`。RGB 模板使用 `method=dp_rgb`。

## 第三步：评估

```bash
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=PATH_TO_CHECKPOINT \
  eval_config=conf/eval/default.yaml
```

Medium 和 Hard 必须使用各自 checkpoint。最终选型使用 `conf/eval/server_50.yaml`，而不是默认少量 episode 配置。

## 训练时间与说明

单张现代 GPU（如 Colab T4）上，默认 state DP 约需 Easy 20–40 分钟、Medium 40–70 分钟、Hard 50–90 分钟；RGB 模板约 30–90 分钟且尚未解决任务。Diffusion Policy 的 action chunking 用于减轻 behavior cloning 的 compounding error。ManiSkill 3.0.1 wheel 不带 `examples/baselines`，因此 DP baseline 已 vendored 至 `il/baselines/diffusion_policy/`。重放或加载新写入 H5 发生竞争时设置 `HDF5_USE_FILE_LOCKING=FALSE`。
