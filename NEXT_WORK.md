# NEXT_WORK.md — Agent Hub

## Current priority

> 2026-09-01 收口（agent-lab #4）。以下 1–3 已完成，仅 4 仍待办。

1. ✅ **验证并落地 GitHub Issue current-status Label** —— 实测 connector `issue_write(labels=[...])` 可写；#4 已由 `status:in-progress` 翻为 `status:done`，Issue 保持 OPEN。`STATUS:` 评论继续作为 audit log。
2. ✅ **`PROJECTS.md` → 仓库 existence/accessibility 校验** —— 已实现为 `scripts/validate_memory_structure.py::validate_project_registry_remote()`。**但为 opt-in**：需仓库配置 `PROJECT_REGISTRY_TOKEN` secret 才会在 CI 实际生效，当前 CI 输出 `WARN ... skipped`。**待 Human 添加该 secret 后自动启用。**
3. ✅ **首次确认 GitHub Actions 中 `memory-structure.yml` 实际通过** —— run #14 / job `99369272495`，HEAD `b1c5fa6`，`conclusion=success`；日志确认 Issue status 检查实际执行（未 skip），仅跨仓库检查按设计 skip。
4. ⬜ **完成一次 canonical fact / reference drift review** —— 待办；按本文件规则需**先建 Issue**，再通知 Buddy 执行。

## STATUS metadata — connector 能力实测结论（2026-09-01）

| 层 | 探测方式 | 结论 |
|---|---|---|
| Label（机器可查询 current status） | `issue_write(labels=[...])` 实测翻 #4 标签成功 | ✅ **已落地** |
| Project field | `list_issue_fields(agent-lab, #4)` 返回 `[]` | ⛔ **BLOCKED**：该 Issue 未挂载任何 Project 字段；与 #1 跨仓库 Projects v2 BLOCKED 结论一致。不引入第二套系统。 |
| `STATUS:` 评论 | `add_issue_comment` | ✅ 保留为 audit log |

状态语义约定：`status:done` = 已交付、等 ChatGPT Review；**不等于 Issue 关闭**，Issue 一律保持 OPEN 直至 Review。

## P2（暂不工程化）

- External Memory：补齐 `source / retrieved_at / review_by` 后再考虑自动 freshness check。
- Concurrency：继续采用 Issue ownership + 避免同时修改同一 canonical file；暂不引入 distributed lock。

## Rules

- 不在本文件复制 Issue 正文；正式任务以 GitHub Issue 为准。
- 新治理任务先建 Issue，再通知 Buddy。
- Unknown 必须先进入 `UNKNOWN_REGISTRY.md`，Buddy 不自行裁决。
