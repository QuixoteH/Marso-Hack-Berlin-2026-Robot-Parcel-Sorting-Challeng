# WarehouseSort 提交指南

本页说明如何训练、声明并提交一个可评分的 learned policy。完整任务定义、观测/动作和权重见 [README](README.md)。

## 1. 提交内容

提交的是 GitHub repository（fork 或基于本仓库的新仓库），而不是单独的 checkpoint。评测方会 fresh clone 后直接运行。仓库必须包含：

1. `module:function` 格式的 policy entrypoint；
2. checkpoint 文件，或可由仓库内脚本下载的 checkpoint；
3. 根目录 `submission.yaml`，声明 `state`、`rgb` 或两者，以及各难度的 checkpoint。

fresh clone 必须能执行 `pixi install` 与 `pixi run install`；评测只调用 `load_fn` 和 `policy.act(obs)`，不会导入你的训练主程序。

## 2. Policy 接口

```python
load_fn(checkpoint, sample_obs, action_space, device) -> policy
policy.act(obs, deterministic=True) -> Tensor (num_envs, action_dim) in [-1, 1]
```

`eval.py` 通过 `policy=module:function` 导入 `load_fn`，传入 checkpoint 路径、样例观测、action space 和 device；随后反复调用 `.act(obs)`。参考实现为 [warehouse_sort/il_policy.py](warehouse_sort/il_policy.py) 的 `load_dp`，评估逻辑在 [warehouse_sort/utils.py](warehouse_sort/utils.py)。checkpoint 格式由 `load_fn` 自己解释，但模型类及依赖必须可从提交仓库导入，policy 不得读取 privileged simulator state。

## 3. 训练参考方案

```bash
pixi install
pixi run install
pixi run python il/download_demos.py
pixi run python il/train.py method=dp demo_dir=easy
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=PATH_TO_CHECKPOINT \
  eval_config=conf/eval/default.yaml
```

state 向量随包裹数变化，因此 Easy、Medium、Hard 必须各训练一个 checkpoint。训练更久可覆盖 `flags.total_iters=`；可调 `flags.pred_horizon=`；可用 `il/gen_demos.py` 录制额外数据。最终选择必须使用 [conf/eval/server_50.yaml](conf/eval/server_50.yaml)，而不是少量训练期 episode。

> 提交必须是从观测学习到的参数化 policy。scripted、hard-coded、rule-based controller，或读取 simulator privileged state 的控制器均不是有效提交。

## 4. 自定义方法

可使用行为克隆、RL、Transformer 等任意 learned policy，只要满足上述接口。`load_fn` 应基于 `sample_obs` 与 `action_space` 构建网络（不要硬编码 state 维度），从 `checkpoint` 参数加载权重并移至 `device`。随后在 manifest 中写入，例如 `policy: my_module:load_policy`。

## 5. Manifest 与评分

```yaml
state:
  policy: warehouse_sort.il_policy:load_dp
  levels:
    easy:   { checkpoint: path/to/easy.pt }
    medium: { checkpoint: path/to/medium.pt }
    hard:   { checkpoint: path/to/hard.pt }
```

`rgb` 赛道同样可声明，但使用 RGB entrypoint。每个已声明赛道独立评分；省略某一难度会得到零分，但该难度权重仍计入。最终分数为：

```text
0.2 * sort_accuracy_easy + 0.3 * sort_accuracy_medium + 0.5 * sort_accuracy_hard
```

提交前请在 clean environment 中核验 entrypoint import、checkpoint 路径、SHA-256 和三种难度评估；不要把本地固定 seed 结果称为 held-out leaderboard 分数。
