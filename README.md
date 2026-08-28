# Agent Hub

ChatGPT ↔ Work Buddy 的跨项目通知与协作总入口。

## 定位

本仓库不是具体项目的工作区，也不存放具体项目的研究成果或内容资产。

它只负责：
- 项目注册与索引（`PROJECTS.md`）
- ChatGPT → Work Buddy 的跨项目任务通知（`INBOX.md`）
- 跨项目状态指针
- 通用协作协议

## 仓库边界

**一个真实项目 = 一个独立 repository；Agent Hub = 唯一跨项目通知入口。**

当前项目：
- `agent-lab`：跨项目协作基础设施
- `-quantitative-trading`：量化研究 / 实盘策略
- `-ai-content`：AI 内容生产
- `-work-buddy-lab`：历史 Work Buddy 工具协作实验，FROZEN

未来新项目直接新建独立 repository，并在 `PROJECTS.md` 登记。

## 协作方式

### Agent Hub

`INBOX.md` **只保存任务指针**：project、repository、项目入口、状态、commit SHA 和简短结果。

不复制任何项目的详细任务正文。

### Project Repo

每个项目自行维护自己的：
- `PROJECT_CONTEXT.md` / `PROJECT.md`
- `README.md`
- `CURRENT_STATE.md`
- `NEXT_WORK.md`
- tasks / reviews / decisions
- 代码、数据、Evidence、研究成果或内容资产
- `CHANGELOG.md`

不同项目之间不共享 `NEXT_WORK.md`，也不混写项目任务。

## Work Buddy 流程

1. 收到通知后读取 `INBOX.md`；
2. 找到 `status: ASSIGNED` 的任务；
3. 根据任务指针进入对应 Project Repo；
4. 读取该项目自己的上下文和工作入口；
5. 在 Project Repo 内完成任务并 commit；
6. 回到 `INBOX.md`，仅更新任务状态、commit SHA 和简短结果。

## ChatGPT Review

ChatGPT 根据 Hub 指针进入对应 Project Repo，检查 commit / artifacts / Evidence，并在该项目上下文基础上决定下一项工作。

**核心原则：Hub 管通知，Project Repo 管工作。**
