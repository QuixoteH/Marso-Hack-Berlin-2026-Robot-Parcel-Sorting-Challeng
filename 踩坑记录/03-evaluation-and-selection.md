# Evaluation and Selection

Training-time metrics were based on small episode counts and diverged materially from fixed 50-seed evaluation. The DP Easy baseline, for example, had a much larger training-time value than its first independent local score.

Use `conf/eval/server_50.yaml`, disable video, retain the exact seeds, and record both `sort_accuracy` and `mean_sorted`. Do not report a local weighted number as a Kaggle leaderboard result, and do not change the challenge weights from Easy/Medium/Hard = `0.20/0.30/0.50`.
