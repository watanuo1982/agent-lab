# INBOX — ChatGPT → Work Buddy

> 跨项目任务通知。项目本身的详细任务必须留在对应 Project Repo，不在这里复制。

## 当前任务

### TASK-20260828-AIC-MIGRATION

- status: ASSIGNED
- project: ai-content
- repository: `watanuo1982/-ai-content`
- task: 将原 `watanuo1982/-work-buddy-lab/ai-content/` 完整迁移为独立项目仓库
- instruction: 进入 `-ai-content`，读取该项目的 `PROJECT_CONTEXT.md`、`README.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`。将原 `-work-buddy-lab/ai-content/` 的历史项目文件、content、reviews、tasks 等完整迁移到 `-ai-content`，保持相对路径和文件内容；完成迁移核对后更新状态。
- boundary: 不修改 `-quantitative-trading`；不要把 AI Content 新工作继续写入 `-work-buddy-lab`。
- legacy: 原 `-work-buddy-lab/ai-content/` 暂作为历史快照保留，迁移核对完成后在旧仓库建立明确的 legacy/frozen 标记；不要直接删除历史资产。
- completion: 新仓库完成完整迁移并核对；提交 commit；回到本 Hub 将本任务更新为 DONE 或 BLOCKED，并给出目标项目 commit SHA。
- assigned_by: ChatGPT
- assigned_at: 2026-08-28

### TASK-20260828-QT-P2B

- status: ASSIGNED
- project: quantitative-trading
- repository: `watanuo1982/-quantitative-trading`
- task: P2-B — BP × REV20 Blind Reproduction Benchmark
- instruction: 进入 `-quantitative-trading`，读取该项目的 `NEXT_WORK.md`，按项目规范执行当前 P2-B；不要修改 V7.1 生产策略代码。
- completion: 在量化项目仓库完成实验、证据、报告并 commit；然后回到本 Hub 将本任务更新为 DONE 或 BLOCKED。
- assigned_by: ChatGPT
- assigned_at: 2026-08-28

## 通知协议

ChatGPT 不通过聊天逐字转述任务给 Buddy。

用户只需要通知 Buddy：**“Agent Hub 有新任务，请读取 INBOX.md。”**

Buddy 完成后必须：
- 在目标项目仓库提交实际工作；
- 回到本 Hub 更新对应任务状态；
- 给出目标项目 commit SHA 和结果摘要；
- 如被阻塞，标记 `BLOCKED` 并说明阻塞原因。

## 状态定义

- `ASSIGNED`：已分配，等待 Buddy 执行
- `IN_PROGRESS`：Buddy 已开始执行
- `DONE`：完成并已提交项目仓库
- `BLOCKED`：无法继续，需要人工决策或外部条件
- `REVIEW`：等待 ChatGPT Review
