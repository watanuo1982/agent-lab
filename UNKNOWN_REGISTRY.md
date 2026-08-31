# Unknown Registry — Global

> 本文件是 `[Unknown]` 的**生命周期与复查登记表**。
> `MEMORY_ARCHITECTURE.md §10` 保留 Unknown 的背景与证据说明；本文件只负责：**何时发现、何时复查、由谁裁决、当前状态**。
>
> 不允许在这里复制完整事实正文。需要完整背景时回到 `MEMORY_ARCHITECTURE.md §10` 或其指向的 canonical source。

## Lifecycle

```text
OPEN → REVIEW_DUE → RESOLVED / RETAINED_UNKNOWN → ARCHIVED
```

- `OPEN`：已登记，尚未到复查日期。
- `REVIEW_DUE`：到达 `review_by`，必须进入下一次 Global Memory Review。
- `RESOLVED`：Human / ChatGPT 已有足够证据完成裁决。
- `RETAINED_UNKNOWN`：复查后仍无法裁决，必须更新 `review_by`，不能无限期悬挂。
- `ARCHIVED`：问题已不再具有当前工作价值，但历史记录保留。

### Required fields

每条 Unknown 至少需要：

| Field | Meaning |
|---|---|
| `id` | 与 `MEMORY_ARCHITECTURE.md §10` 对应的 ID |
| `status` | 生命周期状态 |
| `discovered_at` | 首次发现日期（YYYY-MM-DD） |
| `review_by` | 下一次强制复查日期（YYYY-MM-DD） |
| `owner` | 负责推动裁决的角色：Human / ChatGPT |
| `decision` | RESOLVED 时记录结论；否则写 `PENDING` |
| `evidence` | 指向证据/canonical source，不复制正文 |

## Current registry

| ID | Status | Discovered | Review by | Owner | Decision | Evidence |
|---|---|---|---|---|---|---|
| U-A | OPEN | 2026-08-30 | 2026-09-03 | Human + ChatGPT | PENDING | `MEMORY_ARCHITECTURE.md §10` |
| U-D | OPEN | 2026-08-30 | 2026-09-13 | Human + ChatGPT | PENDING | `MEMORY_ARCHITECTURE.md §10` |
| U-E | OPEN | 2026-08-30 | 2026-09-13 | ChatGPT | PENDING | `MEMORY_ARCHITECTURE.md §10`; `external/` |
| U-F | OPEN | 2026-08-30 | 2026-09-03 | Human + ChatGPT | PENDING | `MEMORY_ARCHITECTURE.md §10`; `PROJECTS.md` |

## Review rule

1. 每次 Global Memory Review 都必须扫描 `review_by <= today` 的条目。
2. 到期条目不得继续保持 `OPEN`；必须变成 `REVIEW_DUE`，并在同一次 Review 中：
   - 裁决并记录 `RESOLVED`；或
   - 明确为什么仍不能裁决，并设置新的 `review_by`。
3. Buddy **不得**自行把 Unknown 改为 Resolved，也不得替 Human / ChatGPT 做最终事实裁决。
4. 新增 Unknown 必须同时登记本文件；只写进其他 Markdown 表格而不登记，视为结构不完整。
5. 本文件只管理生命周期；完整事实、冲突双方与证据仍以 `MEMORY_ARCHITECTURE.md §10` 及对应 canonical source 为准。
