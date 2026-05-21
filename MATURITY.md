# Maturity model

Each section of the [specification](./specification/) carries a status badge
that signals how stable it is. The model is adapted from the
[OpenFeature maturity model](https://openfeature.dev/specification/) and uses
three stages: **Experimental**, **Hardening**, and **Stable**.

## Stages

### Experimental ![experimental](https://img.shields.io/static/v1?label=Status&message=experimental&color=orange)

We are testing this surface and it may change at any time.

- Breaking changes are **permitted in any release**, including minor and
  patch releases.
- Implementations are encouraged but should expect to update against
  spec changes.
- Goal: gather enough adoption signal to either graduate or remove.

### Hardening ![hardening](https://img.shields.io/static/v1?label=Status&message=hardening&color=yellow)

We believe this surface is ready for production use and want feedback.

- Breaking changes are **permitted only in minor releases** and require TSC
  consensus on the PR (see [GOVERNANCE.md](./GOVERNANCE.md#decision-making)).
- Implementations should be safe to ship; users may need to adjust on
  minor-version bumps.
- Goal: collect production feedback for at least one minor release before
  graduating.

### Stable ![stable](https://img.shields.io/static/v1?label=Status&message=stable&color=green)

This surface is battle-tested and stable.

- Breaking changes are **permitted only in major releases**.
- Deprecation policy: any removal must be announced one major release in
  advance and must be backed by a migration path.
- Goal: long-term stability for downstream tooling.

## Current status

At **v0.1.0**, every section of the specification is **Experimental**. The
v0.1 release exists to gather feedback on the overall shape (declare → verify
→ grade) before any subsection is promoted.

A graduation proposal is filed as an ADR under
[`docs/adrs/`](./docs/adrs/) and merged per the lazy-consensus rules in
[GOVERNANCE.md](./GOVERNANCE.md#decision-making).

## Versioning

Open Outcome follows [Semantic Versioning](https://semver.org/) with the
modifications above:

- **MAJOR** version: breaking changes to Stable sections.
- **MINOR** version: breaking changes to Experimental or Hardening sections,
  additive changes anywhere.
- **PATCH** version: editorial fixes, clarifications that do not change
  conformance.

The spec version is recorded in [`specification/README.md`](./specification/README.md)
and emitted by the reference SDKs as the `spec_version` field on every
`Verdict`.
