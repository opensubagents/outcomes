---
title: Verdict
description: The graded result a verifier returns.
toc_max_heading_level: 4
---

# 3. Verdict

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

A *verdict* is the structured graded result a [verifier](./02-verifier.md)
returns. It is the spec's main output type — every artifact the spec
exists to produce ends up as a verdict.

The canonical machine representation is
[`schema/verdict.schema.json`](../../schema/verdict.schema.json).

## 3.1. Required fields

##### Requirement 3.1.1

> A verdict **MUST** include a `dimensions` array containing one or more
> dimension entries. Each entry **MUST** include a non-empty
> [`string`](../types.md#string) `name`, a [`Score`](../types.md#score),
> and a non-empty `justification` string.

##### Requirement 3.1.2

> A verdict **MUST** include an `overall` field of type `number`,
> representing the arithmetic mean of the dimension scores rounded to one
> decimal place. The `overall` field is **REQUIRED** even when only one
> dimension is present.

##### Requirement 3.1.3

> A verdict **MUST** include a `spec_version` field of type
> [`SpecVersion`](../types.md#specversion) naming the version of this
> specification the verdict was produced against.

##### Requirement 3.1.4

> A verdict **MUST** include an `evidence` array of citation entries (see
> [section 4](./04-evidence.md)) — possibly empty — listing the citations
> the verdict considered.

## 3.2. Optional fields

##### Requirement 3.2.1

> A verdict **MAY** include a `notes` field of type
> [`string`](../types.md#string) carrying free-form prose from the
> verifier (e.g. "produced by HeuristicVerifier", or LLM judge prompt
> hash).

##### Requirement 3.2.2

> A verdict **MAY** include a `verifier_id` field of type
> [`string`](../types.md#string) identifying the verifier that produced
> the verdict.

## 3.3. Dimension constraints

##### Requirement 3.3.1

> Within a single verdict, dimension `name` values **MUST** be unique. A
> verifier **MUST NOT** emit two dimensions with the same name in one
> verdict.

##### Requirement 3.3.2

> Dimension `score` values **MUST** be integers in the closed range
> `[1, 5]`. Implementations that wish to use a different scale **MUST NOT**
> claim conformance to this version of the spec.

## 3.4. Equality

##### Requirement 3.4.1

> Two verdicts are *equal* iff their `dimensions` arrays are equal as sets
> (compared by name + score + justification), their `overall` values are
> equal to one decimal place, their `spec_version` values are equal, and
> their `evidence` arrays are equal as sets (compared by citation URI).
> Optional fields are not considered for equality.

## 3.5. Aggregation

This spec does not mandate a particular aggregation rule for `overall`
beyond the arithmetic mean in requirement 3.1.2. Verifiers that wish to
use weighted aggregation **MAY** do so, but **MUST** record the weights in
the `notes` field.
