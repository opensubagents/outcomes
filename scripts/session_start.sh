#!/usr/bin/env bash
# SessionStart hook: deterministic per-session setup for Claude Code on the web.
# - Installs the gh CLI (apt) if missing
# - Starts Docker, Redis 7, and PostgreSQL services
# - Installs the mcp-server-dev plugin from the official marketplace
#
# Runs on every session (startup and resume). Local sessions are skipped so
# this only affects the cloud environment.

set -u

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

log() { printf '[session-start] %s\n' "$*" >&2; }

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo -n"
  fi
fi

# --- gh CLI -----------------------------------------------------------------
if ! command -v gh >/dev/null 2>&1; then
  log "installing gh CLI via apt"
  $SUDO apt-get update -y >/dev/null 2>&1 || true
  $SUDO apt-get install -y gh >/dev/null 2>&1 || log "gh install failed (non-fatal)"
else
  log "gh CLI already present: $(gh --version | head -n1)"
fi

# --- Docker -----------------------------------------------------------------
if command -v docker >/dev/null 2>&1; then
  if ! docker info >/dev/null 2>&1; then
    log "starting docker daemon"
    if command -v service >/dev/null 2>&1; then
      $SUDO service docker start >/dev/null 2>&1 || \
        $SUDO dockerd >/var/log/dockerd.log 2>&1 &
    else
      $SUDO dockerd >/var/log/dockerd.log 2>&1 &
    fi
    # Wait for the daemon socket (up to ~20s)
    for _ in $(seq 1 20); do
      if docker info >/dev/null 2>&1; then break; fi
      sleep 1
    done
  fi
  docker info >/dev/null 2>&1 && log "docker ready" || log "docker not ready (non-fatal)"
else
  log "docker not installed; skipping"
fi

# --- PostgreSQL 16 ----------------------------------------------------------
if command -v pg_isready >/dev/null 2>&1 || command -v psql >/dev/null 2>&1; then
  log "starting postgresql"
  $SUDO service postgresql start >/dev/null 2>&1 || true
  for _ in $(seq 1 15); do
    if pg_isready >/dev/null 2>&1; then break; fi
    sleep 1
  done
  pg_isready >/dev/null 2>&1 && log "postgres ready" || log "postgres not ready (non-fatal)"
else
  log "postgresql client not found; skipping"
fi

# --- Redis 7 ----------------------------------------------------------------
if command -v redis-cli >/dev/null 2>&1; then
  log "starting redis-server"
  $SUDO service redis-server start >/dev/null 2>&1 || true
  for _ in $(seq 1 10); do
    if redis-cli ping 2>/dev/null | grep -q PONG; then break; fi
    sleep 1
  done
  redis-cli ping 2>/dev/null | grep -q PONG && log "redis ready" || log "redis not ready (non-fatal)"
else
  log "redis-cli not found; skipping"
fi

# --- Claude plugin ----------------------------------------------------------
if command -v claude >/dev/null 2>&1; then
  if claude plugin list 2>/dev/null | grep -q '^mcp-server-dev\b'; then
    log "plugin mcp-server-dev already installed"
  else
    log "installing plugin mcp-server-dev@claude-plugins-official"
    claude plugin install mcp-server-dev@claude-plugins-official >/dev/null 2>&1 \
      || log "plugin install failed (non-fatal)"
  fi
else
  log "claude CLI not found; skipping plugin install"
fi

exit 0
