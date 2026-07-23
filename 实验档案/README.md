# 实验档案

本目录保留原先散落在 `/data/coding` 的紧凑、可审阅 DP 与 ACT 材料。文件尽可能保留原名，使报告链接、命令和 hash 可审计。

| 目录 | 内容 |
|---|---|
| [dp训练和评估](dp训练和评估/) | 环境记录与 DP 各批次训练、评估报告 |
| [ACT离线复现](ACT离线复现/) | Easy ACT 30k 离线训练、日志与 Vulkan 闭环评估阻塞说明 |

H5 数据集、checkpoint binary、TensorBoard event file、生成的 run folder 和 tar archive 体积较大，因此不在本目录也不进入 Git。其本地来源与 integrity data 见 [RELEASE_MANIFEST.md](../RELEASE_MANIFEST.md)。

DP 结果表和最终解释分别见 [experiments/results.csv](../experiments/results.csv) 与 [experiments/final_report.md](../experiments/final_report.md)。
