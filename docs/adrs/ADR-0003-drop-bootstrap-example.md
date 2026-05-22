# ADR-0003 — Drop the research-engineering bootstrap example

- **Status:** Accepted
- **Date:** 2026-05-21
- **Deciders:** Founding maintainer
- **Supersedes:** Decision 5 of [ADR-0001](./ADR-0001-name-and-scope.md) (in
  the part about `examples/research-engineering/` being the parity test
  bench) and the build-time portion of [ADR-0002](./ADR-0002-sdk-generation.md)
  that called for re-running the sibling plugin in CI.

## Context

v0.1.0 shipped one large bootstrap PR. That PR included
`examples/research-engineering/`, a worked example that pulled fixtures
from the sibling `opensubagents/research-engineering` Claude Code plugin
and asserted byte-level parity between the Open Outcome
`HeuristicVerifier` and the plugin's grader. The example was useful as a
forcing function for the first commit — it proved the spec could ingest
a real report end-to-end — but it tied a vendor-neutral spec to one
specific consumer:

- The CI job `example-research-engineering` needed a cross-repo PAT
  (`SIBLINGS_READ_TOKEN`) before it could pass.
- `CONTRIBUTING.md` directed every new contributor through a sibling
  checkout that most of them wouldn't have rights to.
- `appendix-d-worked-example.md` made the spec read as if
  research-engineering was a normative dependency, even though the
  appendix was informative.
- New consumers of the spec (other Claude Code plugins, future SDKs,
  third-party verifiers) had no example that did not first require
  another repo.

## Decision

Drop the example directory and every required reference to it. Specifically:

1. Delete `examples/research-engineering/` (and the empty `examples/`
   parent).
2. Delete `specification/appendix-d-worked-example.md`.
3. Remove the `example-research-engineering` job from
   `.github/workflows/python-sdk.yml`.
4. Remove the CI-secrets section and the local-run line from
   `.github/CONTRIBUTING.md`.
5. Drop the example row from `README.md` and `specification/README.md`.
6. Rewrite the comment/docstring/README sections in the SDKs that
   described the parity-with-research-engineering relationship — keep
   "parity between Python and TypeScript SDKs" wording, drop the
   cross-repo wording.

Keep the historical references in:

- `docs/founding-research.md` (the founding pitch, unchanged).
- `docs/adrs/ADR-0001-name-and-scope.md` and `ADR-0002-sdk-generation.md`
  (immutable history; this ADR supersedes their relevant clauses).

Keep namespace/scope mentions of `opensubagents` everywhere else — the
org name and the npm scope `@opensubagents/open-outcome` are not coupled
to the plugin.

## Consequences

- **Positive.** v0.1.x onward, the spec ships as a pure spec + reference
  SDKs with no required sibling. CI does not need a cross-repo token.
  New contributors can clone and run tests with no out-of-repo setup.
- **Negative.** v0.1 no longer has a runnable end-to-end fixture that
  spans an external grader. A follow-up branch should re-introduce a
  small, self-contained example (e.g., a `examples/local-otel/` that
  exercises `appendix-b-otel-extension.md` against an OpenTelemetry
  Collector in `debug` mode) so the OTel projection has a wire-level
  proof again.
- **Neutral.** Parity between the two SDKs is now asserted via each
  SDK's own test suite using shared fixtures, not via a third-repo
  grader.

## Verification

- `grep -rn "research-engineering\|research_engineering" --exclude-dir=.git`
  returns only `docs/founding-research.md`, the two prior ADRs, this
  ADR, and the plan file under `docs/plans/`.
- `cd sdk-python && uv run pytest` passes.
- `cd sdk-typescript && npm test` passes.
- `python -c "import yaml; yaml.safe_load(open('.github/workflows/python-sdk.yml'))"`
  succeeds.
