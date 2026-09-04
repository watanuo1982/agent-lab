<!--
CANONICAL FILE — ARCH-001 Final Architecture (FROZEN).
Transcribed verbatim (no content changes) from watanuo1982/agent-lab#15, comment 5537869348,
by buddy-local per the Buddy Review Task (comment 5537871089); 5 required corrections applied
per Freeze Prep (comment 5538032086, PR #22).
Status: FROZEN — Human Final Approval recorded in Issue #15 comment 5538205132 (2026-09-04).
This file is the canonical architecture baseline. Any edit must go through the normal PR path
with required check `validate-memory` and requires a Human-approved architecture change.
语言版本说明：本文件为 ARCH-001 Final Architecture 的中文版（2026-09-04 buddy-local 中文化，
语义与冻结英文原版逐句对应；机器锚点、编号、代码块保持原样）。语义以本文件为准，翻译歧义时
以冻结原版（git 历史）为裁决依据。
-->

# ARCH-001 Round 5｜最终架构 + 调整计划

> 状态：**FROZEN（已冻结）— canonical 架构基线**（Human Final Approval：Issue #15 评论 5538205132，2026-09-04）
> 历史沿革：本文件由 Round 5 Candidate（评论 5537869348）逐字转录并应用 5 项 Freeze Prep 修正（PR #22）后，经 Human 批准冻结。
> Open items（buddy-local fine-grained PAT 创建 / classic PAT 轮换）不因冻结自动完成，见 §14 与 `architecture/IDENTITY_TOKEN_POLICY.md`。

## 1. 核心架构

系统划分为五个职责：

- **Human（人）** — 最终权威；定义意图，批准架构变更与高风险/不可逆动作。
- **Agent（智能体）** — 智能层；推理、规划、分析、提案、评审、质疑与决策支持。各 Agent 权威对等、能力不对称。
- **GitHub** — canonical 状态 + 治理面；持久化任务/状态/决策/记忆/工件/证据/溯源，并承载可强制执行的仓库规则。
- **Runtime（运行时）** — 执行面；Local Runtime、Cloudflare CoreAgent/Runtime 或其他获授权的 runtime 执行有边界的工作并产出执行证据。
- **Evidence / Verification（证据/验证）** — 证明层；runtime/CI/工具产出证据，独立验证对其进行评估，然后 canonical 状态才被晋升。

不可协商原则：

`Capability ≠ Permission ≠ Authority ≠ Canonical Ownership`（能力 ≠ 权限 ≠ 权威 ≠ canonical 所有权）

`Agent ≠ Runtime`；`Runtime ≠ Truth`（运行时 ≠ 真相）；`Agent claim ≠ Evidence`（Agent 声明 ≠ 证据）。

## 2. 目标架构

```text
                         HUMAN（人）
                 最终权威 / 审批
                           │
                           ▼
                  ┌─────────────────┐
                  │   AGENT LAYER   │
                  │ ChatGPT / Other │
                  │ Reason / Plan / │
                  │ Review / Challenge
                  └────────┬────────┘
                           │ 工作合同（Work Contract）
                           ▼
              ┌───────────────────────────┐
              │     GITHUB CANONICAL      │
              │ Task / State / Decision   │
              │ Memory / Artifact / Rules │
              │ Provenance / Evidence     │
              └────────────┬──────────────┘
                           │ 授权范围（authorized scope）
                  ┌────────┴────────┐
                  ▼                 ▼
           Local Runtime      Cloudflare CoreAgent
                  │                 │
                  └────────┬────────┘
                           ▼
                 执行 + 证据（Execution + Evidence）
                           │
                           ▼
                 机器验证（Machine Verification）
                           │
                           ▼
                 独立 Agent 评审（Independent Agent Review）
                           │
                ┌──────────┴──────────┐
                │                     │
             accepted              rejected
                │                     │
                ▼                     ▼
       Canonical State（canonical 状态）   纠正 / 重试
                │
                ▼
          记忆晋升（Memory Promotion）
             (GMR v0.2)
```

## 3. 权威模型

- Human 拥有最终决策权威。
- Agent 之间不互相命令。
- 权威永不可传递转让：执行者不能把自己不具备的权限授予另一个执行者。
- GitHub 是 canonical 记录/强制执行面，不是语义决策者。
- Runtime 只在明确的工作合同（Work Contract）范围内拥有执行权威。

## 4. 工作合同 / Issue-first

现有 **Issue-first** 工作流仍是任务载体，因为它已在实际运行。

最小合同字段：

- `task_id`
- objective（目标）
- acceptance criteria（验收标准）
- `scope`（范围）
- `non_scope`（非范围）
- `stop_condition`（停止条件）
- `not_authorized_to_decide`（未授权决策项）
- `target_repo`（目标仓库）
- `capability_manifest_ref`（能力清单引用）
- 授权执行者/runtime
- 所需证据
- 审批要求
- 载体 = GitHub Issue

禁止隐性范围扩张。缺失授权/条件含糊一律归入 `Blocked` / `[Unknown]`。

## 5. 执行 / Runtime 边界

Buddy Local 是依赖本地机器的执行体，不假定其具备生产级 SLA。

Cloudflare CoreAgent/Runtime 是云端执行基础设施；其已部署/运行状态是既定基线，不作为每个架构任务的重复验证对象。

Runtime 状态是易失的。关键工作流状态不得只存在于 agent/session/runtime 上下文中；持久状态必须回归 GitHub。

## 6. Evidence-first（证据优先）

每个可执行任务都产出符合 `architecture/EXECUTION_RECEIPT.md` 的 Execution Receipt（执行回执）：

`task_id / executor / execution_id / timestamp / commit_sha / artifact / artifact_hash / exit_status / environment / produced_by`

`agent-declared`（Agent 自声明）只是 claim 级证据，单独不能満足 DoD（完成定义）。

完成语义：

```text
DONE     = executor claim（执行者声明）
VERIFIED = machine verification（机器验证）
           ∧ independent/non-executor review（独立/非执行者评审）
           ∧ required Human approval（必需的 Human 批准）
           ∧ canonical state promotion（canonical 状态晋升）
```

执行成功、工件正确、架构正确三者始终是独立判断。

## 7. 治理

GitHub 应该机械性地拒绝它能够拒绝的东西：

1. 受保护的 canonical 分支
2. 在所有权边界重要处设置 CODEOWNERS
3. 必需的 validator 检查
4. 结构化的 Issue/工作合同要求
5. fail-closed 的 canonical 不变量
6. 不存在 agent 的常规绕过路径

GitHub 强制结构；Agent 评估语义；Human 决定高风险/不可逆事项。

## 8. 身份 / 权限

最低架构要求：

- Buddy Local 与 Buddy Cloud/CoreAgent 必须可独立辨识。
- 二者不得共享不可问责的高权限身份。
- 凭证应按仓库/项目定界并最小权限。
- Secrets 永不进入 Issues、commits 或持久记忆。
- 完整的权限治理（矩阵、生命周期、轮换、撤销与审批边界）属于后续治理轮次；若身份分离已有证据，则不阻塞架构冻结。

## 9. Agent 间交互

```text
REQUEST → ACCEPT → EXECUTE → REPORT（请求 → 接受 → 执行 → 报告）
                         ↓
                      EVIDENCE（证据）
                         ↓
                     REVIEW（评审）
                   ↙         ↘
                ACCEPT       REJECT（接受 / 拒绝）
                  ↓             ↓
              PROMOTE       CORRECT/RETRY（晋升 / 纠正重试）
```

Agent 通过 canonical 工作状态通信，不通过隐藏记忆。分歧保持显式，直到由证据、评审或 Human 决策解决。

Fast Path（快路径）可以产生候选推理/检查；只有 Slow Path（慢路径）可以变更 canonical 状态。Fast Path 的实质性结果必须在任务关闭前晋升。

## 10. 记忆 / GMR v0.2

GMR v0.2 保持不变。

分层：

- Session State — 一次性的 agent 本地上下文
- Task State — 当前工作合同/执行
- Project State — 仓库范围的持久状态
- Global Memory — 受治理的跨项目记忆
- Historical Evidence — 可审计的执行记录

项目隔离仍按 仓库/领域 + 现有记忆路由 执行。ARCH-001 不创建第二套记忆系统。

## 11. 可替换性 / 恢复

稳定接口是：

`工作合同 + Canonical 状态 + 证据合同 + 记忆合同 + 授权边界`

如果 Buddy Local 消失，另一个获授权执行者可以从 GitHub 恢复。如果 Cloudflare CoreAgent 消失，另一个获授权 runtime 可以接管。如果 ChatGPT 消失，另一个推理 Agent 可以消费 canonical 状态。

可替换性必须定期实测，而不是只写在文档里。

## 12. 并发 / 最小化

当前规模不足以支撑新建 orchestrator、队列或数据库。

必要时使用任务级串行化、乐观 Git 并发、显式冲突/Blocked 状态、短生命周期执行与 canonical 回写。

除非有实测的运行证据证明 GitHub 原生协作不足，否则不新增基础设施。

---

# ARCH-001｜实施 / 调整计划

架构现在是**目标模型**。实施必须分阶段、有边界。

### Phase A — agent-lab canonical 化

1. 用 Human 批准后的最终架构状态替换 ARCH-001 Issue 正文中过时的阶段描述。
2. 将最终架构加入为 canonical 仓库文档。
3. 增加一份简洁的实施地图，链接治理、回执、身份、记忆与 runtime 文档。
4. GMR v0.2 保持不变，除非另有明确决策取代特定规则。
5. 项目注册状态：`-agent-runtime` 已在 `PROJECTS.md` 注册（行 `agent-runtime`，ACTIVE，Project Memory PENDING；commit `28a181f8`，2026-09-02）——无需修复注册。Round 4 的「[Conflict] 未注册」结论在此撤回，属测量误差。Phase C 审计应跟踪其 Project Memory `PENDING → ADOPTED` 的晋升。

### Phase B — 协议对齐

5. 将 `AGENTS.md`、`architecture/AI_OS_ARCHITECTURE.md`、`architecture/CLOUD_RUNTIME_ARCHITECTURE.md`、`architecture/AGENT_GIT_MEMORY_CONTRACT.md`、`architecture/PLAN_PROTOCOL.md`、`CURRENT_STATE.md`、`NEXT_WORK.md`，以及 `architecture/ARCH-001_FINAL_ARCHITECTURE.md`、`architecture/IDENTITY_TOKEN_POLICY.md`、`architecture/EXECUTION_RECEIPT.md` 与冻结架构对齐。
6. 移除过时的角色/流程描述，而不是维持多个并行竞争模型。
7. 使 Issue-first + 工作合同 + 证据回执成为唯一正常任务生命周期。每个 canonical 文件必须登记在 README 文件地图中。

### Phase C — 项目集成

对每个活跃项目仓库（quantitative-trading、AI-content、commercial-radar 及其他活跃项目）：

8. 按冻结的角色边界与 GitHub 工作流审计项目。
   - `quantitative-trading`：先只读审计。不得修改生产交易逻辑；架构符合性检查不得触碰冻结的 V7.1 管线。
   - `commercial-radar`：对 buddy-local 而言当前状态为 `[Unknown]`——任何变更前先盘点。
9. 只增加项目本地必需的最小合同/状态文件。
10. 保持项目隔离；不把全局记忆复制进项目仓库。
11. 不为架构符合性而改动生产逻辑，除非项目审计发现具体违规。

### Phase D — 治理加固

12. 开展专门的权限治理轮次：权限矩阵、token 生命周期、轮换/撤销、项目范围与 Human 审批边界。
13. 保持身份归属与最小权限作为强制基线。
14. 定期运行可替换性/交接测试。

### Phase E — 收口

15. 验证 canonical 状态、证据与项目迁移状态。
16. 仅在 Human 批准与架构冻结后关闭 ARCH-001；后续工作转为有边界的实施 Issue。

## 13. 明确推迟项

- 新数据库 / 队列 / orchestrator
- 第二套任务系统
- 新的 AI OS 仓库
- 向量/图记忆系统
- 全局聊天归档
- 冻结前的全量权限治理重设计
- 已运行 Cloudflare CoreAgent 的重新部署/重新验证

## 14. 当前验收状态

本候选之前已有证据：

- P0 Validator 修复 + M2 Execution Receipt
- M0 GitHub 治理基础
- M5 Local ↔ Cloudflare CoreAgent 跨 runtime 交接
- M6 执行身份分离 — **PARTIAL（部分完成）**：buddy-cloud 已平台级分离（GitHub App `ai-content-cloud-runtime`，权限 `contents:write` + `metadata:read`，签名 bot commit）；buddy-local fine-grained PAT 创建是未决的 Human UI 动作（GitHub 无创建 API——实测 POST 404；规格见 `architecture/IDENTITY_TOKEN_POLICY.md` §3.2）。M6 不得被描述为完全完成。
- GMR v0.2 保留

冻结时登记的 open items（跟踪中，不声明已完成）：

- buddy-local fine-grained PAT 创建 — Human UI 动作，规格见 `architecture/IDENTITY_TOKEN_POLICY.md` §3.2；验证协议待执行。
- classic PAT 分离后的轮换/弃用（见 `architecture/IDENTITY_TOKEN_POLICY.md` R-M6-2）。

冻结记录：

**Buddy 评审完成 — PASS WITH CONDITIONS（Issue #15 评论 5537995684）；5 项必需修正已全部经 PR #22 应用。Human Final Approval 已记录（Issue #15 评论 5538205132，2026-09-04）：ARCH-001 已 FROZEN，为 canonical 架构基线。实施按阶段（Phase A–E）经 Issue-first 任务合同推进。**

状态：**FROZEN — CANONICAL ARCHITECTURE BASELINE（已冻结 — canonical 架构基线）**。
