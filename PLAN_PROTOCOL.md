# Plan Protocol v0.1 — Canonical Plan Continuity

> **本文件是 Plan 的 canonical governance 定义。** Plan 不是聊天记录，也不是 Issue 清单；它是已经确认、可跨会话延续的路线合同。

## 1. Core rule

一旦 Human / ChatGPT 明确确认一个 Plan，该 Plan 就成为受保护的项目资产。

新会话默认恢复并继续当前 Active Plan。不能因为 Session memory 不完整、时间间隔较长，或重新推理后出现“看起来更好的方案”而静默替换。

如果认为需要更好的方案，只能提出 **Change Proposal**；确认前原 Plan 继续有效。

## 2. Plan 与其他对象的边界

```text
PROJECT
  ↓
PLAN        = 路线合同：整体怎么走
  ↓
ISSUE       = 执行合同：现在具体做什么
  ↓
EXECUTION   = 实际执行发生了什么
  ↓
REVIEW      = 是否接受执行结果
  ↓
PLAN PROGRESS / NEXT PHASE
```

| 对象 | Canonical authority | 回答什么 |
|---|---|---|
| Project | Project Memory | 我们在做什么 |
| Plan | Project Repo 的 Plan 文件/目录 | 接下来整体怎么走 |
| Decision | `DECISIONS.md` | 为什么这么决定 |
| Issue | GitHub Issue | 当前具体执行什么 |
| Execution | commit / artifacts / Issue report | 实际做了什么 |
| Review | Review record / Issue | 结果是否通过 |
| `CURRENT_STATE.md` | Project Memory | 现在处于什么状态 |
| `NEXT_WORK.md` | Project Memory | 导航到哪里，不产生新任务 |
| Session | 当前对话 | 临时思考，不是 authority |

Plan 与 Decision 不等价：Decision 可以支撑 Plan；Plan 把多个 Decision 组织成路线。

Plan 与 Issue 不等价：Issue 可以执行 Plan 的一个步骤；完成 Issue 不自动触发重新规划。

## 3. Canonical ownership

一个项目最多允许一个 `ACTIVE` Plan。

Plan 应位于对应 Project Repo；Global 层只定义 Plan protocol，不保存业务项目的 Plan 正文。

推荐：

```text
plans/
  PLAN_<slug>_v1.md
  PLAN_<slug>_v2.md
```

项目已有成熟 Plan 文件体系时保留原结构，但必须明确唯一 Active Plan 和版本身份。

## 4. Required metadata

每个确认过的 Plan 至少包含：

```yaml
plan_id: <stable-id>
version: v1
status: ACTIVE | APPROVED | DRAFT | PAUSED | COMPLETED | SUPERSEDED | ABANDONED
project: <repo>
objective: <one sentence>
approved_by: Human | ChatGPT | Human+ChatGPT
approved_at: <date>
supersedes: <plan-id/version or null>
current_phase: <phase-id>
current_issue: <issue URL/number or null>
```

正文至少说明：Objective、Why / assumptions、Phases、Decision gates、Constraints、Completion condition、Change conditions。

## 5. Lifecycle

```text
DRAFT → APPROVED → ACTIVE
                    ├→ PAUSED → ACTIVE
                    ├→ COMPLETED
                    └→ CHANGE PROPOSAL → REVIEW → new version → SUPERSEDED
```

`SUPERSEDED` 不删除。旧版本保留，并明确指向新版本。

## 6. Change control

禁止：
- 新会话静默修改 Plan；
- 仅因为“我现在重新想了一遍”就替换 Plan；
- 用 `NEXT_WORK.md` 覆盖 Plan；
- 用 Issue 标题/评论隐式改变 Plan；
- Buddy 自行改变 Plan 范围、阶段或决策门。

允许改变 Plan 的条件至少满足一个：
1. Human 明确要求重新规划；
2. 原 Plan 已完成；
3. 原 Plan 被证明不可执行；
4. 新证据违反原 Plan 的关键假设；
5. 原 Plan 明确规定的 change condition 被触发。

任何变更必须记录：

```text
CHANGE PROPOSAL:
FROM: Plan vN
TO: Plan vN+1
REASON:
EVIDENCE:
IMPACT:
SUPERSEDES:
APPROVAL:
```

在新版本获得确认前，旧 Active Plan 不失效。

## 7. Session continuity rule

新会话 Bootstrap 时：
1. 查找项目 Active / Approved Plan；
2. 读取 Plan；
3. 将 Plan identity/version/current phase/current Issue 加入 Recovery Card；
4. 对照 `CURRENT_STATE.md`、Issue、最近 commit；
5. 一致 → **继续原 Plan**；
6. 不一致 → `MEMORY BOOTSTRAP BLOCKED`，不得自行重规划。

如果不存在 Plan，不得假装存在；只有在用户明确要求规划时才能提出新 Plan，新 Plan 经过确认后才成为 Active。

## 8. Plan vs Current State

`CURRENT_STATE.md` 描述事实状态；Plan 描述确认后的路线。

例如：

```text
Plan v1: Phase 2 → Phase 3
Current State: Phase 2, Issue #17 DONE
Next Work: Issue #18
```

这是执行 Plan v1 的下一步，不是重新制定计划。

如果 Current State 与 Plan 阶段不一致，属于需要解释的冲突，不允许自动修改其中一方。

## 9. Plan vs Evidence

研究结果、新事实可以挑战 Plan，但**证据不会自动修改 Plan**。

```text
Evidence → ChatGPT evaluates → Change Proposal → confirmation → New Plan version
```

> **Evidence can invalidate a Plan; Evidence cannot silently rewrite a Plan.**

## 10. Validator invariants

Consistency validator 应至少检查：
- 每个项目最多一个 `ACTIVE` Plan；
- Active Plan 有稳定 `plan_id` + `version`；
- `SUPERSEDED` Plan 指向明确的新版本；
- Active Plan 的 `current_issue` 可解析；
- Active Plan / `CURRENT_STATE` / current Issue 不存在未解释的阶段冲突；
- `NEXT_WORK.md` 不声明与 Active Plan / Issue 冲突的独立 current task；
- active task markdown 不得成为第二套 task authority；
- 新版本 Plan 声明 `supersedes` 与变更理由；
- Plan 指针不能悬空。

## 11. Cold-start acceptance test

新 ChatGPT Session 在不依赖旧聊天记录的情况下，至少能恢复：

```text
当前项目：
Active Plan：
Plan Version：
Plan Objective：
Current Phase：
Current Issue：
已完成的 Plan Step：
当前 Plan Step：
下一 Plan Step：
最近关键证据：
Open Unknowns：
是否存在 Plan Conflict：
```

没有明确的 Change Proposal + approval 时，新 Session **不得把这些答案重新设计成另一套计划**。

## 12. Relationship to Memory Architecture

Memory Architecture 管理“信息属于哪里”；本协议管理“已确认路线如何持续”。

```text
Memory Architecture
       ↓
Canonical Plan
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

Plan 是 Project Memory 的一种受保护资产，不新增独立任务系统。
