# NEXT_WORK.md — Agent Hub

## Current priority

1. 验证并落地 GitHub Issue current-status Label；`STATUS:` 评论继续作为 audit log。
2. 增加 `PROJECTS.md` → GitHub repository existence/accessibility 一致性校验。
3. 首次确认 GitHub Actions 中 `memory-structure.yml` 实际通过。
4. 完成一次 canonical fact / reference drift review。

## P2（暂不工程化）

- External Memory：补齐 `source / retrieved_at / review_by` 后再考虑自动 freshness check。
- Concurrency：继续采用 Issue ownership + 避免同时修改同一 canonical file；暂不引入 distributed lock。

## Rules

- 不在本文件复制 Issue 正文；正式任务以 GitHub Issue 为准。
- 新治理任务先建 Issue，再通知 Buddy。
- Unknown 必须先进入 `UNKNOWN_REGISTRY.md`，Buddy 不自行裁决。
