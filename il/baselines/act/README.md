# Transformer 动作分块（ACT）

本目录包含基于论文 [Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware](https://arxiv.org/pdf/2304.13705) 的 ACT 实现，改编自[原始代码](https://github.com/tonyzhaozh/act)。

## 安装

```bash
conda create -n act-ms python=3.9
conda activate act-ms
pip install -e .
```

## 使用说明

ManiSkill imitation learning 的数据下载、预处理、公平评估与常见问题见[官方说明](https://maniskill.readthedocs.io/en/latest/user_guide/learning_from_demos/setup.html)。本项目的实际 ACT 复现参数与证据见 [项目流程/05-act.md](../../../项目流程/05-act.md)。

示范较慢时，`--max-episode-steps` 必须足够长，否则 imitation policy 即使模仿正确也可能来不及完成。通常可设为训练示范平均长度的约两倍；各任务推荐值见 `baselines.sh`。

## 引用

使用该 baseline 时请引用原论文：Zhao et al., *Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware*, RSS 2023。
