# Git-Native Project Memory Protocol（Git 原生项目记忆协议）

> P0 experiment, 2026-08-29. This protocol adapts ideas from current open-source agent-memory systems to the existing ChatGPT ↔ GitHub ↔ Work Buddy workflow.
>
> ## 归属说明（2026-08-30，agent-lab Issue #2）
>
> 本文件是 **P0 记忆协议草案**，**仍然有效**，保留其独有内容：§4 什么值得记、§5 记录语义、§6 写入时机、§10 P0 成功标准、§11 rollout、§12 设计参考。
>
> **四层记忆模型（Global / Project / External / Session）与路由规则的 canonical 归属是** `architecture/MEMORY_ARCHITECTURE.md` 与 `architecture/MEMORY_ROUTER.md`；本文件不再重复定义。
>
> ⚠️ **SUPERSEDED**：本文件 §2 只定义了 Global / Project 两层。External 与 Session 两层以 `architecture/MEMORY_ARCHITECTURE.md` §2.3 / §2.4 为准。
> §9 的仓库隔离原则仍有效，并由 `architecture/MEMORY_ARCHITECTURE.md` §4 的 canonical 表细化。

## 1. 目的（Purpose）

GitHub 是项目状态的持久真相来源。Memory 不是聊天历史的副本，而是经过策展、带版本的事实的表示，必须跨对话、跨 agent 存活。

本协议刻意采用 file-first 与 Git 原生。P0 不需要向量数据库、图数据库、托管记忆服务或新 runtime。

**统一 Agent 入口与自动写回义务由 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 定义。** 本文件负责"什么值得记、如何记录、何时写回"等语义细则。

## 2. 范围模型（Scope model）

### Global / Hub memory（全局/中心记忆）

`agent-lab` 只存跨项目知识：

- 项目注册表与边界
- 协作协议
- 跨项目协调规则
- 指向项目状态的指针

它不得复制详细的业务/项目知识。

### Project memory（项目记忆）

每个真实项目仓库拥有自己的持久记忆。最小 canonical 集合是：

- `PROJECT_CONTEXT.md` — 项目是什么、边界、持久假设
- `CURRENT_STATE.md` — 当前状态与已验证事实
- `NEXT_WORK.md` — 当前优先级与下一步动作
- `DECISIONS.md` — 重要决策与理由
- `CHANGELOG.md` — 按时间排列的实质性变更

已有同等角色的项目文件可以保留；不要为了满足本协议而制造重复真相源。

## 3. 记忆层级（Memory hierarchy）

使用简单的三级模型：

```text
ACTIVE MEMORY（活跃记忆）
  CURRENT_STATE.md + NEXT_WORK.md
  ↓ 最先加载
PROJECT MEMORY（项目记忆）
  PROJECT_CONTEXT.md + DECISIONS.md
  ↓ 相关时加载
HISTORY / EVIDENCE（历史/证据）
  CHANGELOG.md + tasks + reviews + experiments + code/data
  ↓ 需要时检索
```

## 4. 什么值得记（What deserves memory）

满足以下至少一条时保存事实：

1. 它改变未来工作的执行方式。
2. 它解释一个持久的项目决策。
3. 它记录一个不应被重新发现的已验证结果。
4. 它定义项目边界或不变量。
5. 它记录未来工作必须顾及的未决问题。
6. 它沉淀一条可复用的协作规则。

不保存：

- 普通对话填充物
- 无决策的瞬时想法
- 源材料的重复副本
- secrets、凭证、token 或个人敏感数据

## 5. 记忆记录语义（Memory record semantics）

可行时，持久事实应携带：

- `date`: 事实何时生效
- `status`: `active`（活跃）、`superseded`（已被取代）、`blocked`（阻塞）或 `verified`（已验证）
- `source`: issue / commit / file / experiment
- `confidence`: 不确定性重要时标 `high`、`medium` 或 `low`

对会变化的事实，不得静默覆盖历史。把旧事实标记为 superseded，并记录新事实与理由。

## 6. 写入策略 — 自动化、基于检查点（Write policy）

记忆**不是** Human 提醒任务。

通用规则由 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 定义：

> **每个 Agent 必须在有意义的持久变更后自动运行 Memory Sync Gate。**

正常生命周期：

```text
Task / Research / Discussion（任务/研究/讨论）
→ 有持久变更？
→ 经 MEMORY_ROUTER 路由
→ 写入 canonical owner
→ commit / Issue 证据
→ 验证
```

### 6.1 强制记忆同步触发器（Mandatory Memory Sync triggers）

以下任一情况后运行 Memory Sync Gate：

- 持久事实确立
- 持久决策做出/否决
- 项目状态变化
- Plan 创建/变更/完成
- Issue 创建/开始/完成/阻塞/验证/关闭
- Buddy commit/push
- ChatGPT Review
- 研究或实验达到可复用结论
- 已知事实被证据取代
- 新 Unknown 或矛盾
- 协作协议变更

### 6.2 No-op 是合法结果

如果工作单元没有产生持久信息，Agent 必须显式把结果标为：

`Memory Sync: NOT NEEDED`

不得为了证明检查过记忆而制造无意义提交。

### 6.3 写入权限（Write authority）

- **ChatGPT**：判断什么持久、路由、写 canonical 记忆、验证写入。
- **Buddy**：在项目仓库写可直接验证的执行事实；报告 commit/证据；不晋升 inference、不改 Plan。
- **Read-only Agent（只读 Agent）**：需要写入时必须输出 `MEMORY_SYNC_REQUIRED`，且不得声称同步成功。

### 6.4 纯研究工作（Research-only work）

并非每个持久结论都需要 GitHub Issue 或 Work Buddy 执行。当 ChatGPT 只在研究、比较、评估或设计方法——且不需要仓库变更或外部执行时——工作可以留在 ChatGPT 侧，直到形成持久结论。

结论一旦持久，必须按 `architecture/MEMORY_ROUTER.md` 路由进相应的 Global / Project / External 记忆。如果它改变项目 Plan，走 Plan 变更控制流程；不得静默替换路线。

只有存在实际可执行的仓库/项目变更、实验或其他可审计动作时才创建 Buddy 任务。

## 7. 读取策略（Read policy）

进入项目时，按 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 执行强制 bootstrap 序列。

关键原则仍是选择性加载：

1. 项目上下文
2. 当前状态
3. 导航
4. Active Plan
5. 相关决策
6. 当前 Issue
7. 相关证据 / 代码 / 实验历史

默认不加载整个仓库。

## 8. Agent 职责（Agent responsibilities）

### ChatGPT

- 判断什么足够持久值得记住
- 评审记忆是否与已验证的项目现实一致
- 解决矛盾
- 适当时创建下一个任务
- **持久变更后自动执行 Memory Sync**

### Work Buddy

- 执行前读取项目记忆
- 把项目记忆当上下文，不当作发明需求的许可
- 报告 commit/结果证据
- 可写执行可验证的事实
- 可提出记忆更新建议
- **执行检查点后自动执行 Memory Sync**

### GitHub

- 存储持久工件
- 提供 commit 历史与溯源
- 当记忆与对话冲突时是真相来源

## 9. 项目隔离（Project isolation）

记忆默认按仓库定界。

```text
agent-lab
  └── cross-project memory only（仅跨项目记忆）

-quantitative-trading
  └── quantitative memory only（仅量化记忆）

-ai-content
  └── content-project memory only（仅内容项目记忆）

-commercial-radar
  └── commercial-radar memory only（仅商业雷达记忆）
```

跨项目事实只有在真正关乎协作系统或项目组合时才属于 `agent-lab`。业务项目的事实必须留在该业务仓库。

## 10. P0 成功标准（P0 success criteria）

如果一次全新对话后：

- ChatGPT 能从 Git 重建项目当前状态，不依赖旧聊天历史。
- Buddy 能用同样的项目上下文执行新 Issue。
- 评审者能区分当前事实与已被取代的决策。
- 没有引入第二套并行任务/知识系统。
- 记忆文件保持小到可人工检视。
- **Human 不需要提醒 Agent 同步持久记忆。**

则本协议视为成功。

如果这些标准在大规模下失效，再评估检索层（如 QMD/vector search、Mem0 或 Graphiti）。在 file-first 基线被测量之前，不引入这些依赖。

## 11. P0 rollout（落地步骤）

1. `agent-lab`：协议定义与模板 — 当前步骤。
2. 在一个项目仓库验证协议。
3. 把最小必需记忆文件应用到其余项目仓库。
4. 运行跨对话恢复测试。
5. 之后才考虑自动化记忆提取/检索。

## 12. 设计参考（Design references）

- Letta / MemFS: Git-backed Markdown memory, selective loading, versioned memory.
- Mem0: explicit memory extraction and scoped recall; useful later if manual memory curation becomes a bottleneck.
- Graphiti: temporal facts and provenance; useful later if project history becomes too complex for flat Markdown.
- Agent Memory Techniques: useful comparative map of memory patterns and evaluation approaches.

目标不是复刻任何框架。目标是采纳最小有用的想法，同时保持现有 GitHub 原生工作流。

## 13. GMR v0.2 — Session Trigger Monitor and Promotion Gate（会话触发监视与晋升门）

> **Status: FROZEN / IMPLEMENTED 2026-09-02.** 本节是 GMR v0.2 约定的运行时行为操作叠加层。它不取代 `architecture/MEMORY_ARCHITECTURE.md` 的四层归属规则或 `architecture/MEMORY_ROUTER.md` 的路由程序。

### 13.1 每回合触发扫描（Per-turn Trigger Scan）

每个对话回合接收一次轻量语义扫描。扫描是评估步骤，不是 Git 写入。

```text
Conversation turn（对话回合）
  ↓
Lightweight Trigger Scan（轻量触发扫描）
  ├─ 无触发 → 继续
  └─ 有触发 → Memory Evaluation（记忆评估）
```

强触发包括：

- 显式持久决策/规则（`决定 / 以后 / 采用 / 不再 / 确定 / 作为标准`）；
- 推翻或取代（`推翻 / 改成 / 刚才不对`）；
- 项目状态变化（completed / failed / published / verified / restarted）；
- 确立稳定定义或不变量；
- 新的未决 Unknown 或冲突；
- 持久工作流规则/偏好；
- 工作单元完成。

### 13.2 全量检查检查点（Full-check checkpoints）

以下自然边界必须执行完整 Memory Sync Gate：

- 工作单元完成；
- 用户确认结论；
- 把工作交给 Buddy 之前；
- 项目/话题切换；
- session 中断或结束。

### 13.3 触发不等于写回（Trigger is not Writeback）

触发只启动 Memory Evaluation。评估必须先应用持久影响测试（Durable Impact Test）和 `architecture/MEMORY_ROUTER.md`，然后才能写入。

```text
Trigger（触发）
  ↓
Durable Impact Test（持久影响测试）
  ↓
Classify: Fact / Decision / State / Knowledge / Unknown（分类）
  ↓
Route: task / project / global（路由）
  ↓
Promotion policy: L0 / L1 / L2 / L3（晋升策略）
  ↓
CREATE / UPDATE / SUPERSEDE / RESOLVE
```

### 13.4 持久影响测试（Durable Impact Test）

只有当"不保留它可能导致未来 agent 做出错误判断、重复已完成工作或违背既定方向"时，持久记忆才是正当的。

Observation ≠ Knowledge（观察 ≠ 知识）。Idea ≠ Decision（想法 ≠ 决策）。Candidate ≠ Durable Memory（候选 ≠ 持久记忆）。

助手的提案不会仅仅因为助手提出了它就成为持久决策。按风险等级需要用户接受和/或证据。

### 13.5 晋升策略（Promotion policy）

| Level | Policy（策略） | Typical examples（典型例子） |
|---|---|---|
| L0 | 不写入 | 瞬时讨论、被否决的想法、一次性上下文 |
| L1 | 自动写入 | 低风险状态、下一步工作、明确的实验状态/结果 |
| L2 | 提案 | 可复用 Knowledge、Decision、Supersede、Unknown 裁决 |
| L3 | Human 确认 | Global Memory、跨项目规则、重大架构/方向、冲突仲裁 |

### 13.6 范围与历史护栏（Scope and history guardrails）

每次写回都有明确范围：`task | project | global`。

Project Memory 绝不自动晋升为 Global Memory。Global Memory 绝不静默改变 Project Memory。

核心记忆没有 DELETE 迁移。变化的事实通过 `SUPERSEDE` 表示，保留溯源与历史。同一事实的重复检测必须幂等，不得制造重复 canonical 条目。

### 13.7 运行时职责（Runtime responsibility）

**有 Git 写权限时，ChatGPT 是 Memory Owner**：它执行触发评估、晋升判断、路由、直接 Git 写回与写后验证。Buddy 保持 execution-only，不作为记忆同步的中间人。

如果 ChatGPT 没有写权限，必须输出 `MEMORY_SYNC_REQUIRED`，且不得声称同步成功。

### 13.8 回合结束不变量（End-of-turn invariant）

持久变更后返回最终响应之前，ChatGPT 必须已完成 Memory Sync Gate。响应可以报告：

- `Memory Sync: DONE`
- `Memory Sync: NOT NEEDED`
- `Memory Sync: BLOCKED`

目标是：常规持久记忆同步零 Human 提醒。
