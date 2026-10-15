"""Minimal HelpMeOut loader and prediction-file writer.

    python examples/load_helpmeout.py --root HelpMeOut --split test --out predictions.jsonl

It shows (1) how to read episodes, (2) what a monitor may see at step t, and
(3) the prediction format. The "monitor" here is a trivial placeholder that
never raises an alarm; replace `monitor_step` with your model.
"""
import argparse
import json
from pathlib import Path

ERROR_TYPES = ["OMISSION", "SEQUENCE", "ANTICIPATION", "PERSEVERATION", "OBJECT_SUBSTITUTION",
               "TOOL_SUBSTITUTION", "ACTION_ADDITION", "CAPTURE_ERROR", "SPATIAL_MISREACH"]


def load_split(root, split, ids=None):
    """Yield episodes of a split (optionally restricted to a list of ids)."""
    for p in sorted((Path(root) / split).glob("*.json")):
        if ids is None or p.stem in ids:
            yield json.loads(p.read_text())


def monitor_input(ep, t):
    """Everything a monitor may use at step t: task name, initial scene, actions 0..t."""
    return {
        "task": ep["task_name"].replace("_", " "),
        "initial_scene": ep["initial_scene"],
        "prefix": ep["actions"][: t + 1],
    }


def monitor_step(obs):
    """Placeholder monitor: returns (p_instant, p_type). Replace with your model."""
    return 0.0, [0.0] * len(ERROR_TYPES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="HelpMeOut")
    ap.add_argument("--split", default="test", choices=["train", "val", "test"])
    ap.add_argument("--llm60", action="store_true", help="only the 60-episode subset in llm60.txt")
    ap.add_argument("--out", default="predictions.jsonl")
    a = ap.parse_args()

    ids = set((Path(a.root) / "llm60.txt").read_text().split()) if a.llm60 else None
    n = 0
    with open(a.out, "w") as fh:
        for ep in load_split(a.root, a.split, ids):
            p_instant, p_type = [], []
            for t in range(len(ep["actions"])):      # steps before labels.window_start are not scored
                pi, pt = monitor_step(monitor_input(ep, t))
                p_instant.append(pi)
                p_type.append(pt)
            fh.write(json.dumps({"id": ep["id"], "p_instant": p_instant, "p_type": p_type}) + "\n")
            n += 1
    print(f"wrote {n} predictions to {a.out}")


if __name__ == "__main__":
    main()
