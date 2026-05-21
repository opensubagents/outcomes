# Founding research — why Open Outcome, why now

This document captures the research that produced the v0.1 scope decision for
this repository. The verdict below is **why** Open Outcome exists and **why**
it sits at the layer it does (outcomes — declare, verify, grade) rather than
at the layers around it (capabilities, telemetry, SDK generation, packaging).

It is reproduced verbatim from the brief that ran on 2026-05-21, with a
dated addendum below noting subsequent corroborating events.

## Research report (2026-05-21)

```xml
<research_report>
  <verdict>
    There is no market gap for an "Open Coworker SDK" — that surface is already
    being closed by Anthropic's knowledge-work-plugins file format and the
    OpenTelemetry GenAI agent semantic conventions — but there is a real and
    unclaimed gap for an "Open Outcome SDK": a vendor-neutral spec for
    declaring, verifying, and grading the outcomes managed agents are
    supposed to produce.
  </verdict>

  <confidence>medium</confidence>

  <recommendation>
    Ship Open Outcome SDK first, not Open Coworker SDK. Define a vendor-neutral
    schema for outcome declarations (what should be true after an agent runs),
    a verifier interface (how to check it), and a graded-result envelope
    (verdict + cited evidence + confidence). Package it as a Python+TypeScript
    SDK plus an OTel-compatible event schema so verifications show up as
    spans in any existing observability backend. Distribute v0.1 as a
    Claude Code plugin in the opensubagents org so it has at least one
    runtime that exercises it end-to-end on day one. Defer the marketplace
    and the managed service — both are downstream of having a spec.
  </recommendation>

  <evidence>

    <claim idx="1">
      The "Open Coworker" plugin format is already de facto owned by
      Anthropic, who has open-sourced 11 production plugins (productivity,
      sales, customer-support, product-management, marketing, legal,
      finance, data, enterprise-search, bio-research, cowork-plugin-management)
      using a single canonical file layout — .claude-plugin/plugin.json,
      .mcp.json, commands/, skills/ — that has shipped through both Cowork
      and Claude Code.
    </claim>
    <citation claim="1" url="https://github.com/anthropics/knowledge-work-plugins" tier="primary">
      "We're open-sourcing 11 plugins built and inspired by our own work…
      Every plugin follows the same structure: plugin-name/ ├── .claude-plugin/plugin.json
      ├── .mcp.json ├── commands/ └── skills/"
    </citation>

    <claim idx="2">
      OpenTelemetry has already shipped GenAI agent semantic conventions in
      semconv 1.41.0 that normatively define the attributes any "coworker
      capability declaration" SDK would need to invent: gen_ai.agent.name,
      gen_ai.agent.id, gen_ai.agent.version, gen_ai.agent.description,
      gen_ai.workflow.name, gen_ai.tool.definitions, gen_ai.conversation.id,
      and operation names create_agent / invoke_agent / invoke_workflow /
      execute_tool.
    </claim>
    <citation claim="2" url="https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/" tier="primary">
      "gen_ai.operation.name has the following list of well-known values…
      create_agent Create GenAI agent… invoke_agent Invoke GenAI agent…
      invoke_workflow Invoke GenAI workflow… execute_tool Execute a tool."
    </citation>

    <claim idx="3">
      OpenTelemetry's agent conventions are not provider-specific —
      they explicitly enumerate Anthropic, OpenAI, AWS Bedrock, Azure AI,
      Cohere, DeepSeek, Gemini, Groq, IBM Watsonx, Mistral, Perplexity,
      and xAI as recognized values of gen_ai.provider.name, and call out
      LangChain and CrewAI by name in normative span guidance. Any
      "vendor-neutral coworker SDK" would be reinventing this layer.
    </claim>
    <citation claim="3" url="https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/" tier="primary">
      "Examples: LangChain agents, CrewAI agents… gen_ai.provider.name has
      the following list of well-known values… anthropic, aws.bedrock,
      azure.ai.inference, azure.ai.openai, cohere, deepseek, gcp.gemini,
      gcp.gen_ai, gcp.vertex_ai, groq, ibm.watsonx.ai, mistral_ai, openai,
      perplexity, x_ai."
    </citation>

    <claim idx="4">
      The cross-vendor tool/capability layer is also claimed: Model Context
      Protocol is positioned by its spec as the cross-LLM standard for
      exposing tools, resources, and prompts, with explicit JSON-RPC 2.0
      wire format and capability negotiation, and it already has OTel
      semantic conventions of its own. A new "Open Coworker SDK" would have
      to displace MCP, not complement it.
    </claim>
    <citation claim="4" url="https://modelcontextprotocol.io/specification/2025-06-18" tier="primary">
      "MCP provides a standardized way for applications to: Share contextual
      information with language models, Expose tools and capabilities to AI
      systems, Build composable integrations and workflows… The protocol
      uses JSON-RPC 2.0 messages… Server and client capability negotiation."
    </citation>

    <claim idx="5">
      The gap in the existing stack is on the verification side, not the
      declaration side. OpenTelemetry's agent conventions standardize what
      happened (input messages, tool calls, output messages, token counts)
      but contain no normative attributes for what was supposed to happen
      or whether it did — there is no gen_ai.outcome.expected,
      gen_ai.outcome.verdict, or gen_ai.outcome.evidence in the 1.41.0 spec.
    </claim>
    <citation claim="5" url="https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/" tier="primary">
      "gen_ai.input.messages… The chat history provided to the model as an
      input… gen_ai.output.messages… Messages returned by the model where
      each message represents a specific model response."
    </citation>

    <claim idx="6">
      OpenFeature is the closest spec-shape analog: a CNCF specification with
      explicit conformance language ("MUST", "MUST NOT", "REQUIRED") and a
      graduated status model (Experimental → Hardening → Stable) maintained
      by a Technical Steering Committee. An Open Outcome SDK should adopt
      this conformance pattern verbatim — it is a known-working governance
      model for vendor-neutral SDKs in this exact ecosystem.
    </claim>
    <citation claim="6" url="https://openfeature.dev/specification/" tier="primary">
      "An implementation is not compliant if it fails to satisfy one or
      more of the 'MUST', 'MUST NOT', 'REQUIRED', 'SHALL', or 'SHALL NOT'
      requirements defined in the normative sections… It is the
      responsibility of the Technical Steering Committee to consider and
      approve the graduation of documents."
    </citation>

    <claim idx="7">
      Existing agent SDKs (LangGraph, CrewAI, Letta) all expose proprietary
      verification surfaces tied to their own runtime — Letta, for instance,
      requires a Letta API key and a Letta-specific client to create
      stateful agents. None of them ship a vendor-neutral outcome
      verification spec that runs against another vendor's agent. This is
      the gap.
    </claim>
    <citation claim="7" url="https://github.com/letta-ai/letta" tier="primary">
      "Use the Letta API to integrate stateful agents into your own
      applications… import Letta from '@letta-ai/letta-client'; const
      client = new Letta({ apiKey: process.env.LETTA_API_KEY })."
    </citation>

  </evidence>

  <caveats>
    Confidence is medium not high because: (a) I could not load
    anthropic.com/news pages directly in this session so the "Anthropic's
    own outcome story" is inferred from the plugin repo README rather than
    from a product announcement; (b) Anthropic's own Managed Agents
    define_outcome API may already cover this for the Anthropic-only case,
    which would narrow the gap to "cross-vendor outcome verification" —
    still a real gap, but a smaller one; (c) the OTel GenAI conventions are
    still in Development status (not Stable) per the spec page, so they
    could absorb outcome attributes into a future version, which would
    close the Open Outcome SDK gap before it has a chance to standardize.
    The right move is to start the spec NOW, optimistically intending it to
    be upstreamed into OTel semconv as the gen_ai.outcome.* extension, not
    to compete with it.
  </caveats>
</research_report>
```

## Addendum — 2026-05-21 Stainless acquisition

On the same day this brief was filed, **Stainless** (founded 2022; generator
behind Anthropic's official SDKs; founder/CEO Alex Rattray) was acquired by
Anthropic. This is **corroborating** evidence for the verdict above, not
contradicting evidence:

- **MCP** claims the tool / capability layer (claim 4).
- **OpenTelemetry GenAI semconv** claims the telemetry layer (claims 2–3).
- **Stainless** — now Anthropic-internal — claims the SDK-generation layer.
- **The outcome layer** (declare → verify → grade) remains **unclaimed**.

The acquisition raises one open governance question for this project: whether
Open Outcome should ship its own hand-written reference SDKs in perpetuity
(the v0.1 plan), publish a Stainless-compatible OpenAPI spec and let
Stainless emit the SDKs, or run a hybrid (hand-written reference SDKs for
spec validation; Stainless-emitted SDKs for distribution). Because Stainless
is now Anthropic-internal and will optimize for Claude-native ergonomics, the
"let Stainless emit it" path is materially de-risked.

That decision is tracked as [ADR-0002](./adrs/ADR-0002-sdk-generation.md),
status **Pending**, and is queued as task #2 — a re-run of the
research-engineering plugin with `archetype = acquisition_impact` against
the Stainless news, then resolution of the ADR based on that brief's
verdict. It does not block v0.1: the v0.1 SDKs are hand-written reference
implementations regardless of how the question resolves.
