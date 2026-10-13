# Revenue Capture model comparison

Run date: 13 October 2026. This is a small synthetic development test, not a benchmark, merchant study, production accuracy estimate or live prototype integration.

## Observed results

| System | Exact cases correct | Supported proposals found | False proposals |
|---|---:|---:|---:|
| Adapted job-ID plus keyword rules | 13/20 | 4/10 | 0 |
| Guarded synonym rules | 16/20 | 7/10 | 1 |
| Fresh Codex model evaluator | 20/20 | 10/10 | 0 |

An exact correct case requires all three outputs to match the frozen label: decision, amount and completion-record ID. Reasons are retained for inspection but not scored. A false proposal means proposing a charge when the expected decision was hold or exclude. “Propose” means a candidate for merchant review, never permission to bill or send.

The model’s observed proposal precision was 10/10 and recall 10/10 on this set. These tiny denominators do not establish production precision or recall. The guarded rules’ false proposal was C13, where an existing invoice described the same packaging service differently.

## What was run

Codex drafted 20 fictional, partly structured cases spanning logistics and service work. There are ten supported opportunities and ten cases requiring a hold or exclusion. Coverage includes paraphrases, missing job IDs, included labour time, later scope reductions, prior billing, waived or bundled work, missing approval, wrong customers, ambiguous receipts, disputes, incomplete fixed-fee batches and an instruction embedded in a source record.

Cases, labels, the evaluation prompt and both rule baselines were frozen before the fresh model response. Their SHA-256 hashes and freeze time are in `manifest.json`. The scorer verifies those hashes. Neither cases nor baselines were revised after seeing model predictions. No attempt was discarded or retried.

After the user explicitly authorised a separate evaluator, a new Codex agent was started with no inherited conversation history. It was instructed to read only `model-prompt.txt`, which contains the policy and case inputs, and to return JSON without opening other files or using external information. It received no answer key or rule predictions. Its first final response is saved verbatim as `model-response.json`.

This was real model inference through a fresh Codex agent, not the prototype’s scripted AI interpretation. The collaboration tool did not expose an exact model/version identifier or sampling configuration; no version is claimed. The agent inherited the session’s configured model without an override. This limits exact model-level reproducibility. `evaluator-provenance.json` records the run context.

## Relationship to the prototype

The original prototype’s `semanticBaseline()` checks whether the Nila receipt contains the job ID and the words “festive sleeves”; it also counts contextual candidates. A separate runtime check on the unchanged HTML found both literal checks false and two contextual candidates. See `demo-flow-check.json`.

The 20-case baselines are **adaptations**, not the unchanged prototype function. That function handles one scripted case and does not itself classify a general dataset. `run_rules.py` generalises its literal matching approach and adds common approval, completion, pricing and billing safeguards. The second baseline adds a fixed synonym dictionary and permits missing job IDs when context is unique. Both see the same fixture fields as the model. The synonym baseline is stronger than the literal one, but it is not an exhaustive or independently optimised rules system.

## Limits and the next test

- Codex authored both the cases and labels. A fresh evaluator avoids showing it the answer key, but does not make the dataset independently designed or labelled.
- The post-run overlap review identifies five Nila-family cases: C02, C10, C13, C17 and C19. Other fixtures also reuse prototype service families. See `Demo Overlap Review.md`. This is not a held-out test of unfamiliar merchant data.
- Many fields are already structured. The test does not measure OCR, raw message ingestion, identity resolution across real systems, source authenticity or invoice completeness.
- Labels are design expectations, not judgments validated by a merchant or accountant. More expressive rules might close part of the gap.
- One run was scored. Latency, cost, repeatability and merchant review time were not measured. All payment amounts are fictional.
- Next: independently label anonymised merchant records before testing; include difficult negative cases and tune rules on a separate development set. Compare model and rules on the same unseen records, measuring invalid proposals and active review time as well as recall.

## Reproduction and inspection

Use Python 3; no third-party packages are required:

```bash
python3 run_rules.py
python3 score_model.py model-response.json
```

This reproduces the rules and scoring of the saved model response; it does not rerun inference. For a new inference run, supply only `model-prompt.txt` to a fresh model context and retain its first response in a new file. Record the exact model version and settings when the provider makes them available. Do not overwrite the original response or tune the frozen labels against new predictions.

`case-comparison.csv` contains every label and prediction result. `comparison-results.json` contains aggregate scores. `labels.json` gives the author’s rationale for each expected decision.

## Submission wording

“On 20 synthetic cases drafted with Codex, a fresh evaluator matched all 20 frozen labels; guarded synonym rules matched 16. The evaluator did not see the labels. This is a small, partly structured development test, not a benchmark; independent merchant-data testing is next.”
