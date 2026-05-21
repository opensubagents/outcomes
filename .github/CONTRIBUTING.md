# Contributing to Open Outcome

Thank you for your interest in contributing. This document is a quick guide
for working with this repository. Governance — who decides what, and how —
lives in [GOVERNANCE.md](../GOVERNANCE.md).

## Quick start

```sh
git clone https://github.com/opensubagents/outcomes
cd outcomes

# Python reference SDK
cd sdk-python && uv pip install -e '.[dev]' && pytest && cd ..

# TypeScript reference SDK
cd sdk-typescript && pnpm install && pnpm test && cd ..

# End-to-end example
cd examples/research-engineering && uv pip install -e . && python run.py && cd ../..
```

## What lives where

- The **specification** lives in `specification/`. Normative changes here
  require an ADR under `docs/adrs/` and follow lazy consensus
  (see [GOVERNANCE.md](../GOVERNANCE.md#decision-making)).
- The **schemas** in `schema/` are the machine-checkable form of the spec.
  Any change to a `*.schema.json` file is a normative change.
- The **reference SDKs** in `sdk-python/` and `sdk-typescript/` MUST stay in
  parity. A PR that changes one SHOULD also change the other; if it cannot,
  open a tracking issue.
- **Examples** in `examples/` are end-to-end tests that exercise the spec
  against real fixtures.

## Pull request flow

1. **Open an issue first** for anything larger than a typo. This lets us
   surface duplicates and discuss scope before code is written.
2. **Branch from `main`**. Branch names that start with `claude/` are
   reserved for automated agents; if you are not an agent, please use any
   other prefix.
3. **Sign off your commits**. We require the Developer Certificate of Origin
   (DCO): every commit message must end with `Signed-off-by: Your Name
   <you@example.com>`. You can add this automatically with `git commit -s`.
4. **Add tests**. Python changes go in `sdk-python/tests/`; TypeScript
   changes go in `sdk-typescript/test/`. End-to-end changes go in
   `examples/`.
5. **Update the schemas, spec, and SDKs in the same PR** if your change
   touches normative shape. CI will fail otherwise.
6. **Open a draft PR early**. Mark ready-for-review when CI is green and the
   ADR (if any) is in place.

## Conformance to the spec

The reference SDKs are the conformance test bench for the spec itself. If
you find a case where the SDKs and the spec disagree, the spec wins by
default — but please open an issue so we can fix the SDK and add a
regression test.

## Style

- **Markdown.** `specification/` is linted by `markdownlint` (configured in
  `.github/workflows/spec-lint.yml`). RFC 2119 keywords (MUST, SHOULD, MAY)
  appear only inside blockquotes under `#####` headings — see existing
  sections for examples.
- **Python.** Type hints required. `ruff` and `pytest` run in CI; format
  with `ruff format`.
- **TypeScript.** Strict mode. `eslint` and `vitest` run in CI; format with
  `prettier`.

## Reporting security issues

See [SECURITY.md](./SECURITY.md). Please do not file security issues in the
public issue tracker.

## License

By contributing, you agree that your contributions will be licensed under
the [Apache 2.0 license](../LICENSE).
