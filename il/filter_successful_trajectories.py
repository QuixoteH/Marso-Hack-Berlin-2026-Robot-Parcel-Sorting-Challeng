"""Merge successful ManiSkill trajectories into a fixed-size dataset."""

import argparse
import json
from pathlib import Path

import h5py


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--count", required=True, type=int)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    output_json = args.output.with_suffix(".json")
    episodes = []
    base_meta = None

    with h5py.File(args.output, "w") as dst:
        for input_h5 in args.input:
            with open(input_h5.with_suffix(".json")) as f:
                meta = json.load(f)
            if base_meta is None:
                base_meta = {
                    "env_info": meta["env_info"],
                    "commit_info": meta.get("commit_info"),
                }

            with h5py.File(input_h5, "r") as src:
                for episode in meta["episodes"]:
                    if not episode.get("success"):
                        continue
                    new_id = len(episodes)
                    source_group = f"traj_{episode['episode_id']}"
                    src.copy(source_group, dst, f"traj_{new_id}")
                    copied = dict(episode)
                    copied["episode_id"] = new_id
                    episodes.append(copied)
                    if len(episodes) == args.count:
                        break
            if len(episodes) == args.count:
                break

    if len(episodes) != args.count:
        args.output.unlink(missing_ok=True)
        raise RuntimeError(f"needed {args.count} successful episodes, found {len(episodes)}")

    base_meta["episodes"] = episodes
    with open(output_json, "w") as f:
        json.dump(base_meta, f, indent=2)
    print(f"wrote {len(episodes)} successful episodes to {args.output}")


if __name__ == "__main__":
    main()
