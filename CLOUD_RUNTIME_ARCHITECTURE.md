# Cloud Agent Runtime Architecture v0.3

> Status: ADOPTED
> Date: 2026-09-03
> Scope: Global Agent System architecture

## 1. Purpose

Cloudflare is the **Cloud Runtime Layer** of the Agent System. It is not a new business project and does not replace GitHub, Buddy, or ChatGPT.

The runtime implementation is maintained in a **separate project repository** from `agent-lab`. `agent-lab` remains the Governance / Agent Hub / Global Memory layer and does not become an execution repository.

The architecture is deliberately **Free-first**: the initial runtime must be implementable on the Cloudflare Free plan. Paid capabilities are introduced only when an actual workload exceeds free-tier limits or requires Sandbox/Containers.

## 2. Architecture evolution — preserve history, do not rewrite it

The Cloud Runtime layer was **not part of the original AI collaboration design**. It was introduced later as an architectural evolution after the earlier GitHub-centered collaboration model exposed a need for durable cloud-side runtime state, workflows, controlled capabilities and eventually autonomous production execution that should not depend on Buddy/local preparation.

The historical sequence is:

```text
Original collaboration model
Human → ChatGPT → GitHub Memory → Buddy / project execution
                         │
                         │ later evolution
                         ▼
                 Cloud Runtime layer
                         │
                         ▼
                    core-agent
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
     domain runtimes             other capabilities
```

Therefore:

- historical documents describing the pre-CoreAgent system remain historical facts;
- later CoreAgent / Cloud Runtime architecture must not be projected backward into those documents;
- `core-agent` is an **evolved infrastructure layer**, not an original assumption;
- the introduction of Cloud Runtime is a deliberate architecture change recorded here, while the original model remains auditable through Git history.

## 3. System responsibility boundaries

| Layer | Canonical responsibility |
|---|---|
| Human | Real-world actions, business decisions, external approvals |
| ChatGPT | Reasoning, research, architecture, content, decisions, task contracts, review |
| Agent Hub (`agent-lab`) | Governance, Global Memory, project registry, cross-project coordination and protocols |
| Project GitHub repositories | Canonical project code, configuration, project Memory, state, decisions, evidence and task history |
| CoreAgent (`core-agent`) | Unified cloud Agent Runtime: identity, durable runtime state, workflow orchestration, controlled capability/tool routing and bounded execution coordination |
| Domain Runtimes | Domain-specific deterministic execution capabilities (for example content or quantitative execution); they do not become generic autonomous agents merely because they run in Cloudflare |
| Buddy | Development/local execution of explicit GitHub Issue contracts; not a required production-runtime dependency |
| Cloudflare | Hosting/runtime substrate for CoreAgent and domain runtimes |

Hard rule: **GitHub is Canonical; Cloudflare is Runtime; Buddy is Execution; ChatGPT is Reasoning Owner.**

## 4. Repository boundary

`agent-lab` is the **Agent Hub**, not the Cloud Runtime implementation project.

The Cloud Runtime implementation lives in the independent repository:

`watanuo1982/-agent-runtime`

The first runtime target inside that project is:

`core-agent`

This separation prevents the Global Memory / governance repository from becoming a mixed governance-and-execution repository.

## 5. CoreAgent versus Domain Runtime

The current architecture uses a strict two-level runtime boundary:

```text
ChatGPT
   │ reasoning / decision / review
   ▼
CoreAgent
   │ unified runtime / context / orchestration
   ├── GitHub context
   ├── durable state
   ├── Workflow
   ├── controlled MCP/tool capabilities
   └── bounded routing
        │
        ├───────────────┬────────────────
        ▼               ▼
AI Content Runtime   Quant Runtime
(domain execution)   (domain execution)
```

**CoreAgent is not a second business-domain agent.** It should coordinate and expose bounded capabilities rather than independently inventing content, trading strategies or business decisions.

A Domain Runtime is not automatically a Domain Agent. Keep deterministic/domain execution below CoreAgent unless a separate architecture review demonstrates a real need for agent-level identity, planning and isolation.

Avoid this anti-pattern:

```text
ChatGPT → CoreAgent → Generic Proxy → Domain Runtime → another Agent → tools
```

Each added layer must have a demonstrated responsibility; MCP must remain a capability interface, not a generic proxy or hidden second orchestration system.

## 6. Runtime primitives

### 6.1 Worker

Use for stateless HTTP/API entry points, routing, authentication and small transformations.

### 6.2 Agent / Durable Object

Use as the persistent identity and runtime state of an Agent.

Agent-local state may include:
- agent identity
- current task/session
- small structured state
- schedules
- workflow references
- runtime checkpoints

Agent state is **not** canonical project Memory.

### 6.3 Workflow

Use for multi-step, long-running, retryable or checkpointed processes.

Typical pattern:
`CoreAgent -> Workflow -> steps/checkpoints/retry -> result`

### 6.4 D1

Use only for shared structured data that genuinely needs a relational store across runtime components.

Do not use D1 as a dumping ground for large market/history datasets.

### 6.5 R2

Use for large objects/files: CSV, Parquet, PDFs, images, videos, model artifacts and large experiment outputs.

### 6.6 Queues

Use for asynchronous workloads where decoupling is useful. Do not introduce Queues merely because they exist.

### 6.7 Sandbox / Containers

Optional paid-capability boundary for isolated Linux execution, Python/Node/Shell, heavy computation and untrusted or dependency-heavy workloads.

Sandbox is not required for the current CoreAgent baseline.

## 7. Agent topology

Start with exactly one generic runtime Agent:

`core-agent`

Its responsibility is runtime infrastructure, not business-domain reasoning.

Future domain Agents may be introduced only after CoreAgent is stable and a demonstrated isolation/ownership requirement exists.

Do not create `content-agent`, `quant-agent` or other domain Agents merely to wrap existing deterministic Domain Runtimes.

## 8. Canonical Memory boundary

```text
GitHub Memory (canonical)
        |
        +---- ChatGPT reasoning
        |
        +---- CoreAgent / Cloud Runtime
        |
        +---- Buddy execution
```

Cloudflare may cache or persist runtime state, but durable knowledge/decisions/project facts must ultimately be synchronized to the appropriate GitHub canonical location.

Never create a second independent Memory system in Cloudflare.

## 9. Task model

All durable, auditable work remains Issue-first under the existing Agent Git Memory Contract.

Conceptually, runtime tasks use:

```yaml
task_id: unique
agent_id: core-agent
objective: explicit objective
input: structured input
permissions: explicit capability boundary
execution_mode: sync | workflow | sandbox
status: READY | IN_PROGRESS | DONE | BLOCKED
result: structured result
artifacts: references to canonical artifacts
audit: execution metadata
```

This remains a conceptual runtime contract; do not create a competing task system outside GitHub Issues unless a concrete runtime need is demonstrated and separately approved.

## 10. Identity and permissions

Every Agent has an explicit `agent_id` and capability boundary.

Default posture:
- GitHub: read
- Cloudflare: read
- external systems: read unless explicitly required
- Sandbox: disabled until needed

Write/deploy/delete/external side effects require an explicit capability grant and must be auditable.

## 11. Secrets

Secrets are runtime credentials, not Memory.

Never commit secrets, tokens, API keys or credentials into GitHub Memory or project Markdown.

Secrets must be injected through the appropriate runtime/local secret mechanism and exposed to the minimum component that needs them.

## 12. Free-first policy

Initial target:

```text
Workers
+ Agents / Durable Objects / SQLite
+ Workflows
+ MCP
+ D1 (small structured data)
+ R2 (small/moderate files)
+ Queues (when justified)
```

Do not upgrade or add paid infrastructure preemptively.

Upgrade only when:
1. a measured workload exceeds free limits;
2. a required capability is unavailable on Free; or
3. production reliability requirements justify it.

Sandbox/Containers are explicitly treated as a later paid boundary.

## 13. Deployment phases

### P0 — Architecture
Status: ADOPTED

- responsibility boundaries
- canonical Memory rule
- identity/permissions model
- repository boundary
- task model
- Free-first rule

### P1 — Cloudflare account audit

Read-only inventory of available products, current resources, plan/limits and permissions. No deployment changes.

### P2 — Core Agent

Deploy `core-agent` with identity, health, minimal persistent state and a simple task lifecycle.

### P3 — GitHub integration

Connect runtime to GitHub while preserving GitHub as canonical.

### P4 — Workflow

Prove a retryable/checkpointed multi-step task.

### P5 — MCP client capability

Prove bounded capability consumption through an allowlisted MCP client. A future ChatGPT-facing MCP server is a separate architectural step and is not implied by P5.

### P6 — First real workloads

Use bounded real workloads to validate the runtime. Quant and AI Content are now two distinct domain execution paths under the same runtime architecture.

### P7 — Sandbox (conditional)

Introduce only if real workloads demonstrate that Buddy/local execution or Workers are insufficient.

### P8 — Domain Agents (conditional)

Split `core-agent` into domain Agents only after the common runtime is stable and there is demonstrated isolation/ownership value.

## 14. Operational safety

The runtime must be designed so that Cloudflare failure does not destroy canonical project knowledge.

For every durable execution:
- runtime state may live in Cloudflare;
- canonical decision/result/artifact references return to GitHub;
- execution is auditable;
- unknown/conflicting facts are not silently promoted to canonical facts.

## 15. Anti-patterns

Do not introduce:
- VPS solely to host Agents
- Kubernetes
- self-managed Redis/Postgres
- vector DB without a demonstrated retrieval requirement
- multiple domain Agents before CoreAgent validation
- unrestricted shell execution
- automatic production deployment
- Cloudflare as a second Memory source
- a second task system that competes with GitHub Issues
- Cloud Runtime implementation code inside `agent-lab`
- generic MCP proxy / arbitrary MCP endpoint forwarding
- unnecessary runtime layers between CoreAgent and Domain Runtime

## 16. Decision

**ADOPTED:** Cloudflare is part of the global Agent System architecture as an evolved Cloud Runtime Layer, while its implementation is isolated in the independent `-agent-runtime` project.

The historical pre-CoreAgent collaboration model remains valid as history and is not rewritten. The current architecture is an explicit evolution: **ChatGPT → CoreAgent → bounded Domain Runtime → GitHub canonical artifacts/state**, with Human retaining real-world authority and Buddy remaining an execution/development role rather than a production-runtime dependency.
