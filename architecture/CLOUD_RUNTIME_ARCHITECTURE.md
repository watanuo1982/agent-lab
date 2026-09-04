# Cloud Agent Runtime Architecture v0.3

> Status: ADOPTED（已采纳）
> Date: 2026-09-03
> Scope: Global Agent System architecture

## 1. 目的

Cloudflare 是 Agent 系统的**云端运行时层（Cloud Runtime Layer）**。它不是一个新业务项目，也不取代 GitHub、Buddy 或 ChatGPT。

runtime 实现维护在一个独立于 `agent-lab` 的**项目仓库**中。`agent-lab` 保持为治理 / Agent Hub / 全局记忆层，不成为执行仓库。

架构刻意**Free-first（免费层优先）**：初始 runtime 必须能在 Cloudflare Free plan 上实现。只有当实际工作负载超出免费层限额，或需要 Sandbox/Containers 时，才引入付费能力。

## 2. 架构演进 — 保留历史，不重写历史

云端运行时层**不是原始 AI 协作设计的一部分**。它是在早期以 GitHub 为中心的协作模型暴露出对持久云端运行时状态、工作流、受控能力、以及最终不应依赖 Buddy/本地准备的自主生产执行的需求之后，作为架构演进而引入的。

历史顺序是：

```text
原始协作模型
Human → ChatGPT → GitHub Memory → Buddy / project execution
                         │
                         │ 后续演进
                         ▼
                 Cloud Runtime layer
                         │
                         ▼
                    core-agent
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
     domain runtimes（领域运行时）  other capabilities（其他能力）
```

因此：

- 描述 CoreAgent 之前系统的历史文档保持为历史事实；
- 后来的 CoreAgent / Cloud Runtime 架构不得向后投射进那些文档；
- `core-agent` 是**演进的 infrastructure 层**，不是原始假设；
- 引入 Cloud Runtime 是一次记录在案的刻意架构变更，而原始模型仍可通过 Git 历史审计。

## 3. 系统职责边界

| 层 | Canonical 职责 |
|---|---|
| Human | 现实世界动作、业务决策、外部审批 |
| ChatGPT | 推理、研究、架构、内容、决策、任务合同、评审 |
| Agent Hub (`agent-lab`) | 治理、全局记忆、项目注册表、跨项目协调与协议 |
| Project GitHub repositories | Canonical 项目代码、配置、项目 Memory、状态、决策、证据与任务历史 |
| CoreAgent (`core-agent`) | 统一云端 Agent Runtime：身份、持久运行时状态、工作流编排、受控能力/工具路由与有边界的执行协调 |
| Domain Runtimes | 领域特定的确定性执行能力（例如内容或量化执行）；它们不因运行在 Cloudflare 上就自动成为通用自主 agent |
| Buddy | 明确 GitHub Issue 合同的开发/本地执行；不是必需的生产 runtime 依赖 |
| Cloudflare | CoreAgent 与 domain runtimes 的托管/runtime 基座 |

硬规则：**GitHub 是 Canonical；Cloudflare 是 Runtime；Buddy 是 Execution；ChatGPT 是 Reasoning Owner。**

## 4. 仓库边界

`agent-lab` 是 **Agent Hub**，不是 Cloud Runtime 实现项目。

Cloud Runtime 实现位于独立仓库：

`watanuo1982/-agent-runtime`

该项目内的第一个 runtime 目标是：

`core-agent`

这一分离防止全局记忆/治理仓库变成治理与执行混杂的仓库。

## 5. CoreAgent 与 Domain Runtime

当前架构使用严格的两级 runtime 边界：

```text
ChatGPT
   │ reasoning / decision / review（推理 / 决策 / 评审）
   ▼
CoreAgent
   │ unified runtime / context / orchestration（统一运行时 / 上下文 / 编排）
   ├── GitHub context
   ├── durable state（持久状态）
   ├── Workflow
   ├── controlled MCP/tool capabilities（受控 MCP/工具能力）
   └── bounded routing（有边界路由）
        │
        ├───────────────┬────────────────
        ▼               ▼
AI Content Runtime   Quant Runtime
(领域执行)            (领域执行)
```

**CoreAgent 不是第二个业务领域 agent。** 它应当协调并暴露有边界的能力，而不是独立发明内容、交易策略或业务决策。

Domain Runtime 不自动等于 Domain Agent。保持确定性/领域执行位于 CoreAgent 之下，除非单独的架构评审证明确有 agent 级身份、规划与隔离的真实需求。

避免这个反模式：

```text
ChatGPT → CoreAgent → Generic Proxy → Domain Runtime → another Agent → tools
```

每增加一层都必须有被证明的职责；MCP 必须保持为能力接口，不能成为通用代理或隐藏的第二套编排系统。

## 6. Runtime 原语

### 6.1 Worker

用于无状态 HTTP/API 入口、路由、认证与小型转换。

### 6.2 Agent / Durable Object

用作 Agent 的持久身份与运行时状态。

Agent 本地状态可包括：
- agent 身份
- 当前任务/会话
- 小型结构化状态
- 调度
- workflow 引用
- runtime 检查点

Agent 状态**不是** canonical 项目 Memory。

### 6.3 Workflow

用于多步、长时运行、可重试或可检查点的流程。

典型模式：
`CoreAgent -> Workflow -> steps/checkpoints/retry -> result`

### 6.4 D1

只用于真正需要跨 runtime 组件的关系型存储的共享结构化数据。

不得把 D1 当作大型行情/历史数据集的倾倒场。

### 6.5 R2

用于大对象/文件：CSV、Parquet、PDF、图片、视频、模型工件与大型实验输出。

### 6.6 Queues

用于解耦确有帮助的异步工作负载。不因为 Queues 存在就引入。

### 6.7 Sandbox / Containers

可选的付费能力边界，用于隔离 Linux 执行、Python/Node/Shell、重计算与不可信或重依赖工作负载。

当前 CoreAgent 基线不需要 Sandbox。

## 7. Agent 拓扑

从恰好一个通用 runtime Agent 开始：

`core-agent`

它的职责是 runtime 基础设施，不是业务领域推理。

未来领域 Agent 只有在 CoreAgent 稳定且存在被证明的隔离/所有权需求之后才可引入。

不要为了包装现有确定性 Domain Runtime 而创建 `content-agent`、`quant-agent` 或其他领域 Agent。

## 8. Canonical Memory 边界

```text
GitHub Memory (canonical)
        |
        +---- ChatGPT reasoning
        |
        +---- CoreAgent / Cloud Runtime
        |
        +---- Buddy execution
```

Cloudflare 可以缓存或持久化运行时状态，但持久知识/决策/项目事实最终必须同步到相应的 GitHub canonical 位置。

绝不在 Cloudflare 中创建第二套独立 Memory 系统。

## 9. 任务模型

所有持久、可审计的工作保持 Issue-first，遵循现有 Agent Git Memory Contract。

概念上，runtime 任务使用：

```yaml
task_id: unique
agent_id: core-agent
objective: explicit objective（明确目标）
input: structured input（结构化输入）
permissions: explicit capability boundary（明确能力边界）
execution_mode: sync | workflow | sandbox
status: READY | IN_PROGRESS | DONE | BLOCKED
result: structured result（结构化结果）
artifacts: references to canonical artifacts（canonical 工件引用）
audit: execution metadata（执行元数据）
```

这只是概念性 runtime 合同；除非有具体的 runtime 需求被证明并单独获批，否则不在 GitHub Issues 之外创建竞争性任务系统。

## 10. 身份与权限

每个 Agent 有明确的 `agent_id` 与能力边界。

默认姿态：
- GitHub: read（读）
- Cloudflare: read（读）
- 外部系统: read（读），除非明确需要
- Sandbox: 禁用，直到需要

写入/部署/删除/外部副作用需要明确的能力授予，且必须可审计。

## 11. Secrets

Secrets 是 runtime 凭证，不是 Memory。

绝不把 secrets、token、API key 或凭证提交进 GitHub Memory 或项目 Markdown。

Secrets 必须通过适当的 runtime/本地 secret 机制注入，并只暴露给需要的最小组件。

## 12. Free-first 政策

初始目标：

```text
Workers
+ Agents / Durable Objects / SQLite
+ Workflows
+ MCP
+ D1 (small structured data，小型结构化数据)
+ R2 (small/moderate files，中小型文件)
+ Queues (when justified，有理由时)
```

不抢先升级或添加付费基础设施。

只在以下情况升级：
1. 实测工作负载超出免费限额；
2. 所需能力在 Free 上不可用；或
3. 生产可靠性要求足以支撑。

Sandbox/Containers 明确视为后续付费边界。

## 13. 部署阶段

### P0 — Architecture（架构）
Status: ADOPTED

- 职责边界
- canonical Memory 规则
- 身份/权限模型
- 仓库边界
- 任务模型
- Free-first 规则

### P1 — Cloudflare account audit（账号审计）

对可用产品、当前资源、plan/限额与权限的只读盘点。无部署变更。

### P2 — Core Agent

部署带身份、健康检查、最小持久状态与简单任务生命周期的 `core-agent`。

### P3 — GitHub integration（GitHub 集成）

连接 runtime 与 GitHub，同时保持 GitHub 为 canonical。

### P4 — Workflow

证明一个可重试/可检查点的多步任务。

### P5 — MCP client capability（MCP 客户端能力）

通过白名单 MCP client 证明有边界的能力消费。未来面向 ChatGPT 的 MCP server 是单独的架构步骤，P5 不隐含它。

### P6 — First real workloads（首批真实工作负载）

用有边界的真实工作负载验证 runtime。Quant 与 AI Content 现在是同一 runtime 架构下的两条不同领域执行路径。

### P7 — Sandbox (conditional，有条件)

只有当真实工作负载证明 Buddy/本地执行或 Workers 不足时才引入。

### P8 — Domain Agents (conditional，有条件)

只有当公共 runtime 稳定且存在被证明的隔离/所有权价值时，才把 `core-agent` 拆分为领域 Agents。

## 14. 运行安全

runtime 的设计必须保证 Cloudflare 故障不会摧毁 canonical 项目知识。

对每个持久执行：
- 运行时状态可以留在 Cloudflare；
- canonical 决策/结果/工件引用回归 GitHub；
- 执行可审计；
- 未知/冲突事实不被静默晋升为 canonical 事实。

## 15. 反模式

不引入：
- 仅为托管 Agents 的 VPS
- Kubernetes
- 自管 Redis/Postgres
- 无被证明检索需求的向量 DB
- CoreAgent 验证前的多个领域 Agents
- 无限制 shell 执行
- 自动生产部署
- 作为第二 Memory 来源的 Cloudflare
- 与 GitHub Issues 竞争的第二套任务系统
- `agent-lab` 内的 Cloud Runtime 实现代码
- 通用 MCP 代理 / 任意 MCP 端点转发
- CoreAgent 与 Domain Runtime 之间不必要的 runtime 层

## 16. 决策

**ADOPTED（已采纳）**：Cloudflare 作为演进的 Cloud Runtime Layer 纳入全局 Agent 系统架构，其实现隔离在独立的 `-agent-runtime` 项目中。

CoreAgent 之前的历史协作模型作为历史保持有效，不被重写。当前架构是一次明确的演进：**ChatGPT → CoreAgent → 有边界的 Domain Runtime → GitHub canonical 工件/状态**，Human 保留现实世界权威，Buddy 保持执行/开发角色而非生产 runtime 依赖。
