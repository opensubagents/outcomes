---
title: Appendix B — OpenTelemetry extension
description: Proposed gen_ai.outcome.* attributes for OpenTelemetry GenAI semconv.
---

# Appendix B — Proposed OpenTelemetry `gen_ai.outcome.*` extension

> This appendix is **informative** and describes a proposed addition to the
> upstream
> [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).
> Open Outcome reference SDKs emit these attributes today as plain span
> attributes — they show up in any OTel-compatible backend without any
> upstream changes.

## Why an extension is proposed

OpenTelemetry GenAI semconv 1.41.0 normatively defines attributes for what
an agent *did* — `gen_ai.input.messages`, `gen_ai.output.messages`,
`gen_ai.usage.input_tokens`, etc. — but does not define attributes for
what an agent *should have done* or how its output graded against that
expectation. That gap is precisely what Open Outcome standardizes (see
[`docs/founding-research.md`](../docs/founding-research.md), claim 5).

The cleanest place for the missing attributes is the same namespace as the
existing ones: `gen_ai.outcome.*`. Adding them upstream lets every existing
OTel-compatible backend treat verdicts as first-class telemetry without
custom processors.

## Proposed attribute table

| Attribute | Type | Required? | Description |
|---|---|---|---|
| `gen_ai.outcome.spec_version` | `string` | Required when any `gen_ai.outcome.*` attribute is present | Open Outcome spec version the verdict was produced against. Example: `0.1.0`. |
| `gen_ai.outcome.overall` | `double` | Recommended | Verdict's overall score (mean of dimensions, one decimal place). |
| `gen_ai.outcome.dimension_count` | `int` | Recommended | Count of dimensions on the verdict. |
| `gen_ai.outcome.evidence_count` | `int` | Recommended | Count of citations the verdict considered. |
| `gen_ai.outcome.verifier_id` | `string` | Optional | Identifier of the verifier (e.g. `open-outcome.python.heuristic`). |
| `gen_ai.outcome.dimension.<name>.score` | `int` | Optional | Per-dimension score. `<name>` is lower-snake-case. |

## Proposed span name

| Span name | Description |
|---|---|
| `verify_outcome` | A span that carries a verdict. Distinct from the surrounding `invoke_agent` span. |

## What is *not* proposed for span attributes

The verdict's full `evidence` array (citations including titles and
quotes) is intentionally **not** an attribute. Evidence belongs on span
*events* or in a separate log record. The Open Outcome reference SDKs
emit a single `outcome.evidence` event per citation, carrying `url`,
`title`, `kind`, and `accessed` as event attributes.

## Upstream plan

At v0.1 of Open Outcome, the path to upstream is documented but not yet
walked. Once the spec graduates from Experimental to Hardening, the TSC
will file an issue against
[`open-telemetry/semantic-conventions`](https://github.com/open-telemetry/semantic-conventions)
proposing these attributes for inclusion in the GenAI conventions. Until
then, the reference SDKs ship the attribute names exactly as listed above
so that they will be a drop-in match if the upstream proposal is accepted.
