# Git-Native Project Memory Protocol

> P0 experiment, 2026-08-29. This protocol adapts ideas from current open-source agent-memory systems to the existing ChatGPT ↔ GitHub ↔ Work Buddy workflow.

## 1. Purpose

GitHub is the durable source of truth for project state. Memory is not a copy of chat history. It is a curated, versioned representation of facts that must survive across conversations and agents.

The protocol is intentionally file-first and Git-native. No vector database, graph database, hosted memory service, or new runtime is required for P0.

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

This follows the useful part of Letta's file-backed memory approach: keep a small active context while retaining deeper versioned memory outside the active context. Letta's current MemFS documentation explicitly uses Git-backed Markdown memory with a small always-loaded system layer and deeper reference memory. See: https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md

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

This borrows the temporal-awareness principle from Graphiti: facts can change, so memory should preserve when a fact was valid rather than pretending the latest value was always true.

## 6. Write policy

Memory is updated at meaningful checkpoints, not after every message.

Recommended checkpoint:

```text
Task proposed
→ execution
→ commit/result
→ ChatGPT review
→ VERIFIED / BLOCKED
→ update project memory
```

The final verified result is the strongest candidate for `CURRENT_STATE.md` or `DECISIONS.md`.

## 7. Read policy

When entering a project, read in this order:

1. `PROJECT_CONTEXT.md`
2. `CURRENT_STATE.md`
3. `NEXT_WORK.md`
4. relevant `DECISIONS.md`
5. current Issue
6. relevant evidence / code / experiment history

Do not load the entire repository by default.

Search/retrieval should be selective. A filesystem-first approach is deliberate: current agent-memory research shows that searchable Markdown/Git can be a strong baseline and is easier to inspect, diff, and recover than opaque vector-only memory.

## 8. Agent responsibilities

### ChatGPT

- decides what is durable enough to remember
- reviews whether memory matches verified project reality
- resolves contradictions
- creates the next task when appropriate

### Work Buddy

- reads project memory before execution
- treats project memory as context, not as permission to invent requirements
- reports commit/result evidence
- may propose memory updates, but verified project state takes precedence

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
