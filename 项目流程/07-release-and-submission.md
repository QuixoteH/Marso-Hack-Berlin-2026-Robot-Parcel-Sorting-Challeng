# Release and Submission

## Public Repository Contract

The public submission path is state DP, configured by [`submission.yaml`](../submission.yaml) and loaded through `warehouse_sort.il_policy:load_dp`. The repository includes code, configuration, dataset manifests, compact logs, result tables, figures generated from those logs, and SHA-256 values. It deliberately excludes checkpoint binaries, original H5 data, and submission tarballs.

| Artifact | Public form | Binary location / integrity anchor |
|---|---|---|
| Selected DP checkpoints | loader configuration and final logs | `experiments/checkpoints/SHA256SUMS` |
| Final submission archive | manifest entry | `experiments/marso_final_submission.tar.gz.sha256` |
| ACT Easy checkpoint | offline report and loss evidence | SHA-256 in [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md) |
| DP final evaluations | four compact logs | [`evidence/evaluations/`](../evidence/evaluations/) |
| ACT optimization | terminal log and generated curve | [`evidence/act/`](../evidence/act/) |

The 195 MiB submission archive and 133 MiB ACT checkpoint cannot be committed to ordinary GitHub Git due to GitHub's 100 MiB file limit. The 35-38 MiB DP checkpoints are also intentionally omitted to keep an ordinary clone practical. Use a GitHub Release or another documented artifact channel when binary distribution is needed; do not silently replace a binary without recalculating its SHA-256.

## Restore And Validate Before Submission

1. Obtain the exact three DP checkpoint files from the documented artifact source.
2. Put them at the paths declared in `submission.yaml`, or update that manifest deliberately.
3. Compare each file with `experiments/checkpoints/SHA256SUMS` using `sha256sum -c experiments/checkpoints/SHA256SUMS`.
4. In a clean environment, import the loader and evaluate Easy, Medium, and Hard with the intended evaluation configuration.
5. Inspect the metric block and preserve its logs. Do not promote a training-time score or a local fixed-seed score to a held-out leaderboard claim.

Example smoke check after restoring a checkpoint:

```bash
pixi run python -c "from warehouse_sort.il_policy import load_dp; print(load_dp)"
pixi run python eval.py difficulty=easy \
  policy=warehouse_sort.il_policy:load_dp \
  checkpoint=experiments/checkpoints/state_easy_best.pt \
  eval_config=conf/eval/server_50.yaml
```

Publish this repository as a fork or independent archive, never by pushing directly to the upstream challenge repository. The final pre-publication checklist is the [release manifest](../RELEASE_MANIFEST.md), the [evidence index](../evidence/README.md), and the latest clean-shell evaluation records.
