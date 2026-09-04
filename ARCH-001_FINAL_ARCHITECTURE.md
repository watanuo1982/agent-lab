<!--
CANONICAL FILE — ARCH-001 Final Architecture Candidate.
Transcribed verbatim (no content changes) from watanuo1982/agent-lab#15, comment 5537869348,
by buddy-local per the Buddy Review Task (comment 5537871089).
Status: CANDIDATE — NOT FROZEN. Architecture freeze requires explicit Human approval in Issue #15.
Any edit to this file must go through the normal PR path with required check `validate-memory`.
-->

# ARCH-001 Round 5｜Final Architecture Candidate + Adjustment Plan

> Status: **CANDIDATE — pending Buddy review and Human final approval**
> This comment is the canonical design input for the next implementation/review step. It does **not** itself freeze the architecture.

## 1. Core architecture

The system is divided into five responsibilities:

- **Human** — final authority; defines intent, approves architecture changes and high-risk/irreversible actions.
- **Agent** — intelligence; reasoning, planning, analysis, proposal, review, challenge and decision support. Agents are authority-peers with asymmetric capabilities.
- **GitHub** — canonical state + governance plane; durable task/state/decision/memory/artifact/evidence/provenance and enforceable repository rules.
- **Runtime** — execution plane; Local Runtime, Cloudflare CoreAgent/Runtime, or another authorized runtime executes bounded work and produces execution evidence.
- **Evidence / Verification** — proof layer; runtime/CI/tooling produces evidence, independent verification evaluates it, then canonical state is promoted.

Non-negotiable:

`Capability ≠ Permission ≠ Authority ≠ Canonical Ownership`

`Agent ≠ Runtime`; `Runtime ≠ Truth`; `Agent claim ≠ Evidence`.

## 2. Target architecture

```text
                         HUMAN
                 Final Authority / Approval
                           │
                           ▼
                  ┌─────────────────┐
                  │   AGENT LAYER   │
                  │ ChatGPT / Other │
                  │ Reason / Plan / │
                  │ Review / Challenge
                  └────────┬────────┘
                           │ Work Contract
                           ▼
              ┌───────────────────────────┐
              │     GITHUB CANONICAL      │
              │ Task / State / Decision   │
              │ Memory / Artifact / Rules │
              │ Provenance / Evidence     │
              └────────────┬──────────────┘
                           │ authorized scope
                  ┌────────┴────────┐
                  ▼                 ▼
           Local Runtime      Cloudflare CoreAgent
                  │                 │
                  └────────┬────────┘
                           ▼
                 Execution + Evidence
                           │
                           ▼
                 Machine Verification
                           │
                           ▼
                 Independent Agent Review
                           │
                ┌──────────┴──────────┐
                │                     │
             accepted              rejected
                │                     │
                ▼                     ▼
       Canonical State          correction / retry
                │
                ▼
          Memory Promotion
             (GMR v0.2)
```

## 3. Authority model

- Human has final decision authority.
- Agents do not command one another.
- Authority is never transferred transitively: an executor cannot grant another executor permissions it does not possess.
- GitHub is the canonical record/enforcement surface, not a semantic decision-maker.
- Runtime has execution authority only within an explicit Work Contract.

## 4. Work Contract / Issue-first

The current **Issue-first** workflow remains the task carrier because it is already operational.

Minimum contract:

- `task_id`
- objective
- acceptance criteria
- `scope`
- `non_scope`
- `stop_condition`
- `not_authorized_to_decide`
- `target_repo`
- `capability_manifest_ref`
- authorized executor/runtime
- required evidence
- approval requirement
- carrier = GitHub Issue

No silent scope expansion. Missing authorization/ambiguous conditions become `Blocked` / `[Unknown]`.

## 5. Execution / Runtime boundary

Buddy Local is an execution body dependent on its local machine and is not assumed to have production SLA.

Cloudflare CoreAgent/Runtime is the cloud execution infrastructure; its deployed/running status is an established baseline and is not re-verified as part of every architecture task.

Runtime state is ephemeral. Critical workflow state must not exist only in agent/session/runtime context; durable state returns to GitHub.

## 6. Evidence-first

Every executable task produces an Execution Receipt conforming to `EXECUTION_RECEIPT.md`:

`task_id / executor / execution_id / timestamp / commit_sha / artifact / artifact_hash / exit_status / environment / produced_by`

`agent-declared` is claim-level evidence only and cannot alone satisfy DoD.

Completion semantics:

```text
DONE     = executor claim
VERIFIED = machine verification
           ∧ independent/non-executor review
           ∧ required Human approval
           ∧ canonical state promotion
```

Execution success, artifact correctness and architecture correctness remain separate judgments.

## 7. Governance

GitHub should mechanically reject what it can reject:

1. protected canonical branch
2. CODEOWNERS where ownership boundaries matter
3. required validator checks
4. structured Issue/Work Contract requirements
5. fail-closed canonical invariants
6. no normal agent bypass path

GitHub enforces structure; agents evaluate meaning; Human decides high-risk/irreversible matters.

## 8. Identity / Permission

Minimum architectural requirement:

- Buddy Local and Buddy Cloud/CoreAgent must be independently identifiable.
- They must not share an unaccountable high-privilege identity.
- Credentials should be repository/project scoped and least-privilege.
- Secrets never enter Issues, commits or durable memory.
- Full permission governance (matrix, lifecycle, rotation, revocation and approval boundaries) is a later governance round, not a blocker to architecture freeze if identity separation is already evidenced.

## 9. Agent-to-Agent interaction

```text
REQUEST → ACCEPT → EXECUTE → REPORT
                         ↓
                      EVIDENCE
                         ↓
                     REVIEW
                   ↙         ↘
                ACCEPT       REJECT
                  ↓             ↓
              PROMOTE       CORRECT/RETRY
```

Agents communicate through canonical work state, not hidden memory. Disagreement remains explicit until resolved by evidence, review or Human decision.

Fast Path may generate candidate reasoning/checks; only the Slow Path may change canonical state. Material Fast Path results must be promoted before task closure.

## 10. Memory / GMR v0.2

GMR v0.2 remains unchanged.

Layers:

- Session State — disposable agent-local context
- Task State — current Work Contract/execution
- Project State — repository-scoped durable state
- Global Memory — governed cross-project memory
- Historical Evidence — auditable execution record

Project isolation remains repository/domain + existing memory routing. ARCH-001 does not create a second memory system.

## 11. Replaceability / recovery

The stable interfaces are:

`Work Contract + Canonical State + Evidence Contract + Memory Contract + Authorization Boundary`

If Buddy Local disappears, another authorized executor can resume from GitHub. If Cloudflare CoreAgent disappears, another authorized runtime can take over. If ChatGPT disappears, another reasoning agent can consume canonical state.

Replaceability must be periodically tested, not merely documented.

## 12. Concurrency / minimality

Current scale does not justify a new orchestrator, queue or database.

Use task-level serialization where necessary, optimistic Git concurrency, explicit conflict/Blocked states, short-lived execution and canonical writeback.

Do not add infrastructure unless measured operational evidence proves GitHub-native coordination insufficient.

---

# ARCH-001｜Implementation / Adjustment Plan

The architecture is now a **target model**. Implementation must be staged and bounded.

### Phase A — agent-lab canonicalization

1. Replace the obsolete ARCH-001 Issue body phase text with the final architecture status after Human approval.
2. Add the final architecture as a canonical repository document.
3. Add a concise implementation map linking governance, receipt, identity, memory and runtime documents.
4. Keep GMR v0.2 unchanged unless a separate explicit decision supersedes a specific rule.

### Phase B — protocol alignment

5. Align `AGENTS.md`, `AI_OS_ARCHITECTURE.md`, `CLOUD_RUNTIME_ARCHITECTURE.md`, `AGENT_GIT_MEMORY_CONTRACT.md`, `PLAN_PROTOCOL.md`, `CURRENT_STATE.md`, `NEXT_WORK.md` with the frozen architecture.
6. Remove obsolete role/flow descriptions rather than maintaining parallel competing models.
7. Make Issue-first + Work Contract + Evidence Receipt the single normal task lifecycle.

### Phase C — project integration

For each active project repo (quantitative-trading, AI-content, commercial-radar and other active projects):

8. Audit the project against the frozen role boundary and GitHub workflow.
9. Add only the minimum required project-local contract/state files.
10. Preserve project isolation; do not copy global memory into project repositories.
11. Do not alter production logic merely for architectural conformity unless the project audit identifies a concrete violation.

### Phase D — governance hardening

12. Conduct a dedicated permission-governance round: permission matrix, token lifecycle, rotation/revocation, project scope and Human approval boundaries.
13. Keep identity attribution and least privilege as mandatory baseline.
14. Periodically run replaceability / handoff tests.

### Phase E — closeout

15. Verify canonical state, evidence and project migration status.
16. Close ARCH-001 only after Human approval and architecture freeze; subsequent work becomes bounded implementation Issues.

## 13. Explicitly deferred

- New database / queue / orchestrator
- Second task system
- New AI OS repository
- Vector/graph memory system
- Global chat archival
- Full permission-governance redesign before freeze
- Re-deployment/re-validation of already-running Cloudflare CoreAgent

## 14. Current acceptance state

Already evidenced before this candidate:

- P0 Validator repair + M2 Execution Receipt
- M0 GitHub governance foundation
- M5 Local ↔ Cloudflare CoreAgent cross-runtime handoff
- M6 execution identity separation
- GMR v0.2 retained

Remaining gate:

**Buddy reviews this exact candidate architecture + adjustment plan. Any conflict must be recorded explicitly. After review, Human makes the final approval. Only then do we freeze and execute Phase A–E.**