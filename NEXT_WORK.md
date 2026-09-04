# NEXT_WORK.md — Agent Hub

## 当前优先级

> **ARCH-001 已冻结；Phase D 治理加固已于 2026-09-04 全部 VERIFIED 收口（D-6 判定 PASS，Issue #40）。当前优先级 = 转回业务项目执行；架构治理进入稳态维护，仅在新执行实例 / 新仓库 / token 轮换 / 漂移迹象时重启。**

1. ⏳ **GMR v0.2 cold-start acceptance（Issue #14）**：开启全新 Session，仅以 Git 为事实源验证恢复能力——Hub 层唯一遗留待办。
2. ✅ **ARCH-001-IMPL-01（Issue #23）Phase A + Phase B**：完成并 VERIFIED。
3. ✅ **Phase C 核心目标**：由 D-3（Issue #35）与 D-5（Issue #39）覆盖，不再单独立项。
4. ✅ **Phase D（D-2 ~ D-6，Issue #29/#35/#37/#39/#40）**：身份分离、状态统一、权限收敛、定位确认全部 VERIFIED / DONE。
5. 🔧 **顺手项（不立项，随各仓正常任务执行）**：`-agent-runtime` 8 个 open issues 补 `status:*` 标签；消化三业务仓约 24 个 done-but-open 的 Review 积压；`-agent-runtime` 过期 task-state 副本（BUDDY_TASK_CURRENT.md 等）归档。
6. 📅 **日历项**：fine-grained PAT 约 2026-12-03 到期，轮换后更新 `architecture/IDENTITY_TOKEN_POLICY.md`。

### 已完成基线（冻结前）

1. ✅ Issue status Label：已落地并验证。
2. ✅ `PROJECTS.md` remote existence/accessibility 校验：代码已实现；跨私有仓库 CI 仍需 `PROJECT_REGISTRY_TOKEN` 才能启用。
3. ✅ GitHub Actions memory structure validator：已实际成功运行，并已纳入 required check（M0）。
4. ✅ `architecture/PLAN_PROTOCOL.md`：已建立，确认计划成为受保护的 canonical project asset。
5. ✅ `architecture/SESSION_BOOTSTRAP.md`：已升级 v0.3，由 Universal Agent Contract 自动触发。
6. ✅ `architecture/AGENT_GIT_MEMORY_CONTRACT.md`：统一所有 Agent 的 Git Memory Mode、Project Bootstrap、Plan Continuity 与自动 Memory Sync。
7. ✅ GMR v0.2 Session Trigger Monitor / Promotion Policy：已实施（`architecture/MEMORY_PROTOCOL.md` §13 与 `MEMORY_MANIFEST.yaml`）。
8. ✅ ARCH-001 全流程（Round 2–5 → P0/M0/M5/M6 → Freeze Prep → Human Final Approval）完成，见 Issue #15。

## 当前规则

Agent Hub 不保存业务项目的 Plan 正文；业务 Plan 必须留在对应 Project Repo。Hub 只负责全局 Memory / Plan / Session Bootstrap governance，以及跨项目任务指针。

## 规则

- 不在本文件复制 Issue 正文；正式任务以 GitHub Issue 为准。
- 新治理任务先建 Issue，再通知 Buddy；但 ChatGPT 自身直接实施 Memory Owner 变更时，不需要 Buddy 作为中介。
- Unknown 必须先进入 `UNKNOWN_REGISTRY.md`，Buddy 不自行裁决。
- Active Plan 不能被新 Session 静默替换；路线变化必须走 Change Proposal。
- **Human 不负责提醒 Agent 上传/同步记忆；durable change 发生后由 Agent 自动执行 Memory Sync Gate。**
- **每轮会话必须进行轻量 Trigger Scan；Trigger 只触发评估，不等于写入。**
- 没有 durable change 时，不制造无意义 memory commit。

