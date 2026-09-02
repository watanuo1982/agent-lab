# Session Bootstrap Protocol v0.1

> 用途：每次开启新的 ChatGPT 会话时，强制从 Git/GitHub 恢复长期项目上下文。
>
> **Git/GitHub 是长期 canonical source；Session memory 不能覆盖 Git。**
> 本协议不是新的记忆层，也不是任务系统；它只是进入 Session 前的强制加载与一致性检查程序。

## 1. 强制触发

以下任一情况发生前，必须先执行 Git Memory Bootstrap：

- 回答任何依赖历史项目上下文的问题
- 继续上一次项目工作
- 判断项目当前状态 / 当前任务 / 下一步
- 创建、修改、关闭或通知执行 GitHub Issue
- 修改项目或 `agent-lab` 文件
- 通知 Buddy 执行任务
- Review Buddy 的 commit / research / content / experiment

如果只是与项目无关的普通问答，不要求执行本协议。

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
8. `SESSION_BOOTSTRAP.md`（本协议）

必要时再读取：

- `PROJECT_CONTEXT.md`
- `MEMORY_PROTOCOL.md`
- `INBOX.md`
- `external/` 中与当前项目直接相关的条目

## 4. Project Memory Bootstrap

确定目标项目后，按以下顺序读取：

1. `README.md`
2. `PROJECT_CONTEXT.md`（如存在）
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. `MEMORY_INDEX.md`（如存在）
6. `DECISIONS.md`（如存在）
7. `GITHUB_WORKFLOW.md`（如存在）
8. 与当前阶段直接相关的 research / evidence / experiments / archive

**不要为了“完整恢复”读取整个仓库。** 只读取能决定当前状态、任务、结论和下一步的 canonical 文件及相关证据。

## 5. Current Task Resolution

这是最重要的一步。

### 5.1 任务唯一来源

> **GitHub Issue 是具体执行任务的唯一合同。**

以下文件可以提供导航或状态，但不能独立产生一个新的 Buddy 执行任务：

- `CURRENT_STATE.md`
- `NEXT_WORK.md`
- `BUDDY_TASK_CURRENT.md`
- `TASK*.md`
- `INBOX.md`
- 旧聊天记录
- Session memory

如果这些文件描述了“当前任务”，必须找到对应 GitHub Issue。

### 5.2 必须确认的关系

```text
CURRENT_STATE
      ↓
项目当前任务 / 阶段
      ↓
对应 GitHub Issue
      ↓
Issue status label
      ↓
Buddy commit / Issue 回报
      ↓
ChatGPT Review
```

### 5.3 阻断条件

出现以下任一情况，不得继续执行该任务：

- 当前任务找不到对应 Issue
- Issue 与 `CURRENT_STATE.md` 指向不同任务
- `NEXT_WORK.md` 指向另一个“当前任务”
- 存在两个以上文件都声称自己是唯一 current task
- Issue 状态 label 与项目状态明显矛盾且无法解释
- Buddy 正在执行，但无法确认其对应 Issue
- 项目边界无法确定
- Session memory 与 Git canonical facts 冲突且尚未裁决

此时输出：

`MEMORY BOOTSTRAP BLOCKED`

并列出冲突，不自行选边。

## 6. Authority Check

Bootstrap 至少确认以下 8 项：

| 项目 | 要确认什么 | Authority |
|---|---|---|
| Project | 当前项目是谁 | `PROJECTS.md` + 目标 repo |
| State | 当前阶段 / 状态 | `CURRENT_STATE.md` |
| Navigation | 下一步导航 | `NEXT_WORK.md` |
| Task | 当前执行任务 | GitHub Issue |
| Task status | Issue 当前状态 | `status:*` label + Open/Closed |
| Evidence | 结论依据 | research / evidence / experiment |
| Decisions | 关键裁决 | `DECISIONS.md` |
| Unknowns | 尚未确认事项 | `UNKNOWN_REGISTRY.md` |

若某一项没有明确 authority，不得用 Session memory 补齐。

## 7. Buddy 运行保护

如果发现 Buddy 当前正在执行某个任务：

1. 先确认对应 GitHub Issue。
2. **不得修改该任务的执行文件、输入数据、输出目录或任务合同。**
3. 不得为了“修复记忆”改变正在运行任务的范围。
4. 可以只读检查其他仓库的治理文档，但不要触碰 active execution surface。
5. 等 Buddy 完成后，再进行状态对齐和治理修复。

## 8. Session Recovery Card

Bootstrap 完成后，在当前 Session 内形成临时 Recovery Card：

```text
PROJECT:
CURRENT STATE:
CURRENT TASK:
CURRENT ISSUE:
ISSUE STATUS:
LATEST RELEVANT COMMIT:
KEY DECISIONS:
OPEN UNKNOWNS:
BUDDY STATUS:
NEXT STEP:
CONFLICTS:
```

这张卡默认**不写回 Git**。只有产生新的长期事实、决策或任务时，才按 `MEMORY_ROUTER.md` / Issue-first 规则分别落盘。

## 9. Startup Report

完成 Bootstrap 后，向 Human 简要报告：

```text
Git Memory Bootstrap: OK / BLOCKED
Project: ...
Current State: ...
Current Task: ...
Issue: ...
Buddy: ...
Latest Commit: ...
Conflicts: none / ...
Next: ...
```

如果 `BLOCKED`，只报告冲突和需要裁决的地方，不继续执行依赖这些信息的任务。

## 10. 可直接粘贴到新会话的启动提示词

下面这段是 Human 每次新开 ChatGPT 会话时可直接粘贴的最小启动指令：

> **执行 Git Memory Bootstrap。**
>
> Git/GitHub 是我的长期 canonical source；Session memory 不得覆盖 Git。先识别当前项目；如果涉及项目工作，先读取 `agent-lab/README.md`、`PROJECTS.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`、`MEMORY_ARCHITECTURE.md`、`MEMORY_ROUTER.md`、`UNKNOWN_REGISTRY.md`、`SESSION_BOOTSTRAP.md`，再读取目标项目的 `README.md`、`PROJECT_CONTEXT.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`、`MEMORY_INDEX.md`（如有）、`DECISIONS.md`（如有）、`GITHUB_WORKFLOW.md`（如有）及当前阶段相关证据。
>
> 必须确认：当前项目、当前状态、当前任务、对应 GitHub Issue、Issue status、最新相关 commit、关键决策、Open Unknowns、Buddy 是否正在执行。
>
> GitHub Issue 是唯一执行任务合同；`CURRENT_STATE.md` / `NEXT_WORK.md` / `BUDDY_TASK_CURRENT.md` / 旧聊天 / Session memory 都不能独立定义任务。若发现冲突、多个 current task、任务无 Issue、Buddy active task 无法确认，立即输出 `MEMORY BOOTSTRAP BLOCKED`，列出冲突，不要猜、不执行、不修改。
>
> Bootstrap 默认只读。完成后给我一份简短 Startup Report，再继续我的请求。

## 11. 与现有 Memory Architecture 的关系

本协议不改变四层记忆模型：

```text
Global / Project / External / Session
             ↑
      SESSION_BOOTSTRAP
        （启动加载器）
```

它解决的是“已有 canonical memory 是否真的被新 Session 加载并使用”，不是重新定义 memory ownership。

后续应由 consistency validator 检查本协议要求的关键一致性，最终形成：

```text
Git Architecture
      ↓
Consistency Validator
      ↓
Session Bootstrap
      ↓
Safe execution / review
```
