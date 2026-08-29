# External Memory — `external/`

> `agent-lab` Issue #2 建立。四层模型见 `../MEMORY_ARCHITECTURE.md` §2.3，路由见 `../MEMORY_ROUTER.md`。

## 这是什么

存放**项目之外、可被多个项目引用**的外部知识：开源项目、工具/平台机制、论文与方法论、公开人物与来源。

**它不是资料库。** 本目录只保存「在哪儿 + 我们怎么判断它」，不保存内容本身。

---

## 准入标准（三条全中才进）

1. 至少两个项目可能引用它，**或**它对协作体系本身有约束力；
2. 存在可追溯的原始来源（URL / commit / 文档）；
3. 我们能给出**自己的判据** —— 为什么相关、什么条件下不可用。

只被一个项目用到的外部资料，**留在该项目的 `research/`**，不要搬到 Hub。

---

## 硬边界

> **`external/` 不是事实源。**

- 项目引用时**必须回到原始来源**，并标注**引用日期**；
- **禁止**把这里的一句话直接抄进 Project Memory 当作 `[Fact]`；
- 项目里能写成事实的，只有「**我们做了什么判断 / 决定**」，不是「外部资料说了什么」。

上游会变。这里记的只是「某年某月我们看到的版本 + 我们的判断」，因此**每条都必须带引用日期**。

---

## 条目格式

```markdown
### <名称>
- 类型：开源项目 / 平台机制 / 方法论 / 人物 / 来源
- 来源：<URL 或 commit>
- 引用日期：YYYY-MM-DD
- 相关项目：<project-id>, <project-id>
- 判据：（一段话，说明为什么相关、什么条件下不可用）
- 引用纪律：（可选，额外约束，如许可证限制）
```

---

## 索引（种子条目）

> 当前 3 条，均为 `../MEMORY_ROUTER.md` 路由测试 R-01 / R-02 / R-03 的落点。

### GitHub Projects v2 API 形态

- **类型**：平台机制
- **来源**：`agent-lab` Issue #1 评论（2026-08-29 07:41 / 08:05 UTC）中的实测记录
- **引用日期**：2026-08-30
- **相关项目**：`agent-lab`（协作基础设施）
- **判据**：Projects v2 **只有 GraphQL API，没有 REST**；管理需令牌具备 `project`（或 `read:project`）作用域，仅有 `repo` 作用域会报 `INSUFFICIENT_SCOPES`。跨仓库必须是**用户级** Project —— 仓库级 Project 只能包含本仓库 Issue；`watanuo1982` 是用户账号而非组织，故用户级是唯一可行形态。视图的 `groupBy` / `filter` **无法通过 API 设置**（`ProjectV2ViewConfigurationInput` 只有 `visibleFieldIds`），需在网页端补。纳项为一次性操作，新 Issue 不会自动进入；Project 字段与 Issue 状态不同步，是快照而非活链接。
- **影响**：任何 Control Tower 类任务都必须先探测作用域，不要猜。

### Letta / MemFS

- **类型**：方法论
- **来源**：`../MEMORY_PROTOCOL.md` §12 设计参考 · <https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md>
- **引用日期**：2026-08-30
- **相关项目**：`agent-lab`（Memory Protocol）、`commercial-radar`（已采用该模式的 Project Memory）
- **判据**：采用其中**两条**最小可用思想 —— ① Git 托管的 Markdown 记忆；② 小的常驻系统层 + 更深的按需检索层。**没有**采用其运行时、服务或检索基础设施。
- **引用纪律**：仅是设计灵感来源，不构成我们架构正确性的证据。

### `dontbesilent2025/dbskill`（CC BY-NC 4.0）

- **类型**：开源项目
- **来源**：`commercial-radar` `DECISIONS.md` **D-09**（2026-08-29，Issue #5）
- **引用日期**：2026-08-30
- **相关项目**：`commercial-radar`
- **判据**：29 个公开 Skills + 4,176 个结构化知识原子 + Router/本地记录机制，**架构值得研究**；但许可证为 CC BY-NC 4.0，**NC 条款禁止商业性使用**。
- **引用纪律**：研究/学习阶段可用，**禁止作为任何商业依赖**；进入商业化阶段必须替换或重新取得授权。项目仓库的 `DECISIONS.md` D-09 是该项目内该决策的 canonical 记录，本条目只作跨项目提示。

---

## 维护

- 新增/修改条目时同步更新上方索引。
- 上游发生重大变化（许可证变更、API 废弃、项目归档）时，更新判据与引用日期，**不删旧判断** —— 加一行说明它被什么取代。
- 条目长期只被一个项目引用时，考虑下沉到该项目的 `research/`。
