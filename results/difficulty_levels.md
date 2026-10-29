# Results by difficulty level

This is a supplementary analysis that is **not in the paper**. It regroups the nine error categories by the knowledge needed to detect them and re-scores each method on each level.

| Level | Categories | What a monitor needs |
|---|---|---|
| **L1 Local pattern** | SEQUENCE, SPATIAL_MISREACH, PERSEVERATION | Only the current action and the current state |
| **L2 Progress tracking** | OMISSION, ANTICIPATION | Memory of how far the task has progressed (omissions are confirmed at the task-end step) |
| **L3 Task semantics** | OBJECT_SUBSTITUTION, TOOL_SUBSTITUTION, ACTION_ADDITION, CAPTURE_ERROR | Knowing which object or tool the task calls for |

**Scoring.** Each level is scored on its errorful episodes (by primary category) together with **all** correct episodes, pooling the steps of the level rather than averaging per-category scores. Definitions follow [EVALUATION.md](../EVALUATION.md): evaluation window from `N // 4`, including the task-end step; M1 = AUROC of the maximum `p_instant`; M2 = step-level AUPRC with only onset steps positive (the random level is the positive-step rate, shown in brackets); first alarm at θ = 0.5, on target = Δ = 0; M4 = mean of the per-category F1 within the level (correct episodes included). Episodes with missing predictions in the window (re-planner timeouts) are excluded from M1 and the alarm statistics.

## Test set (500 episodes): learned, change-point and symbolic baselines

Errorful episodes per level: L1 Local pattern 87, L2 Progress tracking 154, L3 Task semantics 71; each level is scored together with all correct episodes.

**M2: step-level detection (AUPRC)**

| Method | L1 Local pattern (0.016) | L2 Progress tracking (0.028) | L3 Task semantics (0.020) |
|---|---:|---:|---:|
| Seq2Seq | 0.057 | 0.635 | 0.044 |
| Seq2Seq+SG | 0.065 | 0.665 | 0.050 |
| SGT | 0.739 | 0.710 | 0.106 |
| CUSUM | 0.023 | 0.036 | 0.027 |
| Precondition check | 0.016 | 0.028 | 0.105 |
| Re-planner | 0.052 | 0.765 | 0.054 |

**First alarm on target (Δ = 0)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| Seq2Seq | 0% | 41% | 0% |
| Seq2Seq+SG | 0% | 34% | 0% |
| SGT | 67% | 55% | 6% |
| CUSUM | 9% | 1% | 6% |
| Precondition check | 0% | 0% | 11% |
| Re-planner | 0% | 30% | 9% |

**Missed (no alarm)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| Seq2Seq | 100% | 59% | 97% |
| Seq2Seq+SG | 99% | 66% | 97% |
| SGT | 29% | 42% | 82% |
| CUSUM | 6% | 18% | 7% |
| Precondition check | 100% | 100% | 89% |
| Re-planner | 12% | 1% | 11% |

**M1: trajectory-level discrimination (AUROC)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| Seq2Seq | 0.232 | 0.697 | 0.384 |
| Seq2Seq+SG | 0.317 | 0.737 | 0.448 |
| SGT | 0.857 | 0.834 | 0.558 |
| CUSUM | 0.818 | 0.541 | 0.657 |
| Precondition check | 0.500 | 0.500 | 0.556 |
| Re-planner | 0.747 | 0.984 | 0.819 |

**M4: mean per-category F1 within the level**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| Seq2Seq | 0.622 | 0.640 | 0.344 |
| Seq2Seq+SG | 0.553 | 0.655 | 0.490 |
| SGT | 0.813 | 0.762 | 0.229 |
| CUSUM | 0.000 | 0.000 | 0.000 |
| Precondition check | 0.000 | 0.000 | 0.077 |
| Re-planner | 0.000 | 0.467 | 0.077 |

## 60-episode LLM subset: LLMs and SGT

Errorful episodes per level: L1 Local pattern 10, L2 Progress tracking 7, L3 Task semantics 13; each level is scored together with all correct episodes. **The subset is small, so these numbers are indicative only (no confidence intervals).**

**M2: step-level detection (AUPRC)**

| Method | L1 Local pattern (0.012) | L2 Progress tracking (0.011) | L3 Task semantics (0.021) |
|---|---:|---:|---:|
| SGT | 0.514 | 0.572 | 0.110 |
| Claude Sonnet 4.6 (reasoning) | 0.339 | 0.128 | 0.252 |
| DeepSeek V4 Pro (reasoning) | 0.195 | 0.312 | 0.132 |
| GPT-5.5 low (reasoning) | 0.147 | 0.137 | 0.145 |
| GPT-5.5 medium (reasoning) | 0.158 | 0.118 | 0.135 |
| Gemini 3.1 Pro (reasoning) | 0.084 | 0.045 | 0.069 |
| MiniMax-M2.7 low (reasoning) | 0.040 | 0.030 | 0.069 |
| Kimi K2.6 | 0.144 | 0.011 | 0.159 |
| Grok 4.3 | 0.012 | 0.011 | 0.143 |
| GLM-5.1 | 0.049 | 0.091 | 0.034 |
| GPT-5.4 mini | 0.041 | 0.013 | 0.094 |
| Gemini 3.1 Flash Lite | 0.012 | 0.011 | 0.091 |
| Qwen3.6-35B-A3B | 0.012 | 0.011 | 0.082 |
| DeepSeek V4 Flash | 0.012 | 0.011 | 0.021 |

**First alarm on target (Δ = 0)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| SGT | 50% | 43% | 0% |
| Claude Sonnet 4.6 (reasoning) | 70% | 43% | 31% |
| DeepSeek V4 Pro (reasoning) | 40% | 57% | 31% |
| GPT-5.5 low (reasoning) | 60% | 57% | 31% |
| GPT-5.5 medium (reasoning) | 60% | 43% | 31% |
| Gemini 3.1 Pro (reasoning) | 60% | 29% | 23% |
| MiniMax-M2.7 low (reasoning) | 10% | 14% | 23% |
| Kimi K2.6 | 10% | 0% | 15% |
| Grok 4.3 | 0% | 0% | 8% |
| GLM-5.1 | 10% | 14% | 15% |
| GPT-5.4 mini | 0% | 0% | 8% |
| Gemini 3.1 Flash Lite | 0% | 0% | 15% |
| Qwen3.6-35B-A3B | 0% | 0% | 8% |
| DeepSeek V4 Flash | 0% | 0% | 0% |

**Missed (no alarm)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| SGT | 50% | 57% | 92% |
| Claude Sonnet 4.6 (reasoning) | 30% | 43% | 31% |
| DeepSeek V4 Pro (reasoning) | 30% | 14% | 31% |
| GPT-5.5 low (reasoning) | 0% | 14% | 23% |
| GPT-5.5 medium (reasoning) | 10% | 29% | 31% |
| Gemini 3.1 Pro (reasoning) | 0% | 29% | 8% |
| MiniMax-M2.7 low (reasoning) | 40% | 57% | 62% |
| Kimi K2.6 | 20% | 57% | 69% |
| Grok 4.3 | 50% | 86% | 77% |
| GLM-5.1 | 20% | 14% | 15% |
| GPT-5.4 mini | 50% | 86% | 85% |
| Gemini 3.1 Flash Lite | 90% | 100% | 69% |
| Qwen3.6-35B-A3B | 100% | 100% | 92% |
| DeepSeek V4 Flash | 100% | 100% | 100% |

**M1: trajectory-level discrimination (AUROC)**

| Method | L1 Local pattern | L2 Progress tracking | L3 Task semantics |
|---|---:|---:|---:|
| SGT | 0.737 | 0.829 | 0.564 |
| Claude Sonnet 4.6 (reasoning) | 0.755 | 0.674 | 0.664 |
| DeepSeek V4 Pro (reasoning) | 0.652 | 0.810 | 0.629 |
| GPT-5.5 low (reasoning) | 0.643 | 0.624 | 0.626 |
| GPT-5.5 medium (reasoning) | 0.638 | 0.610 | 0.604 |
| Gemini 3.1 Pro (reasoning) | 0.543 | 0.514 | 0.624 |
| MiniMax-M2.7 low (reasoning) | 0.583 | 0.514 | 0.491 |
| Kimi K2.6 | 0.828 | 0.702 | 0.641 |
| Grok 4.3 | 0.675 | 0.500 | 0.560 |
| GLM-5.1 | 0.577 | 0.531 | 0.599 |
| GPT-5.4 mini | 0.718 | 0.505 | 0.512 |
| Gemini 3.1 Flash Lite | 0.532 | 0.483 | 0.633 |
| Qwen3.6-35B-A3B | 0.500 | 0.500 | 0.538 |
| DeepSeek V4 Flash | 0.500 | 0.500 | 0.500 |

## Observations

- **L3 is unsolved by every method.** On the test set, no method exceeds M2 0.106 or 11% on-target alarms on L3; the best learned monitor (SGT) misses 82% of L3 errors.
- **L1 and L2 reward different capabilities.** SGT, which checks each action against the current state, does well on both (M2 0.739 and 0.710). Seq2Seq and the re-planner are near chance on L1 but strong on L2, which is dominated by omissions confirmed at the task-end step, where a completion check suffices.
- **Reasoning LLMs do relatively better on L3.** On the 60-episode subset, Claude Sonnet 4.6 reaches M2 0.252 and 31% on-target alarms on L3, against 0.110 and 0% for SGT, while SGT is stronger on L1 and L2. With 7–13 errorful episodes per level, this is a trend, not a conclusion.
