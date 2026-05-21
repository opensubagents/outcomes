# Governance

Open Outcome follows a lightweight version of the
[OpenFeature governance model](https://github.com/open-feature/community/blob/main/governance-charter.md).
This document defines who decides what, how decisions are made, and how the
project graduates over time.

## Bodies

### Technical Steering Committee (TSC)

The TSC is the technical decision-making body. It is responsible for:

- Approving normative changes to the [specification](./specification/) and the
  [schemas](./schema/).
- Approving graduation of spec sections through the maturity stages defined in
  [MATURITY.md](./MATURITY.md) (Experimental → Hardening → Stable).
- Setting the release cadence and approving releases.
- Resolving technical disputes between maintainers.

Current TSC members are listed in [MAINTAINERS.md](./MAINTAINERS.md).

### Maintainers

Maintainers have commit access to the repository. They review and merge pull
requests within their area of ownership (see `.github/CODEOWNERS`). At v0.1
the maintainer set is the same as the TSC.

### Contributors

Anyone who submits a pull request, opens an issue, or participates in
discussions is a contributor. Contributors do not need TSC approval to file
issues or open PRs — only to land them.

## Decision making

For normative changes (the specification, the JSON schemas, the public SDK
surface), the TSC uses **lazy consensus**:

1. A change is proposed via a pull request that includes both the change and a
   rationale (typically an ADR under `docs/adrs/`).
2. The PR is left open for at least **5 calendar days** to allow review.
3. If no TSC member objects, the change is accepted. If any TSC member
   objects, the PR is held until the objection is resolved or withdrawn.
4. Disputes that cannot be resolved by discussion are decided by a
   simple-majority vote of the TSC.

For non-normative changes (CI, docs typos, internal refactors that do not
change the public SDK surface), a single maintainer approval is sufficient.

## Adding and removing TSC members

A new TSC member is added by simple-majority vote of the current TSC. There
is no fixed seat count.

A TSC member may step down at any time by opening a PR removing themselves
from `MAINTAINERS.md`. A TSC member may be removed for inactivity (no PR
activity or vote for 90 consecutive days) by simple-majority vote of the
remaining TSC.

## Code of Conduct

All participation in this project is governed by the
[Code of Conduct](./.github/CODE_OF_CONDUCT.md), adapted from the Contributor
Covenant 2.1. Reports of violations are handled by the TSC.

## Changes to this document

Changes to `GOVERNANCE.md` itself require TSC supermajority (two-thirds) and
a 14-day notice period on the PR.
