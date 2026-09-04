# Unknown Registry — Global

> **Canonical source：本文件。** 由 `architecture/MEMORY_ROUTER.md` §1 Q5 迁移而来。
> 本文件回答一个问题：**记载矛盾或无法判定归属的信息，登记在哪、谁来裁决、什么时候复查。**

---

## 1. 登记规则

一条信息进入本表，当且仅当它符合 `architecture/MEMORY_ROUTER.md` §1 Q5：**按 Q1–Q4 判定程序走完仍无法归属**（记载互相矛盾 / 来源不足 / 需要 Human 裁决）。

**不许猜，不许留白** —— 无法判定就必须登记在此，不能悬空在某个文件的旁注里。

### 字段定义

| 字段 | 说明 |
|---|---|
| `ID` | `U-` 前缀 + 字母，按登记顺序递增，不复用已删除的 ID |
| `内容` | 矛盾/未知本身是什么，需可回溯（引用具体文件、Issue、评论时间戳） |
| `状态` | `OPEN` / `REVIEW_DUE` / `RESOLVED` / `RETAINED_UNKNOWN` / `ARCHIVED` |
| `登记日期` | 首次发现并登记的日期 |
| `review_by` | 下一次强制复查日期；是时间兜底，不替代事件触发条件 |
| `复查触发条件` | 什么事件发生时必须重新审视这一条 |
| `裁决方` | Human / ChatGPT，与 `architecture/MEMORY_ARCHITECTURE.md` §7 读写职责一致 |
| `decision` | `RESOLVED` 时记录结论；否则写 `PENDING` |
| `evidence` | 指向证据 / canonical source，不复制正文 |

> `review_by` 防止 Unknown 无限期悬挂；`复查触发条件` 防止只等日期而错过相关工作发生。两者同时满足才算完整登记。

---

## 2. 登记表

| ID | 内容 | 状态 | 登记日期 | review_by | 复查触发条件 | 裁决方 | decision | evidence |
|---|---|---|---|---|---|---|---|---|
| U-A | **Control Tower（AI Venture Control Tower）究竟是否已建立** —— `agent-lab` #1 评论（2026-08-29 08:05 UTC）称已建立并给出 Projects v2 链接（3 Issue / 2 视图 / 5 字段）；同一 Issue 评论（08:36 UTC）与 `PROJECT_CONTEXT.md` §3 称「尚未实际建立，BLOCKED」。两者矛盾。 | REVIEW_DUE | 2026-08-29 | 2026-09-03 | 下次任何工作涉及 Control Tower 或 Projects v2 看板前，必须先裁决 | Human + ChatGPT | PENDING | `architecture/MEMORY_ARCHITECTURE.md` §10；`agent-lab` #1 |
| U-B | `-quantitative-trading` 是否已存在完整 Project Memory。**已核实 → RESOLVED**：P1-A Memory Alignment 确认完整集合存在（qt Issue #1，commit `5169625`）。 | RESOLVED | 2026-08-29 | — | — | — | 已完成 P1-A Memory Alignment | `-quantitative-trading` Issue #1；commit `5169625` |
| U-C | `-ai-content` 是否已存在完整 Project Memory。**已核实 → RESOLVED**：P1-B Memory Alignment 确认完整集合存在（-ai-content Issue #2，commit `fad8b740`）。 | RESOLVED | 2026-08-29 | — | — | — | 已完成 P1-B Memory Alignment | `-ai-content` Issue #2；commit `fad8b740` |
| U-D | 用户长期工作偏好（输出格式、决策方式等）目前只存在于 Buddy 本地 memory，不在 Git。来源不在 Git 且未经 Human 确认，本期不升为 Global 事实。 | OPEN | 2026-08-29 | 2026-09-13 | 下次 Buddy 本地 memory 出现可能影响协作协议的内容时，必须先经此流程确认 | Human + ChatGPT | PENDING | `architecture/MEMORY_ARCHITECTURE.md` §10 |
| U-E | External Memory 的实际收益未验证 —— `external/` 目前只有种子条目，还没有被两个以上项目真实引用。 | OPEN | 2026-08-29 | 2026-09-13 | 任意第二个项目首次引用 `external/` 条目时复查一次 | ChatGPT | PENDING | `architecture/MEMORY_ARCHITECTURE.md` §10; `external/` |
| U-F | `-work-buddy-lab` 的状态不一致 —— `README.md` 记为「FROZEN」并仍列在仓库边界里；`PROJECTS.md` 记为「已从 GitHub 账户消失，已确认删除」。两者未对齐。 | RESOLVED | 2026-08-30 | 2026-09-03 | — | Human + ChatGPT | 已解决（2026-09-04）：当前 README 与 PROJECTS 均记 `-work-buddy-lab` 已删除且不再列入仓库边界/注册表，矛盾实质消失；Human 于 2026-09-04 会话确认按此收口，ChatGPT Review 可复核 | `architecture/MEMORY_ARCHITECTURE.md` §10; `PROJECTS.md`; `README.md` |

---

## 3. 与 `architecture/MEMORY_ROUTER.md` / `architecture/MEMORY_ARCHITECTURE.md` 的关系

```text
一条信息 → architecture/MEMORY_ROUTER.md §1 Q1–Q5 判定
             └── Q5 命中（无法判定）→ 登记本文件
                                       └── 背景/证据回到对应 canonical source
```

- 本文件是 Unknown 事项的**唯一登记表**。
- `architecture/MEMORY_ARCHITECTURE.md` §10 只保留一句话指向本文件，不再维护同等详细的表格。
- 裁决发生后，把该行状态改为 `RESOLVED` 并附解决方式与证据，**不删除该行**（沿用 `architecture/MEMORY_ARCHITECTURE.md` §6「旧事实不删除」原则）。
- `RESOLVED` / `ARCHIVED` 记录保留在历史表中，用于审计；不参与当前待裁决调度。

## 4. 复查规则

1. 每次 Global Memory Review 都必须扫描 `review_by <= today` 的条目。
2. 到期条目必须变成 `REVIEW_DUE`，并在同一次 Review 中：
   - 裁决并记录 `RESOLVED`；或
   - 明确为什么仍不能裁决，改为 `RETAINED_UNKNOWN` 并设置新的 `review_by`。
3. Buddy **不得**自行把 Unknown 改为 `RESOLVED`，也不得替 Human / ChatGPT 做最终事实裁决。
4. 新增 Unknown 必须同时登记本文件；只写进其他 Markdown 表格而不登记，视为结构不完整。
5. 任何与某条 Unknown 的 `复查触发条件` 相匹配的工作开始前，必须先处理该条 Unknown。

