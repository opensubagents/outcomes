# CLAUDE.md — instructions for Claude Code in this repo

This file is read by Claude Code at session start. It encodes the
development discipline for `opensubagents/outcomes`.

## Project-scope plugin and MCP policy

Every Claude Code plugin or MCP server used in this repository is
**version-controlled at project scope**. We do not rely on
per-developer (user-scope) installations.

- Plugins are enumerated in [`.claude/settings.json`](./.claude/settings.json)
  under `enabledPlugins`.
- MCP servers (when added) live in `.mcp.json` at the repo root.
- New plugins or MCPs land **one per branch**, paired with one
  atomic improvement that exercises the new capability. No bundled
  multi-install PRs.

The full discipline (heartbeat, linearized branches, backlog) is in
[`docs/plans/2026-05-21-drop-bootstrap-and-audit-otel.md`](./docs/plans/2026-05-21-drop-bootstrap-and-audit-otel.md)
under "Plan v2 — Linearized dogfood ladder".

## Currently enabled project-scope plugins

| Plugin | Source | Use for |
|---|---|---|
| `commit-commands` | `claude-plugins-official` | Stage + generate commit messages via `/commit-commands:commit`. Activated on this branch; subsequent branches should prefer it over hand-written commits to keep commit-message shape consistent across the dogfood ladder. |

## Dogfood loop

Every diff on this repo should be passed through
`open_outcome.HeuristicVerifier` before push. Pass threshold for the
verdict overall: **>= 4.0 / 5**. PR descriptions record the verdict
table per commit. See the `Dogfood` section of the v0.1 plan for the
working example.

## Spec posture

The Open Outcome spec is **vendor-neutral on OTel backends**. Do not
name Axiom, Honeycomb, Grafana, Datadog, or any other vendor in
`specification/appendix-b-otel-extension.md` or in the SDK projection
helpers (`sdk-python/open_outcome/otel.py`,
`sdk-typescript/src/otel.ts`). Backend choice is dev-infra advice,
captured in `docs/research-reviews/`, never in the normative spec.
