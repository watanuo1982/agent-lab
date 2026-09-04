# Session Bootstrap Protocol（会话引导协议） v0.3

> 用途：每次开启新的 ChatGPT Session（ChatGPT 会话）时，自动从 Git/GitHub 恢复长期项目上下文，并保证已确认 Plan（计划）不因换 Session 而漂移。
>
> **统一 Agent 入口现在是 `architecture/AGENT_GIT_MEMORY_CONTRACT.md`。** 本文件负责 Session 恢复细则，不再要求 Human（人类）每次粘贴启动提示词。

## 1. 强制触发

只要发生以下任一情况，自动进入 Git Memory Mode（Git 记忆模式），并遵守 `architecture/AGENT_GIT_MEMORY_CONTRACT.md`：

- Human 说“检查 Git 的记忆”；
- Human 要求恢复/继续项目；
- Human 开始讨论一个已注册项目；
- 需要判断项目当前状态 / 当前任务 / 下一步；
- 创建、修改、关闭或通知执行 GitHub Issue（GitHub 议题）；
- 修改项目或 `agent-lab` 文件；
- 通知 Buddy（执行智能体）执行任务；
- Review（评审）Buddy 的 commit / research / content / experiment。

**Human 不需要提供启动文件清单。**

## 2. 极简启动方式

Human 可以只说：

> **检查 Git 的记忆。**

Agent 自动执行：

```text
读取 architecture/AGENT_GIT_MEMORY_CONTRACT.md
        ↓
Global Bootstrap（全局引导）
        ↓
识别当前项目（如尚未明确则等待）
        ↓
Project Bootstrap（项目引导）
        ↓
Plan Continuity Check（计划延续检查）
        ↓
Task Resolution（任务解析）
```

如果 Human 后续说“进入量化项目 / 回到 P03 / 继续商业雷达”等，Agent 不需要重新获得读取授权，直接进入对应 Project Bootstrap（项目引导）。

## 3. Global Bootstrap（全局引导）

由 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 规定统一入口与文件顺序。核心 Global 文件为：

1. `architecture/AGENT_GIT_MEMORY_CONTRACT.md`
2. `README.md`
3. `PROJECTS.md`
4. `CURRENT_STATE.md`
5. `NEXT_WORK.md`
6. `architecture/MEMORY_ARCHITECTURE.md`
7. `architecture/MEMORY_ROUTER.md`
8. `architecture/MEMORY_PROTOCOL.md`
9. `UNKNOWN_REGISTRY.md`
10. `architecture/SESSION_BOOTSTRAP.md`
11. `architecture/PLAN_PROTOCOL.md`

按需读取 `PROJECT_CONTEXT.md`、`INBOX.md`、`external/` 与相关历史。

## 4. Project Bootstrap（项目引导）

目标项目明确后，自动读取：

1. `README.md`
2. `PROJECT_CONTEXT.md`（如存在）
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. 唯一 Active Plan（激活计划，ACTIVE Plan）
6. `MEMORY_INDEX.md`（如存在）
7. `DECISIONS.md`（如存在）
8. `GITHUB_WORKFLOW.md`（如存在）
9. 当前阶段直接相关的 Issue / research / evidence / experiment

不要扫描整个仓库。

## 5. Plan Continuity（计划延续）

如果存在 `ACTIVE` / `APPROVED` Plan（激活/已批准计划），必须恢复：

```text
ACTIVE PLAN
PLAN ID
PLAN VERSION
PLAN STATUS
PLAN OBJECTIVE
CURRENT PHASE
CURRENT ISSUE
ISSUE STATUS
COMPLETED PLAN STEPS
CURRENT PLAN STEP
NEXT PLAN STEP
CHANGE PROPOSALS
LATEST RELEVANT COMMIT
KEY DECISIONS
OPEN UNKNOWNS
BUDDY STATUS
CONFLICTS
```

> 中文对照：需恢复的字段包括：激活计划、计划编号、版本、状态、目标、当前阶段、当前议题及议题状态、已完成与当前及下一步计划步骤、变更提案、最近相关提交、关键决策、未决未知项、执行体状态与冲突。

默认动作：**继续原 Plan（计划）。**

不得因为换 Session、时间间隔、Session memory（会话记忆）缺失或重新推理而静默重新规划。

Plan 变更必须遵守：

`Evidence（证据） → Evaluation（评估） → Change Proposal（变更提案） → Approval（批准） → New Plan Version（新计划版本）`

## 6. Task Resolution（任务解析）

GitHub Issue（GitHub 议题）是具体执行任务的唯一合同。

- `CURRENT_STATE.md`：状态
- `NEXT_WORK.md`：导航
- `BUDDY_TASK_CURRENT.md`：指针
- `INBOX.md`：通知指针
- Session memory（会话记忆） / 旧聊天：线索

它们都不能独立产生任务。

若发现 Plan / State / Issue / Next Work / Task Pointer 冲突：

> **MEMORY BOOTSTRAP BLOCKED**

不猜、不执行、不修改。

## 7. Memory Sync 是自动动作，不再依赖 Human 提醒

本文件与 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 一起规定：

> **任何 Agent 在产生 durable change（持久化变更）后，都必须自动运行 Memory Sync Gate（记忆同步闸门）。**

触发包括但不限于：

- 新长期事实；
- 新/改变的决策；
- 当前状态变化；
- Plan step（计划步骤）完成；
- Issue 创建/开始/完成/阻塞/验证/关闭；
- Buddy commit / push；
- ChatGPT Review（评审）；
- 新研究/实验结论；
- 新 Unknown（未知项） / 冲突；
- 协作规则变化。

Agent 必须自行判断并写回 canonical owner（规范归属方）；**Human 不需要提醒“上传记忆”。**

如果没有 durable change（持久化变更），则 `Memory Sync: NOT NEEDED`，避免制造垃圾提交。

如果 Agent 没有写权限，则必须输出 `MEMORY_SYNC_REQUIRED`，不得声称已同步。

记忆同步是每次产生持久化变更后的自动动作，由智能体自行判断是否写回规范归属方，无需人工提醒。

## 8. Session Recovery Card（会话恢复卡）

Bootstrap 完成后，在当前 Session（会话）内形成临时 Recovery Card（恢复卡）：

```text
PROJECT:
CURRENT STATE:
ACTIVE PLAN:
PLAN VERSION:
PLAN PHASE:
CURRENT TASK:
CURRENT ISSUE:
ISSUE STATUS:
LATEST RELEVANT COMMIT:
KEY DECISIONS:
OPEN UNKNOWNS:
BUDDY STATUS:
CURRENT PLAN STEP:
NEXT PLAN STEP:
CONFLICTS:
```

Recovery Card（恢复卡）默认不写回 Git；其 durable（持久）部分通过 Memory Sync Gate（记忆同步闸门）写入 canonical owner（规范归属方）。

## 9. Startup Report（启动报告）

向 Human 简要报告：

```text
Git Memory Bootstrap: OK / BLOCKED
Project: ...
Current State: ...
Active Plan: ...
Plan Version: ...
Plan Phase: ...
Current Task: ...
Issue: ...
Buddy: ...
Latest Commit: ...
Conflicts: none / ...
Next: ...
Memory Sync: DONE / NOT NEEDED / BLOCKED
```

> 中文对照：启动报告字段包括：引导结果（成功或受阻）、项目、当前状态、激活计划及其版本与阶段、当前任务、议题、执行体、最近提交、冲突、下一步，以及记忆同步结果（已完成 / 无需 / 受阻）。

若 BLOCKED，只报告冲突，不继续执行。

## 10. Cold-start acceptance（冷启动验收）

新 Session（会话）在不依赖旧聊天的情况下，至少恢复：

- 当前项目
- Active Plan（激活计划） + version
- Plan objective（计划目标）
- Current phase（当前阶段）
- Current Issue（当前议题） + status
- 已完成 Plan steps（计划步骤）
- 当前 Plan step（计划步骤）
- 下一 Plan step（计划步骤）
- 关键证据
- Open Unknowns（未决未知项）
- 是否存在冲突

并得到：

> **继续当前 Plan（计划） / 当前 Issue（议题），而不是重新制定计划。**

冷启动的目标是从 Git 恢复既有路线，而非凭空另起一套计划。

## 11. 旧启动提示词的兼容说明

历史上使用的长启动提示词仍然有效，但不再是必要条件。

**从 v0.3 开始，Human 只需“检查 Git 的记忆”；读取协议、项目识别、Plan continuity（计划延续）和 Memory Sync（记忆同步）都由统一 Agent Contract 自动触发。**

## 12. 与其他协议的关系

```text
architecture/AGENT_GIT_MEMORY_CONTRACT
        ↓
architecture/MEMORY_ARCHITECTURE
        ↓
architecture/MEMORY_ROUTER
        ↓
architecture/SESSION_BOOTSTRAP
        ↓
architecture/PLAN_PROTOCOL
        ↓
Project Memory + GitHub Issue
        ↓
Review
        ↓
Memory Sync
```

> 中文对照：链路为：统一契约 → 记忆架构 → 记忆路由 → 会话引导 → 计划协议 → 项目记忆与议题 → 评审 → 记忆同步。

`architecture/AGENT_GIT_MEMORY_CONTRACT.md` 是所有 Agent 的统一入口；本文件是 ChatGPT Session（ChatGPT 会话）恢复的专门协议。
