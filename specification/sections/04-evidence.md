---
title: Evidence
description: Citations and claims — the material a verdict rests on.
toc_max_heading_level: 4
---

# 4. Evidence

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

Evidence is the cited material a [verdict](./03-verdict.md) rests on. This
section defines the shape of a [citation](../glossary.md#citation) and a
[claim](../glossary.md#claim). The canonical machine representation lives
in [`schema/evidence.schema.json`](../../schema/evidence.schema.json).

## 4.1. Citations

##### Requirement 4.1.1

> A citation **MUST** include a `url` field of type
> [`URI`](../types.md#uri) that resolves over HTTP or HTTPS. URLs **MUST
> NOT** be `file://` or other local schemes; verifiers cannot validate
> local references.

##### Requirement 4.1.2

> A citation **MUST** include a non-empty
> [`string`](../types.md#string) `title` field.

##### Requirement 4.1.3

> A citation **MUST** include an `accessed` field of type
> [`date`](../types.md#date) naming the date the source was last accessed.

##### Requirement 4.1.4

> A citation **MUST** include a `kind` field of type
> [`SourceKind`](../types.md#sourcekind) classifying the source as
> `primary`, `secondary`, or `community`. See the
> [SourceKind glossary entry](../glossary.md#source-kind) for the meaning
> of each value.

##### Requirement 4.1.5

> A citation **MAY** include a `quote` field of type
> [`string`](../types.md#string) carrying a verbatim excerpt from the
> source that anchors the citation to the claim. Verifiers **SHOULD**
> prefer citations that include a quote when ranking citation quality.

## 4.2. Claims

##### Requirement 4.2.1

> A claim **MUST** include a non-empty
> [`string`](../types.md#string) `statement` field.

##### Requirement 4.2.2

> A claim **MUST** include a `confidence` field of type
> [`Confidence`](../types.md#confidence). The calibration rule that maps
> confidence levels to evidence weight is defined in
> [section 5](./05-confidence.md).

##### Requirement 4.2.3

> A claim **MUST** include a `citations` array — possibly empty — of
> citation entries. The minimum citation count per confidence level is
> defined in [section 5](./05-confidence.md).

##### Requirement 4.2.4

> A claim **MAY** include a `caveats` field of type
> [`string`](../types.md#string) noting conditions that would change the
> claim.

## 4.3. Deduplication

##### Requirement 4.3.1

> When a verifier emits an `evidence` array on a verdict, it **MUST**
> deduplicate citations by URI — the same URI **MUST NOT** appear twice in
> a single verdict's evidence array, even if it was cited by multiple
> claims.

## 4.4. Reachability

##### Requirement 4.4.1

> A citation `url` **MUST** be syntactically a valid HTTP or HTTPS URL.
> Verifiers **MAY** check that the URL is reachable but are **NOT**
> required to — network access is out of scope for the heuristic verifier
> per [requirement 2.2.1](./02-verifier.md#requirement-221).
