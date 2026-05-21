---
title: Appendix A — Reference rubric
description: The five-dimension reference rubric used by the SDKs.
---

# Appendix A — Reference rubric

> This appendix is **informative**. The spec does not mandate this
> particular rubric; it mandates only the *shape* of a verdict (see
> [section 3](./sections/03-verdict.md)).

The reference SDKs ship a heuristic verifier that scores reports along
five dimensions. These dimensions originated in the
[`opensubagents/research-engineering`](https://github.com/opensubagents/research-engineering)
plugin and are reused here so the
[`examples/research-engineering/`](../examples/research-engineering/)
end-to-end can assert byte-level parity with that plugin's grader.

## The five dimensions

### `confidence_calibration`

The fraction of [claims](./glossary.md#claim) whose
[confidence](./glossary.md#confidence) label correctly matches the
evidence cited for them, per the calibration rule in
[section 5](./sections/05-confidence.md). Penalize both over- and under-
calibration.

### `citation_quality`

The fraction of [citations](./glossary.md#citation) that are of
`kind = primary`. Implementations may also check that titles match what
the URL returns and that quotes match the source body; the heuristic
verifier at v0.1 does neither.

### `coverage`

The fraction of `success_criteria` and archetype-specific axes (e.g. a
vendor comparison's `dimensions` array) that are addressed by at least one
claim. Implementations may use substring matching, embedding similarity,
or LLM-judged matching; the heuristic verifier at v0.1 uses substring
matching.

### `decision_usefulness`

A 1–5 score reflecting whether a reader could make a decision from the
report: tradeoffs explicit, recommendations concrete, open questions named,
methodology notes present. The heuristic verifier at v0.1 counts four
binary signals (open_questions present, any claim has caveats, methodology
notes present, summary contains decision verbs).

### `clarity`

A 1–5 score on whether the report's summary is self-contained and the
right length. The heuristic verifier at v0.1 scores summaries of 2–4
sentences as `5`, summaries of 1 or 5 sentences as `3`, anything else as
`2`.

## Why these five

The five-dimension rubric is the empirical contract that drove the
existence of this spec — research-engineering reports were being graded
along these dimensions before Open Outcome existed, and the spec was
deliberately built to *standardize the shape that allows this rubric*, not
to impose this rubric on every implementation. Implementations that want
different dimensions are free to define them, provided the resulting
verdict still satisfies [section 3](./sections/03-verdict.md).
