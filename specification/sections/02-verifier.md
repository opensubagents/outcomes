---
title: Verifier
description: The interface a verifier MUST implement.
toc_max_heading_level: 4
---

# 2. Verifier

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

A *verifier* is a function that consumes an
[outcome declaration](./01-outcome-declaration.md) and a *report* (the
agent's structured output) and returns a [verdict](./03-verdict.md). The
spec defines the interface a verifier must implement; it does not mandate
how the verifier computes the verdict (deterministic rules, LLM judge,
human review, or a hybrid are all allowed).

## 2.1. Interface

##### Requirement 2.1.1

> A verifier **MUST** expose a `verify` operation that accepts two inputs:
> an outcome declaration (see [section 1](./01-outcome-declaration.md)) and
> a report. The operation **MUST** return a verdict (see
> [section 3](./03-verdict.md)).

##### Requirement 2.1.2

> The `verify` operation **MUST** be pure with respect to its inputs: given
> the same outcome and report, repeated calls **MUST** return verdicts that
> compare equal under the equality rule in
> [requirement 3.4.1](./03-verdict.md#requirement-341).
>
> Note: This requirement excludes non-determinism within a single
> verification run. Verifiers backed by stochastic LLM judges satisfy this
> requirement by seeding their judge or by caching the judge's output for a
> given input.

##### Requirement 2.1.3

> A verifier **MUST NOT** mutate the outcome declaration it receives.

## 2.2. Heuristic verifier

##### Requirement 2.2.1

> Implementations **SHOULD** provide a *heuristic verifier* that runs
> without network access and without an LLM. The heuristic verifier serves
> as a cheap pre-check, a CI gate, and the reference for what the spec's
> requirements look like in code.

##### Requirement 2.2.2

> The heuristic verifier provided by a reference SDK **MUST** be
> deterministic: given the same outcome and report bytes, it **MUST**
> return bit-identical verdicts on repeated runs and across platforms.

## 2.3. Error handling

##### Requirement 2.3.1

> If the outcome declaration fails to validate against
> [`schema/outcome.schema.json`](../../schema/outcome.schema.json), the
> verifier **MUST** raise a validation error before producing a verdict.
> Verifiers **MUST NOT** silently degrade to a partial verdict when the
> outcome is malformed.

##### Requirement 2.3.2

> If the report is structurally invalid (for example, missing required
> fields the verifier needs to score), the verifier **MUST** raise a
> validation error rather than emitting low scores.
>
> Note: A *structurally valid* report that scores low on the rubric is a
> normal verdict, not an error. The distinction is between "the input is
> well-formed" and "the input scored well".

## 2.4. Composition

Verifiers compose. Implementations **MAY** chain a heuristic verifier and
an LLM-judge verifier and merge their verdicts, provided the merged result
still satisfies the verdict requirements in [section 3](./03-verdict.md).
The reference SDKs do not include a default chain at v0.1.
