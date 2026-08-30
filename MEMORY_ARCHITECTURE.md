# Memory Architecture v0.1 — Global / Project / External / Session

> 建立于 `agent-lab` Issue #2（2026-08-30）。Git-native Markdown，**无数据库、无向量库、无图数据库、无记忆服务**。
>
> **本文件是四层记忆模型的 canonical 定义。**
>
> | 需要什么 | 去哪里 |
> |---|---|
> | 一条新信息该写到哪儿 | `MEMORY_ROUTER.md`（判定程序 + 路由测试） |
> | 什么值得记 / 记录字段 / 写入时机 | `MEMORY_PROTOCOL.md`（P0 草案，仍有效） |
> | 已落地的 Project Memory 长什么样 | `watanuo1982/-commercial-radar`，由该仓库 Issue #9 交付 |
> | 外部知识/工具/来源 | `external/` |
>
> ⚠️ `MEMORY_PROTOCOL.md` §2 只定义了 Global / Project 两层。**External 与 Session 两层以本文件为准（SUPERSEDED）。**

---

## 1. 为什么是四层

三层（Hub / Project / 外部资料）不够，因为混淆了两种完全不同的东西：

- **「我们是谁、我们在做什么」**（Global + Project）—— 我们的状态与决定；
- **「世界上有什么」**（External）—— 别人的东西，我们引用它，但它不是我们的状态；
- 以及第三种：**「这次对话里我正在想什么」**（Session）—— 默认不该留下来。

把 External 独立出来的唯一目的：防止**外部资料被静默内化成项目事实**。引用一个开源项目 ≠ 我们验证了它。
把 Session 独立出来的唯一目的：给「不写」一个明确的默认答案。

---

## 2. 四层定义与边界

### 2.1 Global Memory — `agent-lab`

**管辖**：整体工作体系、项目地图、跨项目原则、ChatGPT ↔ Human ↔ Buddy 协作协议、Memory Protocol 本身。

| 文件 | 唯一职责 |
|---|---|
| `README.md` | Hub 入口：定位、仓库边界、标准任务流程、状态模型、文件地图 |
| `PROJECTS.md` | 项目注册表 + 新项目接入规范 |
| `PROJECT_CONTEXT.md` | 四仓库边界、项目状态判断语义、Control Tower 定位、Buddy 跨仓库工作约定 |
| `MEMORY_ARCHITECTURE.md` | 本文件：四层模型、归属、证据语义、冲突处理、读写职责 |
| `MEMORY_ROUTER.md` | 路由判定程序与路由测试记录 |
| `MEMORY_PROTOCOL.md` | 记录语义、写入时机、P0 成功标准、设计参考 |
| `INBOX.md` | 跨项目任务**指针**（不复制任务正文） |
| `archive/YYYY-MM.md` | 已完成跨项目任务归档（指针 + commit + 一句结果） |

**硬边界**：Hub **不存放任何业务项目的详细内容**（策略参数、研究成果、选品结论、内容资产）。业务事实一律留在业务仓库。

### 2.2 Project Memory — 每个项目仓库

**管辖**：该项目自己的目标、状态、决策、研究、实验、证据、下一步。**不得污染其他项目。**

最小 canonical 集合（`MEMORY_PROTOCOL.md` §2 定义，此处不重复）：

```text
PROJECT_CONTEXT.md  定位 / 边界 / 长期原则 / 事实唯一归属 / 证据语义
CURRENT_STATE.md    当前阶段、当前已证实结论、当前实验状态
NEXT_WORK.md        当前导航与待办摘要（不重复历史任务、不复制状态协议）
DECISIONS.md        关键决策、理由、被否决方案、显式 Unknown
MEMORY_INDEX.md     纯导航索引（可选，不复制正文）
CHANGELOG.md        历史演进（可选）
research/  experiments/  radar/  ……  证据、研究、实验、机会资产
```

**已有同等作用文件的，保留原文件，不为了凑齐清单而制造第二份事实源。**

参考实现：`-commercial-radar`（Issue #9，commit `b29eebf`）—— 已验证「新会话只读仓库即可恢复项目上下文」。
其后 `-quantitative-trading`（P1-A，commit `5169625`）与 `-ai-content`（P1-B，commit `fad8b740`）也完成对齐，Project Memory 列均为 ADOPTED（见 `PROJECTS.md`）。

### 2.3 External Memory — `external/`

**管辖**：项目之外、可被多个项目引用的外部知识 —— 开源项目、工具/平台机制、论文与方法论、公开人物与来源。

**准入标准（三条全中才进）**：
1. 至少两个项目可能引用它，**或**它对协作体系本身有约束力；
2. 存在可追溯的原始来源（URL / commit / 文档）；
3. 我们能给出**自己的判据**（为什么相关、什么条件下不可用）。

**硬边界（最重要的一条）**：
> External Memory **不是事实源**。项目引用它时，必须回到原始来源并标注引用日期；
> **禁止把 external/ 里的一句话直接抄进 Project Memory 当作 `[Fact]`。**
> 项目里可以写成事实的只有「我们做了什么判断/决定」，不是「外部资料说了什么」。

存什么：指针 + 判据 + 引用日期 + 相关项目。
**不存**：被引用物的正文、复制粘贴的文档、任何需要跟随上游更新的内容。

详见 `external/README.md`。

### 2.4 Session Context — 不落盘

**管辖**：当前对话/临时工作上下文 —— 中间推理、临时文件路径、未定的想法、执行过程。

**默认值 = 不持久化。** 这是唯一默认答案。

唯一入库路径：**显式提炼** → 走 `MEMORY_ROUTER.md` 的判定程序 → 落到 Global / Project / External 之一。
未经提炼的会话内容进入长期记忆，是本架构要防的主要失效模式。

Session 中产生的**工作产物**（代码、数据、报告）按其性质落入 Project Memory 或业务仓库，不属于 Session Context。

---

## 3. 判定优先级

当一条信息同时像两类时，按此顺序裁决（**顺序不可调换**）：

1. **Session 优先排除**：只与本次对话/本次执行有关、不影响未来工作 → Session，不写。
   （Session 是唯一有默认答案的层，必须先滤掉噪声。）
2. **External 优先于 Global**：描述的是外部世界的第三方事物本身（开源项目 / 工具平台机制 / 论文方法论 / 他人事件），**而不是我们自己的状态或决定** → External。
   （理由：防止把「外部平台的机制」误当成「我们的协作协议」。「GitHub Projects v2 只有 GraphQL」是 GitHub 的机制，不是我们的协议 —— 我们**据此**做的决定才是 Global/Project。）
3. **Global 优先于 Project**：定义或改变了协作机制、项目地图、跨项目原则、Memory 协议本身 → Global。
   （某项目的经验要升为跨项目原则，必须**显式迁移**并在原处留指针，不允许两处同时写正文。）
4. **Project 兜底**：只影响某一个项目 → 该项目仓库。
5. **仍无法判定 → 不写**，标 `[Unknown]`，记入本文件 §10 或该项目 `DECISIONS.md` 的 Unknown 段，等 Human / ChatGPT 裁决。

**消解规则（最常用）**：

| 形态 | 归属 |
|---|---|
| 外部事物**本身**是什么样的 | **External** |
| 我们**对它的判断 / 采用决定** | **Project**（若它约束协作体系则 **Global**） |

> **与 `MEMORY_ROUTER.md` 的关系**：本节是裁决原则的摘要，顺序与 `MEMORY_ROUTER.md` §1 的 Q1–Q5 **一一对应且一致**。
> **实际判定时以 `MEMORY_ROUTER.md` §1 的操作性判问为准**，本节用于解释「为什么是这个顺序」。
>
> **修订记录（2026-08-30）**：v0.1 本节只写了「Global 优先于 Project」与「External 与 Project 的消解」，
> **未显式定义 Global 与 External 的相对顺序**，而 `MEMORY_ROUTER.md` §1 把 External 排在 Global 之前。
> 两者读起来像两个不同的答案 —— 由跨会话恢复实测第一轮 G4 题暴露（新会话按本节答、按 Router 答，结果相反）。
> 本次已补全为显式全序。详见 `memory-tests/run-2026-08-30/summary.md` F-2。
>
> **P0.6 跨会话恢复实测产物已自包含于 `memory-tests/`**（题库 `protocol.md` + 三份冷启动答案 `run-2026-08-30/{s1,s2,s3}_answer.md` + `summary.md`），不依赖任何 GitHub Issue 作载体；实测当时 Issue #3 尚不存在，结论独立归档。Issue #3 现为 P1-C（Global Memory 收口），与 P0.6 实测无关。

---

## 4. Canonical Ownership（每类事实只有一个归属）

| 事实类别 | 唯一归属 | 禁止 |
|---|---|---|
| 整体工作体系、项目地图、协作协议、Memory 协议 | `agent-lab`（本层各文件） | 复制到业务仓库 |
| 某项目的定位 / 状态 / 决策 / 研究 / 实验 / 下一步 | 该项目仓库 | 写进 Hub |
| 外部工具/项目/平台机制/方法论 | `external/`（指针 + 判据） | 抄进项目当事实 |
| 本次对话的中间过程、临时状态 | 不落盘 | 自动进长期记忆 |
| 具体任务合同、执行状态、Review 结论 | GitHub Issue（业务仓库） | 另建任务系统 |
| 历史演进 | `CHANGELOG.md` + `archive/` | 删除旧版本 |
| 最终版本历史 | Git history | 用文档覆盖提交记录 |

**同层内**再按第 2 节各文件的「唯一职责」列归属，不跨文件重复正文。

---

## 5. Evidence 语义

五个标记。写在事实末尾或字段值旁，不写就要能被追问出来。

| 标记 | 含义 | 门槛 |
|---|---|---|
| `[Fact]` | 可直接追溯到来源的既成事实 | 有 commit / Issue / 文件 / 实验记录可查 |
| `[Inference]` | 从 `[Fact]` 推出来的结论 | 必须能说出推理链，说不出就降级 |
| `[Assumption]` | 为推进工作而暂设的前提 | 必须写明「待什么数据回归」 |
| `[Experiment]` | 真实世界验证事件 | **只有真实客户同意测试、首笔真实付费、可量化 before/after 才成立** |
| `[Unknown]` | 不知道 / 无法确认 / 记载互相矛盾 | 不许猜，不许留白 |

`[Experiment]` 的红线（沿用 `-commercial-radar`，Hub 层统一）：
平台报价、论坛帖子、GitHub stars、合成 fixture、自测输出 —— **一律不算**。

项目层可使用子集（`-commercial-radar` 当前用 4 个标记，`Unknown` 以独立段落记录），与本表兼容。

---

## 6. 冲突处理

1. **先定层级** —— Global / Project / External / Session 归错层级是最高频的冲突来源。
2. **再定文件** —— 同层内按 §4 表找到唯一 canonical 文件；两处都像就改一处、另一处留指针。
3. **旧事实不删除** —— 标记为 `SUPERSEDED` 并写明新的 canonical 在哪，保留原文。删除历史会让下游无法审计。
4. **Git history 是最终仲裁** —— 文档与提交记录冲突时，以提交记录为准，然后把文档改对。
5. **真不知道就写 `[Unknown]`** —— 记载互相矛盾时，两种说法都保留并标 `[Unknown]`，等 Human / ChatGPT 裁决；**Buddy 不自行选边**。

---

## 7. 读写职责与更新触发条件

### ChatGPT

- **读**：Global 层理解项目地图与协作协议；进具体项目前读该项目的 Project Memory。
- **写**：判定什么值得长期记住；解决矛盾与 `[Unknown]` 裁决；Review 后把结论落进 `CURRENT_STATE.md` / `DECISIONS.md`。
- **触发创建**：判断需要定义新任务时，在**业务仓库**建 Issue（不在 Hub 写任务正文）。

### Buddy（Work Buddy / 本执行体）

- **读**：进 Hub → `PROJECT_CONTEXT.md` → 目标仓库 Project Memory → 具体 Issue。
- **写**：只在**目标仓库** commit/push；只有跨项目索引与协议变更才落在 `agent-lab`。
- **禁止**：自行把 `[Inference]` 升为 `[Fact]`、自行裁决 `[Unknown]`、自行扩大任务范围、**在没有对应 GitHub Issue 的情况下把聊天消息当作已授权任务执行**（任务唯一载体规则见 `README.md` 协作方式）。
- **触发更新**：Issue 执行完成并 commit 后 → 更新目标项目 `CURRENT_STATE.md` / `NEXT_WORK.md`；协议或项目地图变化时 → 更新 Hub。

### Human

- 唯一可提供**真实外部动作**与**业务决策**的角色（真实付费、真实客户接触、平台人工操作、方向裁决）。
- 触发：通知新任务、裁决 `[Unknown]`、批准扩大范围。

### 更新时机（不是每句话都写）

```text
任务提出 → 执行 → commit/结果 → ChatGPT Review → VERIFIED / BLOCKED → 更新项目记忆
```

**Review 后的结论**是最值得进 `CURRENT_STATE.md` / `DECISIONS.md` 的内容。

---

## 8. 新项目接入最小规范

新项目 = **建独立 repository** → 在 `PROJECTS.md` 登记 → 建立最小 Project Memory。

**必须（缺一不可）**：

1. `README.md` —— 项目是什么、怎么跑、边界在哪。
2. `PROJECT_CONTEXT.md` —— 定位、边界、长期原则、**事实唯一归属表**、证据语义、新会话恢复路径。
3. `CURRENT_STATE.md` —— 当前阶段与当前已证实结论。
4. `NEXT_WORK.md` —— 当前导航与待办摘要。
5. `GITHUB_WORKFLOW.md`（沿用既有的话可直接复制协议）—— Issue 生命周期、`STATUS:` 写在评论正文、DoD 模板。
6. 在 `PROJECTS.md` 登记，并把 `Project Memory` 列标为 `ADOPTED`。

**建议**：`DECISIONS.md`、`MEMORY_INDEX.md`、`CHANGELOG.md`。

**不需要**：任何数据库、向量检索、记忆服务。文件-first 基线的效果没被测量之前，不引入这些依赖。

---

## 9. 新会话恢复路径

```text
agent-lab/README.md
  → agent-lab/PROJECT_CONTEXT.md        （项目地图与边界、协作协议）
  → agent-lab/PROJECTS.md               （去哪个仓库）
  → <project>/README.md → PROJECT_CONTEXT.md → CURRENT_STATE.md → NEXT_WORK.md
  → <project>/research/ experiments/ …  （按需检索，不整仓加载）
  → GitHub Issue                        （当前任务合同）
```

- **只读 Global Memory** 就能理解整体项目地图与协作协议（Acceptance 1）。
- **只读某项目的 Project Memory** 就能恢复该项目，不依赖其他项目的聊天历史（Acceptance 2）。
- 需要外部资料时去 `external/`，但**必须回到原始来源复核**（Acceptance 3）。

---

## 10. 已知 Unknown

| ID | 内容 | 状态 |
|---|---|---|
| U-A | **Control Tower（AI Venture Control Tower）究竟是否已建立** —— `agent-lab` #1 评论（2026-08-29 08:05 UTC）称已建立并给出 `https://github.com/users/watanuo1982/projects/1`（3 Issue / 2 视图 / 5 字段）；同一 Issue 评论（08:36 UTC）与 `PROJECT_CONTEXT.md` §3 称「尚未实际建立，BLOCKED」。两者矛盾，`[Unknown]`，不在此裁决。 | 待 Human / ChatGPT 裁决 |
| U-B | `quantitative-trading` 是否已存在完整 Project Memory。**已核实 → RESOLVED**：经 P1-A Memory Alignment（qt Issue #1，commit `51696258698ff2c29f903f7986ee4e9f40f47004`）确认存在 `PROJECT_CONTEXT.md` / `CURRENT_STATE.md` / `NEXT_WORK.md` / `DECISIONS.md` / `MEMORY_INDEX.md` 全集合，并保留成熟的 `research/research_memory/`（INDEX/SCHEMA/manifest/6 条目 + verdict）。原「待核实」系 agent-lab Issue #2（本架构）Non-goals 明确不迁移业务仓库所致，非现状。 | **RESOLVED**（2026-08-30，P1-C；证据：qt Issue #1 + commit `5169625`） |
| U-C | `-ai-content` 是否已存在完整 Project Memory。**已核实 → RESOLVED**：经 P1-B Memory Alignment（-ai-content Issue #2，commit `fad8b740f8ee4041049c18999edccde642a56d30`）确认存在 `PROJECT_CONTEXT.md` / `CURRENT_STATE.md` / `NEXT_WORK.md` / `DECISIONS.md` / `MEMORY_INDEX.md`（新建）+ `GITHUB_WORKFLOW.md` / `README.md` / `CHANGELOG.md` 全套，并声明 Evidence 五标记与 External 边界（A1–A6）。原「待核实」系 agent-lab Issue #2（本架构）Non-goals 明确不迁移业务仓库所致。 | **RESOLVED**（2026-08-30，P1-C；证据：-ai-content Issue #2 + commit `fad8b740`） |
| U-D | 用户长期工作偏好（输出格式、决策方式等）目前只存在于 Buddy 本地 memory，不在 Git。**来源不在 Git 且未经 Human 确认，本期不升为 Global 事实。** | 待 Human 确认后由 ChatGPT 决定是否纳入 |
| U-E | External Memory 的实际收益未验证 —— `external/` 目前只有种子条目，还没有被两个以上项目真实引用。 | 待使用后再评估 |
| U-F | `-work-buddy-lab` 的状态不一致 —— `README.md` 记为「FROZEN」并仍列在仓库边界里，`PROJECTS.md` 记为「已从 GitHub 账户消失，已确认删除」。两者未对齐。本期**不改任何一方**（超出 Issue #2 范围，且删除声明需要 Human 确认）。 | 待 Human 确认后由 ChatGPT 决定 |

---

## 11. Non-goals 与升级条件

**明确不做**：Mem0、Letta、Graphiti、Neo4j、向量数据库、任何托管记忆服务；迁移 `-quantitative-trading` / `-ai-content`；改动业务仓库的业务内容；复制聊天记录。

**什么时候才该重新评估**：

- 全局文件膨胀到人无法在几分钟内通读；
- 跨项目检索频繁失败（找不到明明记得写过的东西）；
- External Memory 条目需要跟随上游频繁更新。

三条里出现**两条**再考虑检索层。在那之前，文件-first 是刻意选择，不是将就。
