# Open Outcome

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](./MATURITY.md)
[![spec: v0.1.0](https://img.shields.io/static/v1?label=Spec&message=v0.1.0&color=blue)](./specification/README.md)
[![license: Apache-2.0](https://img.shields.io/static/v1?label=License&message=Apache--2.0&color=success)](./LICENSE)

**Open Outcome** is a vendor-neutral specification for declaring, verifying, and
grading the outcomes that managed AI agents are supposed to produce.

Existing standards already cover the layers around it: the
[Model Context Protocol](https://modelcontextprotocol.io/) defines how tools
and capabilities are exposed to agents, the
[OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
define how agent runs are observed, and Anthropic's
[knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)
format defines how plugins are packaged. None of them standardize the
**declare → verify → grade** triple: what should be true after an agent runs,
how to check it, and how to report a verdict with cited evidence. That is the
gap Open Outcome closes.

The full rationale lives in [`docs/founding-research.md`](./docs/founding-research.md).

## What's in this repo

| Path | What it is |
|---|---|
| [`specification/`](./specification/) | The normative spec. RFC 2119 keywords (MUST / SHOULD / MAY) inside blockquotes under numbered `Requirement` headings. |
| [`schema/`](./schema/) | JSON Schemas for `outcome`, `verdict`, and `evidence`. The schemas are the machine-checkable form of the spec. |
| [`sdk-python/`](./sdk-python/) | Reference Python SDK — pydantic v2 models, `HeuristicVerifier`, OTel span helper. Package name `open-outcome`. |
| [`sdk-typescript/`](./sdk-typescript/) | Reference TypeScript SDK — zod schemas, `HeuristicVerifier`, OTel span helper. Package name `@opensubagents/open-outcome`. |
| [`docs/`](./docs/) | Founding research, ADRs (architectural decision records), and research reviews. |
| [`GOVERNANCE.md`](./GOVERNANCE.md), [`MAINTAINERS.md`](./MAINTAINERS.md), [`MATURITY.md`](./MATURITY.md) | Governance, current maintainers, and the Experimental → Hardening → Stable lifecycle. |

## The three shapes

An **Outcome** is what *should* be true after a run.

```python
from open_outcome import OutcomeDeclaration

outcome = OutcomeDeclaration(
    title="Vendor comparison: agent SDKs",
    as_of=date(2026, 5, 21),
    question="Which open-source agent SDK is the best foundation?",
    success_criteria=[
        "Each candidate's license is verified from primary sources",
        "A concrete recommendation is given with the main tradeoff named",
    ],
    archetype="vendor_comparison",
)
```

A **Verifier** consumes an outcome plus a report and returns a verdict.

```python
from open_outcome import HeuristicVerifier

verdict = HeuristicVerifier().verify(outcome, report)
```

A **Verdict** is the graded result: per-dimension scores, an overall, and the
evidence the verdict rests on.

```python
print(verdict.overall())              # e.g. 4.2
verdict.to_otel_attributes()          # gen_ai.outcome.verdict, gen_ai.outcome.confidence, ...
```

## Quickstart

```sh
# Spec + schemas
ls specification/ schema/

# Python reference SDK
cd sdk-python && uv pip install -e '.[dev]' && pytest

# TypeScript reference SDK
cd sdk-typescript && pnpm install && pnpm test
```

Each SDK's test suite is the executable proof of conformance — it builds
`OutcomeDeclaration` / `Report` / `Verdict` instances against the JSON
Schemas in [`schema/`](./schema/) and runs them through
`HeuristicVerifier`.

## Status

This is **v0.1.0** and the whole spec is **Experimental** per
[`MATURITY.md`](./MATURITY.md) — breaking changes are permitted in minor
releases. The shape of `Outcome`, `Verifier`, and `Verdict` is what we want
feedback on. File issues, open PRs, or start with an ADR.

## License

Apache-2.0 — see [`LICENSE`](./LICENSE).
