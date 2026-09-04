# NEXT_WORK.md — Agent Hub

## Current priority

> **ARCH-001 已冻结（Issue #15 评论 5538205132，2026-09-04）。当前优先级 = 按冻结架构分阶段实施；GMR v0.2 不变，cold-start 验收仍是待办。**

1. ⏳ **ARCH-001-IMPL-01（Issue #23）：Phase A + Phase B** —— Hub 自身 canonical 收敛与协议对齐；完成后由 ChatGPT 做只读 Review。
2. ⬜ **Phase C（后续 Issue）**：逐项目审计（quantitative-trading 只读先行，V7.1 冻结管道不碰；commercial-radar 状态 [Unknown] 先盘点；ai-content；agent-runtime 跟踪 Project Memory PENDING → ADOPTED）。
3. ⬜ **Phase D（后续 Issue）**：治理加固与周期性 replaceability 测试；完整 Permission Governance 留到本阶段。
4. ⏳ **GMR v0.2 cold-start acceptance**：开启全新 Session，仅以 Git 为事实源验证恢复能力（冻结前遗留待办，继续有效）。

### 已完成基线（冻结前）

1. ✅ Issue status Label：已落地并验证。
2. ✅ `PROJECTS.md` remote existence/accessibility 校验：代码已实现；跨私有仓库 CI 仍需 `PROJECT_REGISTRY_TOKEN` 才能启用。
3. ✅ GitHub Actions memory structure validator：已实际成功运行，并已纳入 required check（M0）。
4. ✅ `PLAN_PROTOCOL.md`：已建立，确认计划成为受保护的 canonical project asset。
5. ✅ `SESSION_BOOTSTRAP.md`：已升级 v0.3，由 Universal Agent Contract 自动触发。
6. ✅ `AGENT_GIT_MEMORY_CONTRACT.md`：统一所有 Agent 的 Git Memory Mode、Project Bootstrap、Plan Continuity 与自动 Memory Sync。
7. ✅ GMR v0.2 Session Trigger Monitor / Promotion Policy：已实施（`MEMORY_PROTOCOL.md §13` 与 `MEMORY_MANIFEST.yaml`）。
8. ✅ ARCH-001 全流程（Round 2–5 → P0/M0/M5/M6 → Freeze Prep → Human Final Approval）完成，见 Issue #15。

## Current rule

Agent Hub 不保存业务项目的 Plan 正文；业务 Plan 必须留在对应 Project Repo。Hub 只负责全局 Memory / Plan / Session Bootstrap governance，以及跨项目任务指针。

## Rules

- 不在本文件复制 Issue 正文；正式任务以 GitHub Issue 为准。
- 新治理任务先建 Issue，再通知 Buddy；但 ChatGPT 自身直接实施 Memory Owner 变更时，不需要 Buddy 作为中介。
- Unknown 必须先进入 `UNKNOWN_REGISTRY.md`，Buddy 不自行裁决。
- Active Plan 不能被新 Session 静默替换；路线变化必须走 Change Proposal。
- **Human 不负责提醒 Agent 上传/同步记忆；durable change 发生后由 Agent 自动执行 Memory Sync Gate。**
- **每轮会话必须进行轻量 Trigger Scan；Trigger 只触发评估，不等于写入。**
- 没有 durable change 时，不制造无意义 memory commit。
