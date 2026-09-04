# Agent Hub

ChatGPT ↔ Work Buddy 的跨项目通知与协作总入口。

## 定位

本仓库不是具体项目的工作区，也不存放具体项目的研究成果或内容资产。

它只负责：
- 项目注册与索引（`PROJECTS.md`）
- ChatGPT → Work Buddy 的跨项目任务通知（`INBOX.md`）
- 跨项目状态指针
- 通用协作协议
- 跨项目记忆架构（见下节文件地图）
- **Agent System 的全局运行时架构（见 `CLOUD_RUNTIME_ARCHITECTURE.md`）**

## Agent 统一入口（强制）

**任何读取本体系 Git/GitHub 的 Agent，都必须先进入 Git Memory Mode。**

Human 不需要再提供启动清单。只要说：

> **检查 Git 的记忆。**

Agent 就自动读取 `AGENT_GIT_MEMORY_CONTRACT.md` 并执行 Global Bootstrap；Human 后续指出具体项目后，Agent 自动执行 Project Bootstrap + Plan Continuity Check。

**任何产生 durable change 的工作单元结束时，Agent 必须自动执行 Memory Sync Gate，并在需要时把记忆写回 Git。Human 不负责提醒“上传记忆”。**

统一规则见 [`AGENT_GIT_MEMORY_CONTRACT.md`](AGENT_GIT_MEMORY_CONTRACT.md)。

## 文件地图

记忆分为四层，完整定义见 `MEMORY_ARCHITECTURE.md`，路由规则见 `MEMORY_ROUTER.md`。

每次进入 Git Memory Mode，先执行 `AGENT_GIT_MEMORY_CONTRACT.md`；Session 恢复细则见 `SESSION_BOOTSTRAP.md`。

| 层 | 位置 | 管什么 |
|---|---|---|
| **Global** | 本仓库 | 项目地图、跨项目原则、协作协议、Memory 协议、Agent Runtime 架构 |
| **Project** | 各业务仓库 | 该项目自己的目标、状态、决策、研究、实验、下一步 |
| **External** | `external/` | 外部知识/工具/来源的**指针与判据**，不是事实源 |
| **Session** | 不落盘 | 本次对话的中间过程，默认不进入长期记忆 |

**Hub 层文件**

| 文件 | 职责 |
|---|---|
| `AGENT_GIT_MEMORY_CONTRACT.md` | **所有 Agent 的统一 Git Memory 入口、自动启动与自动写回合同** |
| `PROJECTS.md` | 项目注册表 + 新项目接入规范 |
| `PROJECT_CONTEXT.md` | 四仓库边界、状态判断语义、Control Tower 定位、Buddy 跨仓库约定 |
| `CURRENT_STATE.md` | Agent Hub 自身当前治理状态与恢复入口 |
| `NEXT_WORK.md` | Agent Hub 自身下一步导航；正式任务仍以 Issue 为准 |
| `MEMORY_ARCHITECTURE.md` | 四层模型、canonical 归属、证据语义、冲突处理、读写职责 |
| `MEMORY_ROUTER.md` | 路由判定程序 + 路由测试记录 |
| `MEMORY_PROTOCOL.md` | 什么值得记 / 记录字段 / 写入时机 / 设计参考 |
| `UNKNOWN_REGISTRY.md` | Unknown 唯一登记、生命周期、复查与裁决状态 |
| `SESSION_BOOTSTRAP.md` | Session 恢复与 Plan continuity 的详细检查协议 |
| `EXECUTION_RECEIPT.md` | **Execution Receipt 规范（M2）：执行回执字段、`produced_by` 独立性分级（Evidence-first，Agent 自述不构成独立 Evidence）** |
| `CLOUD_RUNTIME_ARCHITECTURE.md` | **Cloudflare Agent Runtime 的全局架构、职责边界、权限、Memory、Free-first 与实施路线** |
| `INBOX.md` | 跨项目任务指针（不复制任务正文） |
| `external/` | External Memory（指针 + 判据） |
| `archive/YYYY-MM.md` | 已完成跨项目任务归档 |
| `memory-tests/` | 跨会话恢复实测记录（**含题库与答案，做恢复测试时必须排除**，见 `memory-tests/README.md`） |

> ⚠️ Hub **不存放**任何业务项目的详细内容；业务事实一律留在业务仓库。

## 仓库边界

**一个真实项目 = 一个独立 repository；Agent Hub = 跨项目通知入口。**

当前注册项目：
- `agent-lab`：跨项目协作基础设施
- `-quantitative-trading`：量化研究 / 实盘策略
- `-ai-content`：AI 内容生产
- `-commercial-radar`：商业机会雷达

`-work-buddy-lab` 是历史工具协作实验仓库，已删除，不属于当前项目注册表。历史资料如需引用，应以 Git 历史或其他明确证据为准。

> 当前项目注册表以 `PROJECTS.md` 为 canonical source；发现与其他 Hub 文件不一致的项目事实时，先登记 `UNKNOWN_REGISTRY.md`，不得自行选边。

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

### Issue-first 规则（任务唯一载体，强制）

> **所有交给 Buddy 执行的可审计任务，必须先有对应 GitHub Issue 作为唯一任务载体；聊天消息（含本 Hub 的 `INBOX.md` 指针）只作通知 / 补充，不替代 Issue。**
>
> 生命周期（强制顺序）：
> `Issue（ChatGPT 建，写清 Objective / Scope / Constraints / DoD） → Buddy 执行 → Commit / Push → Issue 回报 DONE / BLOCKED → ChatGPT Review → VERIFIED / CLOSED`

- 没有对应 Issue 的任务，Buddy 不应视为已授权执行；ChatGPT 定义新任务时必须在业务仓库建 Issue，不在 Hub 写任务正文。
- 聊天里的口头指令只通过「Human 通知 Buddy 有新 Issue」进入执行，任务内容以 Issue 正文为准。
- 本规则是各业务仓库 `GITHUB_WORKFLOW.md` 的上层总原则，不与之冲突。

### 标准任务流程

1. ChatGPT 在对应 Project Repo 创建 Issue，写清 Objective、Scope、Constraints、Deliverables 和 Definition of Done。
2. Human 通知 Buddy 有新任务。
3. Buddy 从 Issue 获取任务，不依赖聊天上下文；开始执行后将当前状态标记为 `IN_PROGRESS`。
4. Buddy 完成后 commit/push，并在 Issue 回报 `STATUS: DONE`、验证结果、Artifacts 和 commit SHA；无法完成则回报 `STATUS: BLOCKED`。
5. ChatGPT 检查 commit、成果和 Definition of Done。
6. 通过后 ChatGPT 在 Issue 回报 `STATUS: VERIFIED` 并关闭 Issue；需要继续工作则创建下一 Issue。
7. `INBOX.md` 仅在确有跨项目通知需求时记录指针，不复制 Issue 正文。

## 状态模型

```text
READY → IN_PROGRESS → DONE → VERIFIED → CLOSED
                     ↘ BLOCKED
```

**状态元数据原则**：Issue 上恰好一个 `status:*` Label 是 current status 的机器可查询表达；Issue 评论中的 `STATUS:` 是审计日志，不再作为唯一 current-state authority。GitHub 原生 Open/Closed 仍是 Issue 生命周期的最终状态。

当前允许的 status Label：
`status:ready` / `status:in-progress` / `status:done` / `status:verified` / `status:blocked` / `status:hold`

状态迁移时必须先移除旧的 `status:*` Label，再添加新的 `status:*` Label；任何 Issue 同时拥有 0 个或超过 1 个 `status:*` Label 都属于治理错误。

当前兼容期允许继续写 `STATUS:` 评论，以保持既有历史流程可读；新工具或自动化不得依赖扫描历史评论来推断唯一当前状态。

## ChatGPT ↔ Buddy 的默认交互

```text
ChatGPT 创建 Project Issue
        ↓
Human 告知 Buddy 有新任务
        ↓
Buddy 执行 + Commit/Push
        ↓
Buddy 回写 Issue：状态 Label + STATUS 审计日志
        ↓
ChatGPT Review
        ↓
VERIFIED → Close
        ↓
下一 Issue
```

除非出现明确收益，否则不增加 webhook、自动触发器或其他协作基础设施。

**核心原则：Agent Hub 管跨项目通知；Project Repo 的 Issue 管具体任务；Project Repo 文件管项目知识与成果；`AGENT_GIT_MEMORY_CONTRACT.md` 管所有 Agent 的统一读写入口与记忆同步责任；`CLOUD_RUNTIME_ARCHITECTURE.md` 管 Cloudflare Agent Runtime 的全局架构。**
