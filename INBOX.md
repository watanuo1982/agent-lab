# INBOX — ChatGPT → Work Buddy

> **跨项目通知层。** 本文件只保存当前任务指针、状态和目标仓库，不保存项目详细任务正文。
>
> **核心原则：Hub 管通知，Project Repo 管工作。**

## 当前任务

| task | status | project | repository | project_entry | next_work | assigned_at | assigned_by |
|---|---|---|---|---|---|---|---|

> 当前无跨项目任务指针。新任务由 ChatGPT 在业务仓库建 Issue 后在此登记（仅指针，不复制正文）。
> 历史任务见 `archive/YYYY-MM.md`（最近一批：qt #15 External Candidate Validation，已于 2026-09-04 确认 VERIFIED 后归档）。

## 新任务格式

新增任务只需包含：

- `task`
- `status`
- `project`
- `repository`
- `project_entry`
- `next_work`
- `assigned_at`
- `assigned_by`

任务详细定义、执行过程、Evidence、Review 和历史记录全部留在 Project Repo。

## 通知协议

用户只需要通知 Buddy：**“Agent Hub 有新任务，请读取 INBOX.md。”**

Buddy 收到通知后：
1. 读取本文件；
2. 找到 `status: ASSIGNED` 的任务；
3. 根据 `project` / `repository` 跳转到对应 Project Repo；
4. 读取该项目的 `PROJECT_CONTEXT.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`、Active Plan，再按 Issue 读取具体规范；
5. 只在目标 Project Repo 执行任务并提交 Git；
6. 完成后回到本 Hub，将任务标记为 `DONE` 或 `BLOCKED`，记录 commit SHA 和一句结果摘要；
7. `DONE` 任务随后归档到 `archive/`，不长期堆积在 INBOX。

## 状态定义

- `ASSIGNED`：已分配，等待 Buddy 执行
- `IN_PROGRESS`：Buddy 已开始执行
- `DONE`：完成并已提交项目仓库
- `BLOCKED`：无法继续，需要人工决策或外部条件
- `REVIEW`：等待 ChatGPT Review

## 边界规则

- 一个真实项目 = 一个独立 repository。
- `agent-lab` 只负责跨项目通知、项目索引和协作协议。
- 项目详细工作不得重新集中写入 `INBOX.md`。
- 不同项目之间不得共享 `NEXT_WORK.md` 或混写项目任务。
- `INBOX.md` 的任务状态不得取代 Project Repo 的 GitHub Issue status；Issue 才是执行合同。

