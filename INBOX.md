# INBOX — ChatGPT → Work Buddy

> **跨项目通知层。** 本文件只保存任务指针、状态和目标仓库，不保存项目详细任务正文。
>
> **核心原则：Hub 管通知，Project Repo 管工作。**

## 当前任务

### TASK-20260828-AIC-MIGRATION

- status: DONE
- project: `ai-content`
- repository: `watanuo1982/-ai-content`
- project_entry: `PROJECT_CONTEXT.md`
- next_work: `NEXT_WORK.md`
- completed_commit: `78cd0db`
- result: AI Content 已完成独立仓库迁移与核对。

### TASK-20260828-QT-P2B

- status: DONE
- project: `quantitative-trading`
- repository: `watanuo1982/-quantitative-trading`
- project_entry: `PROJECT_CONTEXT.md`
- next_work: `NEXT_WORK.md`
- completed_commit: `d533720`
- result: P2-B BP × REV20 Blind Reproduction Benchmark 已完成并通过 benchmark；未修改 V7.1 生产代码。

## 通知协议

ChatGPT 不在本文件复制项目任务正文。

用户只需要通知 Buddy：**“Agent Hub 有新任务，请读取 INBOX.md。”**

Buddy 收到通知后：
1. 读取本文件；
2. 找到 `status: ASSIGNED` 的任务；
3. 根据 `project` / `repository` 跳转到对应 Project Repo；
4. 先读取该项目的 `PROJECT_CONTEXT.md`（若项目仍使用 `PROJECT.md`，则读取 `PROJECT.md`）、`README.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`；
5. 任务详细定义、执行过程、Evidence、Review 和历史记录全部在 Project Repo 内完成；
6. 完成后 commit 到目标 Project Repo；
7. 回到本 Hub，仅更新对应任务的状态、commit SHA 和一句结果摘要。

## 状态定义

- `ASSIGNED`：已分配，等待 Buddy 执行
- `IN_PROGRESS`：Buddy 已开始执行
- `DONE`：完成并已提交项目仓库
- `BLOCKED`：无法继续，需要人工决策或外部条件
- `REVIEW`：等待 ChatGPT Review

## 边界规则

- 一个真实项目 = 一个独立 repository。
- `agent-lab` 只负责跨项目通知、项目索引和协作状态。
- 项目详细工作不得重新集中写入 `agent-lab/INBOX.md`。
- 不同项目之间不得共享 `NEXT_WORK.md` 或混写项目任务。
