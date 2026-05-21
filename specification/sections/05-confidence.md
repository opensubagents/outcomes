---
title: Confidence Calibration
description: How self-reported confidence labels MUST relate to evidence weight.
toc_max_heading_level: 4
---

# 5. Confidence Calibration

[![status: experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)](../../MATURITY.md)

## Overview

A [claim](../glossary.md#claim) carries a self-reported confidence label
drawn from `{high, medium, low}`. This section defines the *calibration
rule*: the relationship a verifier **MUST** check between a claim's
confidence label and the evidence cited for it.

The rule is symmetric. Verifiers **MUST** flag both *overconfident* claims
(weak sourcing labeled `high`) and *underconfident* claims (strong sourcing
labeled `low`).

## 5.1. Calibration thresholds

##### Requirement 5.1.1

> A claim labeled `high` confidence **MUST** be supported by at least one
> of:
>
> - Two or more independent citations of `kind = primary` (see
>   [section 4](./04-evidence.md)), or
> - One citation of `kind = primary` that is vendor-authoritative for the
>   subject of the claim (e.g. a vendor's own official documentation for a
>   claim about that vendor's product).

##### Requirement 5.1.2

> A claim labeled `medium` confidence **MUST** be supported by at least one
> of:
>
> - One citation of `kind = primary`, or
> - Two or more citations of `kind in {primary, secondary}`.

##### Requirement 5.1.3

> A claim labeled `low` confidence **MAY** be supported by a single
> citation of any kind, or by no citations at all when the claim is an
> inference explicitly marked as such in its `statement` or `caveats`.

## 5.2. Calibration check (verifier side)

##### Requirement 5.2.1

> A verifier **MUST** compute a calibration verdict for each claim in the
> report. The verdict **MUST** detect both *over-* and *under-*calibration:
>
> - A claim labeled `high` whose citations do not meet
>   [requirement 5.1.1](#requirement-511) is **over-calibrated**.
> - A claim labeled `medium` whose citations do not meet
>   [requirement 5.1.2](#requirement-512) is **over-calibrated**.
> - A claim labeled `low` that satisfies the threshold for `high` is
>   **under-calibrated**.

##### Requirement 5.2.2

> A verifier **SHOULD** include a dimension named `confidence_calibration`
> in its verdict whose score reflects the fraction of claims that are
> calibrated correctly. The reference rubric in
> [appendix A](../appendix-a-rubric.md) defines such a dimension.

## 5.3. Rationale

The calibration rule is the spec's main contribution over and above
"the agent cited some URLs." A claim that is cited but mislabeled (e.g.
`high` confidence with one secondary citation) leaks unjustified certainty
downstream; a claim that is well-cited but labeled `low` wastes evidence
work. Both directions matter and verifiers should not let either pass
silently.
