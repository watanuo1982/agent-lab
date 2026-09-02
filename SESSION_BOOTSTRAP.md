# Session Bootstrap Protocol v0.2

> 用途：每次开启新的 ChatGPT 会话时，强制从 Git/GitHub 恢复长期项目上下文。
>
> **Git/GitHub 是长期 canonical source；Session memory 不能覆盖 Git。**
> 本协议不是新的记忆层，也不是任务系统；它是进入 Session 前的强制加载、一致性与 Plan continuity 检查程序。

## 1. 强制触发

以下任一情况发生前，必须先执行 Git Memory Bootstrap：

- 回答任何依赖历史项目上下文的问题
- 继续上一次项目工作
- 判断项目当前状态 / 当前任务 / 下一步
- 创建、修改、关闭或通知执行 GitHub Issue
- 修改项目或 `agent-lab` 文件
- 通知 Buddy 执行任务
- Review Buddy 的 commit / research / content / experiment

普通项目无关问答不要求执行本协议。

## 2. Bootstrap 原则

1. **先识别项目，再读取项目。** 不确定时读取 `agent-lab/PROJECTS.md`。
2. **Session memory 只能作为线索，不能作为事实源。**
3. **Git 文件负责知识与状态；GitHub Issue 负责具体任务合同。**
4. **一个事实只有一个 canonical owner。** 如果发现多个来源都声称自己是 current/canonical，先停下并报告冲突。
5. **Unknown 不猜。** 冲突或无法确认的内容按 `UNKNOWN_REGISTRY.md` 处理。
6. **不要因为恢复上下文而改写仓库。** Bootstrap 默认只读；发现问题先报告，修复必须另行授权。

## 3. Global Memory Bootstrap

先读取 `agent-lab`：

1. `README.md`
2. `PROJECTS.md`
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. `MEMORY_ARCHITECTURE.md`
6. `MEMORY_ROUTER.md`
7. `UNKNOWN_REGISTRY.md`
8. `SESSION_BOOTSTRAP.md`
9. `PLAN_PROTOCOL.md`

必要时再读取 `PROJECT_CONTEXT.md`、`MEMORY_PROTOCOL.md`、`INBOX.md`、相关 `external/`。

## 4. Project Memory Bootstrap

确定目标项目后，按以下顺序读取：

1. `README.md`
2. `PROJECT_CONTEXT.md`（如存在）
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. **Active Plan**：按 `PLAN_PROTOCOL.md` 查找项目 `plans/` 或项目声明的唯一 Active Plan
6. `MEMORY_INDEX.md`（如存在）
7. `DECISIONS.md`（如存在）
8. `GITHUB_WORKFLOW.md`（如存在）
9. 与当前阶段直接相关的 research / evidence / experiments / archive

不要为了“完整恢复”读取整个仓库。

## 5. Plan Continuity — 新会话不得重新发明已确认计划

### 5.1 Plan 是受保护资产

如果项目存在 `ACTIVE` / `APPROVED` Plan：

> **默认动作是继续原 Plan，而不是重新制定 Plan。**

新会话不能因为：
- 时间间隔较长；
- Session memory 不完整；
- 重新推理后发现“看起来更好的方案”；
- 当前 Issue 已完成；

就静默替换原 Plan。

### 5.2 必须恢复

```text
ACTIVE PLAN:
PLAN ID:
PLAN VERSION:
PLAN STATUS:
PLAN OBJECTIVE:
CURRENT PHASE:
CURRENT ISSUE:
COMPLETED PLAN STEPS:
CURRENT PLAN STEP:
NEXT PLAN STEP:
CHANGE PROPOSALS:
```

### 5.3 Change control

Evidence 可以挑战 Plan，但不能自动修改 Plan：

`Evidence → ChatGPT evaluates → Change Proposal → Human/ChatGPT approval → new Plan version`

没有明确 Change Proposal + approval，不得生成新 Plan 版本。

## 6. Current Task Resolution

### 6.1 任务唯一来源

> **GitHub Issue 是具体执行任务的唯一合同。**

以下文件只能导航/描述状态，不能独立产生 Buddy 任务：

- `CURRENT_STATE.md`
- `NEXT_WORK.md`
- `BUDDY_TASK_CURRENT.md`
- `TASK*.md`
- `INBOX.md`
- 旧聊天记录
- Session memory

如果这些文件描述了“当前任务”，必须找到对应 GitHub Issue。

### 6.2 必须确认关系

```text
Active Plan
    ↓
Current Phase / Plan Step
    ↓
GitHub Issue
    ↓
Issue status label
    ↓
Buddy commit / Issue report
    ↓
ChatGPT Review
    ↓
Plan Progress
```

### 6.3 阻断条件

出现以下任一情况，不得继续：

- 当前任务找不到对应 Issue
- Active Plan 与 `CURRENT_STATE.md` 指向不同阶段且无法解释
- Active Plan 与 current Issue 不一致且无法解释
- `NEXT_WORK.md` 指向另一个“当前任务”
- 存在两个以上文件声称自己是唯一 current task
- Issue 状态 label 与项目状态明显矛盾且无法解释
- Buddy 正在执行，但无法确认对应 Issue
- Session memory 与 Git canonical facts 冲突且尚未裁决

输出：`MEMORY BOOTSTRAP BLOCKED`，列出冲突，不自行选边。

## 7. Authority Check

| 项目 | Authority |
|---|---|
| Project | `PROJECTS.md` + 目标 repo |
| State | `CURRENT_STATE.md` |
| Plan | Project Active Plan |
| Navigation | `NEXT_WORK.md` |
| Task | GitHub Issue |
| Task status | `status:*` label + Open/Closed |
| Evidence | research / evidence / experiment |
| Decisions | `DECISIONS.md` |
| Unknowns | `UNKNOWN_REGISTRY.md` |
| History | Git commits / Issue history |

## 8. Buddy 运行保护

如果 Buddy 正在执行：

1. 确认对应 Issue。
2. 不得修改执行文件、输入数据、输出目录或任务合同。
3. 不得为了“修复记忆”改变任务范围。
4. 可以只读检查治理文档。
5. Buddy 完成后再做状态对齐。

## 9. Session Recovery Card

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

默认不写回 Git。

## 10. Startup Report

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
```

如果 BLOCKED，只报告冲突和需要裁决的地方，不继续执行。

## 11. Cold-start acceptance test

一个新 ChatGPT Session 在不依赖旧聊天记录的情况下，至少必须恢复：

```text
当前项目
Active Plan + version
Plan objective
Current phase
Current Issue + status
已完成 Plan Steps
当前 Plan Step
下一 Plan Step
关键证据
Open Unknowns
是否存在冲突
```

并且必须得到：

> **继续当前 Plan / 当前 Issue，而不是重新制定计划。**

## 12. 可直接粘贴到新会话的启动提示词

> **执行 Git Memory Bootstrap + Plan Continuity Check。**
>
> Git/GitHub 是我的长期 canonical source；Session memory 不得覆盖 Git。先识别当前项目；涉及项目工作时，先读取 `agent-lab/README.md`、`PROJECTS.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`、`MEMORY_ARCHITECTURE.md`、`MEMORY_ROUTER.md`、`UNKNOWN_REGISTRY.md`、`SESSION_BOOTSTRAP.md`、`PLAN_PROTOCOL.md`，再读取目标项目的 `README.md`、`PROJECT_CONTEXT.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`、唯一 Active Plan、`MEMORY_INDEX.md`（如有）、`DECISIONS.md`（如有）、`GITHUB_WORKFLOW.md`（如有）及当前阶段相关证据。
>
> 必须恢复：当前项目、Current State、Active Plan、Plan version、Plan objective、Current Phase、Current Issue、Issue status、已完成 Plan steps、当前 Plan step、下一 Plan step、最新相关 commit、关键决策、Open Unknowns、Buddy 状态。
>
> **如果存在 ACTIVE/APPROVED Plan，默认继续原 Plan。禁止因为换会话、时间间隔、重新推理或出现“更好的方案”而静默重新规划。任何改变必须先形成 Change Proposal，并获得 Human/ChatGPT 明确批准后建立新 Plan 版本。**
>
> GitHub Issue 是唯一执行任务合同；`CURRENT_STATE.md` / `NEXT_WORK.md` / `BUDDY_TASK_CURRENT.md` / 旧聊天 / Session memory 都不能独立定义任务。若发现 Plan、Current State、Issue、Next Work 或任务指针冲突，立即输出 `MEMORY BOOTSTRAP BLOCKED`，列出冲突，不猜、不执行、不修改。
>
> Bootstrap 默认只读。先给我 Startup Report，再继续我的请求。

## 13. 与 Memory Architecture 的关系

```text
Memory Architecture
       ↓
Canonical Plan
       ↓
Consistency Validator
       ↓
Session Bootstrap
       ↓
Plan Continuity Check
       ↓
Issue Execution
       ↓
Review
       ↓
Plan Progress
```

Memory Architecture 管理“信息属于哪里”；Plan Protocol 管理“确认后的路线如何持续”；Session Bootstrap 确保每次新会话真正恢复并遵守它们。
