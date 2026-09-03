# Universal Git Memory Contract v1.1

> **适用对象：任何会读取本工作体系 Git/GitHub 的 Agent。**
> ChatGPT、Buddy/WorkBuddy 以及未来接入本体系的 Agent 都必须遵守。
>
> 本文件解决两个长期问题：
> 1. Agent 开始工作时，不需要 Human 反复告诉它“先读哪些记忆”；
> 2. Agent 产生了值得长期保存的信息时，不需要 Human 再提醒“去上传记忆”。

## 1. Universal Entry Rule

只要 Agent：

- 开启一个新的工作 Session；或
- 读取 `agent-lab`；或
- 读取任何本体系业务项目仓库；或
- 收到“检查 Git 的记忆 / 检查 Git 记忆 / 从 Git 恢复上下文 / 继续项目”等请求；

就自动进入 **Git Memory Mode**。

### 1.1 新 Session 的强制启动

**Git Memory Bootstrap 是每个新工作 Session 的默认启动动作，不是一个等待 Human 触发的可选动作。**

因此：

- 即使 Human 没有说“检查 Git 的记忆”，只要 Session 开始并准备处理本体系工作，Agent 仍必须先执行 Global Bootstrap；
- 不得把 ChatGPT session memory、旧聊天、模型参数记忆或“我大概记得”当成 Git Bootstrap 的替代品；
- 不得因为当前问题看起来简单而跳过 Bootstrap；
- 若当前项目尚未明确，只完成 Global Bootstrap，不猜项目；
- 一旦项目明确，立即继续 Project Bootstrap。

### 1.2 Human 不需要指定启动清单

Human 可以只说：

> **检查 Git 的记忆。**

这句话本身已经授权 Agent 执行本协议的**读取与一致性检查**，无需 Human 再提供文件名、启动提示词或恢复步骤。

如果之后 Human 指定项目，例如“进入量化项目”，Agent 应在已完成 Global Bootstrap 的基础上自动执行该项目的 Project Bootstrap。

### 1.3 两阶段启动

```text
New Session
    ↓
MANDATORY Global Bootstrap
    ↓
识别 / 等待项目上下文
    ↓
Project Bootstrap（项目明确后）
    ↓
Plan Continuity Check
    ↓
Task Resolution
```

如果项目尚未明确，不猜项目、不强行读取业务仓库；先完成 Global Bootstrap，并等待后续项目上下文。

## 2. Global Bootstrap — 所有 Agent 统一入口

进入 Git Memory Mode 后，默认先读取 `agent-lab` 的：

1. `AGENT_GIT_MEMORY_CONTRACT.md`（本文件）
2. `README.md`
3. `PROJECTS.md`
4. `CURRENT_STATE.md`
5. `NEXT_WORK.md`
6. `MEMORY_ARCHITECTURE.md`
7. `MEMORY_ROUTER.md`
8. `MEMORY_PROTOCOL.md`
9. `UNKNOWN_REGISTRY.md`
10. `SESSION_BOOTSTRAP.md`
11. `PLAN_PROTOCOL.md`

按需读取：

- `PROJECT_CONTEXT.md`
- `INBOX.md`
- `external/`
- 相关历史 / 测试记录

**不得为了“完整”而扫描整个仓库。**

## 3. Project Bootstrap — 进入具体项目后自动执行

项目一旦由 Human、Issue、INBOX 或当前工作上下文明确，Agent 自动读取该项目的：

1. `README.md`
2. `PROJECT_CONTEXT.md`（如存在）
3. `CURRENT_STATE.md`
4. `NEXT_WORK.md`
5. 唯一 Active Plan（如存在）
6. `MEMORY_INDEX.md`（如存在）
7. `DECISIONS.md`（如存在）
8. `GITHUB_WORKFLOW.md`（如存在）
9. 当前阶段直接相关的 Issue / research / evidence / experiment

不需要 Human 再说“把这些都读一遍”。

## 4. Plan Continuity — 默认继续，不重新发明

如果存在 `ACTIVE` / `APPROVED` Plan：

> **默认继续原 Plan。**

Agent 必须恢复：

```text
PROJECT
ACTIVE PLAN
PLAN ID
PLAN VERSION
PLAN STATUS
PLAN OBJECTIVE
CURRENT PHASE
CURRENT ISSUE
ISSUE STATUS
COMPLETED PLAN STEPS
CURRENT PLAN STEP
NEXT PLAN STEP
LATEST RELEVANT COMMIT
KEY DECISIONS
OPEN UNKNOWNS
BUDDY STATUS
CONFLICTS
```

任何“更好的方案”只能形成 Change Proposal，不能静默替换现有 Plan。

标准变更链：

`Evidence → Evaluation → Change Proposal → Approval → New Plan Version`

## 5. Task Authority — 任务不从聊天里漂移

- GitHub Issue = 唯一具体执行任务合同。
- `CURRENT_STATE.md` = 当前状态 canonical owner。
- `NEXT_WORK.md` = 导航，不独立派发任务。
- `BUDDY_TASK_CURRENT.md` = 指针，不独立派发任务。
- `INBOX.md` = 跨项目通知指针，不复制任务正文。
- Session memory / 聊天记录 = 线索，不覆盖 Git canonical facts。

如果这些来源冲突：

> **输出 `MEMORY BOOTSTRAP BLOCKED`，不猜、不执行、不修改。**

## 6. Mandatory Memory Sync — 记忆写回不是 Human 的提醒事项

### 6.1 核心规则

> **Agent 对长期记忆拥有“自动检查义务”，而不是等待 Human 提醒。**

每个有实质性工作结果的交互、任务阶段结束、Issue 状态变化、Review 完成、Plan 步骤完成或外部研究形成稳定结论后，Agent 必须自动运行 **Memory Sync Gate**。

Human 不需要说：

- “记得更新 Git”
- “上传一下记忆”
- “把刚才的结论写进去”
- “同步 CURRENT_STATE”

这些属于 Agent 的协议责任。

### 6.2 Memory Sync Gate

结束一个有实质内容的工作单元前，Agent 必须逐项检查：

| 检查项 | 是 → 必须做什么 |
|---|---|
| 是否产生新的长期事实？ | 写入唯一 canonical owner |
| 是否改变项目当前状态？ | 更新 `CURRENT_STATE.md` |
| 是否改变下一步路线？ | 更新 `NEXT_WORK.md` / Plan（按 authority） |
| 是否形成/否决关键决策？ | 更新 `DECISIONS.md` |
| 是否产生可审计研究/实验结果？ | 写入 Project evidence / research，并更新状态指针 |
| 是否出现 Unknown / 冲突？ | 登记 `UNKNOWN_REGISTRY.md`，必要时阻断 |
| 是否创建/完成/阻塞 Issue？ | Issue + 状态与项目状态保持一致 |
| 是否完成 Plan step？ | 更新 Plan progress / project state |
| 是否有跨项目协作规则变化？ | 更新 `agent-lab` 对应 canonical 文件 |
| 是否只是临时思考、闲聊或一次性过程？ | **不写入长期记忆** |

### 6.3 写入原则

记忆写回必须遵守：

1. **Canonical owner only**：一个事实只写一个权威位置，其他地方只留指针。
2. **Evidence first**：尽可能附 Issue / commit / file / experiment 来源。
3. **不要把 Inference 升格为 Fact**。
4. **Unknown 不猜**，登记并保留裁决状态。
5. **旧事实不删除**；变化时标记 `SUPERSEDED` 或按项目既有历史规则处理。
6. **不上传聊天全文**；只上传经提炼的 durable memory。
7. **不上传秘密、凭证、token 或敏感信息。**

## 7. Role-specific Write Responsibility

### ChatGPT

ChatGPT 负责：

- 判断什么值得长期记住；
- 形成/审核 Plan；
- Review 后确认事实、决策与状态；
- 自动把确认后的 durable memory 写回正确 Git 仓库；
- 不等待 Human 提醒。

### Buddy / WorkBuddy

Buddy 负责：

- 执行 Issue；
- 在 commit / push 后写入可由执行直接证明的事实；
- 更新项目状态中的执行结果；
- 不自行把 Inference 升为 Fact；
- 不自行裁决 Unknown；
- 不改变 Plan；
- 完成 Issue 后向 Issue 写回 DONE / BLOCKED + evidence + commit SHA。

ChatGPT Review 后，再把“已验证结论”提升为 canonical project memory。

### 只读 Agent

如果 Agent 没有写权限：

- 仍必须执行 Memory Sync Gate；
- 发现需要写回时，必须明确输出 `MEMORY_SYNC_REQUIRED` 及建议写入的 canonical owner；
- **不得声称“已同步”。**

## 8. Checkpoint 触发器

以下任一事件自动触发 Memory Sync Gate：

- 用户确认一个长期原则 / 决策；
- 新 Plan 建立或 Plan 版本变化；
- 当前阶段变化；
- Issue 创建、开始、完成、阻塞、验证或关闭；
- Buddy commit / push 完成；
- ChatGPT Review 完成；
- 新实验 / 回测 / 真实外部验证完成；
- 新研究结论达到可复用程度；
- 已知事实被新证据推翻；
- 新增 Unknown / 冲突；
- 跨项目协作协议发生变化。

## 9. End-of-Turn Rule

只要本轮对话发生了上述任一变化，Agent 在向 Human 返回最终结果前必须：

1. 运行 Memory Sync Gate；
2. 必要时完成 Git 写回；
3. 验证写回成功；
4. 在最终回复中简要说明 `Memory Sync: DONE / NOT NEEDED / BLOCKED`。

**不得把“以后再上传”当作默认行为。**

若没有任何 durable change，则 `Memory Sync: NOT NEEDED`，不产生无意义提交。

若当前 Agent 没有写权限，必须输出 `MEMORY_SYNC_REQUIRED`。

## 10. Separation of Concerns

```text
Session Context
    ↓ extract
Durable Fact / Decision / State / Evidence / Unknown
    ↓ route
MEMORY_ROUTER
    ↓ canonical owner
Global / Project / External / Issue
    ↓ verify
Git commit / Issue history
```

Memory 不是聊天备份；Memory 是经提炼、可追溯、可恢复的长期工作状态。

## 11. Compatibility with Existing Protocols

本文件是所有 Agent 的**统一入口合同**；已有协议继续负责具体细节：

- `MEMORY_ARCHITECTURE.md`：四层记忆模型与 canonical ownership
- `MEMORY_ROUTER.md`：信息应该写到哪里
- `MEMORY_PROTOCOL.md`：什么值得记、记录字段、写入时机
- `SESSION_BOOTSTRAP.md`：Session 恢复与 Plan continuity 的详细检查
- `PLAN_PROTOCOL.md`：Plan 版本与变更控制
- 各项目 `GITHUB_WORKFLOW.md`：项目级 Issue 执行细则

如果协议之间出现冲突：

1. 更具体的 canonical owner 规则优先；
2. Git history 是最终事实来源；
3. 无法裁决则 `MEMORY BOOTSTRAP BLOCKED` / `[Unknown]`，不猜。

## 12. Minimum Human Interaction

Human 只需要负责：

- 提供真实外部动作；
- 做需要 Human 决定的业务裁决；
- 通知 Buddy 有新 Issue（按现有工作流）；
- 在需要时批准 Change Proposal。

Human **不负责记忆管理提醒**。

因此标准启动可以极简：

```text
New Session
    ↓
Agent 自动 Global Bootstrap
    ↓
Human: 进入量化项目 / P03 / 商业雷达
    ↓
Agent 自动 Project Bootstrap + Plan Continuity
    ↓
Agent 执行/继续工作
    ↓
Agent 自动 Memory Sync
```

## 13. Success Criteria

本协议成立的最低标准：

1. **每个新 Session 默认执行 Global Bootstrap**，不依赖 Human 的“检查 Git 记忆”提示；
2. 任一遵约 Agent 听到“检查 Git 的记忆”即可自动启动，无需额外提示词；
3. Human 进入具体项目后无需重复给读取清单；
4. 已确认 Plan 不因换 Session 被静默替换；
5. 有 durable change 时 Agent 自动写回 Git；
6. 无 durable change 时不产生垃圾提交；
7. 无写权限时不会假装同步成功；
8. 所有项目仍保持 repository-level memory isolation。
