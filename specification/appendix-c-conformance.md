---
title: Appendix C — Conformance
description: How an implementation claims conformance to Open Outcome.
---

# Appendix C — Conformance

> This appendix is **informative** in tone but the requirements it
> aggregates are normative — they are reproduced from the numbered
> requirements in [sections 1–6](./sections/).

## How to claim conformance

An implementation may claim conformance to Open Outcome **v0.1.0** if and
only if all of the following are true:

1. The implementation accepts outcome declarations whose JSON form
   validates against
   [`schema/outcome.schema.json`](../schema/outcome.schema.json), and
   rejects outcomes whose JSON form does not.
2. The implementation produces verdicts whose JSON form validates against
   [`schema/verdict.schema.json`](../schema/verdict.schema.json).
3. The implementation satisfies every `MUST` / `MUST NOT` / `REQUIRED`
   requirement in [sections 1–6](./sections/).
4. The implementation emits the spec version (`0.1.0`) as the
   `spec_version` field on every verdict it produces.

There are no graduated conformance levels at v0.1 — an implementation is
either conformant or it is not. This mirrors the OpenFeature conformance
model.

## Self-certification

There is no central registry of conforming implementations at v0.1.
Implementations self-certify by:

1. Linking to this appendix from their README and stating which spec
   version they target.
2. Running the conformance test corpus published in
   [`sdk-python/tests/test_conformance.py`](../sdk-python/tests/test_conformance.py)
   and [`sdk-typescript/test/conformance.test.ts`](../sdk-typescript/test/conformance.test.ts)
   against their implementation — or reproducing those tests in their own
   language. Both reference SDKs share their fixtures with the conformance
   tests.

## Spec version pinning

Every verdict carries the `spec_version` field (see
[requirement 3.1.3](./sections/03-verdict.md#requirement-313)). Downstream
tooling SHOULD pin to a specific spec version rather than blindly
accepting any version, because the v0.1 spec is **Experimental** (see
[MATURITY.md](../MATURITY.md)) and breaking changes are permitted in any
release until graduation.

## Reporting non-conformance

If you find a case where an implementation does not satisfy a `MUST`
requirement, please file an issue against that implementation's repository.
If you find a case where the reference SDKs in this repository disagree
with the spec, file the issue here — the spec wins by default.
