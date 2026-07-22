#!/usr/bin/env python3
"""Generate repository figures only from versioned experiment evidence."""

import csv
import re
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results.csv"
ACT_LOG = ROOT / "evidence" / "act" / "act_easy_training.log"
OUT = ROOT / "evidence" / "figures"


def read_dp_results():
    with RESULTS.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row["phase"] != "final_dp_deterministic"]


def read_act_losses():
    pattern = re.compile(r"Iteration (\d+), loss: ([0-9.eE+-]+)")
    return [(int(step), float(loss)) for step, loss in pattern.findall(ACT_LOG.read_text())]


def plot_dp(rows):
    labels = [row["experiment"].removeprefix("dp_") for row in rows]
    scores = [100 * float(row["sort_accuracy"]) for row in rows]
    colors = {"easy": "#1f77b4", "medium": "#2ca02c", "hard": "#d62728"}
    bar_colors = [colors[row["level"]] for row in rows]

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(range(len(rows)), scores, color=bar_colors)
    ax.set_title("State Diffusion Policy: fixed 50-episode candidate evaluations")
    ax.set_ylabel("sort_accuracy (%)")
    ax.set_ylim(0, 45)
    ax.set_xticks(range(len(rows)), labels, rotation=55, ha="right", fontsize=8)
    ax.grid(axis="y", alpha=0.25)
    for bar, score in zip(bars, scores):
        ax.text(bar.get_x() + bar.get_width() / 2, score + 0.7, f"{score:.1f}",
                ha="center", va="bottom", fontsize=7)
    ax.text(0.99, 0.97, "Source: experiments/results.csv\nNot a Kaggle leaderboard score",
            transform=ax.transAxes, ha="right", va="top", fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#999999", "pad": 4})
    fig.tight_layout()
    fig.savefig(OUT / "dp_candidate_scores.png", dpi=180)
    plt.close(fig)


def plot_act(losses):
    steps, values = zip(*losses)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(steps, values, color="#9467bd", marker="o", markersize=3)
    ax.set_title("ACT Easy offline training loss")
    ax.set_xlabel("update")
    ax.set_ylabel("reported total loss")
    ax.set_yscale("log")
    ax.grid(alpha=0.25)
    ax.text(0.99, 0.97,
            "Source: evidence/act/act_easy_training.log\nOffline optimization evidence only; no closed-loop score",
            transform=ax.transAxes, ha="right", va="top", fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#999999", "pad": 4})
    fig.tight_layout()
    fig.savefig(OUT / "act_easy_loss.png", dpi=180)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    plot_dp(read_dp_results())
    plot_act(read_act_losses())


if __name__ == "__main__":
    main()
