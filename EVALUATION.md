# HelpMeOut evaluation protocol

This document defines the monitor input and output and the four metrics (M1–M4) used in the paper. The official scoring script, coming soon (see the [Roadmap](README.md#roadmap)), implements exactly these rules.

## Monitor input and output

At evaluation step `t`, a monitor receives **only**

1. the task name (`task_name`, e.g. "folding and storing clothes"),
2. the initial scene (`initial_scene`), and
3. the action prefix `actions[0..t]`, including the current action.

It must not use future actions, the episode length, `labels`, or anything in `metadata` (the formal goal, the subgoal boundaries, or the reference execution). The monitor knows the task, as in the clinical tests the categories come from, but not its formal requirements.

At every step the monitor outputs

* `p_instant[t]`: the probability that an error occurs at step `t`, and
* `p_type[t]`: nine probabilities that an error of each category has occurred at or before step `t`, in this order:
  `OMISSION, SEQUENCE, ANTICIPATION, PERSEVERATION, OBJECT_SUBSTITUTION, TOOL_SUBSTITUTION, ACTION_ADDITION, CAPTURE_ERROR, SPATIAL_MISREACH`.

## Metrics

All four metrics are computed from the two per-step outputs above.

**Notation.** For an episode with `T` steps, `W = {window_start, ..., T-1}` is its evaluation window; steps before `window_start` are never scored and never count as alarms. `T-1` is always the task-end step. An episode is *errorful* if `labels.onsets` is non-empty; its *first onset* is the smallest onset step. Pool all scored episodes of the split (or of `llm60.txt`).

**Missing predictions.** If `p_instant` is missing for any step in `W`, the episode is excluded from M1 and M3 (including the false-alarm rate); its available steps still enter M2 and M4.

**M1: trajectory-level discrimination.**
Score each episode by `s = max_{t in W} p_instant[t]`. M1 is the AUROC of `s` with label 1 for errorful and 0 for correct episodes. M1 does not depend on when the alarm is raised.

**M2: step-level detection.**
Pool every step `t in W` of every episode with label `has_error[t]` and score `p_instant[t]`. M2 is the AUPRC (average precision) over this pool. Only onset steps are positive; later steps where an error's consequences persist are negative, so a late alarm earns no credit. Also report two subsets of the same pool:

* **M2-end**: only the task-end steps (`t = T-1`, one per episode), where omissions are confirmed;
* **M2-mid**: only the steps before task end (`t < T-1`), where all other errors occur.

**M3: first-alarm timing** (threshold θ = 0.5, fixed).
The first alarm is `t̂ = min{t in W : p_instant[t] >= 0.5}` (none if no such step).

* *Errorful episodes whose first onset is before task end*: `Δ = t̂ − first onset`. Report the share of these episodes that are **early** (`Δ < 0`), **on target** (`Δ = 0`), **late** (`Δ > 0`), and **missed** (no alarm). The four shares sum to 1.
* *Errorful episodes whose first onset is the task-end step* (omission only): report the share alarmed **at the task-end step**, **before it**, and **missed**.
* *Correct episodes*: the **false-alarm rate** is the share with any alarm in `W`.

**M4: error-type diagnosis** (threshold 0.5, fixed).
At step `t`, the true category set is every category whose onset is `<= t`; the prediction for category `c` is `p_type[t][c] >= 0.5`. Scored steps are:

* in errorful episodes, every `t in W` with `t >=` first onset;
* in correct episodes, every `t in W` (the true set is empty, so predicting any category is a false positive).

Each episode has total weight 1, split equally over its scored steps (weight `1/n` per step). For each category, compute the weighted binary F1 over all scored steps. M4 is the mean F1 over the categories that have at least one positive step in the evaluated set (macro-F1).

**What to report.** M1, M2 (with M2-end and M2-mid), the M3 shares and false-alarm rate, and M4. M1 alone can be high for a monitor that only checks task completion at the end, so please always report M2-mid and M3 alongside it. Use θ = 0.5 for M3 and M4; do not tune it on `test`.

**Prediction file** (one JSON object per line, one line per episode):

```json
{"id": "CAPTURE_ERROR__folding_and_storing_clothes__0001", "p_instant": [0.01, ...], "p_type": [[0.0, ...], ...]}
```

`p_instant` has length `T`; `p_type` has length `T` with nine entries per step in the category order above. Values for steps before `window_start` are ignored.
