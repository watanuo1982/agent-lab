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

**一个真实项目 = 一个独立 repository；Agent Hub = 跨项目通知入口。**

当前项目：
- `agent-lab`：跨项目协作基础设施
- `-quantitative-trading`：量化研究 / 实盘策略
- `-ai-content`：AI 内容生产
- `-commercial-radar`：商业机会雷达
- `-work-buddy-lab`：历史 Work Buddy 工具协作实验，FROZEN

未来新项目直接新建独立 repository，并在 `PROJECTS.md` 登记。

## 协作方式

### Agent Hub

`INBOX.md` 只保存跨项目通知指针：project、repository、项目入口、状态、commit SHA 和简短结果。

不复制具体项目的详细任务正文。

### Project Repo

每个项目自行维护自己的：
- `PROJECT_CONTEXT.md` / `PROJECT.md`
- `README.md`
- `CURRENT_STATE.md`
- `NEXT_WORK.md`
- tasks / reviews / decisions
- 代码、数据、Evidence、研究成果或内容资产
- `CHANGELOG.md`
- `GITHUB_WORKFLOW.md`（项目级 Issue 协作规则）

**具体任务统一使用 Project Repo 的 GitHub Issue。** 文件用于知识、状态、导航和成果沉淀，不再作为任务派发的第二套系统。

## 标准任务流程

1. ChatGPT 在对应 Project Repo 创建 Issue，写清 Objective、Scope、Constraints、Deliverables 和 Definition of Done。
2. Human 通知 Buddy 有新 Issue。
3. Buddy 从 Issue 获取任务，不依赖聊天上下文；开始执行后将 `STATUS` 更新为 `IN_PROGRESS`。
4. Buddy 完成后 commit/push，并在 Issue 回报 `STATUS: DONE`、验证结果、Artifacts 和 commit SHA；无法完成则回报 `STATUS: BLOCKED`。
5. ChatGPT 检查 commit、成果和 Definition of Done。
6. 通过后 ChatGPT 在 Issue 回报 `STATUS: VERIFIED` 并关闭 Issue；需要继续工作则创建下一 Issue。
7. `INBOX.md` 仅在确有跨项目通知需求时记录指针，不复制 Issue 正文。

## 状态模型

```text
READY → IN_PROGRESS → DONE → VERIFIED → CLOSED
                     ↘ BLOCKED
```

GitHub 原生 Open/Closed 是最终状态；Issue 正文中的 `STATUS:` 是协作流程状态。

## ChatGPT ↔ Buddy 的默认交互

```text
ChatGPT 创建 Project Issue
        ↓
Human 告知 Buddy 有新任务
        ↓
Buddy 执行 + Commit/Push
        ↓
Buddy 回写 Issue：DONE / BLOCKED
        ↓
ChatGPT Review
        ↓
VERIFIED → Close
        ↓
下一 Issue
```

除非出现明确收益，否则不增加 webhook、自动触发器或其他协作基础设施。

**核心原则：Agent Hub 管跨项目通知；Project Repo 的 Issue 管具体任务；Project Repo 文件管项目知识与成果。**
