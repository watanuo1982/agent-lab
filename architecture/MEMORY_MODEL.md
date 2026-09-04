# Memory Model（记忆模型） v0.1 — Memory / Skill / Asset（记忆 / 技能 / 资产）

> 2026-08-30。全局架构决策，提炼自 Agent Skills 研究与 `punk-ip-illustrations` / 开源 Agent Skills 模式。

## 1. 核心区分

智能体操作系统包含三个不同的概念：

| Layer | Question | Meaning |
|---|---|---|
| **Memory（记忆）** | “我们知道 / 决定了什么？” | 持久的事实、决策、历史、规则、上下文 |
| **Skill（技能）** | “我们怎么做？” | 被触发的程序化能力：工作流、证据、校验、交接 |
| **Asset（资产）** | “我们应该复用什么？” | 已确认、带版本的输出或资源，后续工作应引用而非重建 |

**硬性规则：** `Skill ≠ Memory ≠ Asset`。

## 2. 关系

```text
                 Agent Operating Layer
                         │
              ┌──────────┴──────────┐
              │                     │
            SKILL                MEMORY
              │                     │
        “怎么做”                 “知道什么”
              │                     │
              └──────────┬──────────┘
                         ▼
                       ASSET
                         │
                 “复用什么成果”
```

一个 Skill 可以读取 Memory 并引用 Asset。一条 Memory 记录可以指向一个 Asset 或一个 Skill。Asset 本身并不会仅仅因为被某个 Skill 消费就变成了 Skill。

## 3. Memory（记忆）

规范归属仍由 `architecture/MEMORY_ARCHITECTURE.md` 定义：

- 全局记忆 Global Memory → `agent-lab`
- 项目记忆 Project Memory → 项目仓库
- 外部记忆 External Memory → `agent-lab/external/`
- 会话上下文 Session Context → 通常不持久化

Memory 记录的是**我们工作的状态**，而不是外部文档的副本。

## 4. Skill（技能）

Skill 是一个会在任务中改变智能体行为的程序化包。

最小概念契约：

```text
Identity
Trigger
Goal
Inputs
Procedure
Evidence
Validation
Failure
Handoff
Cost
Expected Benefit
Evaluation
```

当前 Agent Skills 约定强化这种分离：Skill 以 `SKILL.md` 为核心，而脚本、参考资料与资产按需通过渐进式披露单独加载。 citeturn0search0turn0search5

Skill 应当包含**流程而非知识**。稳定的参考资料、模板与可复用文件，若可以单独加载，就不应重复写进程序化指令中。

## 5. Asset（资产）

Asset 是一个带有身份与生命周期的可复用制品。

示例：

- 账号 / 头像 / 角色身份
- 品牌规则或视觉资产
- 研究 schema 或报告模板
- 已验证的实验 protocol
- 量化因子定义
- 内容模板

最小概念契约：

```text
identity
 type
 owner_scope
 status
 version
 source
 created_at
 confirmed_at
 used_by
 supersedes
```

推荐生命周期：

```text
draft → review → confirmed → active → deprecated
```

通常只有 `confirmed` / `active` 的 Asset 才应被视为生产工作的规范可复用输入。

## 6. Scope（范围）

### 全局资产 Global Assets

只有真正跨项目的资产才属于 `agent-lab`，例如：

- Skill Contract
- Evidence semantics（证据语义）
- 跨项目 review protocol
- 协作模板

### 项目资产 Project Assets

项目级可复用资产留在所属项目仓库中。

示例：

- `ai-content`：账号身份、视觉身份、内容模板
- `commercial-radar`：证据 schema、雷达评分模型、校验 protocol
- `quantitative-trading`：因子定义、回测 protocol、实验 schema

不要仅仅因为另一个项目将来可能复用，就把项目资产搬进 Global。只有在明确的跨项目决策之后才提升其层级。

## 7. 来源与状态（Provenance and status）

Asset 必须能与外部建议区分开来。

- 外部来源 → `External Memory`
- 我们的评估 → `Memory`
- 已采纳的可复用制品 → `Asset`

Git 历史仍是最终的来源层。不要静默替换规范的 Asset；应通过 supersede / 版本化来取代它。

## 8. 渐进式披露原则（Progressive disclosure principle）

不要默认把所有 Skill、Memory 文件或 Asset 都加载进上下文。

当前 Agent Skills 指南采用渐进式披露：先加载目录元数据，激活时再加载完整 Skill 指令，然后仅在需要时加载参考资料 / 脚本 / 资产。这明确是为了控制上下文成本。 citeturn0search0turn0search11

我们自身的实现在架构层面应遵循同一原则：

```text
Need → route → load relevant Skill
     → read relevant Memory
     → load required Asset
     → execute
     → validate
     → record durable result
```

## 9. 决策状态（Decision status）

本文档定义了 `agent-lab` 系统的**全局架构规则**。

这并不意味着每个项目都必须立即创建 Asset 目录或转换现有文件。在明确的项目级决策改变它们之前，现有项目结构仍保持规范。

## 10. 研究来源（Research provenance）

该模型提炼自：

- Agent Skills 开放规范 / 渐进式披露模式
- 兼容 Anthropic / Microsoft 的 Skill 目录约定
- `adrianpunk/punk-ip-illustrations`：持久身份资产、确认状态、可复用内容资产，以及交付感知的生成
- `agent-lab` 中持续进行的 Skill Architecture Benchmark 工作

外部来源是设计的证据；它们本身不是项目事实。所采纳的规则是本文档中定义的区分。
