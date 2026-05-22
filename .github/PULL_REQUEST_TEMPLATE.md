<!--
Thanks for sending a PR! A few quick prompts:

- What does this change do, in one sentence?
- Does it touch the spec or schemas? If yes, link the ADR.
- Did you update both SDKs (Python + TypeScript) if the change is normative?
- Did you add tests?
-->

## Summary

<!-- One or two sentences. What changed and why. -->

## Outcome

This repo gates merges on its own rubric. Every PR — including docs and
tooling — adds a new outcome+report pair under `outcomes/`. The pair is
scored by `HeuristicVerifier` (see
[Appendix A](../specification/appendix-a-rubric.md)) and merge is blocked
when `verdict.overall < 3.5`.

- [ ] Added `outcomes/<slug>.outcome.json` describing what this PR claims to achieve.
- [ ] Added `outcomes/<slug>.report.json` carrying the evidence that the claim is met.
- [ ] Verified locally: `python -m open_outcome.cli verify outcomes/<slug>.outcome.json outcomes/<slug>.report.json`

Example slug for this PR: `<short-kebab-case>` (e.g. `revert-session-start-hook`).

## Type of change

- [ ] Normative (spec, schema, or public SDK surface)
- [ ] Reference SDK implementation
- [ ] Example
- [ ] Tooling / CI / docs

## Linked ADR

<!-- For normative changes only. e.g. "Closes ADR-0003." -->

## Checklist

- [ ] I signed off the commits (`git commit -s`) per
      [CONTRIBUTING.md](./CONTRIBUTING.md).
- [ ] If the change is normative, both `sdk-python/` and `sdk-typescript/`
      are updated.
- [ ] Tests cover the new behavior.
- [ ] `specification/`, `schema/`, and the SDKs agree.
