# AGENTS.md — Git Memory Runtime Bootstrap

> GMR v0.2 runtime entrypoint. This file is intentionally tiny; it is not a memory store.

## Mandatory behavior

1. If this repository or any registered project repository is read, enter **Git Memory Mode**.
2. Follow `AGENT_GIT_MEMORY_CONTRACT.md` for Global Bootstrap, Project Bootstrap, Plan Continuity, Trigger Monitor, and Memory Sync Gate.
3. Treat Git as canonical truth; do not use session/chat context to override Git facts.
4. During every conversation turn, perform a lightweight **Session Trigger Scan**. Strong triggers enter Memory Evaluation; triggers do not imply a write.
5. At work-unit/checkpoint boundaries, run the full Memory Sync Gate before returning the result.
6. ChatGPT is the Memory Owner when Git write access is available. Buddy is execution-only and is never required as a memory intermediary.
7. Project scope must be explicit. Never promote Project Memory to Global Memory automatically.
8. Never silently delete or overwrite core memory; use canonical-owner updates and `SUPERSEDE` history.
9. If an architectural conflict or unresolved canonical-memory conflict cannot be adjudicated, fail closed and record/route it as `[Unknown]` rather than guessing.

## Minimal startup

`检查 Git 的记忆` / `CHECK_GIT_MEMORY` → Global Bootstrap → identify project → Project Bootstrap → Plan Continuity Check → task resolution.
