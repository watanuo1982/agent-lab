# Memory Router — 路由规则与路由测试

> `agent-lab` Issue #2 交付物之一。四层模型见 `MEMORY_ARCHITECTURE.md`，本文件只回答一个问题：
> **一条新信息该写到哪儿，或者根本不该写。**
>
> **Canonical rule source：本文件 §1。** `MEMORY_ARCHITECTURE.md` 只负责解释四层模型与原则，不再重新定义 Q1–Q5 的操作性判定。

---

## 1. 判定程序（唯一操作性规则）

拿到一条信息 `I`，**按顺序**走。命中即停。

```text
Q1  I 只与本次对话/本次执行有关，且不影响未来工作？
    ├── 是 → SESSION（不写）
    └── 否 ↓

Q2  I 描述的是外部世界的第三方事物本身
    （开源项目 / 工具平台机制 / 论文方法论 / 他人事件），
    而不是我们自己的状态或决定？
    ├── 是 → EXTERNAL（external/）
    └── 否 ↓

Q3  I 定义或改变了协作机制、项目地图、跨项目原则、Memory 协议本身？
    ├── 是 → GLOBAL（agent-lab）
    └── 否 ↓

Q4  I 只影响某一个具体项目？
    ├── 是 → PROJECT（该项目仓库）
    └── 否 ↓

Q5  无法判定 → 不写。标 [Unknown]，记入 `UNKNOWN_REGISTRY.md`，
    并在 `MEMORY_ARCHITECTURE.md §10` 保留背景/证据指针，等 Human / ChatGPT 裁决。
```

### 关于 Q2 / Q3 / Q4 的顺序

顺序是刻意设计的：

- **Q1 在最前**：Session 是唯一有默认答案的层（默认不写），必须先过滤掉噪声。
- **Q2 在 Q3 之前**：防止把「外部平台的机制」误当成「我们的协作协议」。
  例：「GitHub Projects v2 只有 GraphQL」是 GitHub 的机制（External），
  不是我们的协议（Global）——我们**据此**做的决定才是 Global/Project。
- **Q3 在 Q4 之前**：一条信息如果约束了整个协作体系，就不能只落在单个项目里，
  否则其他项目永远看不到。

### 消解规则（Q2 与 Q4 打架时最常用）

| 形态 | 归属 |
|---|---|
| 外部事物**本身**是什么样的 | **External** |
| 我们**对它的判断 / 采用决定** | **Project**（若约束协作体系则 **Global**） |
| 某项目经验要升为跨项目原则 | **显式迁移**：Global 写正文，Project 留指针；不允许两处都写正文 |

---

## 2. 反向检查（写完必查）

写完任何一条长期记忆，过这三条：

1. **有没有被复制到两处？** 有 → 保留 canonical 一处，另一处改成指针。
2. **External 内容有没有被抄进项目当事实？** 有 → 改成「我们的判断」+ 原始来源 + 引用日期。
3. **Session 内容有没有直接落盘？** 有 → 删掉，除非它通过了第 1 节的判定程序。

---

## 3. 路由测试（11 例）

> 全部取自本体系内**真实存在**的信息，可回溯核对。路由结果以 2026-08-30 的仓库状态为准。
> **「归属位置」列统一使用 `<repo>/<path>` 全限定写法**，避免跨仓库时歧义。

| # | 信息 | 路由 | 归属位置 | 理由 | 证据 |
|---|---|---|---|---|---|
| R-01 | GitHub Projects v2 只能通过 GraphQL 管理，且令牌需要 `project` 作用域 | **External** | `agent-lab/external/` | 描述的是 GitHub 平台自身机制，不是我们的状态 | `[Fact]`（agent-lab #1 评论，2026-08-29 07:41 UTC 实测 `INSUFFICIENT_SCOPES`） |
| R-02 | Letta / MemFS 使用 Git-backed Markdown memory + 小 always-loaded 系统层 | **External** | `agent-lab/external/` | 第三方方法论；我们只是借鉴了其中一小部分 | `[Fact]`（agent-lab `MEMORY_PROTOCOL.md` §12 设计参考） |
| R-03 | `dbskill` 为 CC BY-NC 4.0，商业化阶段必须重新评估 | **External** | `agent-lab/external/` | 第三方许可证**本身**是外部事实 | `[Fact]`（来源见 `-commercial-radar/DECISIONS.md` D-09） |
| R-04 | Commercial Radar 主线重新聚焦 ToC；B2B 实验暂停，**不进行客户外联** | **Project** | `-commercial-radar/CURRENT_STATE.md` | 只影响单个项目的当前阶段 | `[Fact]`（commercial-radar #7 CLOSED `PAUSED / NOT PLANNED`，2026-08-29 14:12 UTC） |
| R-05 | ToC 管线用 **7 维**评分，机会卡用 **B2B 10 维**，两套互斥 | **Project** | `-commercial-radar/PROJECT_CONTEXT.md` + `-commercial-radar/DECISIONS.md` D-02 | 项目内部模型边界 | `[Fact]`（commercial-radar Issue #9 审计确认） |
| R-06 | 009 RFP 实验包已提交，但不构成 Validated Opportunity | **Project** | `-commercial-radar/experiments/` + `-commercial-radar/DECISIONS.md` | 项目自己的实验与结论 | `[Fact]`（#7 已 CLOSED 为 PAUSED） |
| R-07 | `STATUS:` 写在 Issue **评论正文**里，不替代 GitHub 原生 Open/Closed | **Global** | `agent-lab/README.md`（状态模型） | 定义协作机制，所有项目共用 | `[Fact]`（README + 四个仓库既有实践） |
| R-08 | 新项目必须建独立 repository 并在 `PROJECTS.md` 登记 | **Global** | `agent-lab/PROJECTS.md` | 项目地图与接入规则 | `[Fact]`（PROJECTS.md 新项目规则） |
| R-09 | 执行 Issue #2 时把工作副本放在本机 `/tmp`，用完即弃 | **Session** | **不落盘** | 只与本次执行有关，不影响未来工作 | — |
| R-10 | Control Tower 究竟是否已建立（两种记载互相矛盾） | **Pending** | 不进事实层 → `UNKNOWN_REGISTRY.md` U-A | 记载冲突，Buddy 不自行选边 | `[Unknown]` |
| R-11 | 用户偏好表格化输出、倾向保守方案、喜欢 A/B/C 选项 | **Pending** | 不进事实层 → `UNKNOWN_REGISTRY.md` U-D | 来源在 Buddy 本地 memory（不在 Git）且未经 Human 确认 | `[Unknown]` |

**统计**：External 3 · Project 3 · Global 2 · Session 1 · Pending/`[Unknown]` 2 —— 共 11 例，超过 DoD 要求的 8 例。

### 测试用例的选取说明

刻意覆盖了四种「容易路由错」的边界：

- **R-01 vs R-07**：同样是「GitHub 怎么工作」，前者是平台机制（External），后者是我们的协议（Global）。
- **R-03 vs R-06**：同样是 dbskill / 实验，外部属性归 External，我们的判断归 Project。
- **R-04 vs R-05**：同样是项目事实，前者进 `CURRENT_STATE`（会变），后者进 `PROJECT_CONTEXT` + `DECISIONS`（稳定）。
- **R-09 / R-10 / R-11**：三种「不该写」——临时、冲突、来源不足。

---

## 4. 待补充

- 路由测试目前只有 11 例，且全部来自 Hub 与 commercial-radar。**迁移 `-quantitative-trading` / `-ai-content` 时应各补 3–5 例**，尤其是「业务事实 vs 外部资料」的边界。
- 若后续出现「本程序判定不出」的 recurring 类型，应在此文件补规则，而不是在个案里临时决定。
