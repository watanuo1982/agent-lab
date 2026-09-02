# CURRENT_STATE.md — Agent Hub

> `agent-lab` 是 Global Memory / Agent Hub，不是普通业务项目；本文件记录 Hub 自身的当前治理状态。

## Current state

- **治理基线**：v0.3，Git-native、文件优先，无数据库/向量库/第二套任务系统。
- **Universal Agent entrypoint**：`AGENT_GIT_MEMORY_CONTRACT.md` v1.0 已建立；所有读取本体系 Git/GitHub 的 Agent 都以它作为统一启动与记忆同步合同。
- **Memory architecture**：四层模型已建立；`MEMORY_ARCHITECTURE.md` 定义模型，`MEMORY_ROUTER.md §1` 是唯一操作性路由规则源。
- **Plan continuity**：`PLAN_PROTOCOL.md` 定义已确认计划的 canonical ownership、版本与变更控制；新 Session 默认继续 Active Plan。
- **Session bootstrap**：`SESSION_BOOTSTRAP.md` v0.3 已改为由 Universal Agent Contract 自动触发，不再要求 Human 粘贴启动提示词。
- **Automatic Memory Sync**：已正式纳入 Universal Agent Contract；产生 durable change 时 Agent 必须自动执行 Memory Sync Gate，并在需要时写回 canonical owner；无 durable change 则不产生无意义提交。
- **Unknown governance**：`UNKNOWN_REGISTRY.md` 是唯一登记与生命周期入口。
- **Project registry**：`PROJECTS.md` 是跨项目注册表；业务项目的详细事实留在各自仓库。
- **Task protocol**：GitHub Issue 是正式任务载体；`STATUS:` 评论是审计日志，机器 current status 使用 `status:*` Label。
- **Control Tower**：仍只作为设计概念，不在未裁决情况下猜测其实际建立状态。

## Governance status

- Issue #4：已完成并关闭；`status:verified`。
- Universal Git Memory Contract：v1.0 已落地。
- Current governance priority：以 quantitative-trading Active Plan + Issue #15 做真实新 Session cold-start 验收，并逐步把 canonical/reference drift 检查工程化。
- Quantitative Trading 当前已有明确 Active Plan 与唯一 current Issue；详见该项目仓库，不在本文件复制业务任务正文。

## Known open risks

1. Plan continuity 的跨仓库自动一致性检查尚未完全工程化。
2. `PROJECTS.md` 跨私有仓库 existence/accessibility 校验需要 `PROJECT_REGISTRY_TOKEN` 才能在 CI 实际执行。
3. External Memory freshness 目前只有规则层要求，尚无自动检查。
4. 并发目前采用 Issue ownership + 避免同时修改同一 canonical file；暂不引入 distributed lock。
5. **真实 cold-start 最终验收仍需 Human 在新 Session 触发；但启动动作本身已不再依赖 Human 提供长提示词。**

## Recovery path

新会话进入 Agent Hub 时，统一从：

`AGENT_GIT_MEMORY_CONTRACT.md` → Global Bootstrap → 项目识别 → Project Bootstrap → Active Plan → Issue → Review → Memory Sync

恢复。
