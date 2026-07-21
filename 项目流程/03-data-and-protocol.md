# Data and Protocol

Each official difficulty has 200 demonstrations. State observation dimensions are 54, 72, and 90 for Easy, Medium, and Hard respectively; models are therefore difficulty-specific. The local evaluation protocol is 50 episodes with seeds `5000-5049`, no video, and the official policy loader.

The H5 audit found raw action values outside the environment's declared `[-1, 1]` Box. Training code must state whether it regresses, clips, normalises, or converts these labels. For RL, `terminated` and `truncated` cannot be assumed to define correct bootstrap behaviour without replay validation.

Extra successful state datasets were generated for Medium (400 episodes) and Hard (600 episodes). Their H5 files remain local because of size; JSON manifests and SHA-256 values are retained in `experiments/datasets/` and the historical reports.

Use `conf/eval/server_50.yaml` for the fixed local protocol. Training-time 4/8/16-episode metrics do not select the final model.
