# AI OS Architecture v1.0

> Status: Drafted from architecture audit, 2026-08-30
> Canonical owner: `agent-lab`
> Scope: Cross-project AI working system for Human + ChatGPT + WorkBuddy/Codex + GitHub
>
> **与 ARCH-001 的关系（2026-09-04 起）**：全局架构的 canonical baseline 是已冻结的 `architecture/ARCH-001_FINAL_ARCHITECTURE.md`（Human 批准，Issue #15 评论 5538205132）。本文件保留为冻结前的系统描述与行业对齐参考；凡与 ARCH-001 冲突之处（权威模型、层结构），以 ARCH-001 为准——ARCH-001 定义了本文件未覆盖的 Runtime 层与 Evidence/Verification 层（见 `architecture/CLOUD_RUNTIME_ARCHITECTURE.md`），并统一 `DONE`/`VERIFIED` 完成语义。

## 1. 目的

本文档定义现有 AI 工作系统的架构。它**不**引入任何新产品、仓库、记忆服务、向量数据库或 agent runtime。

设计原则是：

> **GitHub 是持久的项目状态；agent 是可替换的工人；Human 始终是目标、高影响决策与审批的权威。**

即使模型、agent、connector 或 runtime 更换，架构也必须保持可用。

## 2. 系统模型

```text
                         HUMAN（人）
                   目标 / 判断
                         |
                         v
                  +-------------+
                  |  Reasoning  |
                  |  ChatGPT    |
                  +------+
                         |
              上下文 / 任务 / 评审
                         |
                         v
                  +-------------+
                  |  agent-lab  |
                  | Control Hub |
                  +------+
                         |
                    GitHub 状态
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      Quant          AI Content      Commercial Radar
        |                |                |
        +----------------+----------------+
                         |
                    Agent 工人
                  WorkBuddy / Codex / other
                         |
                    工具 / 技能
                         |
                       动作
                         |
                       工件
                         |
                       评审
                         |
                       决策
                         |
                       记忆
```

## 3. 十个核心对象

| 对象 | 含义 | Canonical 归属 |
|---|---|---|
| Goal（目标） | Human 想达成什么 | Human / 全局或项目上下文 |
| Context（上下文） | 当前运行所需的信息 | Session + 项目/全局记忆 |
| Task（任务） | 带验收标准的有边界工作单元 | GitHub Issue |
| Agent（智能体） | 能推理/执行的工人 | ChatGPT / WorkBuddy / Codex / 未来 agent |
| Tool（工具） | agent 调用的外部能力 | Connector / MCP / API / 本地工具 |
| Skill（技能） | 一类工作的可复用流程 | 项目文档 / agent 技能 |
| Permission（权限） | agent 允许读/写/做什么 | 工具/账号/仓库边界 |
| Artifact（工件） | 工作的持久产出 | 项目仓库 |
| Review（评审） | 对工件或结果的 Human/agent 验证 | Issue / 评审工件 |
| Decision（决策） | 改变未来工作的持久判断 | `DECISIONS.md` 或 Hub 决策记录 |

## 4. Memory OS 与 Agent OS 分离

### Memory OS（记忆操作系统）

现有四层模型保持 canonical：

```text
Global（全局）/ agent-lab
Project（项目）/ 项目仓库
External（外部）/ 外部知识指针
Session（会话）/ 临时上下文，默认不持久化
```

见 `architecture/MEMORY_ARCHITECTURE.md` 与 `architecture/MEMORY_ROUTER.md`。

### Agent OS（智能体操作系统）

执行生命周期是：

```text
Goal（目标）
 -> Context（上下文）
 -> Task（任务）
 -> Agent（智能体）
 -> Tool/Skill（工具/技能）
 -> Action（动作）
 -> Artifact（工件）
 -> Review（评审）
 -> Decision（决策）
 -> Memory（记忆）
```

因此记忆是经过评审的工作的产出，不是自动的对话转储。

## 5. Canonical 所有权

- 跨项目运行规则属于 `agent-lab`。
- 项目事实、研究、实验与决策属于相关项目仓库。
- 外部事实保持为外部引用，直到我们独立采纳某个判断或决策。
- 当前可执行工作属于 GitHub Issues。
- Git 历史是最终历史记录。
- 聊天/会话历史不是 canonical 项目数据库。

不引入第二套任务系统。

## 6. 任务合同

一个任务应当能让另一个 agent 在不重建整个对话的情况下执行。至少应标识：

1. Objective（目标）
2. Scope / non-scope（范围 / 非范围）
3. 相关上下文指针
4. Acceptance criteria（验收标准）
5. 预期工件
6. 相关时的权限/安全约束
7. 汇报格式
8. 当前状态

任务应指向 canonical 文件，而不是复制其内容。

## 7. Agent 角色分离

当前优先分工：

- **Human**：目标、战略选择、不可逆/高影响审批、自动化不安全的平台原生动作。
- **ChatGPT**：研究、综合、架构、任务分解、评审与跨项目推理。
- **WorkBuddy**：任务合同下的仓库本地执行与实现。
- **Codex/其他编码 agent**：适当时承担编码密集型执行。
- **GitHub**：持久状态、任务合同、工件、历史与审计轨迹。

**权威模型（对齐冻结的 ARCH-001 §3）**：Human 是唯一最终权威；agent 之间权威对等、能力不对称——没有 agent 命令另一个 agent（跨 agent 交互是请求/指派/接受）；权威永不可传递转让（执行者不能把自己不具备的权限授予另一个执行者）。替换一个 agent 不得要求把项目记忆迁移进该 agent。

## 8. Workflow 与 Agent 的取舍

当顺序和验收标准已知时，优先确定性 workflow。

当路径需要动态探索、判断、工具选择或适应时，使用 agent。

例子：

- 量化回测与固定研究协议：workflow 优先。
- AI 内容生产管线：workflow 优先 + agent 辅助。
- Commercial Radar 机会发现：agent 密集探索 + 确定性证据门。

不要因为 agent 能做某件事就把任务 agent 化。

## 9. 记忆写入策略

现有 `agent-lab` 记忆模型保持刻意保守。

```text
Session 观察
      |
      v
候选知识
      |
   分类
      |
+-----+-------------------+
|                         |
无未来价值                有未来价值
|                         |
丢弃                      路由
                          |
              +-----------+-----------+
              |           |           |
           Global      Project     External
```

一个持久记忆候选应当有：

- 溯源/来源；
- 清晰的归属；
- 存在理由（对未来工作为何重要）；
- 相关时的状态/证据语义；
- 若可能过时，有过时处理（supersession）。

外部内容绝不因为某个 agent 复述了它而被晋升。

## 10. 治理与权限

最小规则集：

1. 读取范围不应宽于任务所需。
2. 写入范围通常应限于目标仓库。
3. 跨项目变更只在改变共享基础设施或跨项目协作时才属于 `agent-lab`。
4. 不可逆/高影响动作与有已知安全边界的平台动作需要 Human 批准。
5. Agent 必须为持久工作报告 commit/工件标识。
6. 未知或冲突状态必须显性呈现，不得猜测。

## 11. 溯源与信任

每个持久声明应可追溯到以下之一：

- Human 指示；
- 项目工件 / commit / Issue；
- 外部一手来源；
- 显式标注的 inference/assumption/experiment。

适用时使用现有证据词汇：

`[Fact]`、`[Inference]`、`[Assumption]`、`[Experiment]`、`[Unknown]`。

外部信息可以影响决策，但不会自动成为项目事实。

## 12. 评审与评估

评审是架构的一部分，不是可选的最后一步。

对 agent 工作，至少评估：

- 是否解决了既定任务？
- 是否遵守了范围？
- 是否修改了正确的 canonical 文件？
- 是否保持了项目边界？
- 结果是否可复现/可审计？
- 是否有决策或教训应晋升为持久记忆？

系统最终应记录轻量评估结果，但 **v1 不需要单独的可观测性栈**。

## 13. 行业对齐 — 我们采纳什么

当前外部设计强化了若干原则：

- OpenClaw 将策展的长期记忆与情景材料分离，把写入/溯源视为安全边界，并在模型判断周围使用确定性门。我们采纳其原则，不采纳其 runtime 或存储栈。
- OpenAI Agents SDK 将对话式 Session 状态与较长寿命的记忆分离，并把 agents、tools、handoffs、guardrails、human-in-the-loop 与 tracing 作为 runtime 原语提供。
- MCP 正在向更无状态的协议核心、显式 Tasks、更强的授权与路由演进。我们把 MCP 视为工具集成边界，不作为我们的记忆或项目状态系统。

References checked 2026-08-30:
- OpenClaw memory architecture: https://github.com/openclaw/openclaw/blob/main/docs/concepts/memory-architecture.md
- OpenAI Agents SDK: https://openai.github.io/openai-agents-python/
- OpenAI Agents SDK Sessions: https://openai.github.io/openai-agents-js/guides/sessions/
- MCP 2026-07-28 specification announcement: https://blog.modelcontextprotocol.io/posts/2026-07-28/

## 14. v1 的刻意非目标

**不要**为了让架构显得更高级而添加以下任何一项：

- Mem0 或其他外部记忆服务
- 向量数据库 / 图数据库
- 第二套任务跟踪器
- 新的 AI-OS 仓库
- 自主记忆晋升
- 常驻自主 agent
- 自动跨项目写入
- 每个对话的中央副本
- 强制的 OpenClaw runtime

只有当具体工作负载证明出现当前架构无法解决的失败时，这些才可能变得合适。

## 15. 压力测试标准

如果这三个项目能同时运行而无状态泄漏，架构即被视为健康：

### Quantitative Trading（量化交易）

研究状态、策略参数、实验与交易决策留在 `-quantitative-trading` 内。跨项目 AI OS 规则留在 `agent-lab`。

### AI Content（AI 内容）

内容资产、平台实验、发布状态与安全边界留在 `-ai-content` 内。Human-only 平台动作保持显式。

### Commercial Radar（商业雷达）

机会证据、评分、实验与业务验证留在 `-commercial-radar` 内。外部市场知识只被引用，不被静默转化为项目事实。

通过条件：

> 一个新 agent 能通过读取 canonical 恢复路径进入任意一个项目，执行一个有边界的 Issue，产出一个持久工件，并完成回报——不需要隐藏的 ChatGPT 历史，也不改变其他项目的状态。

## 16. 下一步审计目标

架构刻意停留在 v1。下一步工作是测试系统，而不是扩展它：

1. 通过 `agent-lab` 的跨项目任务交接。
2. Agent 替换：WorkBuddy 不可用 → 另一个工人能从 GitHub 恢复。
3. 冷启动恢复：新 session → 无聊天历史恢复 canonical 项目状态。
4. 记忆晋升：有用的决策/教训只在评审后晋升。
5. 权限边界：项目本地工人不能意外改写另一个项目。
6. 冲突处理：矛盾状态以 `[Unknown]` 显性呈现直到解决。

只有这些测试产生的失败才应触发 v1.1 变更。
