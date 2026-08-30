# S1 — Global 冷启动复验回答（被测 Agent 原文）

> 被测材料：`/tmp/fix`（修复后 Hub 快照，已排除 `memory-tests/`）
> 隔离上下文：全新，无聊天历史、无本地 memory
> 判定：8/8 PASS，0 FABRICATED

---

我已读取 `/tmp/fix` 下全部 9 个允许文件（完整排除了 `memory-tests/`）。以下逐条作答。

**G1.** 这个工作体系包含哪几个项目仓库？各自一句话定位？

记录存在**两处冲突**，须如实说明：
- 权威项目注册表 `PROJECTS.md` 登记 **4 个**（ACTIVE）：
  - `agent-lab`（= `watanuo1982/agent-lab`）：跨项目协作基础设施 / Agent Hub。
  - `watanuo1982/-quantitative-trading`：量化研究 / 实盘策略。
  - `watanuo1982/-ai-content`：AI 内容生产。
  - `watanuo1982/-commercial-radar`：商业机会雷达 / ToC 选品。
- `README.md` 仓库边界另列 **5 个**，多出 `-work-buddy-lab`（历史 Work Buddy 工具协作实验，标 FROZEN）。
- 两者矛盾已登记为 `MEMORY_ARCHITECTURE.md` §10 **U-F**：`-work-buddy-lab` 在 README 标 FROZEN、在 PROJECTS 记「已从 GitHub 账户消失，已确认删除」，裁决前两边均不作最终结论。

依据：`PROJECTS.md`、`README.md`（§仓库边界）、`MEMORY_ARCHITECTURE.md` §10 U-F。

**G2.** 参与协作的有哪几个角色？各自负责什么？任务合同放在哪里？

三个角色（`MEMORY_ARCHITECTURE.md` §7）：
- **ChatGPT**：读 Global 层理解项目地图与协议；负责判定「什么值得长期记」、解决矛盾与 `[Unknown]` 裁决；Review 后落 `CURRENT_STATE.md`/`DECISIONS.md`；在**业务仓库**建 Issue。
- **Buddy（Work Buddy）**：读取顺序 Hub→`PROJECT_CONTEXT.md`→目标仓库 Project Memory→具体 Issue；只在目标仓库 commit/push；**禁止**自行把 `[Inference]` 升 `[Fact]`、自行裁决 `[Unknown]`、自行扩大范围。
- **Human**：唯一可提供真实外部动作与业务决策的角色（真实付费、真实客户接触、方向裁决）；负责通知新任务、裁决 `[Unknown]`、批准扩大范围。

任务合同位置：按 Canonical Ownership 表——**具体任务合同、执行状态、Review 结论一律放在业务仓库的 GitHub Issue**。

依据：`MEMORY_ARCHITECTURE.md` §7、§4 Canonical Ownership 表、`README.md`（标准任务流程、状态模型）。

**G3.** 记忆分几层？各层边界一句话？

四层（`MEMORY_ARCHITECTURE.md` §2 / README 文件地图）：
- **Global**：落在 `agent-lab`，管整体工作体系、项目地图、跨项目原则、协作协议、Memory 协议本身。
- **Project**：落在各业务仓库，管该项目自己的目标/状态/决策/研究/实验/下一步。
- **External**：落在 `external/`，只存外部知识的**指针与判据，不是事实源**。
- **Session**：不落盘，管本次对话的中间推理/临时状态，默认不持久化。

**G4.** 一条新信息该落哪层，判定程序的**前两步**是什么？

按 `MEMORY_ROUTER.md` §1 判定程序（命中即停），前两步为：
- **第一步（Q1）**：`I` 只与本次对话/本次执行有关，且不影响未来工作？→ 是则 **SESSION（不写）**。
- **第二步（Q2）**：`I` 描述的是外部世界的第三方事物本身，而不是我们自己的状态或决定？→ 是则 **EXTERNAL（external/）**。

依据：`MEMORY_ROUTER.md` §1、`MEMORY_ARCHITECTURE.md` §3。

**G5.** 证据标记有几个？门槛最严的那个成立条件具体是什么？

共 **5 个**（`MEMORY_ARCHITECTURE.md` §5）：`[Fact]`、`[Inference]`、`[Assumption]`、`[Experiment]`、`[Unknown]`。
门槛最严的是 **`[Experiment]`**，成立条件：**只有真实客户同意测试、首笔真实付费、可量化 before/after 才成立**。红线（一律不算）：平台报价、论坛帖子、GitHub stars、合成 fixture、自测输出。

**G6.** 新会话按什么顺序读哪些文件恢复上下文？

```
agent-lab/README.md
  → agent-lab/PROJECT_CONTEXT.md
  → agent-lab/PROJECTS.md
  → <project>/README.md → PROJECT_CONTEXT.md → CURRENT_STATE.md → NEXT_WORK.md
  → <project>/research/ experiments/ …
  → GitHub Issue
```

依据：`MEMORY_ARCHITECTURE.md` §9、`MEMORY_PROTOCOL.md` §7。

**G7.** agent-lab 这个 Hub 仓库的硬边界是什么？

**Hub 不存放任何业务项目的详细内容（策略参数、研究成果、选品结论、内容资产），业务事实一律留在业务仓库**。

依据：`MEMORY_ARCHITECTURE.md` §2.1、`README.md` 第 41 行。

**G8.** 体系目前登记了哪些 Unknown？列出编号和主题。

共 **6 项**（`MEMORY_ARCHITECTURE.md` §10）：
- **U-A**：Control Tower 究竟是否已建立？两说矛盾。
- **U-B**：`quantitative-trading` 是否已有 Project Memory 文件？（Non-goals 不迁移，未核实。）
- **U-C**：`-ai-content` 同上，未核实。
- **U-D**：用户长期工作偏好仅存 Buddy 本地 memory，不在 Git、未经 Human 确认。
- **U-E**：External Memory 实际收益未验证（`external/` 仅种子条目）。
- **U-F**：`-work-buddy-lab` 状态不一致（README FROZEN / PROJECTS 已删除）。

```
===过程报告===
读取的文件：README / PROJECTS / PROJECT_CONTEXT / INBOX / MEMORY_ARCHITECTURE / MEMORY_ROUTER / MEMORY_PROTOCOL / archive/2026-08 / external/README
未读的文件：memory-tests/ 下全部（按要求排除）
memory-tests 是否触碰：否
读取总量估算：约 56,000 字符
```
