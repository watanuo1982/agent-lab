# Agent Hub

ChatGPT ↔ Work Buddy 的跨项目通知与协作总入口。

## 定位

本仓库不是具体项目的代码仓库，也不存放具体项目的研究成果。

它只负责：
- 项目注册与索引
- ChatGPT → Work Buddy 的任务通知
- 跨项目状态摘要
- 协作协议

## 仓库边界

每个实际项目必须独立使用一个 GitHub repository。

- `agent-lab`：总通知 / 项目索引
- `-quantitative-trading`：量化交易项目
- `-work-buddy-lab`：历史 Work Buddy 工具协作实验，冻结，不再承载新项目

未来新项目直接新建独立 repository，并在本仓库登记。

## 协作入口

Work Buddy 每次被通知有新任务时：
1. 读取本仓库 `INBOX.md`
2. 找到 `status: ASSIGNED` 的任务
3. 跳转到任务指定的项目 repository
4. 读取该项目自己的 `NEXT_WORK.md` / `TASK.md` / 项目规范
5. 在项目 repository 中执行任务
6. 将结果、证据、状态和 commit 留在项目 repository
7. 回到本仓库更新任务状态为 `DONE` 或 `BLOCKED`，并提交 commit

ChatGPT Review 时：
1. 读取本仓库状态
2. 进入对应项目 repository
3. 检查 Buddy 的 commit / artifacts
4. Review 后决定下一任务
5. 只在本仓库写下一项跨项目通知，不把项目内容复制到这里

## 核心原则

**Hub 管通知，Project Repo 管工作。**

不得把多个项目重新混入一个 repository。
