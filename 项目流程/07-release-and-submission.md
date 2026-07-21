# Release and Submission

The selected state submission uses `warehouse_sort.il_policy:load_dp` and `submission.yaml`. The final local checkpoint hashes are retained in `experiments/checkpoints/SHA256SUMS` and the submission archive hash in `experiments/marso_final_submission.tar.gz.sha256`.

GitHub cannot accept individual files above 100 MiB. Raw H5 data, checkpoints, TensorBoard files, logs, and tarballs are therefore deliberately excluded. Their provenance is stated in [RELEASE_MANIFEST.md](../RELEASE_MANIFEST.md), and scripts/configuration/JSON manifests remain available for reconstruction.

Before a real submission:

1. obtain the checkpoint artifacts through the documented local archive or a GitHub Release/LFS;
2. verify SHA-256 values;
3. run all three difficulties with the official loader and the intended held-out protocol;
4. confirm `submission.yaml` paths and loader imports in a clean environment;
5. publish a fork rather than pushing to the upstream challenge repository.
