# Cloud Agent Runtime Architecture v0.1

> Status: ADOPTED
> Date: 2026-09-02
> Scope: Global Agent System architecture

## 1. Purpose

Cloudflare is the **Cloud Runtime Layer** of the Agent System. It is not a new business project and does not replace GitHub, Buddy, or ChatGPT.

The architecture is deliberately **Free-first**: the initial runtime must be implementable on the Cloudflare Free plan. Paid capabilities are introduced only when an actual workload exceeds free-tier limits or requires Sandbox/Containers.

## 2. System responsibility boundaries

| Layer | Canonical responsibility |
|---|---|
| Human | Real-world actions, business decisions, external approvals |
| ChatGPT | Reasoning, research, architecture, content, decisions, task contracts, review |
| GitHub | Canonical code, configuration, Memory, project state, decisions, evidence, task history |
| Buddy | Execution in local/dev environment; implements explicit Issue contracts |
| Cloudflare | Cloud runtime: persistent Agent state, scheduling, workflows, APIs, async work, files, optional code execution |

Hard rule: **GitHub is Canonical; Cloudflare is Runtime; Buddy is Execution; ChatGPT is Reasoning Owner.**

## 3. Runtime primitives

### 3.1 Worker

Use for stateless HTTP/API entry points, routing, authentication and small transformations.

### 3.2 Agent / Durable Object

Use as the persistent identity and runtime state of an Agent.

Agent-local state may include:
- agent identity
- current task/session
- small structured state
- schedules
- workflow references
- runtime checkpoints

Agent state is **not** canonical project Memory.

### 3.3 Workflow

Use for multi-step, long-running, retryable or checkpointed processes.

Typical pattern:
`Agent -> Workflow -> steps/checkpoints/retry -> result`

### 3.4 D1

Use only for shared structured data that genuinely needs a relational store across runtime components.

Do not use D1 as a dumping ground for large market/history datasets.

### 3.5 R2

Use for large objects/files: CSV, Parquet, PDFs, images, videos, model artifacts and large experiment outputs.

### 3.6 Queues

Use for asynchronous workloads where decoupling is useful. Do not introduce Queues merely because they exist.

### 3.7 Sandbox / Containers

Optional paid-capability boundary for isolated Linux execution, Python/Node/Shell, heavy computation and untrusted or dependency-heavy workloads.

Sandbox is **not required for Core Agent v0.1**.

## 4. Agent topology

Start with exactly one generic runtime Agent:

`core-agent`

Its responsibility is runtime infrastructure, not business-domain reasoning.

Future domain Agents may include:
- `quant-agent`
- `research-agent`
- `content-agent`
- `automation-agent`

Do not create domain sub-agents until `core-agent` is stable.

## 5. Canonical Memory boundary

```text
GitHub Memory (canonical)
        |
        +---- ChatGPT reasoning
        |
        +---- Cloudflare runtime state
        |
        +---- Buddy execution
```

Cloudflare may cache or persist runtime state, but durable knowledge/decisions/project facts must ultimately be synchronized to the appropriate GitHub canonical location.

Never create a second independent Memory system in Cloudflare.

## 6. Task model

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

## 7. Identity and permissions

Every Agent has an explicit `agent_id` and capability boundary.

Default posture:
- GitHub: read
- Cloudflare: read
- external systems: read unless explicitly required
- Sandbox: disabled until needed

Write/deploy/delete/external side effects require an explicit capability grant and must be auditable.

## 8. Secrets

Secrets are runtime credentials, not Memory.

Never commit secrets, tokens, API keys or credentials into GitHub Memory or project Markdown.

Secrets must be injected through the appropriate runtime/local secret mechanism and exposed to the minimum component that needs them.

## 9. Free-first policy

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

## 10. Deployment phases

### P0 — Architecture
Status: ADOPTED

- responsibility boundaries
- canonical Memory rule
- identity/permissions model
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

## 11. Operational safety

The runtime must be designed so that Cloudflare failure does not destroy canonical project knowledge.

For every durable execution:
- runtime state may live in Cloudflare;
- canonical decision/result/artifact references return to GitHub;
- execution is auditable;
- unknown/conflicting facts are not silently promoted to canonical facts.

## 12. Anti-patterns

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

## 13. Decision

**ADOPTED:** Cloudflare is now part of the global Agent System architecture as the Cloud Runtime Layer.

The first implementation target is a Free-plan-compatible `core-agent`; paid compute is an escalation path, not a prerequisite.
