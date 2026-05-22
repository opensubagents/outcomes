# Reference MCP server

> Pointer to [`opensubagents/outcomes-mcp`](https://github.com/opensubagents/outcomes-mcp), vendored at `./mcp-server/` as a git submodule.

This directory is a **git submodule** pinned at a specific commit of the
canonical Open Outcome MCP server repo. The submodule keeps the spec
(this repo) and the reference MCP server (outcomes-mcp) colocated for
contributors, while preserving a single source of truth at
`opensubagents/outcomes-mcp`.

## Updating the pin

```sh
git submodule update --remote mcp-server
git add mcp-server
git commit -s -m "chore(mcp-server): bump submodule to <sha>"
```

Open the bump as a normal PR on this repo. The outcome-gate will run.

## Why a submodule and not a vendored copy

The MCP server has its own CI, version, and release cycle. A vendored
copy would duplicate the verifier algorithm and create a drift surface;
a submodule explicitly points at a SHA and forces the reader to go to
the canonical source.

## Trust boundary

Submodules respect the same trust model as any external code: they do
not run during clone or checkout, and their CI does not run as part of
this repo's CI. The submodule contents are not part of this repo's
outcome-gate evaluation; only the submodule pointer (the SHA) is.

## See also

- [`opensubagents/outcomes-mcp`](https://github.com/opensubagents/outcomes-mcp) — canonical repo
- [`specification/sections/02-verifier.md`](../specification/sections/02-verifier.md) — what the MCP server wraps
- [`docs/adrs/`](../docs/adrs/) — architectural decisions
