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

This repo is the **spec home**. The reference SDKs that implement the spec live in sibling repos so they can release independently:

| Path | What it is |
|---|---|
| [`specification/`](./specification/) | The normative spec. RFC 2119 keywords (MUST / SHOULD / MAY) inside blockquotes under numbered `Requirement` headings. |
| [`schema/`](./schema/) | JSON Schemas for `outcome`, `verdict`, and `evidence`. The schemas are the machine-checkable form of the spec. |
| [`outcomes/`](./outcomes/) | Dogfooded outcome+report pairs that exercise the spec against itself. |
| [`docs/`](./docs/) | Founding research, ADRs (architectural decision records), and research reviews. |
| [`GOVERNANCE.md`](./GOVERNANCE.md), [`MAINTAINERS.md`](./MAINTAINERS.md), [`MATURITY.md`](./MATURITY.md) | Governance, current maintainers, and the Experimental → Hardening → Stable lifecycle. |

### Reference SDKs (separate repos)

| Repo | Package | Install |
|---|---|---|
| [`opensubagents/outcomes-sdk-python`](https://github.com/opensubagents/outcomes-sdk-python) | `open-outcome` on [PyPI](https://pypi.org/project/open-outcome/) | `pip install open-outcome` or `uv add open-outcome` |
| [`opensubagents/outcomes-sdk-typescript`](https://github.com/opensubagents/outcomes-sdk-typescript) | `@opensubagents/outcomes-sdk` on [npm](https://www.npmjs.com/package/@opensubagents/outcomes-sdk) | `npm install @opensubagents/outcomes-sdk` |
| [`opensubagents/outcomes-mcp`](https://github.com/opensubagents/outcomes-mcp) | MCP server wrapping the verifier | (deployed on Cloudflare Workers) |

Both SDKs implement the **same `HeuristicVerifier` algorithm** with shared fixtures so they produce equal verdicts on the same input.

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
# Spec + schemas (this repo)
ls specification/ schema/
```

Then install one of the reference SDKs:

```sh
# Python
pip install open-outcome
# TypeScript
npm install @opensubagents/outcomes-sdk
```

Each SDK's test suite is the executable proof of conformance — both repos build `OutcomeDeclaration` / `Report` / `Verdict` instances against the JSON Schemas in [`schema/`](./schema/) of this repo and run them through `HeuristicVerifier`.

## Status

This is **v0.1.0** and the whole spec is **Experimental** per
[`MATURITY.md`](./MATURITY.md) — breaking changes are permitted in minor
releases. The shape of `Outcome`, `Verifier`, and `Verdict` is what we want
feedback on. File issues, open PRs, or start with an ADR.

## License

Apache-2.0 — see [`LICENSE`](./LICENSE).
