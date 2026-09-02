# NEXT_WORK.md — Agent Hub

## Current priority

> Plan Continuity + Session Bootstrap 已落地到 v0.2；当前进入真实 cold-start 验收与 consistency validator 的工程化准备。

1. ✅ Issue status Label：已落地并验证。
2. ✅ `PROJECTS.md` remote existence/accessibility 校验：代码已实现；跨私有仓库 CI 仍需 `PROJECT_REGISTRY_TOKEN` 才能启用。
3. ✅ GitHub Actions memory structure validator：已实际成功运行。
4. ✅ `PLAN_PROTOCOL.md`：已建立，确认计划成为受保护的 canonical project asset。
5. ✅ `SESSION_BOOTSTRAP.md`：已升级 v0.2，强制恢复 Active Plan / Plan version / phase / Issue。
6. ⏳ **Cold-start acceptance：以 quantitative-trading Active Plan + Issue #15 作为真实样例；Human 在新 Session 最终验收。**
7. ⬜ 后续：把 Plan/Current State/Issue/NEXT_WORK pointer 的一致性检查进一步工程化。

## Current rule

Agent Hub 不保存业务项目的 Plan 正文；业务 Plan 必须留在对应 Project Repo。Hub 只负责全局 Memory / Plan / Session Bootstrap governance，以及跨项目任务指针。

## Rules

- 不在本文件复制 Issue 正文；正式任务以 GitHub Issue 为准。
- 新治理任务先建 Issue，再通知 Buddy。
- Unknown 必须先进入 `UNKNOWN_REGISTRY.md`，Buddy 不自行裁决。
- Active Plan 不能被新 Session 静默替换；路线变化必须走 Change Proposal。
