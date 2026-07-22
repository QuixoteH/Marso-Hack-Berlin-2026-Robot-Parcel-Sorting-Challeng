# Task and Evaluation

## Goal

WarehouseSort is a learned-control task: a Franka Panda must identify the colour tag on each parcel, grasp the parcel, move it into the bin with the same colour, and release it so that it settles inside the bin. The task is an end-to-end pick-and-place problem, not only a reaching or grasping benchmark.

The environment control mode is `pd_ee_delta_pos`. Each action has four values: three end-effector delta-position commands and one gripper command. Policies are expected to emit actions through the challenge loader rather than directly changing scene state.

## Difficulty Contract

| Difficulty | Parcels | Episode horizon | Generalisation pressure |
|---|---:|---:|---|
| Easy | 2 | 200 | Fixed parcel and bin layout |
| Medium | 4 | 400 | Parcel XY jitter and a longer sequence |
| Hard | 6 | 550 | Parcel XY/yaw jitter, long horizon, and 50% bin-side swap probability |

The state and RGB tracks differ in the information available to a policy:

| Track | Input | Consequence for this archive |
|---|---|---|
| State DP | privileged low-dimensional geometry and colour state | Main completed submission path |
| RGB ACT | scene image plus robot proprioception | Offline training reproduced, but no renderer-backed evaluation on the recorded host |

Do not treat a score difference between these rows as an isolated algorithm comparison. They solve different observation problems.

## Score Definition

`sort_accuracy` is the number of correctly sorted parcels divided by the total number of parcels in the episode. A parcel counts only when it is released, settled, inside the matching bin footprint, and below the rim. The following events do not count as success:

- grasping a parcel without placing it;
- holding a parcel above a correct bin;
- dropping a parcel outside a bin;
- placing a parcel in the wrong-colour bin.

The evaluator also reports diagnostics such as `mean_sorted/episode`, `all_placed_rate`, and `mis_sort_rate`. In this project, `sort_accuracy` is the primary reported metric. A zero `all_placed_rate` must not be rewritten as a complete-task success.

## Evaluation And Reporting Rules

The official weighted aggregate is:

```text
0.20 * Easy + 0.30 * Medium + 0.50 * Hard
```

All archive comparisons use the official loader, no video, 50 episodes, and fixed seeds `5000-5049`; the exact procedure is in [03-data-and-protocol.md](03-data-and-protocol.md). These are reproducible local evidence, not held-out Kaggle evaluations. Preserve the configuration block, checkpoint checksum, and output metrics with any new result so a reader can distinguish a rerun from a new experiment.
