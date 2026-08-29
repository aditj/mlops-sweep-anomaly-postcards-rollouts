The FinOps and Model Risk teams are closing the July GPU-spend review. Reconcile the review across Weights & Biases and Linear, then publish one incident record per eligible run on Hugging Face and one company-wide reconciliation summary.

Do all work in the visible app UIs; no APIs, no database access.

- **W&B** — http://wandb.clone.test/ — read-only.
- **Linear** — http://linear.clone.test/ — read-only. Approved exceptions are issues on the Model Risk team.
- **Hugging Face** — http://huggingface.clone.test/ — this is the only app where you should create anything.

All three apps start authenticated in the same browser session.

## 1. Build the candidate ledger

Across the ten W&B product projects (`cardamom-typology`, `clove-policy`, `cumin-merchant`, `lotus-identity`, `marigold-fraud`, `pepper-drift`, `saffron-decision`, `sesame-consortium`, `turmeric-scam`, `zaffron-aml`), find every run that meets all four conditions:

1. state is `killed`;
2. `estimated_cost_usd` is at least `$6,500.00`;
3. tag `budget-review` is present; and
4. tag `production` is present.

There are 35 killed runs at or above the dollar threshold before applying the two tag checks. Use cost descending, then run id ascending as the deterministic order.

For each candidate, record the run id, exact cost, `gpu_type`, and product slug.

## 2. Apply the two evidence-based exclusions

Exclude a candidate when either condition is true:

- **Later replacement:** in the same W&B project, a later run is state `finished`, has tag `replacement`, and its `replaces_run_id` config value exactly matches the killed run id.
- **Approved exception:** Linear has a completed Model Risk issue whose title is exactly `[Approved GPU cost exception] <run_id>` and whose description says the exception is valid through `2026-07-31`.

Do not exclude a run for a draft, expired, differently titled, or non-completed issue. Do not treat an arbitrary later successful run as a replacement unless both the `replacement` tag and exact `replaces_run_id` link are present.

Expected reconciliation shape: 35 threshold candidates; 3 non-production tag exclusions; 4 later-replacement exclusions; 4 approved-exception exclusions; 24 incidents to file. These counts are a control total, not a list of which runs qualify.

## 3. File the 24 incident discussions

For each eligible run, create exactly one Community Discussion on `saffron-ledger-ai/<product-slug>`.

- Title exactly: `[July GPU review] <product-slug> — <run-id>`
- Description exactly: `Run <run_id> in <product-slug> incurred $<cost_usd> on <gpu_type> and ended killed. No later finished replacement and no active approved exception were found.`

Use the exact two-decimal cost shown by W&B. Do not file an incident for any excluded or below-threshold run.

## 4. File the reconciliation summary

Create one additional Community Discussion on `saffron-ledger-ai/saffron-decision`.

- Title exactly: `GPU spend incident review — 2026-07-31`
- Description must contain these seven lines exactly, with the final run-id line in the same deterministic order used above:

  - `Candidates: 35`
  - `Excluded — non-production: 3`
  - `Excluded — replacement: 4`
  - `Excluded — approved exception: 4`
  - `Incidents filed: 24`
  - `Total incident spend: $296,638.05`
  - `Run IDs: <the 24 eligible run ids, comma-and-space separated>`

Scope limit: create exactly 25 new Hugging Face discussions total—24 incidents plus the summary. Do not modify or comment on existing discussions. Do not change W&B or Linear.
