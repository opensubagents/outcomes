---
title: Observability
description: How verdicts SHOULD be emitted to telemetry backends.
toc_max_heading_level: 4
---

# 6. Observability

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

Verdicts are most useful when they show up in the same observability backend
that already collects agent traces. This section defines how a verdict
**SHOULD** be projected onto OpenTelemetry span attributes so that any
OTel-compatible backend can index and alert on them.

The attribute table below is a proposed extension to the
[OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/).
The extension is not yet upstreamed; see
[appendix B](../appendix-b-otel-extension.md) for the rationale and the
upstream plan.

## 6.1. Span attributes

##### Requirement 6.1.1

> When a verifier emits a verdict to an OpenTelemetry span, it **SHOULD**
> set the following attributes on the span:
>
> | Attribute | Type | Source |
> |---|---|---|
> | `gen_ai.outcome.spec_version` | `string` | `verdict.spec_version` |
> | `gen_ai.outcome.overall` | `double` | `verdict.overall` |
> | `gen_ai.outcome.dimension_count` | `int` | `len(verdict.dimensions)` |
> | `gen_ai.outcome.evidence_count` | `int` | `len(verdict.evidence)` |
> | `gen_ai.outcome.verifier_id` | `string` | `verdict.verifier_id` (if present) |

##### Requirement 6.1.2

> For each dimension in the verdict, the verifier **MAY** set the per-
> dimension score as an attribute of the form
> `gen_ai.outcome.dimension.<name>.score` with type `int`. Dimension names
> **MUST** be normalized to lower-snake-case before being inlined into the
> attribute key.

##### Requirement 6.1.3

> Verifiers **MUST NOT** put the verdict's full `evidence` array onto the
> span as a single string attribute. Evidence belongs on span *events* or
> in a separate log record, not on the span itself, to avoid blowing up
> per-span size limits in common backends.

## 6.2. Span name

##### Requirement 6.2.1

> A span that carries a verdict **SHOULD** be named `verify_outcome` to
> distinguish it from the surrounding agent operation spans
> (`invoke_agent`, `execute_tool`, etc., defined by the upstream GenAI
> conventions).

## 6.3. Sampling

##### Requirement 6.3.1

> Verifier implementations **MUST NOT** introduce custom sampling logic
> that drops verdict spans based on their score. The sampling decision is
> the responsibility of the surrounding tracer; dropping low-score
> verdicts inside the verifier would hide exactly the data operators most
> want to see.
