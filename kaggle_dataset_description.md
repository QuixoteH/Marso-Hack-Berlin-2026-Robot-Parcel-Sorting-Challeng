# WarehouseSort——示范数据集

WarehouseSort 抓取与放置挑战的专家示范：Franka Panda 需要将包裹放入与包裹顶面颜色标签相同的箱子（红标签对应红箱、蓝标签对应蓝箱）。

## 内容

每个难度包含 **200 条示范 episode**：

| 文件夹 | 难度 | 包裹数 | 随机化 |
|---|---|---:|---|
| `easy/` | 简单 | 2 | 布局完全固定 |
| `medium/` | 中等 | 4 | 小幅位置扰动 |
| `hard/` | 困难 | 6 | 小幅位置/朝向扰动，箱子可能互换 |

每个文件夹都包含成对的 ManiSkill trajectory 文件（`.h5` 和同名 `.json` 必须同时存在）：

- `trajectory.state.pd_ee_delta_pos.physx_cuda.{h5,json}`：主 state 赛道；
- `trajectory.rgb.pd_ee_delta_pos.physx_cuda.{h5,json}`：可选 RGB 图像赛道。

**观测。** state 赛道是机器人 proprioception、包裹位姿/标签颜色与箱子位置/颜色构成的低维向量，长度随包裹数变化；RGB 赛道是固定第三人称相机图像 `(128, 128, 3)` uint8 加上 `(26,)` proprioception。两条赛道的动作均为 `pd_ee_delta_pos`：范围 `[-1, 1]` 内的四维向量（末端执行器 Δxyz 与夹爪）。

## 生成方式

在 GPU 加速的 [ManiSkill 3](https://maniskill.readthedocs.io/en/latest/) 中，确定性的 scripted waypoint policy 完成任务。流程为标准的 **record → replay**：先由 `RecordEpisode` 录制 rollout，再由 `replay_trajectory` 重放并渲染对应观测。轨迹没有动作噪声，所有包裹正确分拣后 episode 结束。

> scripted policy 读取特权 simulator state 只用于**数据生成**。提交的 policy 必须仅从观测做动作。

## 使用方式

可使用行为克隆从最近观测预测动作序列。仓库中的 Diffusion Policy baseline 直接加载这些 `.h5` 文件；主赛道为 state（因向量长度随难度变化，每个难度单独训练一个 checkpoint），另提供可选 RGB 赛道。完整训练与评估步骤见仓库主 README。
