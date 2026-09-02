# Cloud Agent Runtime Architecture v0.2

> Status: ADOPTED
> Date: 2026-09-02
> Scope: Global Agent System architecture

## 1. Purpose

Cloudflare is the **Cloud Runtime Layer** of the Agent System. It is not a new business project and does not replace GitHub, Buddy, or ChatGPT.

The runtime implementation is maintained in a **separate project repository** from `agent-lab`. `agent-lab` remains the Governance / Agent Hub / Global Memory layer and does not become an execution repository.

The architecture is deliberately **Free-first**: the initial runtime must be implementable on the Cloudflare Free plan. Paid capabilities are introduced only when an actual workload exceeds free-tier limits or requires Sandbox/Containers.

## 2. System responsibility boundaries

| Layer | Canonical responsibility |
|---|---|
| Human | Real-world actions, business decisions, external approvals |
| ChatGPT | Reasoning, research, architecture, content, decisions, task contracts, review |
| Agent Hub (`agent-lab`) | Governance, Global Memory, project registry, cross-project coordination and protocols |
| Project GitHub repositories | Canonical project code, configuration, project Memory, state, decisions, evidence and task history |
| Buddy | Execution in local/dev environment; implements explicit Issue contracts |
| Cloud Runtime project | Implementation of cloud runtime components and deployment artifacts |
| Cloudflare | Cloud runtime: persistent Agent state, scheduling, workflows, APIs, async work, files, optional code execution |

Hard rule: **GitHub is Canonical; Cloudflare is Runtime; Buddy is Execution; ChatGPT is Reasoning Owner.**

## 3. Repository boundary

`agent-lab` is the **Agent Hub**, not the Cloud Runtime implementation project.

The Cloud Runtime implementation must live in an independent repository, currently designated:

`watanuo1982/-agent-runtime`

The first runtime target inside that project is:

`core-agent`

This separation prevents the Global Memory / governance repository from becoming a mixed governance-and-execution repository.

The runtime project follows the existing Project Memory minimum: README, PROJECT_CONTEXT, CURRENT_STATE, NEXT_WORK and GITHUB_WORKFLOW, with DECISIONS / MEMORY_INDEX / CHANGELOG as appropriate.

## 4. Runtime primitives

### 4.1 Worker

Use for stateless HTTP/API entry points, routing, authentication and small transformations.

### 4.2 Agent / Durable Object

Use as the persistent identity and runtime state of an Agent.

Agent-local state may include:
- agent identity
- current task/session
- small structured state
- schedules
- workflow references
- runtime checkpoints

Agent state is **not** canonical project Memory.

### 4.3 Workflow

Use for multi-step, long-running, retryable or checkpointed processes.

Typical pattern:
`Agent -> Workflow -> steps/checkpoints/retry -> result`

### 4.4 D1

Use only for shared structured data that genuinely needs a relational store across runtime components.

Do not use D1 as a dumping ground for large market/history datasets.

### 4.5 R2

Use for large objects/files: CSV, Parquet, PDFs, images, videos, model artifacts and large experiment outputs.

### 4.6 Queues

Use for asynchronous workloads where decoupling is useful. Do not introduce Queues merely because they exist.

### 4.7 Sandbox / Containers

Optional paid-capability boundary for isolated Linux execution, Python/Node/Shell, heavy computation and untrusted or dependency-heavy workloads.

Sandbox is **not required for Core Agent v0.1**.

## 5. Agent topology

Start with exactly one generic runtime Agent:

`core-agent`

Its responsibility is runtime infrastructure, not business-domain reasoning.

Future domain Agents may include:
- `quant-agent`
- `research-agent`
- `content-agent`
- `automation-agent`

Do not create domain sub-agents until `core-agent` is stable.

## 6. Canonical Memory boundary

```text
GitHub Memory (canonical)
        |
        +---- ChatGPT reasoning
        |
        +---- Cloud Runtime project / Cloudflare runtime state
        |
        +---- Buddy execution
```

Cloudflare may cache or persist runtime state, but durable knowledge/decisions/project facts must ultimately be synchronized to the appropriate GitHub canonical location.

Never create a second independent Memory system in Cloudflare.

## 7. Task model

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

This is a conceptual schema for v0.1; do not create a second task system outside GitHub Issues until a concrete runtime need is demonstrated.

## 8. Identity and permissions

Every Agent has an explicit `agent_id` and capability boundary.

Default posture:
- GitHub: read
- Cloudflare: read
- external systems: read unless explicitly required
- Sandbox: disabled until needed

Write/deploy/delete/external side effects require an explicit capability grant and must be auditable.

## 9. Secrets

Secrets are runtime credentials, not Memory.

Never commit secrets, tokens, API keys or credentials into GitHub Memory or project Markdown.

Secrets must be injected through the appropriate runtime/local secret mechanism and exposed to the minimum component that needs them.

## 10. Free-first policy

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

## 11. Deployment phases

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

### P5 — MCP

Expose only the capabilities required by the Agent System.

### P6 — First real workload

Use a bounded real workload to validate the runtime. Quant is a strong candidate because it naturally exercises data, Python, long-running jobs, schedules and artifacts.

### P7 — Sandbox (conditional)

Introduce only if real workloads demonstrate that Buddy/local execution or Workers are insufficient.

### P8 — Sub-agents (conditional)

Split `core-agent` into domain Agents only after the common runtime is stable and there is demonstrated isolation/ownership value.

## 12. Operational safety

The runtime must be designed so that Cloudflare failure does not destroy canonical project knowledge.

For every durable execution:
- runtime state may live in Cloudflare;
- canonical decision/result/artifact references return to GitHub;
- execution is auditable;
- unknown/conflicting facts are not silently promoted to canonical facts.

## 13. Anti-patterns

Do not introduce, in v0.1:
- VPS solely to host Agents
- Kubernetes
- self-managed Redis/Postgres
- vector DB without a demonstrated retrieval requirement
- multiple domain Agents before Core Agent validation
- unrestricted shell execution
- automatic production deployment
- Cloudflare as a second Memory source
- a second task system that competes with GitHub Issues
- Cloud Runtime implementation code inside `agent-lab`

## 14. Decision

**ADOPTED:** Cloudflare is part of the global Agent System architecture as the Cloud Runtime Layer, while its implementation is isolated in the independent `-agent-runtime` project.

The first implementation target is a Free-plan-compatible `core-agent`; paid compute is an escalation path, not a prerequisite.
