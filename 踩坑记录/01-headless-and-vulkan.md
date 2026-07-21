# Headless and Vulkan

The host can execute CUDA and GPU PhysX but does not expose an NVIDIA Vulkan graphics driver compatible with SAPIEN. RGB environments and video recording fail even though `torch.cuda.is_available()` is true.

For state-only data generation and evaluation, use `render_mode=None`, `render_backend="none"`, and disable video. A previous raw-state generation path still created `rgb_array`; this was changed so `--no-replay --no-media` genuinely avoids renderer setup.

Do not replace RGB evaluation with CPU `llvmpipe`: it cannot interoperate with the CUDA path used here. Move ACT/RGB evaluation to a graphics-capable NVIDIA host.
