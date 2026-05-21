# ADR-0002 — SDK generation strategy

- **Status:** Pending (blocked on task #2 — Stainless `acquisition_impact` brief)
- **Date opened:** 2026-05-21
- **Deciders:** TSC (single seat at v0.1, see [MAINTAINERS.md](../../MAINTAINERS.md))
- **Supersedes:** —

## Context

On 2026-05-21, **Stainless** (founded 2022; the SDK generator behind
Anthropic's official SDKs; founder/CEO Alex Rattray) was acquired by
Anthropic. See the addendum in
[`docs/founding-research.md`](../founding-research.md#addendum--2026-05-21-stainless-acquisition).

The acquisition materially changes the calculation around how Open Outcome
ships its reference SDKs. Before the acquisition, Stainless was a neutral
third-party generator; after it, Stainless is Anthropic-internal and will
optimize for Claude-native ergonomics — which aligns with this project's
existing distribution (the sibling `opensubagents/research-engineering`
plugin is a Claude Code plugin).

v0.1 of Open Outcome ships **hand-written** reference SDKs for Python and
TypeScript. This ADR records the open question of whether to continue with
hand-written SDKs, switch to Stainless-emitted SDKs, or run a hybrid — and
parks the decision until task #2 resolves it.

## Options under consideration

### Option A — Stay hand-written

Continue maintaining `sdk-python/` and `sdk-typescript/` by hand. Add Go /
Rust / Java SDKs later by writing them.

- **Pro:** Maximum control over surface ergonomics; no external dependency on
  Stainless's roadmap or pricing; SDKs ship in the same repo as the spec.
- **Pro:** Reference implementations stay simple enough to read top-to-bottom
  while the spec is still Experimental.
- **Con:** N SDKs means N codebases to keep in lockstep with each spec change.
- **Con:** Will not scale to four+ languages without a generator.

### Option B — Author a Stainless-compatible OpenAPI spec, emit SDKs natively

Author a single OpenAPI spec under (e.g.) `schema/openapi.yaml` and let
Stainless emit TS / Python / Go / Java / Rust SDKs. Delete the hand-written
SDKs once parity is reached.

- **Pro:** One spec → many SDKs in lockstep, regenerated on every spec change.
- **Pro:** Now that Stainless is Anthropic-internal, the emitted SDKs will
  be Claude-native by default.
- **Con:** Bakes a dependency on a single (now-corporate) generator into a
  spec project that is meant to be vendor-neutral.
- **Con:** OpenAPI does not natively express some of the things this spec
  needs (e.g. discriminator unions for outcome archetypes, JSON Schema
  `$defs` cross-references) — some generator-specific extensions may be
  required.

### Option C — Hybrid: hand-written reference SDKs + Stainless-emitted distribution SDKs

Keep `sdk-python/` and `sdk-typescript/` as small, hand-written **reference**
implementations whose only purpose is to validate the spec
(unit-test-friendly, easy to read, no codegen). Author the OpenAPI spec
separately under `schema/openapi.yaml` and ship Stainless-emitted SDKs under
`sdk-python-generated/`, `sdk-go/`, etc. for distribution.

- **Pro:** Reference SDKs stay simple and human-auditable.
- **Pro:** Distribution gets the broad language support of a generator.
- **Pro:** Decouples "is the spec right?" from "are the SDKs ergonomic?".
- **Con:** Two sets of SDKs to maintain.

## Decision

**Pending.** This ADR will be resolved after task #2 completes:

1. Re-run the `opensubagents/research-engineering` plugin with
   `archetype = acquisition_impact` against the Stainless acquisition.
2. The resulting brief should specifically evaluate option B vs. option C
   on dimensions including: spec-feature expressivity in OpenAPI, generator
   licensing and pricing, language coverage, maintenance cost, and the
   neutrality optics of depending on a now-Anthropic generator.
3. Land the verdict here, update Status to **Accepted**, and either keep,
   replace, or augment the v0.1 hand-written SDKs accordingly.

This ADR does **not** block v0.1: the v0.1 SDKs are hand-written reference
implementations regardless of which option resolves. The question is whether
future versions add or replace them.

## Consequences (once resolved)

To be written when the ADR moves to **Accepted**.
