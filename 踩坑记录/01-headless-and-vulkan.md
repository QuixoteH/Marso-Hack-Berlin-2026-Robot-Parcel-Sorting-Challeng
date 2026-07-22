# Headless 与 Vulkan

该主机可执行 CUDA 和 GPU PhysX，但未提供与 SAPIEN 兼容的 NVIDIA Vulkan graphics driver；即使 `torch.cuda.is_available()` 为真，RGB 环境和视频录制仍会失败。

仅生成或评估 state 数据时，使用 `render_mode=None`、`render_backend="none"` 并关闭视频。此前的 raw-state 生成路径仍会创建 `rgb_array`；现已调整，使 `--no-replay --no-media` 确实不会初始化 renderer。

不要用 CPU `llvmpipe` 替代 RGB 评估：它不能与本项目的 CUDA 路径互操作。应把 ACT/RGB 评估迁移到具备 graphics-capable NVIDIA host 的机器。
