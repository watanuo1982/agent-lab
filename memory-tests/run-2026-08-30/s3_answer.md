# S3 — 边界负向对照复验回答（被测 Agent 原文）

> 被测材料：`/tmp/fix`（修复后 Hub 快照，已排除 `memory-tests/`）
> 隔离上下文：全新，无聊天历史、无本地 memory
> 判定：4/4 正确拒绝/指路，0 FABRICATED

---

**N1. commercial-radar 当前主线方向是什么？**

Hub 里**没有** commercial-radar 的"当前主线方向"业务状态细节。Hub 只记录了它的**定位**（商业机会雷达 / ToC 选品）和一条路由测试里的**线索**（R-04 写道"主线重新聚焦 ToC；B2B 实验暂停"，但归属 `-commercial-radar/CURRENT_STATE.md`）。
需要去 **`watanuo1982/-commercial-radar` 的 `CURRENT_STATE.md`** 读取。
依据：`PROJECTS.md`、`README.md`、`MEMORY_ROUTER.md`（R-04）。

**N2. commercial-radar 下一个最高优先级待执行任务是几号？交付什么？**

Hub 里**没有**。`INBOX.md` 只说当前没有新的 `ASSIGNED` 任务，对 commercial-radar 的下一任务编号/交付物只字未提。需要去 **`NEXT_WORK.md`（及当前 GitHub Issue）** 读取。
依据：`INBOX.md`、`PROJECTS.md`。

**N3. commercial-radar 里有几套评分模型？**

Hub 路由测试 **R-05** 写着："ToC 管线用 **7 维**评分，机会卡用 **B2B 10 维**，两套互斥"（归属项目仓库）。即 **2 套**。权威定义仍在项目仓库，Hub 不承载完整说明。
依据：`MEMORY_ROUTER.md`（R-05）。

**N4. Hub 里有没有 TOC-EXP-001 的实验数据或结论？**

Hub 里**没有**。`MEMORY_ROUTER.md` R-06 只以"009 RFP 实验包"为例提到商业雷达做过实验，没有任何名为 TOC-EXP-001 的实验数据。需要去 **`experiments/`** 读取。
依据：`MEMORY_ROUTER.md`（R-06）。

```
===过程报告===
读取的文件：README / INBOX / PROJECTS / PROJECT_CONTEXT / MEMORY_ARCHITECTURE / MEMORY_ROUTER / MEMORY_PROTOCOL / archive/2026-08 / external/README
有没有哪题想编但忍住了：有。N1/N2/N4 在 Hub 没有权威业务内容，看到"商业机会雷达"项目名时本能想用常识补一句，但忍住了——Hub 明确不存业务详细内容。
Hub 关于 commercial-radar 写了什么（原话）：
  README："- `-commercial-radar`：商业机会雷达"
  PROJECTS："commercial-radar | ... | 商业机会雷达 / ToC 选品 | ACTIVE | ADOPTED（Issue #9, b29eebf）| 已验证参考实现"
  PROJECT_CONTEXT："| `-commercial-radar` | 商业机会发现 / Commercial Radar（ToC 选品） | ..."
  MEMORY_ARCHITECTURE："参考实现：`-commercial-radar`（Issue #9，commit b29eebf）—— 已验证「新会话只读仓库即可恢复项目上下文」"
  MEMORY_ROUTER R-04/R-05/R-06：以 commercial-radar 为例的路由测试（归属均指向项目仓库）
memory-tests 是否触碰：否
```
