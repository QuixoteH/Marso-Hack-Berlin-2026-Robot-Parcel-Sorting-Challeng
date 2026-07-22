# Data and Protocol

## Demonstrations And Observation Contract

Each official difficulty starts from 200 demonstrations. State observation widths are 54, 72, and 90 for Easy, Medium, and Hard, respectively. That parcel-count-specific contract is why the state track trains and submits one model per difficulty. The RGB ACT experiment uses the Easy scene camera dataset plus proprioception; it must not silently fall back to privileged state fields.

| Difficulty | Base demonstrations | Additional local state data | State observation width |
|---|---:|---:|---:|
| Easy | 200 | none recorded | 54 |
| Medium | 200 | 400 successful trajectories | 72 |
| Hard | 200 | 600 successful trajectories | 90 |

The H5 audit found raw action values outside the environment's declared `[-1, 1]` Box. A training run must make its label treatment explicit: regression, clipping, normalization, or conversion. Do not assume that an action array already matches the control API. For RL additions, validate replay handling of `terminated` and `truncated` before claiming the bootstrap target is correct.

## Fixed Local Evaluation Protocol

All reportable DP comparisons use [`conf/eval/server_50.yaml`](../conf/eval/server_50.yaml) and the official policy loader. The contract is:

| Setting | Required value |
|---|---|
| Episode count | 50 |
| Environment seeds | `5000-5049` |
| Video | disabled |
| Primary metric | `sort_accuracy` |
| Supporting diagnostics | `mean_sorted/episode`, `all_placed_rate`, `mis_sort_rate` |
| Submission track | state DP only for the recorded final policy |

Run it through the public entry point:

```bash
pixi run python eval.py difficulty=hard \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=PATH_TO_CHECKPOINT \
  eval_config=conf/eval/server_50.yaml
```

Keep the emitted configuration block and metrics as the evidence record. The final clean-shell logs are published in [`evidence/evaluations/`](../evidence/evaluations/). Training-time 4/8/16-episode metrics can select which candidate to investigate, but they cannot replace this final protocol.

## Metric Interpretation

`sort_accuracy` is the fraction of all parcels that finish in a matching bin. A parcel must be released, settled, inside the matching footprint, and below the rim. Grasping a parcel, moving it above a bin, or releasing it outside the match does not count.

The challenge aggregate is `0.20 * Easy + 0.30 * Medium + 0.50 * Hard`. Apply it only to results obtained under the same intended protocol. The current final local scores yield `0.1565`; do not relabel that aggregate as a held-out competition result.

## Artifact Handling

Generated H5 files, original demonstrations, and checkpoints stay outside normal Git history because of size and competition-data constraints. The public repository retains JSON manifests, final CSV rows, checksums, logs, and the artifact index needed to audit claims. See [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md) and [`evidence/README.md`](../evidence/README.md) before restoring or publishing binaries.
