# Marso 实验报告：批次 03 扩充示范数据

- 日期：2026-07-16
- 仓库提交：`6048f33217f26ae39009a812f53c81171517f393`
- 环境：state，GPU PhysX，headless，无 replay、无媒体

## 最终数据集

| 难度 | episodes | successes | unique seeds | H5 大小 | SHA-256 |
|---|---:|---:|---:|---:|---|
| Medium | 400 | 400 | 400 | 77,980,741 bytes | `62dba4d846333cf17ded5abb98cbad029f16cdda5600e580c3a1b8d41ec8e9b7` |
| Hard | 600 | 600 | 600 | 212,317,595 bytes | `e6b7714a3f0809b6b58e19f044b88fcf9eaad5bdb624246a406ac9928a2aa0d7` |

路径：

- Medium：`/data/coding/berlin-marso-hackathon/experiments/datasets/medium_seed2000_n400/trajectory.h5`
- Hard：`/data/coding/berlin-marso-hackathon/experiments/datasets/hard_seed2000_n600_success/trajectory.h5`

## 生成与修复过程

1. Medium 按 seeds 2000-2399、horizon 400 生成，400 条全部成功。
2. Hard 按 seeds 2000-2599、horizon 550 首轮生成，得到 576 成功、24 失败。
3. 对 24 个失败 seed 将 horizon 提高到 900，仅 2 条成功，证明失败不只是步数不足，scripted policy 对部分初始状态会稳定卡住。
4. 生成后续 seeds 2600-2629，得到 27 条成功替代轨迹。
5. 使用 `il/filter_successful_trajectories.py` 结构化过滤并合并原始 576 条成功轨迹和前 24 条替代成功轨迹，得到 600 条全成功、600 个唯一 seed 的最终 Hard 数据集。

所有原始、失败修复和替代批次均保留在 `experiments/datasets/`，未覆盖源数据。

## 指导文档问题

1. `gen_demos.py` 的 raw state 路径原先固定 `render_mode="rgb_array"`。因此文档中的 `--no-replay --no-media` 仍会初始化 Vulkan，并在 headless 服务器报 `ErrorIncompatibleDriver`。已改为 raw state 录制使用 `render_mode=None, render_backend="none"`。
2. 文档预期 Hard 在 `--max-steps 550` 下达到 600/600，但实测只有 576/600。
3. 文档建议失败后仅提高 `--max-steps`；实测提高到 900 后原 24 个失败 seed 仍仅 2 个成功，因此该指导不足。可靠方案是过滤失败轨迹，并用新的成功 seeds 补齐数据集。

## 结论

Task 6 已完成。两个训练输入均通过 H5/JSON 数量、成功标记和唯一 seed 检查，可以进入扩充数据 DP 训练。
