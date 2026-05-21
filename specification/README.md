---
title: Open Outcome Specification
description: Vendor-neutral spec for declaring, verifying, and grading AI agent outcomes.
version: 0.1.0
status: experimental
---

# Open Outcome Specification

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../MATURITY.md)
[![version: 0.1.0](https://img.shields.io/static/v1?label=Version&message=0.1.0&color=blue)](./README.md)

## Notational conventions

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**,
**SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in
this document are to be interpreted as described in
[BCP 14](https://datatracker.ietf.org/doc/html/bcp14)
([RFC 2119](https://datatracker.ietf.org/doc/html/rfc2119),
[RFC 8174](https://datatracker.ietf.org/doc/html/rfc8174)) when, and only
when, they appear in all capitals inside a blockquote, as the body of a
labeled `Requirement` heading.

An implementation is **not compliant** if it fails to satisfy one or more of
the **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, or **SHALL NOT**
requirements defined in the normative sections of this specification.
Conformance to **SHOULD** is recommended but not required, and **MAY**
denotes optional behavior.

## Status

Every section of v0.1.0 is **Experimental**: the surface may change without
deprecation in any release. See [MATURITY.md](../MATURITY.md) for the
breaking-change policy at each maturity stage.

## Table of contents

### Normative sections

| Section | Title | Status |
|---|---|---|
| [1](./sections/01-outcome-declaration.md) | Outcome declaration | experimental |
| [2](./sections/02-verifier.md) | Verifier | experimental |
| [3](./sections/03-verdict.md) | Verdict | experimental |
| [4](./sections/04-evidence.md) | Evidence | experimental |
| [5](./sections/05-confidence.md) | Confidence calibration | experimental |
| [6](./sections/06-observability.md) | Observability | experimental |

### Supporting documents

| Document | Purpose |
|---|---|
| [Glossary](./glossary.md) | Defined terms used across the spec |
| [Types](./types.md) | Primitive value types (URI, ISO date, enums) |

### Appendices (informative)

| Appendix | Title |
|---|---|
| [A](./appendix-a-rubric.md) | Reference rubric — the five dimensions |
| [B](./appendix-b-otel-extension.md) | Proposed OpenTelemetry `gen_ai.outcome.*` extension |
| [C](./appendix-c-conformance.md) | Conformance — how to claim it |

## Versioning

This document is at **v0.1.0**. The version applies to the normative content
of the sections only; appendices are informative and may change without a
version bump. Versioning rules are defined in [MATURITY.md](../MATURITY.md).

The reference SDKs MUST emit the spec version as `spec_version` on every
`Verdict` they produce (see [section 3](./sections/03-verdict.md)).
