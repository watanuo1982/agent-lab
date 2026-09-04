# ARCH-001 — 多 AI 协作操作架构 v2 — 初稿

> 状态：**工作初稿 / 未冻结**
> 日期：2026-09-04
> 规范工作区：`agent-lab`
> 对应评审 Issue：#15

## 1. 目的

建立一套适用于 **Human + 多个 AI Agent + GitHub + Runtime** 的通用工作架构。

目标不是再造一个复杂的 Agent 平台，而是把当前已经实际运行的工作方式抽象出来，并让 ChatGPT、Buddy、其他 AI、GitHub 和 Cloud Runtime 各自承担正确的职责。

核心判断：

> **Agent 可以在对话层平等参与，但能力、权限和权威可以不同；GitHub 是持久化共享状态，Runtime 是执行基础设施，Human 保留最终权威。**

本文件只是多 AI 共评审的初稿，尚未形成最终规范。

## 2. 总体框架

```text
                               HUMAN
                       目标 / 判断 / 批准
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
         ChatGPT             Buddy              Other AI
       研究 / 推理 /         全端执行 /          专业能力 /
       架构 / 审核           环境运维             特定执行
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
                      Agent 协作 / 协议层
             Task / Handoff / Status / Result / Review
                                │
                                ▼
                 ┌─────────────────────────┐
                 │       GITHUB            │
                 │   共享控制面 / 权威状态  │
                 └────────────┬────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
          PROJECT REPOS                RUNTIME LAYER
       项目事实 / 素材 / 记忆          Cloud / Local / Remote
       决策 / 任务 / 产物              执行 / 自动化 / 服务
                │                           │
                └─────────────┬─────────────┘
                              ▼
                       Evidence / Logs
                              │
                              ▼
                     Verification / Review
                              │
                              ▼
                      State / Memory 更新
```

## 3. 六层结构

### L0 — Human 层

负责：
- 目标
- 优先级
- 战略判断
- 最终决策
- 高风险/不可逆操作批准
- 架构最终批准

Human 不需要成为每一个执行动作的中间人。

### L1 — Agent 层

ChatGPT、Buddy、其他 AI 都可以成为**一等参与者**。

“一等参与者”意味着，在自身能力和授权范围内，Agent 可以：
- 直接接受 Human 工作；
- 独立分析和提出方案；
- 与 Human 对话；
- 与其他 Agent 协作；
- 执行工作；
- 产生证据；
- 审核或质疑其他 Agent 的结果。

但一等参与者不意味着能力相同，也不意味着权威相同。

### L2 — Agent 协作 / 协议层

定义 Agent 之间如何协作：
- Task
- Handoff
- Status
- Result
- Evidence
- Review
- Disagreement
- Escalation
- Approval

GitHub Issue 继续作为默认的持久化任务契约；Issue Comment、Commit、Artifact 等承担过程和结果记录。

### L3 — Canonical State 层

GitHub 是整个系统的**持久化共享状态和控制面**。

这里保存：
- 项目 Context / State
- Task
- Artifact
- Decision
- Durable Memory
- Provenance
- Evidence 指针
- Audit History

任何 Agent 的私有上下文都不是 Canonical State。

### L4 — Runtime / Execution 层

包括：
- Cloudflare
- 本地计算机
- 远程机器
- 浏览器环境
- API / MCP
- 其他执行环境

Runtime 负责“把事情做出来”，而不是决定“什么是真实状态”。

### L5 — Evidence / Verification / Governance 层

核心链路：

```text
Claim → Evidence → Verification → Canonical State
```

例如：
- Commit SHA
- Test Result
- Deployment ID
- Runtime Log
- Generated Artifact
- 可复现的执行结果

“我做完了”只是 Claim，不是 Evidence。

## 4. 四个必须分开的概念

### Capability ≠ Permission

Agent 有能力做某事，不代表它被允许做。

### Permission ≠ Authority

Agent 有权限修改某个 Repo，不代表它拥有修改项目规则或架构的权威。

### Authority ≠ Canonical Ownership

Agent 可以在授权范围内作出判断，但最终的持久化事实仍应进入 Canonical State。

### 对话平等 ≠ 能力平等

ChatGPT、Buddy、Other AI 都可以直接和 Human 对话，但 Buddy 可以拥有明显更强的本地电脑、浏览器、云环境、部署、文件和应用操作能力。

## 5. Agent 模型初稿

| 参与者 | 主要能力假设 | 不自动拥有 |
|---|---|---|
| Human | 目标、判断、最终批准 | — |
| ChatGPT | 研究、推理、架构、规划、内容、审核、已有工具支持下的执行 | Human 最终权威 |
| Buddy | 全端执行、环境操作、实现、诊断、修复、部署、直接对话 | Canonical Truth / 自动架构权威 |
| Other AI | 根据自身能力提供专业推理或执行 | 其他 Agent 的私有上下文 |

注意：以上只是初始假设，最终角色必须以 Round 1 的实际 Capability Statement 为依据。

## 6. 整体工作链路

```text
Human Intent
      ↓
Task / Decision
      ↓
Agent 接手
      ↓
Plan / Reason
      ↓
Execute
      ↓
Artifact + Evidence
      ↓
Verify
      ↓
Review / Challenge
      ↓
Canonical State
      ↓
Memory / Next Work
```

核心不是“谁来执行”，而是：

> **任何 Agent 都可以成为工作入口或执行者，但结果必须最终回到共享的 Canonical State。**

## 7. Task / Handoff 初稿

一个可以跨 Agent 传递的 Task 至少包含：

1. Objective
2. Scope / Non-scope
3. Context 指针
4. Acceptance Criteria
5. Expected Artifact
6. Permission / Authority Constraints
7. Verification Requirements
8. Reporting Format
9. Status

Handoff 不应该依赖隐藏的聊天上下文，而应该指向 GitHub 中的 Canonical State。

允许 Agent → Agent 直接交接，但必须遵守 Task Contract 和权限边界。

## 8. Agent 生命周期

```text
Receive
  ↓
Understand
  ↓
Plan / Propose
  ↓
Execute（如果获得授权）
  ↓
Verify
  ↓
Report Evidence
  ↓
Review / Challenge
  ↓
Promote Canonical State
```

对于确定性很强的工作，优先使用 Workflow，而不是为了“AI 化”而增加 Agent 自主性。

## 9. Agent 之间允许不同意见

多 Agent 架构不能假设所有 Agent 都会得出相同结论。

出现冲突时，应明确记录：

```text
Claim A
Evidence A

Claim B
Evidence B

Conflict / Unknown

Resolution Owner
Resolution Evidence
Final Decision
```

不能因为一个 Agent 声音更大就自动成为真相来源。

涉及架构、重大权限或不可逆行为的冲突，最终升级给 Human，除非此前已经明确授权给某个 Agent。

## 10. Failure / Repair 模型

如果 Agent 具备足够执行能力，可以在**原有授权范围内**自行诊断和修复。

不能因为发现问题就自动扩大自己的权限。

```text
Failure
  ↓
Diagnose
  ↓
Classify
  ├─ transient → 按策略 Retry
  ├─ known repair → 授权范围内 Repair
  ├─ insufficient evidence → Investigate
  └─ authority conflict → Escalate
  ↓
Verify
  ↓
Report Evidence
```

这点对 Buddy 特别重要：

> Buddy 的价值不仅是“执行任务”，还包括在授权范围内完成执行、验证、诊断、修复和环境管理的完整闭环。

## 11. Memory 与现有 GMR 的关系

现有 GMR v0.2 继续作为 Memory 基线。

ARCH-001 不自动推翻 GMR；只有明确发生冲突的条款才进入后续 Supersession / Revision。

基本原则继续保持：

- Session 不等于 Durable Memory
- Project Memory 与 Global Memory 隔离
- Memory 必须有 Provenance
- 有效的长期信息才进入 Durable Memory
- 冲突不能静默覆盖
- 不确定状态进入 Unknown
- Agent 不因为“发现信息”就自动拥有 Global Memory

多 Agent 架构增加的是：

> **多个 Agent 可以共同产生 Memory Candidate，但 Canonical Memory 仍必须按照统一规则进入 Git。**

## 12. Git / Runtime 边界

### GitHub 负责

- Durable State
- Task
- Project Memory
- Decision
- Artifact
- Provenance
- Audit

### Runtime 负责

- Process State
- Queue
- 临时文件
- Runtime Logs
- 执行环境
- Secrets
- Deployment

Runtime 的结果如果具有长期价值，必须通过 Evidence 回写 Git。

因此：

> **Runtime 可以消失，项目仍然应该尽可能从 Git 恢复。**

## 13. Invocation 模型

Invocation 是机制，不是架构角色。

可以来自：
- Human
- GitHub Event / Webhook
- Schedule
- API
- Runtime Event
- Agent Direct Action

因此系统不应该绑定某一种触发方式。

## 14. 权限与安全

默认原则：

1. Agent 不得自动扩大权限。
2. 遵循 **Least Authority**，而不是简单追求 Least Capability。
3. Read / Write 权限尽量明确。
4. 跨项目修改必须拥有明确的跨项目授权。
5. 高风险、不可逆、平台敏感操作原则上需要 Human Approval，除非明确授权。
6. Secrets 不进入 Git Memory。
7. 不确定和冲突必须显式暴露。

## 15. 可替换性

系统不应该依赖某一个 Agent 才能运行。

### ChatGPT 被替换

新的 Agent 读取 Git Canonical State 后应该可以继续工作。

### Buddy 被替换

只要新的 Agent 具备所需执行能力，也应该可以从 Git 接续任务。

### Runtime 被替换

Cloudflare 不可用时，项目 Durable State 不应该因此丢失，并应尽可能切换其他 Runtime。

### Session 被替换

新会话不应该依赖旧聊天记录才能恢复项目。

## 16. 整体治理流程

```text
Round 1
Capability Statements
        ↓
Round 2
各 Agent 独立提出架构方案
        ↓
Round 3
Cross-Agent Conflict Review
        ↓
Round 4
ChatGPT 综合形成 Consolidated Draft
        ↓
Round 5
Buddy 做 Implementation Feasibility Review
        ↓
Round 6
Human Final Decision
        ↓
Architecture Freeze
        ↓
Round 7
拆解为具体 Implementation Issues
        ↓
Pressure Test
        ↓
只有在真实失败证据出现时修改架构
```

## 17. 对现有三个项目进行压力测试

### AI Content

重点验证：
- Git → Cloud Runtime
- AI 执行
- Runtime 持久化
- Git Writeback
- Review
- Retry / Failure
- Evidence

P04 已经是目前最重要的真实验证案例。

### Quantitative Trading

重点验证：
- Research State
- Data State
- Strategy Decision
- Agent Handoff
- Execution Boundary
- Memory Isolation

### Commercial Radar

重点验证：
- Research
- Evidence
- 多 Agent 协作
- Opportunity State
- Validation

## 18. 当前不做什么

暂不因为“架构看起来更完整”而增加：

- 新 AI OS Repo
- 第二套 Task Tracker
- Vector DB / Graph DB
- 强制 Orchestrator
- 自动跨项目 Memory Promotion
- 没有实际需求的 Always-on Agent
- 隐藏在 Agent 私有上下文中的关键共享状态

原则：

> **先证明现有架构失败，再增加新的基础设施。**

## 19. Round 2 待解决问题

1. 什么标准才算“一等 Agent”？
2. 哪些 Agent 行为可以无需 Human Approval？
3. Agent 能否授权另一个 Agent？如果能，授权边界是什么？
4. Agent-to-Agent Handoff 最小协议是什么？
5. 哪些 Runtime State 必须持久化？
6. 什么级别的 Evidence 才足以推动 State Promotion？
7. 什么情况下 Disagreement 必须阻塞执行？
8. 多 Agent 并发修改 Git 时如何处理？
9. GMR v0.2 哪些规则需要针对多 Agent 扩展？
10. P04 / Quant / Commercial Radar 分别应该承担哪些 Acceptance Tests？

## 20. 当前状态

**WORKING DRAFT — 未冻结。**

这份文档现在的作用是给所有参与的 AI 一个共同讨论底稿，而不是直接成为最终架构规范。

在 Round 1 Capability Statements 收齐、Round 2 各 Agent 独立提出方案之前，不进行最终架构冻结，也不批量拆 Implementation Issues。
