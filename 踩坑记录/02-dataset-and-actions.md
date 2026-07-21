# Dataset and Actions

The demonstration H5 action labels exceed the environment's declared `[-1, 1]` bounds. This may reflect pre-controller commands, scaling, or clipping elsewhere in the stack. It is not safe to train a tanh-bounded policy against these labels without documenting the target transformation.

The recordings also need careful temporal handling: observations have one more entry than actions, and `terminated`/`truncated` are not automatically a reliable RL replay rule. State and RGB observations have different schemas and cannot share a loader.

The generated state datasets retain JSON manifests and SHA-256 values under `experiments/datasets/`; large H5 payloads remain local.
