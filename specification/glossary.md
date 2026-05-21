---
title: Glossary
description: Defined terms used across the Open Outcome specification.
---

# Glossary

This document defines terms used across the Open Outcome specification.
Terms are listed alphabetically. Where a term has a precise machine
representation, the relevant schema is linked from the entry.

## Archetype

A discriminator on an [outcome declaration](#outcome-declaration) that names
the *kind* of outcome being declared, so verifiers can apply
archetype-specific rules. The three archetypes seen in the reference
example are `vendor_comparison`, `deep_dive`, and `capability_audit`.
Implementations MAY define additional archetypes.

## Calibration

The property that a self-reported [confidence](#confidence) label on a
[claim](#claim) matches the weight of the evidence cited for that claim.
Section [5](./sections/05-confidence.md) defines the calibration rule
normatively.

## Citation

A reference to a source that supports a [claim](#claim). A citation includes
a URI, a human-readable title, the date the source was accessed, a
[source kind](#source-kind), and an optional verbatim quote. See
[`schema/evidence.schema.json`](../schema/evidence.schema.json).

## Claim

A single assertion produced by an agent run, carrying its own
[confidence](#confidence) label and zero or more [citations](#citation).
A claim is the smallest unit of evidence a [verifier](#verifier) operates on.

## Confidence

A calibrated label on a [claim](#claim), drawn from the closed set
`{high, medium, low}`. The calibration rule that maps confidence levels to
evidence weight is in section [5](./sections/05-confidence.md).

## Conformance

The property that an implementation satisfies every normative **MUST**,
**MUST NOT**, **REQUIRED**, **SHALL**, and **SHALL NOT** in this
specification. See [appendix C](./appendix-c-conformance.md) for how to
claim conformance.

## Dimension

A named axis along which a [verdict](#verdict) scores an agent's output.
Each dimension carries a name, a numeric score, and a one-line
justification. The reference rubric in
[appendix A](./appendix-a-rubric.md) lists five dimensions; this spec does
not mandate a particular dimension set.

## Evidence

The cited material that supports a [verdict](#verdict). At minimum, evidence
is the set of all [citations](#citation) across the [claims](#claim) that
were produced for the [outcome](#outcome-declaration).

## Outcome declaration

A typed description of what should be true after an agent run, defined
before the run starts. An outcome declaration is the input to a
[verifier](#verifier); it is also called an *outcome* for short. See
[section 1](./sections/01-outcome-declaration.md) and
[`schema/outcome.schema.json`](../schema/outcome.schema.json).

## Report

The structured output an agent produces in response to an outcome
declaration. The spec does not constrain the report's shape beyond what a
verifier needs to read — implementations typically include a summary, a
list of [claims](#claim), and methodology notes.

## Source kind

A coarse classification of a [citation](#citation), drawn from the closed
set `{primary, secondary, community}`. Primary sources are vendor
documentation, source code, RFCs, or other authoritative artifacts.
Secondary sources are reputable third-party explanations (e.g. engineering
blogs). Community sources are forums, social media, or other crowd-sourced
content.

## Success criterion

A free-form English clause that a [verifier](#verifier) checks the report
against. Every [outcome declaration](#outcome-declaration) **MUST** contain
at least one success criterion.

## Verdict

The graded result returned by a [verifier](#verifier): a list of
[dimension](#dimension) scores, an overall score, the
[evidence](#evidence) the verdict rests on, and the spec version under
which the verdict was produced. See
[section 3](./sections/03-verdict.md) and
[`schema/verdict.schema.json`](../schema/verdict.schema.json).

## Verifier

A function — pure, in spec terms — that consumes an
[outcome declaration](#outcome-declaration) and a [report](#report) and
returns a [verdict](#verdict). See
[section 2](./sections/02-verifier.md).
