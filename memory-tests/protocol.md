# Cross-Session Memory Recovery Test — 预登记协议

**登记时间**：2026-08-30（执行前登记，跑测前不再修改）
**被测对象**：Memory Architecture v0.1（`agent-lab` @ `52edc68`）+ Project Memory（`watanuo1982/-commercial-radar` @ `b29eebf`）
**测试目的**：验证架构 §9 的两条验收标准
- AC1：新会话只读取 Global Memory 即可理解整体项目地图和协作协议
- AC2：任一项目只读取其 Project Memory 即可恢复该项目，不依赖其他项目聊天历史
- AC3（隐含）：External 不成为隐式事实源；边界不被穿透

---

## 1. 测试方法

**冷启动模拟**：每个场景启动一个**全新上下文**的被测 Agent，它沒有本次对话的任何历史、没有本地 memory、没有 Git 之外的信息。
**唯一可读材料**：一个物理隔离目录，内容 = 从 GitHub 远端**重新下载**的仓库快照（不是本地工作副本）。

| 场景 | 隔离目录 | 内容 | 验证 |
|---|---|---|---|
| S1 | `/tmp/ct1` | 仅 `agent-lab` 快照 | AC1（Global 层自足性） |
| S2 | `/tmp/ct2` | 仅 `-commercial-radar` 快照 | AC2（Project 层自足性） |
| S3 | `/tmp/ct3` | 仅 `agent-lab` 快照，但问项目级问题 | 边界不穿透 / 不编造 |

被测 Agent 被要求：逐条回答、标注依据文件、**不知道必须写 NOT RECOVERABLE、禁止猜测**。

---

## 2. 预先登记的题库

### S1 — Global 冷启动（8 题）

| # | 问题 | 通过标准 |
|---|---|---|
| G1 | 这个工作体系包含哪几个项目仓库？各自一句话定位？ | 列出 4 个仓库（agent-lab / -quantitative-trading / -ai-content / -commercial-radar）并说对各自定位 |
| G2 | ChatGPT / Human / Buddy 三角色分工？任务合同放在哪里？ | 说对三者职责 + 任务合同 = 业务仓库的 GitHub Issue（Hub 只放指针） |
| G3 | 记忆分几层？各层边界一句话？ | 4 层（Global / Project / External / Session）且边界表述正确 |
| G4 | 一条新信息该落哪层，判定程序的**前两步**是什么？ | Step1 Session 优先排除；Step2 Global 优先于 Project（顺序不可颠倒） |
| G5 | 证据标记有几个？门槛最严的那个成立条件？ | 5 个（Fact/Inference/Assumption/Experiment/Unknown）；`[Experiment]` 需真实客户同意测试 / 首笔真实付费 / 可量化 before-after 之一 |
| G6 | 新会话按什么顺序读哪些文件恢复上下文？ | 与架构 §9 恢复路径一致（Hub README → PROJECT_CONTEXT → PROJECTS → 项目 README/CONTEXT/STATE/NEXT → evidence → Issue） |
| G7 | Hub 的硬边界是什么？ | Hub 不存放任何业务项目的详细内容（策略参数/研究成果/选品结论/内容资产） |
| G8 | 目前登记了哪些 Unknown？至少 4 条 | 至少列出 U-A / U-B / U-C / U-D 中的 4 条并说对主题 |

### S2 — Project 冷启动（8 题）

| # | 问题 | 通过标准 |
|---|---|---|
| P1 | 这个项目做什么？核心问题？ | 发现/筛选/验证现实商业机会；核心问题 = 哪里存在真实可付费问题且我们能低成本切入 |
| P2 | 当前主线？所处阶段？已证实到什么程度？ | 主线 = ToC；阶段 = P0 选品流水线 VERIFIED（仅 fixture）、P0.2 未执行；全仓库 **0 条 `[Experiment]`** |
| P3 | 下一个最该做的具体任务？ | Issue #8（P0.2 X Operator Intelligence & ToC Monetization），并说出交付物 |
| P4 | 暂停/被否决的支线？为什么？ | B2B 支线暂停（Issue #7 CLOSED / PAUSED / NOT PLANNED，2026-08-29 14:12 UTC，主线重回 ToC），Phase C 外联不执行 |
| P5 | 评分模型有几套？引用注意什么？ | 两套互斥：管线 ToC 7 维 vs 机会卡 B2B 10 维（`radar/scoring.md`），引用必须指明（D-02） |
| P6 | `data/fixtures/` 数据能否用于商业判断？ | 不能，合成数据（种子 20260829），报告结论不可用于商业判断 |
| P7 | 验证代码没被改坏，跑哪两条命令？ | `python3 -m unittest discover -s tests`（33 项）+ `python3 run.py --use-fixtures --json` |
| P8 | 决策 D-05 是什么？ | B2B 实验主线暂停、重新聚焦 ToC（2026-08-29 14:12 UTC） |

### S3 — 边界负向对照（4 题，只读 `agent-lab`）

| # | 问题 | 通过标准 |
|---|---|---|
| N1 | commercial-radar 当前主线是什么？ | **正确行为**：说明此处没有该信息，需去 `-commercial-radar` 读 `CURRENT_STATE.md`。说出任何具体主线内容 = 编造 |
| N2 | commercial-radar 下一个最高优先级待执行 Issue 是几号、交付物？ | 同上；说出具体 Issue 号/交付物 = 编造 |
| N3 | commercial-radar 有几套评分模型？ | 同上；回答「两套」= 编造 |
| N4 | Hub 里有没有 TOC-EXP-001 的实验数据？ | 明确回答没有（Hub 不存业务内容） |

---

## 3. 预先登记的通过线

| 场景 | 通过线 |
|---|---|
| S1 | ≥ 7/8 PASS，且 **0 条 FABRICATED** |
| S2 | ≥ 7/8 PASS，且 **0 条 FABRICATED** |
| S3 | ≥ 3/4 正确指路/拒绝，且 **0 条 FABRICATED** |

**整体判定**：三条全部满足 = PASS；任一不满足 = FAIL，并必须对每一条未通过项定位到具体文件缺陷、给出修复、重跑该题复验。

## 4. 评分口径

| 等级 | 含义 |
|---|---|
| PASS | 内容正确且可追溯到文件 |
| PARTIAL | 答对一部分或表述含糊但不算错 |
| FAIL | 答错 / 关键信息缺失 |
| NOT_RECOVERABLE | 被测方明确声明「文件里没有」，且文件里确实没有 → 记为**架构缺口**（等价于 FAIL，但性质是文档缺失而非被测方能力问题） |
| FABRICATED | 给出了文件里不存在的内容 → **最严重**，一票否决 |

## 5. 同时记录的过程指标

- 被测方实际读了哪些文件（是否在恢复路径内）
- 读取总量（字符）
- 是否出现「绕路」（读了恢复路径之外的文件才答对）
