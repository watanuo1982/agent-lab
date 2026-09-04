# AI OS Architecture v1.0

> Status: Drafted from architecture audit, 2026-08-30
> Canonical owner: `agent-lab`
> Scope: Cross-project AI working system for Human + ChatGPT + WorkBuddy/Codex + GitHub
>
> **与 ARCH-001 的关系（2026-09-04 起）**：全局架构的 canonical baseline 是已冻结的 `ARCH-001_FINAL_ARCHITECTURE.md`（Human 批准，Issue #15 评论 5538205132）。本文件保留为冻结前的系统描述与行业对齐参考；凡与 ARCH-001 冲突之处（权威模型、层结构），以 ARCH-001 为准——ARCH-001 定义了本文件未覆盖的 Runtime 层与 Evidence/Verification 层（见 `CLOUD_RUNTIME_ARCHITECTURE.md`），并统一 `DONE`/`VERIFIED` 完成语义。

## 1. Purpose

This document defines the architecture of the existing AI working system. It does **not** introduce a new product, repository, memory service, vector database, or agent runtime.

The design principle is:

> **GitHub is the durable project state; agents are replaceable workers; Human remains the authority for goals, high-impact decisions and approvals.**

The architecture must remain useful even if models, agents, connectors, or runtimes change.

## 2. System model

```text
                         HUMAN
                   Goals / Judgment
                         |
                         v
                  +-------------+
                  |  Reasoning  |
                  |  ChatGPT    |
                  +------+------+ 
                         |
              Context / Task / Review
                         |
                         v
                  +-------------+
                  |  agent-lab  |
                  | Control Hub |
                  +------+------+ 
                         |
                    GitHub state
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      Quant          AI Content      Commercial Radar
        |                |                |
        +----------------+----------------+
                         |
                    Agent Workers
                  WorkBuddy / Codex / other
                         |
                    Tools / Skills
                         |
                       Action
                         |
                      Artifact
                         |
                       Review
                         |
                     Decision
                         |
                       Memory
```

## 3. Ten core objects

| Object | Meaning | Canonical home |
|---|---|---|
| Goal | What Human is trying to achieve | Human / Global or Project context |
| Context | Information required for the current run | Session + Project/Global memory |
| Task | A bounded unit of work with acceptance criteria | GitHub Issue |
| Agent | A worker capable of reasoning/execution | ChatGPT / WorkBuddy / Codex / future agents |
| Tool | An external capability invoked by an agent | Connector / MCP / API / local tool |
| Skill | Reusable procedure for a class of work | Project docs / agent skills |
| Permission | What an agent is allowed to read/write/do | Tool/account/repository boundary |
| Artifact | Durable output of work | Project repository |
| Review | Human/agent verification of an artifact or result | Issue / review artifact |
| Decision | A durable judgment that changes future work | `DECISIONS.md` or Hub decision record |

## 4. Memory OS and Agent OS are separate

### Memory OS

The existing four-layer model remains canonical:

```text
Global / agent-lab
Project / project repository
External / external knowledge pointers
Session / temporary context, default not persisted
```

See `MEMORY_ARCHITECTURE.md` and `MEMORY_ROUTER.md`.

### Agent OS

The execution lifecycle is:

```text
Goal
 -> Context
 -> Task
 -> Agent
 -> Tool/Skill
 -> Action
 -> Artifact
 -> Review
 -> Decision
 -> Memory
```

Memory is therefore an output of reviewed work, not an automatic transcript dump.

## 5. Canonical ownership

- Cross-project operating rules belong in `agent-lab`.
- Project facts, research, experiments and decisions belong in the relevant project repository.
- External facts remain external references until we independently adopt a judgment or decision.
- Current executable work belongs in GitHub Issues.
- Git history is the final historical record.
- Chat/session history is not a canonical project database.

No second task system should be introduced.

## 6. Task contract

A task should be executable by another agent without reconstructing the whole conversation. At minimum it should identify:

1. Objective
2. Scope / non-scope
3. Relevant context pointers
4. Acceptance criteria
5. Expected artifact
6. Permission/safety constraints where relevant
7. Reporting format
8. Current status

The task should point to canonical files rather than copy their contents.

## 7. Agent role separation

Current preferred division:

- **Human**: goals, strategic choices, irreversible/high-impact approval, platform-native actions where automation is unsafe.
- **ChatGPT**: research, synthesis, architecture, task decomposition, review and cross-project reasoning.
- **WorkBuddy**: repository-local execution and implementation under the task contract.
- **Codex/other coding agents**: coding-heavy execution when appropriate.
- **GitHub**: durable state, task contracts, artifacts, history and audit trail.

**Authority model (aligned with frozen ARCH-001 §3)**: Human is the sole final authority; agents are authority-peers with asymmetric capabilities — no agent commands another (cross-agent interaction is request / assign / accept); authority is never transferred transitively (an executor cannot grant another executor permissions it does not possess). Replacing an agent must not require migrating the project's memory into that agent.

## 8. Workflow vs Agent

Prefer deterministic workflows when the sequence and acceptance criteria are known.

Use an agent when the path requires dynamic exploration, judgment, tool selection, or adaptation.

Examples:

- Quant backtests and fixed research protocols: workflow-first.
- AI content production pipeline: workflow-first with agent assistance.
- Commercial Radar opportunity discovery: agent-heavy exploration followed by deterministic evidence gates.

Do not agentize a task merely because an agent can perform it.

## 9. Memory write policy

The current `agent-lab` memory model remains intentionally conservative.

```text
Session observation
      |
      v
Candidate knowledge
      |
   classify
      |
+-----+-------------------+
|                         |
No future value          Future value
|                         |
Discard                   route
                          |
              +-----------+-----------+
              |           |           |
           Global      Project     External
```

A durable memory candidate should have:

- provenance/source;
- clear ownership;
- a reason it matters in future work;
- status/evidence semantics where relevant;
- supersession handling if it can become stale.

External content is never promoted merely because an agent repeated it.

## 10. Governance and permissions

Minimum rule set:

1. Read scope should be no broader than required for the task.
2. Write scope should normally be limited to the target repository.
3. Cross-project changes belong in `agent-lab` only when they change shared infrastructure or cross-project coordination.
4. Human approval is required for irreversible/high-impact actions and platform actions with known safety boundaries.
5. Agents must report commit/artifact identifiers for durable work.
6. Unknown or conflicting state must be surfaced, not guessed.

## 11. Provenance and trust

Every durable claim should be traceable to one of:

- Human instruction;
- project artifact / commit / Issue;
- external primary source;
- explicitly labeled inference/assumption/experiment.

Use the existing evidence vocabulary where applicable:

`[Fact]`, `[Inference]`, `[Assumption]`, `[Experiment]`, `[Unknown]`.

External information may inform a decision but is not automatically a project fact.

## 12. Review and evaluation

Review is part of the architecture, not an optional final step.

For agent work, evaluate at least:

- Did it solve the stated task?
- Did it respect scope?
- Did it modify the correct canonical files?
- Did it preserve project boundaries?
- Is the result reproducible/auditable?
- Should any decision or lesson be promoted to durable memory?

The system should eventually record lightweight evaluation results, but **no separate observability stack is required at v1**.

## 13. Industry alignment — what we adopt

Current external designs reinforce several principles:

- OpenClaw separates curated long-term memory from episodic material, treats writing/provenance as the security boundary, and uses deterministic gates around model judgment. We adopt the principles, not its runtime or storage stack.
- OpenAI Agents SDK separates conversational Session state from longer-lived memory and provides agents, tools, handoffs, guardrails, human-in-the-loop and tracing as runtime primitives.
- MCP is evolving toward a more stateless protocol core, explicit Tasks, stronger authorization and routing. We treat MCP as a tool integration boundary, not as our memory or project-state system.

References checked 2026-08-30:
- OpenClaw memory architecture: https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory-architecture.md
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK Sessions: https://openai.github.io/openai-agents-js/guides/sessions/
- MCP 2026-07-28 specification announcement: https://blog.modelcontextprotocol.io/posts/2026-07-28/

## 14. Deliberate non-goals for v1

Do **not** add any of the following solely to make the architecture look more advanced:

- Mem0 or another external memory service
- vector database / graph database
- a second task tracker
- a new AI-OS repository
- autonomous memory promotion
- always-on autonomous agents
- automatic cross-project writes
- a central copy of every conversation
- a mandatory OpenClaw runtime

These may become appropriate only when a concrete workload demonstrates a failure that the current architecture cannot solve.

## 15. Pressure-test criteria

The architecture is considered healthy if these three projects can operate simultaneously without state leakage:

### Quantitative Trading

Research state, strategy parameters, experiments and trading decisions remain inside `-quantitative-trading`. Cross-project AI OS rules remain in `agent-lab`.

### AI Content

Content assets, platform experiments, publishing state and safety boundaries remain inside `-ai-content`. Human-only platform actions remain explicit.

### Commercial Radar

Opportunity evidence, scoring, experiments and business validation remain inside `-commercial-radar`. External market knowledge is referenced, not silently converted into project fact.

Pass condition:

> A new agent can enter any one project by reading the canonical recovery path, execute a bounded Issue, produce a durable artifact, and report back without needing hidden ChatGPT history and without changing another project's state.

## 16. Next audit targets

The architecture is intentionally v1. The next work should test, rather than expand, the system:

1. Cross-project task handoff through `agent-lab`.
2. Agent replacement: WorkBuddy unavailable → another worker can resume from GitHub.
3. Cold-start recovery: new session → canonical project state recovered without chat history.
4. Memory promotion: useful decision/lesson is promoted only after review.
5. Permission boundary: project-local worker cannot accidentally rewrite another project.
6. Conflict handling: contradictory state is surfaced as `[Unknown]` until resolved.

Only failures from these tests should generate v1.1 changes.
