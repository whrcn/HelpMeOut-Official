# HelpMeOut

**HelpMeOut: A Neuropsychology-Grounded Benchmark for Error-Aware Monitoring of Household Task Execution** (CoRL 2026)

[Project page](https://whrcn.github.io/HelpMeOut-Official/) · [arXiv](https://arxiv.org/abs/2610.17694)

Existing household benchmarks ask what a person wants to do. HelpMeOut asks whether their ongoing execution is going wrong, when, and how. It contains 20,000 symbolic household episodes (12,000 errorful, 8,000 correct) over 50 ADL/IADL task templates. The errorful episodes contain nine categories of everyday-action error from clinical neuropsychology (NAT/MLAT), and each error has a deterministic step-level onset label.

This release contains the **dataset**. The symbolic simulator, baselines, and the official scoring script will follow.

---

## Download

Download `HelpMeOut_v1.0.tar.gz` (69 MB; 761 MB unpacked) from [Google Drive](https://drive.google.com/file/d/1DNhPMcixl8WYiG7GEkp9f7LJ81GPdwux/view?usp=sharing) and unpack it:

```bash
tar -xzf HelpMeOut_v1.0.tar.gz
```

```
HelpMeOut/
├── train/        17,478 episodes (10,447 errorful, 7,031 correct)
├── val/           2,022 episodes  (1,241 errorful,   781 correct)
├── test/            500 episodes    (312 errorful,   188 correct)
├── manifest.csv  one row per episode: id, split, template, complexity, category, length, number of onsets
└── llm60.txt     the 60-episode test subset used for LLM and human evaluation (30 errorful, 30 correct)
```

Each episode is one JSON file named `<CATEGORY>__<task_name>__<index>.json`. Correct episodes use the category `CORRECT` (the file prefix is `CLEAN`).

## Error categories

| Category | Onset (the step labelled as the error) |
|---|---|
| `OMISSION` | the task-end step; a skipped subgoal can only be confirmed when the person declares the task finished |
| `SEQUENCE` | the step done out of order (stirring before the last ingredient is added, or a step-order norm such as buttering bread before toasting it) |
| `ANTICIPATION` | the step that commits an item before the processing the task requires (e.g. storing an unfolded shirt) |
| `PERSEVERATION` | the repeated action, after something else was done in between |
| `OBJECT_SUBSTITUTION` | the first step that uses a similar object of the same kind instead of the right one |
| `TOOL_SUBSTITUTION` | the first step that uses a similar tool instead of the right one |
| `ACTION_ADDITION` | the step that puts an unrelated item into the task's container, plate, or tray |
| `CAPTURE_ERROR` | the step that applies a needed action to an unrelated object of a different kind |
| `SPATIAL_MISREACH` | the step of leaving, empty-handed, a storage place the task never uses |

Full definitions are in Appendix A.5 of the paper. Category counts over the 20,000 episodes: OMISSION 5,280, SEQUENCE 1,478, OBJECT_SUBSTITUTION 1,142, PERSEVERATION 1,008, SPATIAL_MISREACH 874, CAPTURE_ERROR 874, ANTICIPATION 672, TOOL_SUBSTITUTION 336, ACTION_ADDITION 336. About 6.8% of errorful episodes contain more than one error.

## Episode format

```jsonc
{
  "id": "CAPTURE_ERROR__folding_and_storing_clothes__0001",
  "split": "test",
  "template_idx": 28,
  "task_name": "folding_and_storing_clothes",
  "complexity": "medium",                 // simple | medium | complex (template tier)
  "category": "CAPTURE_ERROR",            // primary category, or "CORRECT"
  "initial_scene": {                     // every object: class, subclass, type, abilities, location, states
    "glass#0": {"class": "RECEPTACLE", "subclass": "tableware", "type": "glass", "ability": [...],
                "inside": "sink", "states": {"dusty": true, "size": "small"}},
    ...
  },
  "actions": [                            // the observed execution, T steps
    {"name": "human-move", "arguments": ["h", "floor", "washing_machine"]},
    ...,
    {"name": "human-task-end", "arguments": ["h"]}   // every episode ends with the task-end event
  ],
  "labels": {
    "window_start": 7,                    // first evaluated step (= N // 4, N = actions excluding task end)
    "has_error": [0, 0, ..., 1, ..., 0],  // 1 only at onset steps (length T)
    "error_types": [[], [], ..., ["CAPTURE_ERROR"], ...],  // categories whose onset is at this step
    "onsets": [{"step": 15, "type": "CAPTURE_ERROR"}, {"step": 23, "type": "ACTION_ADDITION"}]
  },
  "metadata": {                           // NOT part of the monitor input (see below)
    "goal_expr_list": ["(forall (?x - phyobj) ...)", ...],   // formal PDDL goal of this episode
    "subgoal_boundaries": [{"subgoal_idx": 0, "subgoal_expr": "...", "start": 0, "end": 28}],
    "reference_actions": [...]            // the correct execution this episode was derived from
  }
}
```

Notes:

* `labels.has_error[t] = 1` only at the step where an error becomes observable. Later steps that are merely its consequences are labelled 0.
* `reference_actions` is the paired correct execution. For correct episodes it equals `actions`. It is `null` for 2,734 errorful episodes from an earlier generation round, whose reference was not stored; their actions and labels are complete, so they can be used for training and evaluation like any other episode.
* Actions and arguments use the PDDL domain of the paper (38 operators). The agent is always `h`; objects are named `<type>#<k>`, e.g. `shirt#0`.

## Usage

`examples/load_helpmeout.py` loads a split, builds the monitor input for a given step, and writes a prediction file:

```bash
python examples/load_helpmeout.py --root HelpMeOut --split test --out predictions.jsonl
```

## Evaluation

The official scoring script, which turns `predictions.jsonl` into M1–M4, is coming soon. The metric definitions are in [EVALUATION.md](EVALUATION.md).

## Roadmap

- ✅ Dataset: 20,000 episodes with train / val / test splits and the 60-episode LLM subset
- ⬜ Scoring script: official implementation of M1–M4 from a prediction file
- ⬜ Baseline weights: trained checkpoints of Seq2Seq, Seq2Seq+SG, and SGT
- ⬜ 3D scene graphs: time-aligned room–fixture–object scene graphs for every episode
- ⬜ Expert evaluation: results of the extended expert evaluation of the generated errors

## License

The dataset is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Citation

```bibtex
@article{wang2026helpmeout,
  title         = {HelpMeOut: A Neuropsychology-Grounded Benchmark for Error-Aware Monitoring of Household Task Execution},
  author        = {Wang, Haoran and Huang, Jingwei and Duan, Anqing and Ahn, Ho Seok and Macdonald, Bruce},
  journal       = {arXiv preprint arXiv:2610.17694},
  year          = {2026}
}
```

Contact: b.macdonald@auckland.ac.nz
