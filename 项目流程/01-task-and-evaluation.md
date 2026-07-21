# Task and Evaluation

WarehouseSort is a learned-control challenge: a Franka Panda sorts coloured parcels into the matching coloured bins. The environment uses `pd_ee_delta_pos`, a four-dimensional action where the first three values are end-effector deltas and the fourth controls the gripper.

| Difficulty | Parcels | Generalisation pressure |
|---|---:|---|
| Easy | 2 | Fixed parcel and bin layout |
| Medium | 4 | Parcel XY jitter and longer horizon |
| Hard | 6 | Position/yaw jitter, longer horizon, and bin-side swaps |

`sort_accuracy` is correct parcels divided by total parcels at the end of an episode. A parcel must be released, settled, inside the matching bin footprint, and below the rim. Grasping or moving above a bin is not success.

The official aggregate weights are Easy/Medium/Hard = `0.20/0.30/0.50`. All archive comparisons use the official loader and the fixed seed range `5000-5049`; they are local evidence, not a substitute for held-out Kaggle evaluation.

The state track exposes geometry and colours in a low-dimensional vector. The RGB ACT track must infer this information from images. Do not treat the two as a controlled algorithm-only comparison.
