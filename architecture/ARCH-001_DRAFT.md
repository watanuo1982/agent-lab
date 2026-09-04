# ARCH-001 — Multi-Agent Operating Architecture v2 — Draft

> Status: **Working Draft / not frozen**
> Date: 2026-09-04
> Canonical workspace: `agent-lab`
> Related review Issue: #15

## 1. Purpose

Define a general operating architecture for Human + multiple AI agents + GitHub + runtime environments.

The architecture must support the user's actual working pattern rather than forcing agents into legacy roles.

The central idea is:

> **Agents can be peers in conversation while remaining asymmetric in capability, permission and authority. GitHub is the durable shared state; runtimes are execution substrates; Human retains ultimate authority.**

This document is a draft for multi-AI review. It is not yet a final specification.

## 2. System at a glance

```text
                              HUMAN
                    Goal / Judgment / Approval
                               |
          +--------------------+--------------------+
          |                    |                    |
       ChatGPT              Buddy              Other AI
     intelligence         full-end             specialized
      + review            operation              capability
          |                    |                    |
          +--------------------+--------------------+
                               |
                     Agent Collaboration Layer
                task / handoff / status / result / review
                               |
                               v
                    +----------------------+
                    |   GITHUB CONTROL /   |
                    |   CANONICAL STATE    |
                    +----------+-----------+
                               |
             +-----------------+------------------+
             |                                    |
             v                                    v
       PROJECT REPOS                         RUNTIME LAYER
  facts / artifacts / memory            Cloud / local / remote
       / decisions                      execution / automation
             |                                    |
             +-----------------+------------------+
                               v
                         Evidence / Logs
                               |
                               v
                    Verification / Review
                               |
                               v
                     State + Memory Update
```

## 3. Six layers

### L0 — Human layer

Human defines goals, priorities, strategic choices and final authority.

Human approval is required where the action is irreversible, high-impact, platform-sensitive, or explicitly reserved.

### L1 — Agent layer

ChatGPT, Buddy and other AIs are first-class participants.

First-class means an agent can, subject to its actual capabilities and permissions:
- receive work directly;
- reason and propose;
- communicate with Human and other agents through supported channels;
- execute available actions;
- produce evidence;
- review or challenge another agent's result.

First-class does **not** mean equal capability or equal authority.

### L2 — Collaboration / Protocol layer

Defines how agents cooperate:
- Task
- Handoff
- Status
- Result
- Evidence
- Review
- Disagreement
- Escalation
- Approval

GitHub Issues remain the default durable task contract; comments and commits provide execution/review evidence.

### L3 — Canonical State layer

GitHub is the durable shared state and control plane.

It contains, as appropriate:
- project context and state;
- tasks and acceptance criteria;
- artifacts;
- decisions;
- durable memory;
- provenance and evidence pointers;
- audit history.

No agent's private context is canonical.

### L4 — Runtime / Execution layer

Local machines, remote machines, Cloudflare and other runtime environments execute work.

Runtime may be persistent, event-driven, scheduled or manually invoked.

Runtime is not the source of truth.

### L5 — Evidence / Verification layer

Every material claim follows:

```text
Claim → Evidence → Verification → Canonical State
```

Examples of evidence:
- commit SHA;
- test output;
- deployment identifier;
- runtime logs;
- generated artifact;
- reproducible execution result.

A report saying “done” is a claim, not evidence.

## 4. Core distinctions

### Capability ≠ Permission

An agent may technically be able to perform an action without being authorized to perform it.

### Permission ≠ Authority

Permission to modify a repository does not automatically grant authority to redefine project policy or architecture.

### Authority ≠ Canonical ownership

An agent may make a decision within its scope, while the durable canonical representation belongs in GitHub.

### Conversational equality ≠ execution equality

All participating AIs may talk directly with Human, while Buddy may have substantially broader local/cloud/browser/deployment execution capabilities than another AI.

## 5. Proposed agent model

| Participant | Primary strength | Not assumed to own |
|---|---|---|
| Human | Goal, judgment, ultimate approval | — |
| ChatGPT | Research, synthesis, architecture, planning, review, supported execution | Human authority |
| Buddy | Full-end execution, environment operations, implementation, diagnosis, repair, direct conversation | Canonical truth / automatic architecture authority |
| Other AI | Domain-specific reasoning or execution according to its actual capability statement | Other agents' private state |

These are starting hypotheses only. Final roles must be derived from Round 1 capability statements.

## 6. Canonical state model

The system should have one durable state model rather than separate agent memories.

```text
Human intent
    ↓
Task / Decision
    ↓
Execution
    ↓
Artifact + Evidence
    ↓
Review
    ↓
Canonical State
    ↓
Memory / Next Work
```

Agents may keep temporary session/runtime state, but durable state must be promoted explicitly.

## 7. Task and handoff model

A durable task should minimally contain:

1. Objective
2. Scope / non-scope
3. Context pointers
4. Acceptance criteria
5. Expected artifact
6. Authority / permission constraints
7. Verification requirements
8. Reporting format
9. Current status

A handoff should point to the task and canonical state, not depend on hidden conversation history.

An agent may hand work directly to another agent if the task contract and permissions permit it.

## 8. Agent lifecycle

```text
Receive
  ↓
Understand
  ↓
Plan / Propose
  ↓
Execute (if authorized)
  ↓
Verify
  ↓
Report Evidence
  ↓
Review / Challenge
  ↓
Promote Canonical State
```

For known deterministic sequences, use workflows instead of unnecessary agent autonomy.

## 9. Disagreement model

Agents are allowed to disagree.

Disagreement must be represented explicitly rather than silently selecting one answer.

Minimum structure:

```text
Claim A
Evidence A

Claim B
Evidence B

Conflict / Unknown

Resolution owner
Resolution evidence
Final decision
```

Architecture conflicts ultimately escalate to Human unless authority has been explicitly delegated.

## 10. Failure and repair model

A capable agent may diagnose and repair failures **inside its already-authorized scope**.

It may not silently expand scope to fix a problem.

```text
Failure
  ↓
Diagnose
  ↓
Classify
  ├─ transient → retry within policy
  ├─ known repair → repair within scope
  ├─ evidence insufficient → investigate
  └─ authority/scope conflict → escalate
  ↓
Verify
  ↓
Report evidence
```

## 11. Memory integration

The existing GMR v0.2 model remains the baseline unless ARCH-001 explicitly supersedes a rule.

New multi-agent events should enter Memory only when they have durable future value and satisfy the existing promotion policy.

Examples:
- stable architecture decision → Decision / Global
- project execution result → Project State / Knowledge
- temporary agent conversation → Session only
- unresolved architectural conflict → Unknown

No agent automatically becomes the owner of Global Memory merely because it discovered or proposed something.

## 12. Git / Runtime boundary

GitHub owns durable truth.

Runtime owns execution state that is inherently operational and temporary, such as:
- process state;
- transient queues;
- logs before promotion;
- ephemeral files;
- runtime credentials and secrets.

When runtime work changes durable project state, it must produce evidence and promote the result back to Git.

If runtime disappears, the project should remain recoverable from Git to the maximum practical extent.

## 13. Invocation model

Invocation is a mechanism, not an architectural role.

Supported invocation sources may include:
- Human request;
- GitHub event/webhook;
- schedule;
- API;
- runtime event;
- direct agent action.

The architecture should not depend on one specific trigger mechanism.

## 14. Security and authority

Default rules:

1. No autonomous scope expansion.
2. Least authority, not least capability.
3. Read/write permissions are explicit where practical.
4. Cross-project writes require cross-project authority.
5. High-impact and irreversible actions require Human approval unless explicitly delegated.
6. Secrets remain in appropriate secret-management/runtime boundaries and are not copied into Git memory.
7. Agents must surface uncertainty and conflicts.

## 15. Replaceability tests

A healthy architecture should pass:

### Agent replacement
If ChatGPT is unavailable, another agent can recover from Git and continue.

If Buddy is unavailable, another execution-capable agent can continue from Git where tooling permits.

### Runtime replacement
If Cloudflare is unavailable, durable project state remains in Git and another runtime can be substituted where practical.

### Conversation replacement
A new session should recover the necessary state from canonical project/global memory without reconstructing hidden chat history.

## 16. Review and governance cycle

```text
Capability Statements
        ↓
Independent Architecture Proposals
        ↓
Cross-Agent Conflict Review
        ↓
Consolidated Draft
        ↓
Implementation Feasibility Review
        ↓
Human Approval
        ↓
Architecture Freeze
        ↓
Bounded Implementation Issues
        ↓
Pressure Tests
        ↓
Architecture Revision only when evidence requires it
```

## 17. Proposed repository organization

Keep the existing `agent-lab` structure minimal.

Potential architecture documents:

- `AI_OS_ARCHITECTURE.md` — current/frozen operating architecture
- `architecture/ARCH-001_DRAFT.md` — this review draft
- `AGENT_PROTOCOL.md` — finalized cross-agent interaction contract
- `CANONICAL_STATE_MODEL.md` — finalized state ownership model
- `EXECUTION_AUTHORITY.md` — capability / permission / authority rules
- `CLOUD_RUNTIME_ARCHITECTURE.md` — runtime boundary
- existing Memory documents — GMR and memory rules

Do not create these as final documents until review establishes that each is necessary.

## 18. Pressure-test projects

The architecture should be validated against at least:

- `-ai-content`: real Cloudflare + Git + AI workflow, including P04 end-to-end execution and review.
- `-quantitative-trading`: research workflow, data state, strategy decisions and execution boundaries.
- `-commercial-radar`: research/evidence workflow and cross-agent handoffs.

Tests should focus on actual failure modes rather than architectural completeness.

## 19. Current non-goals

Do not add:
- a new AI OS repository;
- a second task tracker;
- a vector/graph database merely for completeness;
- a mandatory orchestrator;
- automatic cross-project memory promotion;
- always-on agents without a demonstrated need;
- hidden agent-to-agent state outside canonical artifacts.

## 20. Open questions for Round 2

1. What exactly qualifies an agent as first-class?
2. Which agent actions may occur without Human confirmation?
3. Can agents delegate authority, or only work?
4. What minimum protocol is needed for direct agent-to-agent handoff?
5. Which runtime states must be persisted?
6. What evidence is sufficient for each class of claim?
7. When should disagreement block execution versus merely create an Unknown?
8. How should concurrent Git writes be coordinated?
9. Which existing GMR v0.2 rules need extension for multi-agent operation?
10. Which current project workflows should be used as acceptance tests?

## 21. Status

**Draft only.**

This document intentionally does not freeze the architecture. Round 1 capability statements and subsequent multi-AI review may change any section.
