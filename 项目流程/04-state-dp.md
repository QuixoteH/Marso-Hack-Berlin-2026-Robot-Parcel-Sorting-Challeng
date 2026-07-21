# State Diffusion Policy

DP is the completed state-track method. It models action sequences from state demonstrations, uses EMA at evaluation, and has one checkpoint per difficulty.

| Difficulty | Sealed checkpoint score | Mean correctly sorted |
|---|---:|---:|
| Easy | 0.390 | 0.78 / 2 |
| Medium | 0.090 | 0.36 / 4 |
| Hard | 0.103 | 0.62 / 6 |

The selected checkpoints were independently re-evaluated in a clean shell using fixed Torch/CUDA RNG seed 0, 50 inference steps, and the 50-episode protocol. The Easy repeat matched. Checkpoint hashes are in `experiments/checkpoints/SHA256SUMS`; binary checkpoints remain local and are excluded from Git.

Candidate-level results, including baseline, longer training, augmented-data, batch-size, and seed controls, are in [experiments/results.csv](../experiments/results.csv). The final interpretation is in [experiments/final_report.md](../experiments/final_report.md).
