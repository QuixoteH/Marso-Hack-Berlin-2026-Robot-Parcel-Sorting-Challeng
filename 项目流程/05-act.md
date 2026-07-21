# RGB ACT Offline Reproduction

The archived ACT branch reproduces the leaderboard Easy RGB ACT training setup: ResNet-18 backbone, DETR/CVAE, L1 plus KL objective, EMA, 30 action queries, batch size 32, seed 1, and 30,000 updates. It completed offline and its checkpoint independently loaded with finite `(2, 4)` output.

No RGB closed-loop score exists on this host because SAPIEN cannot initialise a compatible NVIDIA Vulkan renderer. This is an infrastructure limitation, not a zero score. ACT source is included under `il/baselines/act/`, its loader is `warehouse_sort.act_policy:load_act`, and the evidence is in [实验档案/ACT离线复现](../实验档案/ACT离线复现/).
