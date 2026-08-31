# CURRENT_STATE.md — Agent Hub

> `agent-lab` 是 Global Memory / Agent Hub，不是普通业务项目；本文件记录 Hub 自身的当前治理状态。

## Current state

- **治理基线**：v0.1，Git-native、文件优先，无数据库/向量库/第二套任务系统。
- **Memory architecture**：四层模型已建立；`MEMORY_ARCHITECTURE.md` 定义模型，`MEMORY_ROUTER.md §1` 是唯一操作性路由规则源。
- **Unknown governance**：`UNKNOWN_REGISTRY.md` 是唯一登记与生命周期入口，支持 `OPEN / REVIEW_DUE / RESOLVED / RETAINED_UNKNOWN / ARCHIVED`。
- **Project registry**：`PROJECTS.md` 是跨项目注册表；业务项目的详细事实留在各自仓库。
- **Task protocol**：GitHub Issue 是正式任务载体；`STATUS:` 评论是审计日志，机器 current status 逐步迁移到 Label。
- **Control Tower**：设计存在，但实际建立状态仍由 U-A 管理，未裁决前不得猜测。
- **当前治理任务**：见 `agent-lab` Issue #4；本文件不复制 Issue 正文。

## Known open risks

1. GitHub Issue status Label 的实际落地能力仍需验证。
2. `PROJECTS.md` 与 GitHub repository 实际存在性的自动一致性校验需要补齐。
3. External Memory freshness 目前只有规则层要求，尚无自动检查。
4. 并发目前采用 Issue ownership + 避免同时修改同一 canonical file 的规则，暂不引入 distributed lock。

## Recovery path

新会话进入 Agent Hub 时，依次读取：

`README.md` → `PROJECTS.md` → `CURRENT_STATE.md` → `NEXT_WORK.md` → `MEMORY_ARCHITECTURE.md` / `MEMORY_ROUTER.md` → 目标仓库 Project Memory → 具体 Issue。
