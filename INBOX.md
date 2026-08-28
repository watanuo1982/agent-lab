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

### TASK-20260828-QT-P2C

- status: DONE
- completed_commit: e6bcbce (watanuo1982/-quantitative-trading, research/P2-C_portfolio_translation/)
- result: P2-C 组合翻译实验完成。三种翻译（C1 宽度 N=3/5/10/20、C2 显式交互项 λ 网格、C3 高-高五分位层）均未能把 BP×REV20 联合结构翻译成统计可靠组合超额；Judge=NO_VALIDATED_CANDIDATE（全样本最佳 t=1.522<1.645 临界，所有 Bootstrap CI 含 0，无候选满足 improves_reliability AND survives_oos）。C1_N3 控制组与 P2-B bp_rev20 逐位一致（+11.35%），证明 P2-B 的 NO_JOINT_ALPHA 稳健。V7.1 冻结未改，不开 V7.2。建议在 ChatGPT Review 中与 P2-B 一并审视。
- project: quantitative-trading
- repository: `watanuo1982/-quantitative-trading`
- task: P2-C — BP×REV20 Portfolio Translation
- instruction: 进入 `-quantitative-trading`，读取 `NEXT_WORK.md` 与 `research/P2-C_portfolio_translation/spec.md`，按 V7.1 冻结框架执行组合翻译实验；不修改 V7.1 生产策略代码。
- completion: 在量化项目仓库完成实验、证据、报告并 commit；回到本 Hub 更新状态并给 commit SHA。
- assigned_by: User (direct command "执行 P2-C")
- assigned_at: 2026-08-28

### TASK-20260828-QT-P2D

- status: DONE
- completed_commit: 9fe8def (watanuo1982/-quantitative-trading, research/research_memory/)
- result: P2-D Research Memory 完成。把 P0-PIT / P1-A / P1-B / P2-A / P2-B / P2-C 全部标准化存入 `research/research_memory/`（SCHEMA.md 条目契约 + INDEX.md 人工检索 + manifest.json 机器检索 + entries/ 6 个快照），形成可检索、可累积的研究历史。边界：V7.1 冻结构建未改，历史条目不覆盖。
- project: quantitative-trading
- repository: `watanuo1982/-quantitative-trading`
- task: P2-D — Research Memory
- instruction: 进入 `-quantitative-trading`，按基准路线图 §P2-D 把已完成实验结果标准化为可检索研究历史存入 GitHub。
- completion: 在量化项目仓库完成研究记忆层、commit；回到本 Hub 更新状态并给 commit SHA。
- assigned_by: User (direct command "GitHub 有新任务，执行 P2-D")
- assigned_at: 2026-08-28

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
