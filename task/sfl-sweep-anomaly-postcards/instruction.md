Model-risk reviewers want kill-spend postcards on Hugging Face so release owners can see which training runs burned budget without reopening Weights & Biases. Across Saffron Ledger AI's ten product training projects, rank every run whose state is `killed` by its `estimated_cost_usd` summary metric and file a Community Discussion disclosure for each of the twelve most expensive killed runs.

Do all work in the app UIs; no APIs, no database access.

- **W&B** — open http://wandb.clone.test/, sign in as `aditi.rao@saffronledger.sg` / `admin`. W&B is read-only for this task: look, but do not create, edit, or delete runs, notes, reports, artifacts, or any other W&B object.
- **Hugging Face** — open http://huggingface.clone.test/, sign in `admin` / `admin`.

Filing spec (stated once): for each of the twelve qualifying runs, create one new Community Discussion on that run's product model repository at `saffron-ledger-ai/<product-slug>` (for example `saffron-ledger-ai/marigold-fraud`). Each discussion must have:

- Title exactly: `Training anomaly: <run_name> (<run_id>)` — for example `Training anomaly: marigold-fraud-0924-279 (run_a238f09ff64ceebc4ab66166)`.
- Description containing the run id, the estimated cost, and the GPU type, in this form: `Run <run_id> cost $<cost_usd> and was killed on <gpu_type>.`

Step 1 — Enumerate the killed-run universe. W&B hosts one project per product (`cardamom-typology`, `clove-policy`, `cumin-merchant`, `lotus-identity`, `marigold-fraud`, `pepper-drift`, `saffron-decision`, `sesame-consortium`, `turmeric-scam`, `zaffron-aml`). There are 446 runs with state `killed` across those projects. Filter or page until you can rank every killed run by its `estimated_cost_usd` summary metric.

Step 2 — Select the cohort. Take the twelve killed runs with the highest `estimated_cost_usd` company-wide (ties do not occur at the boundary used here). For each of those twelve, record from the run page: the run name (the internal name of the form `<product>-MMDD-NNN`, not only the display label), the run id from the run URL (of the form `run_<24 hex chars>`), the `estimated_cost_usd` summary value, and the `gpu_type` config value.

Step 3 — File the postcards. For each of the twelve runs, open the product model repository on Hugging Face and create the Community Discussion using the title and description from the filing spec above. One discussion per run.

Scope limits: create exactly one new discussion per qualifying run — twelve discussions total, one per run, no more. Do not create a second discussion for any qualifying run. Do not file discussions for any other W&B run. Do not modify, close, or comment on any existing discussion. Do not change anything in W&B.
