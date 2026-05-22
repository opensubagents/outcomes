# Research review — Claude Code OTel backend recommendation

- **Reviewed:** 2026-05-22
- **Reviewer:** founding maintainer (`@zhoukalex`)
- **Subject:** an externally supplied research doc titled "Claude Code OTel
  Backend Recommendation — Cloudflare Workers Integration Required" that
  ranks Axiom > Honeycomb > Grafana Cloud as the OTel destination for
  Claude Code CLI telemetry, with a hard CF Workers integration premise.
- **Question this memo answers:** Should the Open Outcome spec or its
  reference SDKs change in response to this research?
- **Verdict:** **No spec changes.** The spec stays vendor-neutral. The
  research is about Claude Code CLI telemetry, not the Open Outcome spec.
  Two of the research's load-bearing claims do not hold up under audit
  (Honeycomb Metrics is GA, not Beta; the CF Workers premise is not
  motivated by anything in this repo). The first-choice Axiom
  recommendation survives as a defensible dev-infra default *only if the
  CF Workers premise turns out to apply*, which the operator has not
  confirmed.

## Method

Each substantive claim in the research was re-fetched at the cited URL
on 2026-05-22 and compared to the wording in the research doc. The
Claude-Code-CLI-specific claims (`prompt.id` exclusion, default export
intervals) were verified via the `claude-code-guide` subagent against
the current `<https://code.claude.com/docs/en/monitoring-usage>` page.

## Per-claim verdicts

| # | Research claim | Verdict | Source fetched | Notes |
|---|---|---|---|---|
| 1 | Axiom Metrics GA on 2026-03-27 with MetricsDB / MPL, "no active time series limits" | **Confirmed** | <https://axiom.co/changelog/metrics-mpl> | Verbatim: *"Metrics are now generally available. MetricsDB applies the same architecture Axiom already uses for logs, traces, and events..."*; date 2026-03-27. |
| 2 | Axiom publishes a Claude-Code-specific OTel guide using `x-axiom-metrics-dataset` and `x-axiom-dataset` headers | **Confirmed** | <https://axiom.co/docs/guides/opentelemetry-claude-code> | Page resolves, two datasets required, env vars `OTEL_EXPORTER_OTLP_{METRICS,LOGS}_{ENDPOINT,HEADERS}`. |
| 3 | Cloudflare's CF-native "Destinations" path does **not** support OTel metrics for any vendor today | **Confirmed** | <https://developers.cloudflare.com/workers/observability/exporting-opentelemetry-data/> | Verbatim: *"Exporting Worker infrastructure metrics and custom metrics via OpenTelemetry is not currently available."* (Known limitations.) |
| 4 | Honeycomb Metrics is still in Beta as of May 2026 with carve-outs ("Creating SLOs using metrics" unsupported, Metrics datasets excluded from environment-wide queries) | **Contradicted** | <https://www.honeycomb.io/blog/honeycomb-metrics-generally-available> | Verbatim: *"Today, we are announcing the general availability of Honeycomb Metrics: native time series storage for infrastructure metrics, fully integrated with Honeycomb's existing events platform, with both models queryable through a single interface."* Date: **2026-03-11**, ~two weeks before Axiom's metrics GA. The cited beta-status doc page (`docs.honeycomb.io/.../experimental-features/metrics/`) is now a historical artifact. **This materially weakens the Honeycomb "runner-up" tradeoff in the research.** |
| 5 | Claude Code monitoring docs say "prompt.id is intentionally excluded from metrics" and default intervals are "60 seconds for metrics and 5 seconds for logs" | **Confirmed verbatim** | <https://code.claude.com/docs/en/monitoring-usage> (via `claude-code-guide` subagent) | Both quotes match the page word-for-word. |
| 6 | Honeycomb's "Claude Code Monitoring" Board template exists; Honeycomb blog walks through env-var setup | **Confirmed** | <https://www.honeycomb.io/blog/can-claude-code-observe-its-own-code> | Verbatim: *"To create the monitoring board, go to the 'Boards' tab, select 'Templates,' and select 'Claude Code Monitoring.'"* |
| 7 | Honeycomb pricing — Free 20M events, Pro from $130 / 100M events | **Confirmed (with addendum)** | <https://www.honeycomb.io/pricing> | Verbatim: *"Free: Up to 20M events and 100M time series data points"* and *"Pro: Starting at $130 / 100M events (up to 1.5B) and 500M time series data points"*. The research understated by omitting the metrics-data-point allowances. |
| 8 | Grafana Cloud "billable series = active series × DPM" | **Partially incorrect** | <https://grafana.com/docs/grafana-cloud/cost-management-and-billing/manage-invoices/understand-your-invoice/metrics-invoice/> | Active-series definition is correct: *"A time series is considered active if new data points have been received within the last 20 minutes."* But the billing formula is the maximum of two terms, not their product: `usage = max(active_series, total_dpm/included_dpm)` × `$6.50 / 1000`. The qualitative high-cardinality cost trap still holds; the multiplicative phrasing is wrong. |

## Material findings the research did not state

1. **Claude Code's own monitoring docs are not vendor-neutral.** They
   specifically name Honeycomb, Datadog, Grafana Tempo, Jaeger, and
   Zipkin as supported backends, with Honeycomb cited four times for
   metrics, events, and traces. Axiom is *not* named in the official
   docs. This cuts against the research's first-choice Axiom
   recommendation: a team that defaults to "what the official docs
   point at" will not pick Axiom.

2. **Honeycomb's GA changes the runner-up calculus.** With metrics GA
   on 2026-03-11 and SLOs available on Pro plans (per a separate
   Honeycomb changelog entry), the research's main reason to prefer
   Axiom over Honeycomb — "Honeycomb Metrics is still Beta with no
   SLOs" — no longer applies. The remaining differentiators
   (`per-GB ingest vs per-event pricing`, `hyper-cardinality without
   active-series tax`, `Cloudflare-native metrics support`) are
   narrower and more workload-dependent.

3. **The CF Workers premise is not motivated by anything in this
   repo.** Open Outcome v0.1 ships pure Python and TypeScript SDKs.
   There is no Cloudflare Worker code, no Wrangler config, no Workers
   AI dependency. If the CF Workers requirement comes from a separate
   effort (Claude Code dogfood infra, an MCP server hosted on Workers,
   another sibling repo), the operator should confirm before that
   premise is allowed to drive the recommendation.

## Scope correction

The research is **about Claude Code CLI telemetry**, not about Open
Outcome. Two reasons keep it out of the spec:

- `specification/appendix-b-otel-extension.md` is explicit that Open
  Outcome emits plain `gen_ai.outcome.*` span attributes "without any
  upstream changes" and that the SDK projection deliberately does not
  depend on the OTel SDK. Naming a vendor in appendix B or the SDKs
  would contradict that commitment.
- Open Outcome's surface is `OutcomeDeclaration` / `Report` /
  `Verdict` plus a `HeuristicVerifier`. None of those types know which
  backend the consumer ships spans to.

The research is therefore informative dev-infra advice, not normative
spec input.

## Recommendation

For **the spec**: no change. Keep
`appendix-b-otel-extension.md` vendor-neutral. Do not introduce any
vendor-specific config to the SDKs.

For **dev infra** (i.e., where to ship the OTel data this repo's own
Claude Code agents generate while developing the spec):

- If the CF Workers premise is confirmed, **Axiom** remains a defensible
  default — its CF Workers guide is first-party, MetricsDB removes the
  active-series tax that bites `user.account_id`/`model`/`speed`/`effort`
  cross-products on `claude_code.cost.usage`, and the Claude-Code-specific
  guide is concrete.
- If the CF Workers premise is **not** real, the recommendation flips:
  **Honeycomb** is the safer first choice because Claude Code's own
  monitoring docs steer users there, Metrics is now GA with SLOs on Pro
  plans, the Free tier (20M events) is enough for a single-maintainer
  dogfood at the v0.1 stage, and there is a dedicated "Claude Code
  Monitoring" Board template that skips the dashboard-construction work.
- **Grafana Cloud** stays third for our workload because its
  active-series pricing model is a poor fit for Claude Code's
  high-cardinality attributes, regardless of the CF Workers question.

For **the next branch on this repo**: stage the vendor-neutral
follow-ups already named in
`docs/plans/2026-05-21-drop-bootstrap-and-audit-otel.md` Step 3
(`examples/local-otel/` end-to-end and an *informative* backend-notes
appendix) so the OTel posture is exercised at the wire level without
the spec ever picking a vendor.

## Open questions for the operator

1. Is the "Cloudflare Workers integration required" premise real for
   this repo, or did it come from a sibling effort? The answer flips
   the dev-infra first choice between Axiom and Honeycomb.
2. Is metrics-side SLO alerting in scope for the dogfood?
   (Honeycomb Pro now has it; Free does not.)
3. Approximate event volume per active developer per month? The
   per-GB-ingest vs per-event-count tradeoff depends on this. With
   `OTEL_LOG_USER_PROMPTS=1` enabled, a single developer can pass 20M
   events/month quickly, which moves Honeycomb from Free to Pro.

## Citations

- <https://axiom.co/changelog/metrics-mpl> (primary, accessed 2026-05-22)
- <https://axiom.co/docs/guides/opentelemetry-claude-code> (primary, accessed 2026-05-22)
- <https://developers.cloudflare.com/workers/observability/exporting-opentelemetry-data/> (primary, accessed 2026-05-22)
- <https://www.honeycomb.io/blog/honeycomb-metrics-generally-available> (primary, accessed 2026-05-22)
- <https://docs.honeycomb.io/troubleshoot/product-lifecycle/experimental-features/metrics/> (primary, accessed 2026-05-22 — now historical)
- <https://code.claude.com/docs/en/monitoring-usage> (primary, accessed 2026-05-22 via `claude-code-guide` subagent)
- <https://www.honeycomb.io/blog/can-claude-code-observe-its-own-code> (secondary, accessed 2026-05-22)
- <https://www.honeycomb.io/pricing> (primary, accessed 2026-05-22)
- <https://grafana.com/docs/grafana-cloud/cost-management-and-billing/manage-invoices/understand-your-invoice/metrics-invoice/> (primary, accessed 2026-05-22)
- <https://changelog.honeycomb.io/metrics-and-slos-available-for-pro-plans-228153> (secondary, surfaced via WebSearch on 2026-05-22)
