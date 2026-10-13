# Revenue Capture — supporting build artifact

Revenue Capture is a local, interactive submission prototype for reviewing approved, completed work that may be missing from invoices. It presents linked evidence and calculations, lets the merchant edit or reject a proposal, requires approval before simulated sending, and separates pending charges from matched collections.

## Open the prototype

Download **Revenue Capture.html** and open it in a desktop browser. The file contains its own styles, application code and logo. No installation, API key or merchant account is required. Start with **Connections**, then **Overview → Nila Foods**, and finish with **Value realisation**. The built-in Northstar records and monetary amounts are fictional.

Use **Reset workspace** before a fresh demo if you previously changed the case state. This resets this prototype's locally saved walkthrough state. Interface preferences and review activity use browser storage; no server stores this walkthrough. Data/privacy options affect local demo state, not records held by an external provider.

## Included files

| File/folder | Purpose |
|---|---|
| Revenue Capture.html | Self-contained interactive artifact |
| src/ | Editable HTML, JavaScript, CSS, language catalogue and logo asset |
| AI_Build_Log.md | Standalone build log with research, prompts, human decisions, all 20 case outcomes and limitations |
| ARCHITECTURE.md | What exists today and the proposed production architecture |
| DEMO_SCRIPT.md | Section-wise video narration and click instructions |
| evaluation/ | Frozen synthetic cases/labels, baselines, prompt, first response, scorer, provenance and results |
| build.py | Rebuild the self-contained HTML from src/ using Python 3 |
| FILE_MANIFEST.json | SHA-256 hashes of the packaged files |

## What the prototype demonstrates

- Connector/provider choices, processing-policy preview, permission boundaries and account removal.
- Overview metrics and case/source breakdowns.
- Evidence review, rejection, editable charges and approval-based invoice drafts.
- A separate scripted investigation that illustrates scope revision, conflict and clarification.
- Simulated send, customer response and matched payment; sending or acceptance alone does not count as collections.
- Value reporting, activity history, profile/settlement/preferences, accessibility options, Help and Ask Ray guidance.

## Implementation status

The prototype is custom browser code, with Razorpay Blade and other design systems used as references. It does not install the Blade component library. Source authorisation, external scanning, real invoice delivery, payments and settlements are not connected. AI interpretations and Ask Ray answers in the interface are scripted. The separate model evaluation is real inference recorded outside the prototype, not a runtime integration.

The work is a submission demonstration, not an official Razorpay release. The included Razorpay logo is a brand-reference asset; it does not imply affiliation.

## Inspect the evaluation

The saved comparison reports 13/20 exact cases for job-ID/keyword rules, 16/20 for guarded synonyms and 20/20 for one fresh evaluator run. Cases and labels were AI-authored and partly structured. Five cases overlap with the Nila service family; the set is development material rather than an independent benchmark.

Open **evaluation/README.md** for methodology. To reproduce the rules and scoring of the saved response, use Python 3:

```sh
cd evaluation
python3 run_rules.py
python3 score_model.py model-response.json
```

These commands regenerate local scoring outputs. They do not invoke a model or reproduce inference. Exact evaluator model/version metadata was unavailable. The original freeze manifest, response and overlap-review note are included for inspection.

## Rebuild from source

```sh
python3 build.py
```

Then open **Revenue Capture.html**. The self-contained file is the recommended reviewer entry point; src/index.html is supplied for code inspection and editing.

## Sharing

This pack is prepared for a public repository or a Drive folder with Viewer access. It has not been published by this packaging step. Upload the contents together so relative documentation links work. No paid reports, private merchant records, API keys, credentials, personal filesystem paths or conversation exports are included.
