# Git-Native Project Memory Protocol

> P0 experiment, 2026-08-29. This protocol adapts ideas from current open-source agent-memory systems to the existing ChatGPT ↔ GitHub ↔ Work Buddy workflow.
>
> ## 归属说明（2026-08-30，agent-lab Issue #2）
>
> 本文件是 **P0 记忆协议草案**，**仍然有效**，保留其独有内容：§4 什么值得记、§5 记录语义、§6 写入时机、§10 P0 成功标准、§11 rollout、§12 设计参考。
>
> **四层记忆模型（Global / Project / External / Session）与路由规则的 canonical 归属是** `MEMORY_ARCHITECTURE.md` 与 `MEMORY_ROUTER.md`；本文件不再重复定义。
>
> ⚠️ **SUPERSEDED**：本文件 §2 只定义了 Global / Project 两层。External 与 Session 两层以 `MEMORY_ARCHITECTURE.md` §2.3 / §2.4 为准。
> §9 的仓库隔离原则仍有效，并由 `MEMORY_ARCHITECTURE.md` §4 的 canonical 表细化。

## 1. Purpose

GitHub is the durable source of truth for project state. Memory is not a copy of chat history. It is a curated, versioned representation of facts that must survive across conversations and agents.

The protocol is intentionally file-first and Git-native. No vector database, graph database, hosted memory service, or new runtime is required for P0.

**统一 Agent 入口与自动写回义务由 `AGENT_GIT_MEMORY_CONTRACT.md` 定义。** 本文件负责“什么值得记、如何记录、何时写回”等语义细则。

## 2. Scope model

### Global / Hub memory

`agent-lab` stores only cross-project knowledge:

- project registry and boundaries
- collaboration protocol
- cross-project coordination rules
- pointers to project state

It must not copy detailed business/project knowledge.

### Project memory

Each real project repository owns its own durable memory. The minimum canonical set is:

- `PROJECT_CONTEXT.md` — what the project is, boundaries, durable assumptions
- `CURRENT_STATE.md` — current state and verified facts
- `NEXT_WORK.md` — current priorities and next actions
- `DECISIONS.md` — important decisions and rationale
- `CHANGELOG.md` — chronological material changes

Existing project files with equivalent roles may be retained; do not create duplicate sources of truth merely to satisfy this protocol.

## 3. Memory hierarchy

Use a simple three-level model:

```text
ACTIVE MEMORY
  CURRENT_STATE.md + NEXT_WORK.md
  ↓ loaded first
PROJECT MEMORY
  PROJECT_CONTEXT.md + DECISIONS.md
  ↓ loaded when relevant
HISTORY / EVIDENCE
  CHANGELOG.md + tasks + reviews + experiments + code/data
  ↓ retrieved when needed
```

## 4. What deserves memory

Save a fact when at least one is true:

1. It changes how future work should be performed.
2. It explains a durable project decision.
3. It records a verified result that should not be rediscovered.
4. It defines a project boundary or invariant.
5. It records an unresolved issue that future work must account for.
6. It captures a reusable collaboration rule.

Do not save:

- ordinary conversation filler
- transient thoughts with no decision
- duplicate copies of source material
- secrets, credentials, tokens, or personal sensitive data

## 5. Memory record semantics

When practical, durable facts should carry:

- `date`: when the fact became relevant
- `status`: `active`, `superseded`, `blocked`, or `verified`
- `source`: issue / commit / file / experiment
- `confidence`: `high`, `medium`, or `low` when uncertainty matters

For changing facts, do not silently overwrite history. Mark the previous fact as superseded and record the new fact and reason.

## 6. Write policy — automatic, checkpoint-based

Memory is **not** a Human-reminder task.

The universal rule is defined by `AGENT_GIT_MEMORY_CONTRACT.md`:

> **Every Agent must automatically run Memory Sync Gate after meaningful durable change.**

The normal lifecycle is:

```text
Task / Research / Discussion
→ durable change detected?
→ route through MEMORY_ROUTER
→ write canonical owner
→ commit / Issue evidence
→ verify
```

### 6.1 Mandatory Memory Sync triggers

Run Memory Sync Gate after any of the following:

- durable fact established
- durable decision made/rejected
- project state changes
- Plan created/changed/completed
- Issue created/started/completed/blocked/verified/closed
- Buddy commit/push
- ChatGPT Review
- research or experiment reaches a reusable conclusion
- known fact is superseded by evidence
- new Unknown or contradiction
- collaboration protocol changes

### 6.2 No-op is valid

If the work unit produced no durable information, the Agent must explicitly treat the result as:

`Memory Sync: NOT NEEDED`

No meaningless commit should be created merely to prove that memory was checked.

### 6.3 Write authority

- **ChatGPT**: decides what is durable, routes it, writes canonical memory, and verifies the write.
- **Buddy**: writes directly verifiable execution facts in the project repo; reports commit/evidence; does not promote inference or alter Plan.
- **Read-only Agent**: must emit `MEMORY_SYNC_REQUIRED` when a write is needed and must not claim synchronization succeeded.

### 6.4 Research-only work

Not every durable conclusion requires a GitHub Issue or Work Buddy execution. When ChatGPT is only researching, comparing, evaluating, or designing a method—and no repository change or external execution is required—the work can remain ChatGPT-side until a durable conclusion is established.

Once the conclusion is durable, it must be routed into the appropriate Global / Project / External memory according to `MEMORY_ROUTER.md`. If it changes a project Plan, use the Plan change-control process; do not silently replace the route.

Create a Buddy task only when there is an actual executable repository/project change, experiment, or other auditable action for Buddy to perform.

## 7. Read policy

When entering a project, follow `AGENT_GIT_MEMORY_CONTRACT.md` for the mandatory bootstrap sequence.

The key principle remains selective loading:

1. Project context
2. Current state
3. Navigation
4. Active Plan
5. Relevant decisions
6. Current Issue
7. Relevant evidence / code / experiment history

Do not load the entire repository by default.

## 8. Agent responsibilities

### ChatGPT

- decides what is durable enough to remember
- reviews whether memory matches verified project reality
- resolves contradictions
- creates the next task when appropriate
- **automatically performs Memory Sync after durable changes**

### Work Buddy

- reads project memory before execution
- treats project memory as context, not as permission to invent requirements
- reports commit/result evidence
- may write execution-verifiable facts
- may propose memory updates
- **automatically performs Memory Sync after execution checkpoints**

### GitHub

- stores the durable artifact
- provides commit history and provenance
- is the source of truth when memory and conversation disagree

## 9. Project isolation

Memory is repository-scoped by default.

```text
agent-lab
  └── cross-project memory only

-quantitative-trading
  └── quantitative memory only

-ai-content
  └── content-project memory only

-commercial-radar
  └── commercial-radar memory only
```

Cross-project facts belong in `agent-lab` only when they genuinely concern the collaboration system or project portfolio. A business-project fact must remain in that business repository.

## 10. P0 success criteria

The protocol is considered successful if, after a fresh conversation:

- ChatGPT can reconstruct the project's current state from Git without relying on old chat history.
- Buddy can execute a new Issue using the same project context.
- A reviewer can distinguish current facts from superseded decisions.
- No second parallel task/knowledge system is introduced.
- The memory files remain small enough to inspect manually.
- **Human does not need to remind an Agent to synchronize durable memory.**

If these criteria fail at scale, then evaluate a retrieval layer such as QMD/vector search, Mem0, or Graphiti. Do not introduce those dependencies before the file-first baseline is measured.

## 11. P0 rollout

1. `agent-lab`: protocol definition and template — current step.
2. Validate the protocol on one project repository.
3. Apply the minimum required memory files to the remaining project repositories.
4. Run a cross-conversation recovery test.
5. Only then consider automated memory extraction/retrieval.

## 12. Design references

- Letta / MemFS: Git-backed Markdown memory, selective loading, versioned memory.
- Mem0: explicit memory extraction and scoped recall; useful later if manual memory curation becomes a bottleneck.
- Graphiti: temporal facts and provenance; useful later if project history becomes too complex for flat Markdown.
- Agent Memory Techniques: useful comparative map of memory patterns and evaluation approaches.

The objective is not to reproduce any framework. The objective is to adopt the smallest useful ideas while preserving the existing GitHub-native workflow.

## 13. GMR v0.2 — Session Trigger Monitor and Promotion Gate

> **Status: FROZEN / IMPLEMENTED 2026-09-02.** This section is the operational overlay for the runtime behavior agreed for GMR v0.2. It does not replace the four-layer ownership rules in `MEMORY_ARCHITECTURE.md` or the routing procedure in `MEMORY_ROUTER.md`.

### 13.1 Per-turn Trigger Scan

Every conversation turn receives a lightweight semantic scan. The scan is an evaluation step, not a Git write.

```text
Conversation turn
  ↓
Lightweight Trigger Scan
  ├─ no trigger → continue
  └─ trigger → Memory Evaluation
```

Strong triggers include:

- explicit durable decision/rule (`决定 / 以后 / 采用 / 不再 / 确定 / 作为标准`);
- reversal or supersession (`推翻 / 改成 / 刚才不对`);
- project state change (completed / failed / published / verified / restarted);
- stable definition or invariant established;
- new unresolved Unknown or conflict;
- durable workflow rule/preference;
- work-unit completion.

### 13.2 Full-check checkpoints

A full Memory Sync Gate is mandatory at these natural boundaries:

- work-unit completion;
- user confirmation of a conclusion;
- before handing work to Buddy;
- project/topic switch;
- session interruption or end.

### 13.3 Trigger is not Writeback

A trigger only starts Memory Evaluation. The evaluation must then apply the Durable Impact Test and `MEMORY_ROUTER.md` before any write.

```text
Trigger
  ↓
Durable Impact Test
  ↓
Classify: Fact / Decision / State / Knowledge / Unknown
  ↓
Route: task / project / global
  ↓
Promotion policy: L0 / L1 / L2 / L3
  ↓
CREATE / UPDATE / SUPERSEDE / RESOLVE
```

### 13.4 Durable Impact Test

Durable memory is justified only when failure to retain it could cause a future agent to make a wrong judgment, repeat completed work, or violate an established direction.

Observation ≠ Knowledge. Idea ≠ Decision. Candidate ≠ Durable Memory.

An assistant proposal does not become a durable decision merely because the assistant proposed it. User acceptance and/or evidence is required according to the risk level.

### 13.5 Promotion policy

| Level | Policy | Typical examples |
|---|---|---|
| L0 | No write | transient discussion, rejected ideas, one-off context |
| L1 | Auto write | low-risk state, next work, explicit experiment status/results |
| L2 | Proposal | reusable Knowledge, Decision, Supersede, Unknown resolution |
| L3 | Human confirmation | Global Memory, cross-project rules, major architecture/direction, conflict arbitration |

### 13.6 Scope and history guardrails

Every writeback has an explicit scope: `task | project | global`.

Project Memory never automatically promotes to Global Memory. Global Memory never silently mutates Project Memory.

Core memory has no DELETE transition. A changed fact is represented through `SUPERSEDE` with provenance and history retained. Repeated detection of the same fact must be idempotent and must not create duplicate canonical entries.

### 13.7 Runtime responsibility

**ChatGPT is the Memory Owner** when Git write access is available: it performs trigger evaluation, promotion judgment, routing, direct Git writeback, and post-write verification. Buddy remains execution-only and is not required as an intermediary for memory synchronization.

If ChatGPT lacks write access, it must emit `MEMORY_SYNC_REQUIRED` and must not claim that synchronization succeeded.

### 13.8 End-of-turn invariant

Before returning a final response after a durable change, ChatGPT must have completed the Memory Sync Gate. The response may report:

- `Memory Sync: DONE`
- `Memory Sync: NOT NEEDED`
- `Memory Sync: BLOCKED`

The goal is zero Human reminders for routine durable-memory synchronization.
