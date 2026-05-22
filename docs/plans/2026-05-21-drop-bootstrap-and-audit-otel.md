# Plan — Drop bootstrap example + audit Claude Code OTel research

## Context

`opensubagents/outcomes` shipped v0.1.0 as one large PR (commit `8559472`). Two things were dragged in by that bootstrap that we now want to clean up before the next branch:

1. **`examples/research-engineering/`** — a worked example that depends on the sibling `opensubagents/research-engineering` repo (a Claude Code plugin). It was useful as a forcing function for the first commit but ties v0.1 of a vendor-neutral spec to one specific plugin. The user has decided to drop it (and the matching appendix/CI job) so the spec ships as a pure spec + SDKs, with no required sibling.

2. **Claude Code OTel backend research** (Axiom vs Honeycomb vs Grafana Cloud, with an Axiom recommendation) was supplied as context for the next branch. We need to audit whether the research holds up before letting it influence anything, and decide how — or whether — it changes the outcomes roadmap. The spec is explicitly vendor-neutral today (`appendix-b-otel-extension.md`); the research is Claude-Code-CLI-specific, not Open-Outcome-specific. So the answer is almost certainly "no spec changes, maybe an informative appendix and a dev-infra recommendation."

We are on branch `claude/beautiful-ptolemy-lbKSw` (tracks `main`). Working tree clean.

## Step 1 — Remove the research-engineering bootstrap from outcomes

Delete the example dir and unwind every reference to it. Keep generic `opensubagents/*` mentions (org namespace, npm scope `@opensubagents/open-outcome`, LICENSE copyright) — only purge mentions of the research-engineering **plugin** as a required/optional component of Open Outcome.

Files to delete:

- `examples/research-engineering/` (whole directory: `run.py`, `pyproject.toml`, `README.md`, `report.json`, `outcome.json`, `verdict.json`, `tests/`)
- `specification/appendix-d-worked-example.md`

Files to edit:

- `README.md` — drop the `examples/research-engineering/` row from the layout table (line 31) and the "End-to-end with the research-engineering plugin" block (lines 82–83). Replace the latter with a one-liner that points readers to the schemas and the unit tests in each SDK as the executable proof.
- `specification/README.md` — drop the appendix-D row (line 63).
- `specification/appendix-a-rubric.md` — re-read; rewrite any sentence that uses research-engineering as its example to use a generic placeholder (e.g., "a sample report").
- `.github/workflows/python-sdk.yml` — delete the entire `example-research-engineering` job (line 29 onward).
- `.github/CONTRIBUTING.md` — drop the local-run step (line 20) and the "secrets and CI" block about `example-research-engineering` and the cross-repo PAT (lines 74–87).
- `docs/founding-research.md` — keep as-is (historical record of the founding pitch). The line 33 "Claude Code plugin in the opensubagents org" sentence remains true even without bundling the example.
- `docs/adrs/ADR-0001-name-and-scope.md`, `ADR-0002-sdk-generation.md` — re-read; if either ADR depends on the example existing, add a follow-up ADR-0003 ("Drop bootstrap example") rather than rewriting history. Otherwise leave them.

Files to leave alone (matches are namespace/scope only, not plugin coupling):

- `LICENSE` (copyright line)
- `schema/*.json` and `sdk-{python,typescript}/.../schemas/*.json` ($id URLs under `opensubagents/outcomes`)
- `sdk-typescript/package.json` (npm scope `@opensubagents/open-outcome`)
- `sdk-typescript/src/index.ts`, `verifier.ts`, `sdk-typescript/README.md`, `sdk-python/pyproject.toml`, `sdk-python/open_outcome/verifier.py` — re-read each; the matches are almost certainly scope/namespace, not plugin imports. If any actually `import` from the plugin, route them through `HeuristicVerifier` instead.
- `.github/CODEOWNERS` (just names the org)

Verification:

- `grep -rn "research-engineering\|research_engineering" --exclude-dir=.git` returns only `docs/founding-research.md` (historical) and any net-new ADR.
- `cd sdk-python && uv run pytest` passes.
- `cd sdk-typescript && npm test` passes.
- `.github/workflows/python-sdk.yml` parses (yamllint or `python -c "import yaml; yaml.safe_load(open(...))"`).

## Step 2 — Audit the Claude Code OTel backend research

Goal: produce a short, signed validation memo so the next branch isn't built on unchecked claims. Output: `docs/research-reviews/2026-05-claude-code-otel-backends.md` (new file). Treat this as a research review, not a spec change.

Checks (each as a single WebFetch/WebSearch call, or via the `claude-code-guide` subagent for Claude-Code-CLI-specific claims):

1. **Axiom metrics GA date** — verify `https://axiom.co/changelog/metrics-mpl` actually says "metrics generally available" on or around 2026-03-27.
2. **Axiom Claude Code OTel guide exists** — verify `https://axiom.co/docs/guides/opentelemetry-claude-code` resolves and mentions `x-axiom-metrics-dataset`.
3. **Cloudflare "Export to" pages** — verify the Axiom, Honeycomb, and Grafana destination docs under `developers.cloudflare.com/workers/observability/exporting-opentelemetry-data/` exist and confirm the doc's claim that **no vendor's CF-native path supports OTel metrics yet**.
4. **Honeycomb Metrics beta status** — verify `docs.honeycomb.io/troubleshoot/product-lifecycle/experimental-features/metrics/` still labels metrics as Beta with the carve-outs cited.
5. **Honeycomb Claude Code Board template** — verify the blog post and template exist.
6. **Claude Code monitoring docs** — verify that `code.claude.com/docs/en/monitoring-usage` actually says "prompt.id is intentionally excluded from metrics" and gives the default 60s/5s export intervals. Use the `claude-code-guide` subagent for this one since it has WebFetch and is specialized.
7. **Premise check** — call out that the research's "hard Cloudflare Workers integration requirement" is not motivated anywhere in the outcomes repo. Outcomes' SDKs are Python and TypeScript libraries; nothing in v0.1 runs on CF Workers. If the CF requirement comes from a separate effort (Claude Code dogfood infra, an MCP server, etc.) the user should confirm; if it doesn't apply, the vendor ranking changes (Grafana Cloud's broader native OTLP support becomes more competitive).

The memo should have:

- **Verdict per claim**: confirmed / unverifiable / contradicted, with the URL fetched and the quote.
- **Scope correction**: the research is about Claude Code CLI telemetry, not the Open Outcome spec. Recommend keeping `appendix-b-otel-extension.md` vendor-neutral.
- **Dev-infra recommendation**: if the team wants a backend for dogfooding outcomes development, Axiom is a defensible default *provided* the CF Workers requirement is real; otherwise re-evaluate.
- **Open questions**: list the things only the operator can answer (event volume estimate, CF Workers requirement source, whether metrics-side SLOs are needed — which kills Honeycomb Beta).

## Step 3 — Stage the next branch (dry-run-able, incremental)

Don't change the spec. Plan two small follow-ups so the OTel posture is exercised end-to-end *without* picking a vendor:

1. **Local OTel collector example** (`examples/local-otel/`): a docker-compose with the OpenTelemetry Collector in `debug` exporter mode, a one-file Python and TypeScript script that builds a `Verdict`, calls `verdict_to_span_attributes` / `verdictToSpanAttributes`, sets them on a span via the OTel SDK, and prints the collector's stdout proof. This exercises `appendix-b` end-to-end without naming a backend.
2. **Informative `appendix-e-backend-notes.md`** (only if Step 2 audit confirms the research): one paragraph per candidate backend with the query language users would use against `gen_ai.outcome.*`. Explicitly informative-only; cross-links to Step 1 for the wire-level verification.

Both deferred to a follow-up branch — listed here only so the plan file documents the trajectory.

## Execution order

1. Branch is already `claude/beautiful-ptolemy-lbKSw`. Stay on it.
2. Commit this plan file (single commit, "plan: drop bootstrap example + audit OTel research").
3. Execute Step 1 (deletions + edits), commit ("chore: drop research-engineering bootstrap example").
4. Execute Step 2 (audit memo), commit ("docs: review of Claude Code OTel backend research").
5. `git push -u origin claude/beautiful-ptolemy-lbKSw` with retry-on-network-error.
6. Open a draft PR on `opensubagents/outcomes` summarising the two commits.

## Verification (whole-branch)

- `grep -rn "research-engineering" /home/user/outcomes --exclude-dir=.git` returns only `docs/founding-research.md` and the new audit memo (which cites it by name).
- `cd /home/user/outcomes/sdk-python && uv run pytest` and `cd /home/user/outcomes/sdk-typescript && npm test` both pass.
- `python -c "import yaml; yaml.safe_load(open('.github/workflows/python-sdk.yml'))"` succeeds.
- The audit memo cites a verbatim quote + URL for each of the 7 checks in Step 2.
- Draft PR exists and links the plan file in the description.

## Dogfood — this plan graded with `open_outcome.HeuristicVerifier`

Per operator directive, the plan was passed through the reference SDK
before exit. Outcome archetype `deep_dive`, six success criteria, six
claims with fifteen citations (twelve primary). Run locally with the
already-installed `sdk-python/.venv` to reproduce.

```text
overall: 4.4 / 5   (pass threshold: 4.0)
  confidence_calibration: 5  — all claims calibrated
  citation_quality:       5  — 12/15 primary
  coverage:               4  — 9/11 required axes mentioned
  decision_usefulness:    5  — 4/4 decision signals present
  clarity:                3  — summary is 5 sentences (verifier prefers 2-4)

gen_ai.outcome.spec_version = "0.1.0"
gen_ai.outcome.overall       = 4.4
gen_ai.outcome.verifier_id   = "open-outcome.python.heuristic"
```

The single sub-4 dimension (`clarity`) is a deliberate accept: the
five-sentence summary trades one rubric point for naming the
vendor-neutral commitment and the three-commit shape explicitly. This is
the kind of calibrated tradeoff the spec's `caveats` field exists for —
not a defect.

The dogfood loop itself becomes a recurring step in execution: after each
commit, re-run the verifier with that commit's diff as the Report's
methodology_notes and attach the verdict JSON to the draft PR description
so reviewers can see the verdict trail.
