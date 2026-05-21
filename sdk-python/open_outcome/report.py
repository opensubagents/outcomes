"""Report — the agent's structured output that a verifier consumes.

The spec deliberately does not constrain the report shape beyond what a
verifier needs to read (``summary``, ``claims``). Implementations may
extend ``Report`` with their own fields; the reference verifier only reads
the documented ones.
"""
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .evidence import Citation, Claim


class Report(BaseModel):
    """Structured output the agent produces in response to an outcome."""

    model_config = ConfigDict(frozen=True)

    summary: str = Field(min_length=1)
    claims: tuple[Claim, ...] = Field(min_length=1)
    open_questions: tuple[str, ...] = Field(default_factory=tuple)
    methodology_notes: str | None = None

    def all_citations(self) -> tuple[Citation, ...]:
        """Deduplicated citations across every claim, by URL."""
        seen: dict[str, Citation] = {}
        for claim in self.claims:
            for c in claim.citations:
                seen.setdefault(str(c.url), c)
        return tuple(seen.values())
