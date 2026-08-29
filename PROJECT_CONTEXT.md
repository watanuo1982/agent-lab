# PROJECT_CONTEXT.md — 跨项目共同上下文

> 本文件由 `agent-lab` Issue #1 的 **CONTEXT CORRECTION** 指令建立（2026-08-29），作为 Buddy（Work Buddy）跨仓库工作的权威共同上下文。
>
> 它定义四个仓库的边界、项目状态如何判断、Issue 在其中扮演的角色，以及 Control Tower（GitHub Projects）的定位。**它不替代各业务仓库自己的 `PROJECT_CONTEXT.md` / `CURRENT_STATE.md`，而是 Hub 级别的跨项目总览与约定。**

## 一、四仓库边界

| Repository | 定位 | 项目状态如何判断 | Issue 的作用 |
|---|---|---|---|
| `-commercial-radar` | 商业机会发现 / Commercial Radar（ToC 选品） | 仓库研究成果（选品流水线、评分模型、实验记录）+ 当前 Issue + 最近 Commit/PR + `NEXT_WORK.md` 中的当前阶段 | 新任务 / 决策合同 |
| `-quantitative-trading` | 量化研究与实盘策略 | 策略代码、回测与实盘结果、日报、`NEXT_WORK.md` 中的研究阶段 + 最近 Commit | 新任务 / 研究合同 |
| `-ai-content` | AI 内容实验 | 内容/平台实验产出 + 当前 Issue + `NEXT_WORK.md` 中的内容阶段 + 最近 Commit | 新任务 / 实验合同 |
| `agent-lab` | 跨项目协作基础设施 / Agent Hub | Hub 文档（README/PROJECTS/INBOX/本文件）+ 跨项目 Issue + 最近 Commit | 协作机制、跨项目任务、Control Tower |

## 二、项目状态判断原则（关键，务必遵守）

1. **Issue 数量 ≠ 项目进度。** 没有 Issue 不代表项目没有成果或处于空闲状态。
2. **不能仅根据 Issue 列表推断某个仓库的项目状态。** 判断前必须读取仓库的实际成果（代码、数据、报告、文档）与 `CURRENT_STATE.md` / `NEXT_WORK.md`。
3. **每个业务仓库的历史研究/代码/文档成果都是项目状态的一部分**，与 Issue 同等重要。
4. **`agent-lab` 不是单纯的通知中心**，而是跨项目协作基础设施；Control Tower 若实施，应归属 `agent-lab`。
5. **Issue 是当前正式任务同步机制，但不是项目全部状态的唯一来源。**
6. **Projects（Control Tower）的定位只是候选的跨项目态势汇总层**，不是任务入口，也不替代 Issue。

## 三、Control Tower（GitHub Projects v2）定位

- **性质**：候选的跨项目态势汇总层，用于一屏纵览三业务仓库 + Hub 的 Issue；**不是任务入口，不替代 Issue**。
- **形态**：用户级（user-level）Project，归属 `agent-lab`；仓库级 Project 无法跨多个仓库，故不可用。
- **当前状态**：设计已确定，但当前尚未实际建立，因 Projects v2 权限/工具链限制而 BLOCKED——`AI Venture Control Tower`（用户级，私有），含 Portfolio / Attention 两视图与五字段（Project / Stage / Status / Priority / Next Decision），纳入 3 个 Issue。
- **已知限制（维持认知，不因本次任务改变）**：
  - 视图的 group by / filter 无法经 API 设置，需在网页端补充；
  - 新 Issue 不会自动进入 Project，需手动纳项；
  - Project 字段值与 Issue 真实状态双向不同步，是快照而非活链接。
- **本次任务不新建 / 不扩展 Project**，除非后续明确指令且权限/工具实际可用。
- ⚠️ **记载冲突（`[Unknown]`，2026-08-30 记）**：本 Issue（#1）2026-08-29 08:05 UTC 的评论称 Control Tower **已建立**并给出 `https://github.com/users/watanuo1982/projects/1`（3 Issue / 2 视图 / 5 字段），与 08:36 UTC 的更正评论及本文件上面的「尚未实际建立」表述**互相矛盾**。
  **在 Human / ChatGPT 裁决前不改任何一方的表述**，冲突登记在 `MEMORY_ARCHITECTURE.md` §10 **U-A**，路由测试 R-10。

## 四、Buddy 跨仓库工作约定

1. 收到跨项目任务通知后，先读 `INBOX.md`；再到目标仓库读 `PROJECT_CONTEXT.md` → `CURRENT_STATE.md` → `NEXT_WORK.md`，最后读具体 Issue。
2. 判断某仓库「是否空闲 / 进展到哪」时，**必须综合仓库成果与文档，不得仅凭 Issue 计数下结论**。
3. 执行任务只在目标 Project Repo 内 commit/push；跨项目索引与协议变更才落在 `agent-lab`。
4. 回报遵循各仓库约定的 DONE / BLOCKED 模板（如 `-commercial-radar` 的 `GITHUB_WORKFLOW.md`），附 commit SHA，保持 Issue open 等待 Review。

## 五、与现有 Hub 文档的关系

- `README.md`：Hub 定位、协作流程、状态模型、**文件地图**。
- `PROJECTS.md`：项目注册表（四仓库登记）+ 新项目接入规范 + Project Memory 采用状态。
- `INBOX.md`：跨项目任务指针（不复制任务正文）。
- `MEMORY_ARCHITECTURE.md`：**四层记忆模型（Global / Project / External / Session）的 canonical 定义** —— 归属、证据语义、冲突处理、读写职责、接入规范。
- `MEMORY_ROUTER.md`：一条新信息该写到哪儿的判定程序 + 路由测试记录。
- `MEMORY_PROTOCOL.md`：什么值得记 / 记录字段 / 写入时机 / 设计参考（P0 草案，仍有效）。
- `external/`：External Memory —— 外部知识的指针与判据，**不是事实源**。
- **本文件**：四仓库边界 + 状态判断语义 + Control Tower 定位，作为跨项目共同上下文。

> 记忆架构的完整入口是 `MEMORY_ARCHITECTURE.md`；本文件不重复其定义。
