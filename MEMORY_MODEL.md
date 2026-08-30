# Memory Model v0.1 — Memory / Skill / Asset

> 2026-08-30. Global architecture decision distilled from Agent Skills research and `punk-ip-illustrations` / open Agent Skills patterns.

## 1. Core distinction

The agent operating system has three different concepts:

| Layer | Question | Meaning |
|---|---|---|
| **Memory** | “What do we know / decide?” | Durable facts, decisions, history, rules, context |
| **Skill** | “How do we do it?” | Triggered procedural capability: workflow, evidence, validation, handoff |
| **Asset** | “What should we reuse?” | Confirmed, versioned output or resource that future work should reference rather than recreate |

**Hard rule:** `Skill ≠ Memory ≠ Asset`.

## 2. Relationship

```text
                 Agent Operating Layer
                         │
              ┌──────────┴──────────┐
              │                     │
            SKILL                MEMORY
              │                     │
        “怎么做”                 “知道什么”
              │                     │
              └──────────┬──────────┘
                         ▼
                       ASSET
                         │
                 “复用什么成果”
```

A Skill may read Memory and reference Assets. A Memory record may point to an Asset or a Skill. An Asset is not itself a Skill merely because a Skill consumes it.

## 3. Memory

Canonical ownership remains defined by `MEMORY_ARCHITECTURE.md`:

- Global Memory → `agent-lab`
- Project Memory → project repository
- External Memory → `agent-lab/external/`
- Session Context → normally not persisted

Memory records the state of **our work**, not a copy of external documentation.

## 4. Skill

A Skill is a procedural package that changes agent behavior on a task.

Minimum conceptual contract:

```text
Identity
Trigger
Goal
Inputs
Procedure
Evidence
Validation
Failure
Handoff
Cost
Expected Benefit
Evaluation
```

Current Agent Skills conventions reinforce this separation: a Skill centers on `SKILL.md`, while scripts, references, and assets are loaded separately as needed through progressive disclosure. citeturn0search0turn0search5

A Skill should contain **process over knowledge**. Stable reference material, templates, and reusable files should not be duplicated into the procedural instructions when they can be loaded separately.

## 5. Asset

An Asset is a reusable artifact with an identity and lifecycle.

Examples:

- account/avatar/character identity
- brand rules or visual assets
- research schema or report template
- validated experiment protocol
- quantitative factor definition
- content template

Minimum conceptual contract:

```text
identity
 type
 owner_scope
 status
 version
 source
 created_at
 confirmed_at
 used_by
 supersedes
```

Recommended lifecycle:

```text
draft → review → confirmed → active → deprecated
```

Only `confirmed` / `active` Assets should normally be treated as canonical reusable inputs for production work.

## 6. Scope

### Global Assets

Only genuinely cross-project assets belong in `agent-lab`, e.g.:

- Skill Contract
- Evidence semantics
- cross-project review protocol
- collaboration templates

### Project Assets

Project-specific reusable assets stay in the owning project repository.

Examples:

- `ai-content`: account identity, visual identity, content templates
- `commercial-radar`: evidence schema, radar scoring model, validation protocol
- `quantitative-trading`: factor definitions, backtest protocol, experiment schemas

Do not move a project asset into Global merely because another project might someday reuse it. Promote it only after an explicit cross-project decision.

## 7. Provenance and status

An Asset must be distinguishable from an external suggestion.

- External source → `External Memory`
- Our assessment → `Memory`
- Adopted reusable artifact → `Asset`

Git history remains the final provenance layer. Do not silently replace a canonical Asset; supersede/version it.

## 8. Progressive disclosure principle

Do not load every Skill, Memory file, or Asset into context by default.

Current Agent Skills guidance uses progressive disclosure: catalog metadata first, full Skill instructions on activation, then references/scripts/assets only when required. This is explicitly intended to control context cost. citeturn0search0turn0search11

Our own implementation should follow the same principle at the architecture level:

```text
Need → route → load relevant Skill
     → read relevant Memory
     → load required Asset
     → execute
     → validate
     → record durable result
```

## 9. Decision status

This document defines a **Global architecture rule** for the agent-lab system.

It does not mean every project must immediately create an Asset directory or convert existing files. Existing project structures remain canonical until an explicit project-level decision changes them.

## 10. Research provenance

This model was distilled from:

- Agent Skills open specification / progressive disclosure patterns
- Anthropic/Microsoft-compatible Skill directory conventions
- `adrianpunk/punk-ip-illustrations`: persistent identity assets, confirmation state, reusable content assets, and delivery-aware generation
- the ongoing Skill Architecture Benchmark work in `agent-lab`

The external sources are evidence for the design; they are not themselves project facts. The adopted rule is the distinction defined in this file.
