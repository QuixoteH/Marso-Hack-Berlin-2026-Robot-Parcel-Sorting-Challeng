# 数据集与动作

示范 H5 的动作标签超出环境声明的 `[-1, 1]` 范围，可能对应 pre-controller command、缩放或栈中其他位置的裁剪。若不说明目标变换，不能安全地用这些标签训练 tanh 有界 policy。

录制数据还需要谨慎处理时间关系：观测条目比动作多一个；`terminated`/`truncated` 不能自动作为可靠的 RL replay 规则。state 与 RGB 的观测 schema 不同，不能共享 loader。

生成的 state 数据集在 `experiments/datasets/` 下保留 JSON manifest 与 SHA-256；大体积 H5 payload 留在本地。
