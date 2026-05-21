# ADR-0001 — Name and scope of the project

- **Status:** Accepted
- **Date:** 2026-05-21
- **Deciders:** Founding maintainer (single-seat TSC at v0.1, see [MAINTAINERS.md](../../MAINTAINERS.md))
- **Supersedes:** —

## Context

Four candidate scopes were on the table for the next repository in the
`opensubagents` organization:

1. **Open Coworker SDK** — a vendor-neutral plugin file format and capability
   declaration for "coworker" agents.
2. **Open Outcome SDK** — a vendor-neutral spec for declaring, verifying, and
   grading agent outcomes.
3. **cowork-marketplace** — a registry for distributing coworker plugins.
4. **managed-agents** — a hosted service for running managed agents.

The founding research brief filed on 2026-05-21 (reproduced verbatim in
[`docs/founding-research.md`](../founding-research.md)) returned a clear
verdict: options 1, 3, and 4 are blocked or premature, and option 2 is the
one unclaimed gap in the agent ecosystem stack.

The specific findings the decision rests on:

- **MCP** owns the tool / capability layer.
- **OpenTelemetry GenAI semconv** owns the telemetry layer (and explicitly
  does not define `gen_ai.outcome.*` attributes — see claim 5 of the
  founding research).
- **Anthropic's knowledge-work-plugins** owns the plugin file format.
- **Stainless** (acquired by Anthropic on the same day) owns SDK generation.
- The **outcome layer** — what *should* be true after an agent runs, how to
  check it, and how to report a verdict with cited evidence — has no public
  standard.

The empirical basis for what an outcome shape looks like already exists in
the sibling repo `opensubagents/research-engineering`: pydantic models for
`Brief` / `Claim` / `Citation` / `GeneratedReport`, a 5-dimension rubric, and
a deterministic `HeuristicGrader`. v0.1 of this project generalizes those
into a vendor-neutral spec.

## Decision

1. **Name.** The project is named **Open Outcome**.
   - Python package: `open-outcome` (importable as `open_outcome`).
   - TypeScript package: `@opensubagents/open-outcome`.
   - Repository: `opensubagents/outcomes`.

2. **Scope.** v0.1 standardizes the **declare → verify → grade** triple:
   - The **outcome declaration**: a typed description of what should be true
     after an agent run.
   - The **verifier**: an interface that consumes an outcome plus a report
     and returns a verdict.
   - The **verdict**: a graded result with per-dimension scores, an overall,
     cited evidence, and a calibrated confidence label.

   Out of scope at v0.1: marketplaces, hosted services, cross-vendor
   verification clients, and any layer already owned by MCP, OTel, or
   knowledge-work-plugins.

3. **Governance.** Mirror OpenFeature:
   - RFC 2119 keywords (MUST / SHOULD / MAY) inside blockquotes under
     numbered `Requirement` headings.
   - Single-bar conformance: an implementation is compliant iff it satisfies
     every MUST / MUST NOT / REQUIRED.
   - Maturity stages: Experimental → Hardening → Stable, defined in
     [MATURITY.md](../../MATURITY.md).
   - Technical Steering Committee with lazy-consensus decision making, per
     [GOVERNANCE.md](../../GOVERNANCE.md).

4. **License.** Apache-2.0.

5. **Reference SDKs.** Two hand-written reference SDKs at v0.1: Python and
   TypeScript. Both implement the same `HeuristicVerifier` algorithm so the
   `examples/research-engineering/` end-to-end can assert byte-level parity
   between the two implementations against the same fixtures.

## Consequences

- **Positive.** Open Outcome sits in a layer with no existing standard and
  no incumbent vendor; the founding rationale (founding-research.md) is
  durable against the Stainless acquisition (see addendum) because that
  acquisition lands in a different layer.
- **Positive.** Reusing the OpenFeature governance template lets us inherit
  a known-working spec process without inventing one.
- **Negative.** Two hand-maintained SDKs is more work than one — see
  ADR-0002 for the open question of whether to keep maintaining them by hand.
- **Negative.** "Outcome" overlaps in plain-English meaning with terms like
  "result", "evaluation", "eval". The spec glossary fixes precise meanings
  for the project's vocabulary in [`specification/glossary.md`](../../specification/glossary.md).

## Notes

- ADR-0002 captures the SDK-generation question raised by the Stainless
  acquisition on the same day.
- Future ADRs should be filed as `ADR-NNNN-short-name.md` in this directory.
