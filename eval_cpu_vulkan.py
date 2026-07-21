"""Evaluate an RGB policy with CPU PhysX + software Vulkan on compute-only hosts."""

import argparse
import os

os.environ.setdefault("VK_ICD_FILENAMES", "/usr/share/vulkan/icd.d/lvp_icd.json")
os.environ.setdefault("MARSO_RENDER_BACKEND", "cpu")
os.environ.setdefault("MARSO_SIM_BACKEND", "cpu")

import torch
from omegaconf import OmegaConf

from warehouse_sort.utils import compose_cfg, load_agent, make_env, print_metrics, rollout_metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--difficulty", default="easy", choices=("easy", "medium", "hard"))
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--eval-config", default="conf/eval/default.yaml")
    parser.add_argument("--policy", default="warehouse_sort.act_policy:load_act")
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    cfg = compose_cfg([f"difficulty={args.difficulty}", "num_envs=1"])
    eval_cfg = OmegaConf.load(args.eval_config)
    randomization = eval_cfg.get("randomization", None) or cfg.randomization
    env, _ = make_env(cfg, cfg.obs_mode, randomization, num_envs=1)
    # Initializing CUDA before llvmpipe makes SAPIEN try to bind the renderer to
    # the compute-only NVIDIA device. Build the CPU renderer first, then CUDA model.
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    agent, _ = load_agent(args.checkpoint, env, device, entrypoint=args.policy)
    metrics = rollout_metrics(
        env,
        agent,
        device,
        int(eval_cfg.eval.n_episodes),
        list(eval_cfg.eval.seeds),
        cfg.max_episode_steps,
    )
    print_metrics("EVAL", args.difficulty, cfg.obs_mode, metrics, hard=args.difficulty == "hard")
    env.close()


if __name__ == "__main__":
    main()
