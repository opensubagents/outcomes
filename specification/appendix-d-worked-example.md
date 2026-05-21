---
title: Appendix D — Worked example
description: One end-to-end Outcome → Report → Verdict cycle.
---

# Appendix D — Worked example: research-engineering

> This appendix is **informative**. It walks through one end-to-end
> Outcome → Report → Verdict cycle using a fixture from the
> [`opensubagents/research-engineering`](https://github.com/opensubagents/research-engineering)
> plugin. The runnable form lives in
> [`examples/research-engineering/`](../examples/research-engineering/).

## 1. The outcome

A research-engineering brief from 2026-05-21, mapped into an Open Outcome
declaration. The brief asks which open-source agent SDK is the best
foundation for building a coworker system.

```json
{
  "title": "Open-source SDKs for building autonomous coworker / subagent systems",
  "as_of": "2026-05-21",
  "question": "Which open-source agent SDK is the best foundation for building autonomous 'coworker' systems that delegate to subagents in May 2026?",
  "success_criteria": [
    "Each candidate's license is verified from primary sources",
    "Each candidate's stance on subagent / multi-agent delegation is stated",
    "Each candidate's lock-in to a specific model provider is stated",
    "A concrete recommendation is given with the main tradeoff named"
  ],
  "archetype": "vendor_comparison",
  "archetype_fields": {
    "candidates": ["Claude Agent SDK", "OpenAI Agents SDK", "LangGraph", "CrewAI", "Strands Agents"],
    "dimensions": ["license", "subagent model", "provider lock-in", "production posture", "solo-maintainer learning curve"]
  }
}
```

The fields are mandated by [section 1](./sections/01-outcome-declaration.md):
`title`, `as_of`, `question`, and `success_criteria` are required;
`archetype` and `archetype_fields` are optional.

## 2. The report

The agent produces a structured report. The full fixture lives at
[`examples/research-engineering/report.json`](../examples/research-engineering/report.json);
abbreviated here:

```json
{
  "summary": "For a solo maintainer building a coworker system in May 2026, the live field is five MIT/Apache-licensed SDKs with materially different subagent stories. The Claude Agent SDK has the most explicit subagent primitive but is locked to Claude models...",
  "claims": [
    {
      "statement": "The Claude Agent SDK exposes subagents as a first-class primitive via an `agents` parameter and forbids subagents from spawning their own subagents.",
      "confidence": "high",
      "citations": [
        {"url": "https://code.claude.com/docs/en/agent-sdk/subagents", "kind": "primary", "...": "..."},
        {"url": "https://www.anthropic.com/engineering/...", "kind": "primary", "...": "..."}
      ]
    }
  ]
}
```

## 3. The verdict

The reference `HeuristicVerifier` consumes the outcome + report and
returns a verdict satisfying [section 3](./sections/03-verdict.md):

```json
{
  "spec_version": "0.1.0",
  "verifier_id": "open-outcome.python.heuristic",
  "dimensions": [
    {"name": "confidence_calibration", "score": 4, "justification": "1/8 miscalibrated: low-confidence claim is well-sourced (under-calibrated)..."},
    {"name": "citation_quality", "score": 5, "justification": "13/22 primary"},
    {"name": "coverage", "score": 5, "justification": "9/9 required axes mentioned"},
    {"name": "decision_usefulness", "score": 5, "justification": "4/4 decision signals present"},
    {"name": "clarity", "score": 5, "justification": "summary is 4 sentences"}
  ],
  "overall": 4.8,
  "evidence": [
    {"url": "https://code.claude.com/docs/en/agent-sdk/subagents", "title": "Subagents in the SDK - Claude Docs", "kind": "primary", "accessed": "2026-05-21"}
  ],
  "notes": "HeuristicVerifier (no LLM)"
}
```

## 4. The OTel projection

Per [section 6](./sections/06-observability.md), the verdict projects onto
a `verify_outcome` span with these attributes:

```text
gen_ai.outcome.spec_version       = "0.1.0"
gen_ai.outcome.overall            = 4.8
gen_ai.outcome.dimension_count    = 5
gen_ai.outcome.evidence_count     = 22
gen_ai.outcome.verifier_id        = "open-outcome.python.heuristic"
gen_ai.outcome.dimension.confidence_calibration.score = 4
gen_ai.outcome.dimension.citation_quality.score       = 5
gen_ai.outcome.dimension.coverage.score               = 5
gen_ai.outcome.dimension.decision_usefulness.score    = 5
gen_ai.outcome.dimension.clarity.score                = 5
```

## 5. Parity check

The runnable example in
[`examples/research-engineering/run.py`](../examples/research-engineering/run.py)
also grades the same report using `research-engineering`'s own
`HeuristicGrader` and asserts that the dimension scores match exactly.
This is the spec's main acceptance test: the Open Outcome SDK and the
research-engineering plugin must agree on the same fixture.
