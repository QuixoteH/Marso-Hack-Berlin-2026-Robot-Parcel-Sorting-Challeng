# Public Evidence Index

This directory contains compact, reviewable evidence copied from
`warehouse-sort-dp-act-key-artifacts-2026-07-21.zip`. It intentionally does
not include the large checkpoint binaries from that archive.

## Provenance

| Item | Source in the artifact archive | Purpose |
|---|---|---|
| `evaluations/` | `dp/evaluation_logs/` | Final clean-shell, 50-episode DP evaluations |
| `act/act_easy_training.log` | `act/training/训练日志_final.log` | ACT Easy offline optimization log |
| `figures/dp_candidate_scores.png` | `experiments/results.csv` | Candidate DP scores plotted from versioned CSV data |
| `figures/act_easy_loss.png` | `act/act_easy_training.log` | ACT loss plotted from the copied terminal log |

The two figures are not TensorBoard exports. The supplied artifact archive has
no `events.out.tfevents.*` files, so the figures are explicitly labelled as
CSV/log-derived evidence. Regenerate them after changing their inputs:

```bash
python scripts/generate_evidence_figures.py
```

## Interpretation Rules

- A plotted DP score is `sort_accuracy` from a fixed local 50-episode run,
  not a held-out Kaggle leaderboard result.
- The ACT curve demonstrates that the documented 30,000-update optimization
  completed. It does not demonstrate closed-loop manipulation success.
- The matching checkpoint SHA-256 values are recorded in
  [`RELEASE_MANIFEST.md`](../RELEASE_MANIFEST.md). Checkpoints remain outside
  Git because the ACT file is 133 MiB and the DP files are 35-38 MiB each.
