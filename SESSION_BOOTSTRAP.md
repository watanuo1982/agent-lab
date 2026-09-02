# Session Bootstrap Protocol v0.3

> 用途：每次开启新的 ChatGPT 会话时，自动从 Git/GitHub 恢复长期项目上下文，并保证已确认 Plan 不因换 Session 而漂移。
>
> **统一 Agent 入口现在是 `AGENT_GIT_MEMORY_CONTRACT.md`。** 本文件负责 Session 恢复细则，不再要求 Human 每次粘贴启动提示词。

## 1. 强制触发

只要发生以下任一情况，自动进入 Git Memory Mode，并遵守 `AGENT_GIT_MEMORY_CONTRACT.md`：

- Human 说“检查 Git 的记忆”；
- Human 要求恢复/继续项目；
- Human 开始讨论一个已注册项目；
- 需要判断项目当前状态 / 当前任务 / 下一步；
- 创建、修改、关闭或通知执行 GitHub Issue；
- 修改项目或 `agent-lab` 文件；
- 通知 Buddy 执行任务；
- Review Buddy 的 commit / research / content / experiment。

**Human 不需要提供启动文件清单。**

## 2. 极简启动方式

Human 可以只说：

> **检查 Git 的记忆。**

Agent 自动执行：

```text
读取 AGENT_GIT_MEMORY_CONTRACT.md
        ↓
Global Bootstrap
        ↓
识别当前项目（如尚未明确则等待）
        ↓
Project Bootstrap
        ↓
Plan Continuity Check
        ↓
Task Resolution
```

如果 Human 后续说“进入量化项目 / 回到 P03 / 继续商业雷达”等，Agent 不需要重新获得读取授权，直接进入对应 Project Bootstrap。

## 3. Global Bootstrap

由 `AGENT_GIT_MEMORY_CONTRACT.md` 规定统一入口与文件顺序。核心 Global 文件为：

1. `AGENT_GIT_MEMORY_CONTRACT.md`
2. `README.md`
3. `PROJECTS.md`
4. `CURRENT_STATE.md`
5. `NEXT_WORK.md`
6. `MEMORY_ARCHITECTURE.md`
7. `MEMORY_ROUTER.md`
8. `MEMORY_PROTOCOL.md`
9. `UNKNOWN_REGISTRY.md`
10. `SESSION_BOOTSTRAP.md`
11. `PLAN_PROTOCOL.md`

按需读取 `PROJECT_CONTEXT.md`、`INBOX.md`、`external/` 与相关历史。

## 4. Project Bootstrap

目标项目明确后，自动读取：

1. `README.md`
2. `PROJECT_CONTEXT.md`（如存在）
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. 唯一 Active Plan（如存在）
6. `MEMORY_INDEX.md`（如存在）
7. `DECISIONS.md`（如存在）
8. `GITHUB_WORKFLOW.md`（如存在）
9. 当前阶段直接相关的 Issue / research / evidence / experiment

不要扫描整个仓库。

## 5. Plan Continuity

如果存在 `ACTIVE` / `APPROVED` Plan，必须恢复：

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

默认动作：**继续原 Plan。**

不得因为换 Session、时间间隔、Session memory 缺失或重新推理而静默重新规划。

Plan 变更必须遵守：

`Evidence → Evaluation → Change Proposal → Approval → New Plan Version`

## 6. Task Resolution

GitHub Issue 是具体执行任务的唯一合同。

- `CURRENT_STATE.md`：状态
- `NEXT_WORK.md`：导航
- `BUDDY_TASK_CURRENT.md`：指针
- `INBOX.md`：通知指针
- Session memory / 旧聊天：线索

它们都不能独立产生任务。

若发现 Plan / State / Issue / Next Work / Task Pointer 冲突：

> **MEMORY BOOTSTRAP BLOCKED**

不猜、不执行、不修改。

## 7. Memory Sync 是自动动作，不再依赖 Human 提醒

本文件与 `AGENT_GIT_MEMORY_CONTRACT.md` 一起规定：

> **任何 Agent 在产生 durable change 后，都必须自动运行 Memory Sync Gate。**

触发包括但不限于：

- 新长期事实；
- 新/改变的决策；
- 当前状态变化；
- Plan step 完成；
- Issue 创建/开始/完成/阻塞/验证/关闭；
- Buddy commit / push；
- ChatGPT Review；
- 新研究/实验结论；
- 新 Unknown / 冲突；
- 协作规则变化。

Agent 必须自行判断并写回 canonical owner；**Human 不需要提醒“上传记忆”。**

如果没有 durable change，则 `Memory Sync: NOT NEEDED`，避免制造垃圾提交。

如果 Agent 没有写权限，则必须输出 `MEMORY_SYNC_REQUIRED`，不得声称已同步。

## 8. Session Recovery Card

Bootstrap 完成后，在当前 Session 内形成临时 Recovery Card：

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

Recovery Card 默认不写回 Git；其 durable 部分通过 Memory Sync Gate 写入 canonical owner。

## 9. Startup Report

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

若 BLOCKED，只报告冲突，不继续执行。

## 10. Cold-start acceptance

新 Session 在不依赖旧聊天的情况下，至少恢复：

- 当前项目
- Active Plan + version
- Plan objective
- Current phase
- Current Issue + status
- 已完成 Plan steps
- 当前 Plan step
- 下一 Plan step
- 关键证据
- Open Unknowns
- 是否存在冲突

并得到：

> **继续当前 Plan / 当前 Issue，而不是重新制定计划。**

## 11. 旧启动提示词的兼容说明

历史上使用的长启动提示词仍然有效，但不再是必要条件。

**从 v0.3 开始，Human 只需“检查 Git 的记忆”；读取协议、项目识别、Plan continuity 和 Memory Sync 都由统一 Agent Contract 自动触发。**

## 12. 与其他协议的关系

```text
AGENT_GIT_MEMORY_CONTRACT
        ↓
MEMORY_ARCHITECTURE
        ↓
MEMORY_ROUTER
        ↓
SESSION_BOOTSTRAP
        ↓
PLAN_PROTOCOL
        ↓
Project Memory + GitHub Issue
        ↓
Review
        ↓
Memory Sync
```

`AGENT_GIT_MEMORY_CONTRACT.md` 是所有 Agent 的统一入口；本文件是 ChatGPT Session 恢复的专门协议。
