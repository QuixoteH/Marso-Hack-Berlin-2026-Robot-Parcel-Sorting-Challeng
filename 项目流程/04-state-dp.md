# State Diffusion Policy

## Goal And Scope

The state DP track is the completed, submit-ready path in this archive. It maps the task's privileged low-dimensional state observation to short end-effector action sequences. Each difficulty has a different state dimension, so one checkpoint cannot be shared across Easy, Medium, and Hard. This section documents what was actually trained and evaluated; it does not present state DP and RGB ACT as a like-for-like comparison.

The implementation is selected through `il/train.py method=dp`. The method configuration is [`il/conf/method/dp.yaml`](../il/conf/method/dp.yaml), the submit-time loader is `warehouse_sort.il_policy:load_dp`, and the three selected paths are declared in [`submission.yaml`](../submission.yaml).

## Reproduce A Training Candidate

From a prepared Pixi environment with the official demonstrations available:

```bash
# Easy baseline: 200 state demonstrations, seed 1, 30k updates.
pixi run python il/train.py method=dp demo_dir=easy \
  flags.seed=1 flags.total_iters=30000 flags.batch_size=256 \
  flags.exp_name=dp_easy_baseline_s1

# Hard selected-family setting: 600 state demonstrations, batch 512, 100k updates.
pixi run python il/train.py method=dp demo_dir=hard \
  flags.seed=3 flags.total_iters=100000 flags.batch_size=512 \
  flags.exp_name=dp_hard_aug_b512_s3
```

The DP defaults are observation horizon 2, action horizon 8, prediction horizon 16, and fixed evaluation with 16 episodes during training. Training-time values are only screening signals. They must not replace the 50-episode final protocol in [03-data-and-protocol.md](03-data-and-protocol.md).

## Candidate Evidence

![State DP fixed 50-episode candidate scores](../evidence/figures/dp_candidate_scores.png)

The chart is generated from [`experiments/results.csv`](../experiments/results.csv), where every row records phase, difficulty, seed, demo count, iterations, batch size, fixed episode count, checkpoint path, score, and short diagnostic notes. It covers these controls:

| Control | Evidence-bound conclusion |
|---|---|
| Longer training | Easy was tied at 0.170; Medium dropped from 0.110 to 0.080; Hard increased from 0.037 to 0.040. More updates were not a universal improvement. |
| More demonstrations | Medium 400-demo candidate was 0.055 versus the 200-demo baseline at 0.110; Hard 600-demo candidate was retained over the earlier 200-demo runs. |
| Batch size 512 | Medium fell to 0.050; Hard reached 0.087 in the first 512-batch check. |
| Seed controls | Final family reruns cover seeds 1-3. The selected clean-shell checkpoints were evaluated separately with seed 0. |

This figure is a CSV-derived publication aid, not TensorBoard output. The supplied artifact archive does not contain DP TensorBoard event files.

## Final Checkpoints And Independent Evaluation

The selected checkpoints were re-evaluated through the official loader in a clean shell with Torch/CUDA RNG seed 0, 50 diffusion inference steps, 50 episodes, fixed seeds `5000-5049`, and video disabled. Easy was run twice and matched. The logs are included under [`evidence/evaluations/`](../evidence/evaluations/).

| Difficulty | Selected checkpoint | `sort_accuracy` | Mean correctly sorted | Repeat evidence |
|---|---|---:|---:|---|
| Easy | `state_easy_best.pt` | 0.390 | 0.78 / 2 | matching second 0.390 run |
| Medium | `state_medium_best.pt` | 0.090 | 0.36 / 4 | one recorded clean-shell run |
| Hard | `state_hard_best.pt` | 0.103 | 0.62 / 6 | one recorded clean-shell run |

Run the same protocol after restoring the binaries:

```bash
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=experiments/checkpoints/state_easy_best.pt \
  eval_config=conf/eval/server_50.yaml
```

Repeat it for `medium` and `hard`, changing both the difficulty and checkpoint. Compare SHA-256 against [`experiments/checkpoints/SHA256SUMS`](../experiments/checkpoints/SHA256SUMS) before evaluation. The precise result interpretation is in [`experiments/final_report.md`](../experiments/final_report.md).

## What The Result Does Not Establish

- A 50-episode local value is not a held-out competition score.
- `all_placed_rate` is zero in all three logged final evaluations; `sort_accuracy` is therefore the reported primary metric rather than a claim of complete-episode success.
- The state track uses privileged observations. Its result cannot establish that an RGB-only method is worse or better.
