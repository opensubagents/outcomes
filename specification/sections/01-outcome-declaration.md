---
title: Outcome Declaration
description: How an outcome is declared before an agent runs.
toc_max_heading_level: 4
---

# 1. Outcome Declaration

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

An *outcome declaration* describes what should be true after an agent runs.
It is the input to a [verifier](./02-verifier.md), is produced *before* the
agent runs, and is intended to be machine-checkable rather than
human-prose.

The canonical machine representation is
[`schema/outcome.schema.json`](../../schema/outcome.schema.json).

## 1.1. Required fields

##### Requirement 1.1.1

> An outcome declaration **MUST** include a non-empty `title` of type
> [`string`](../types.md#string).

##### Requirement 1.1.2

> An outcome declaration **MUST** include an `as_of` field of type
> [`date`](../types.md#date) naming the date the outcome was declared.

##### Requirement 1.1.3

> An outcome declaration **MUST** include a non-empty `question` of type
> [`string`](../types.md#string) stating the question the agent will answer.

##### Requirement 1.1.4

> An outcome declaration **MUST** include a `success_criteria` field
> containing at least one non-empty [`string`](../types.md#string). Each
> criterion is a free-form English clause that a verifier checks the
> report against.

## 1.2. Optional fields

##### Requirement 1.2.1

> An outcome declaration **SHOULD** include an `archetype` field of type
> [`string`](../types.md#string), drawn from a vocabulary chosen by the
> implementation. The reference vocabulary at v0.1 is
> `{"vendor_comparison", "deep_dive", "capability_audit"}`. Implementations
> **MAY** define additional archetype values.

##### Requirement 1.2.2

> An outcome declaration **MAY** include an `archetype_fields` object
> carrying archetype-specific keys (for example, `candidates` and
> `dimensions` for a `vendor_comparison`). Verifiers that do not understand
> an archetype **MUST** fall back to checking only the
> archetype-independent requirements above.

## 1.3. Immutability

##### Requirement 1.3.1

> Once an outcome declaration has been passed to a verifier, the declaration
> **MUST NOT** be mutated for the duration of the verification call. The
> reference SDKs achieve this with frozen / immutable model types.

## 1.4. Non-requirements

This section deliberately does **not** mandate a specific archetype
vocabulary, a specific schema for `archetype_fields`, or a fixed list of
top-level keys. The minimum bar is `title` + `as_of` + `question` +
`success_criteria`; everything else is open for archetype designers to
define.
