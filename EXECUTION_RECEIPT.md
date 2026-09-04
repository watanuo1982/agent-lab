# Execution Receipt 规范（M2）

> **定位**：Evidence-first 的机器可读执行回执约定。它回答一个问题——**「谁在哪个环境里实际执行了什么，留下了什么不可伪造的痕迹」**。
> 来源：ARCH-001 Round 3/4 已收敛的裁决（Issue #15）。本文只落约定，不改架构、不新增基础设施。
> 加载时机：按需（产出或验证 Evidence 时读本文），不进入 Session Bootstrap 必读清单。

## 1. 原则（不可协商）

1. **Evidence 优先来自 Runtime / CI 的执行副产物**。执行环境自己留下的痕迹（check run、workflow run、webhook 回写、产物哈希）天然不可被 Agent 伪造。
2. **Agent 自称 `STATUS: DONE` 不构成独立 Evidence**。它只是审计日志，最多算 `agent-declared` 级别的自述（见 §3）。
3. **写者 ≠ 验证者（尽可能）**。执行者产出的回执，由非执行方（另一个实例 / CI / ChatGPT Review / Human）确认后才算 Verified。
4. **GMR v0.2 不受影响**。Receipt 是 task-scope 的过程记录，随 Issue 评论与 commit 历史沉淀，不进入 Memory 四层的 canonical 状态文件，不新建 DB / queue / orchestrator / repo。

## 2. 必填字段

每个 Receipt 是一个结构化块（建议 YAML，嵌入 Issue 回报评论或 PR body）：

| 字段 | 必填 | 含义与格式 |
|---|---|---|
| `task_id` | ✅ | 任务唯一标识 = 承载该任务的 GitHub Issue（如 `agent-lab#15`）。Issue-first：没有 Issue 就没有任务。 |
| `executor` | ✅ | **实例限定**执行者 ID：`buddy-local` / `buddy-cloud` / `core-agent` / `chatgpt` / `human`。禁止只写产品名（"Buddy"），能力与权限不跨实例继承。 |
| `execution_id` | ✅ | 本次执行尝试的唯一 ID：`<executor>-<yyyymmddHHMMSS>`（同任务可多次执行，每次一个新 ID）。 |
| `timestamp` | ✅ | ISO 8601（UTC），执行完成时刻。 |
| `commit_sha` | ✅ | 携带本次变更的 commit 完整 SHA；纯元数据操作（如改 Label）填触发本次验证的 head SHA 并注明 `commit_carrying=no-op`。 |
| `artifact` | ✅ | 产物引用：文件路径 / Issue 评论 URL / CI run URL。至少一项。 |
| `artifact_hash` | 适用时 | 产物的 sha256（确定性产物必填；纯文档变更可用 `git hash-object` 值）。 |
| `exit_status` | ✅ | 退出状态：exit code 或 `success` / `failure` / `partial`。 |
| `environment` | ✅ | 执行环境描述：`runtime:local-macos` / `runtime:cloud-sandbox` / `runtime:github-actions` / `runtime:cloudflare-worker`，可附 OS/runner 简述。 |
| `produced_by` | ✅ | 本回执**由谁机械地产出**，取值见 §3。这是防自证冒充的关键字段。 |

## 3. `produced_by` 取值（Evidence 独立性分级）

与 Round 3 合并方案一致：**等级轴 × 独立性轴**。`produced_by` 标注独立性：

| 值 | 含义 | 独立性 | 能否单独作为完成依据 |
|---|---|---|---|
| `ci-generated` | GitHub Actions check run / artifact，由 GitHub 自产 | 机器级，Agent 不可伪造 | ✅ 可以（如 required check 绿） |
| `runtime-executed` | Cloud Runtime（CoreAgent 链路）执行副产物，含 webhook 签名校验记录 | 机器级 | ✅ 可以 |
| `tool-verified` | 确定性工具输出（如 `validate_memory_structure.py` exit 0），他人可用同一输入复现 | 可复现 | ✅ 可以（附复现命令） |
| `human-confirmed` | Human 在 Git/Issue 中的显式确认 | 最终权威 | ✅ 可以 |
| `agent-declared` | Agent 的叙述（`STATUS: DONE`、口头总结、回执本身由 Agent 手写） | **无独立性** | ❌ 不可以；只能作为线索，必须有上述四类之一补强 |

**规则：`produced_by: agent-declared` 的回执封顶为线索级**。一条回报要满足 DoD，至少需要一条非 `agent-declared` 的 Evidence 与之对应。

## 4. 标准格式（示例）

```yaml
# EXECUTION_RECEIPT v1
task_id: agent-lab#15
executor: buddy-local
execution_id: buddy-local-20260904T070000Z
timestamp: 2026-09-04T07:05:12Z
commit_sha: "<修复 commit 完整 SHA>"
artifact:
  - "scripts/validate_memory_structure.py"
  - "https://github.com/watanuo1982/agent-lab/actions/runs/<run_id>"
artifact_hash: "sha256:<产物哈希或 git hash-object>"
exit_status: 0
environment: "runtime:local-macos (macOS, python3.13)"
produced_by: tool-verified
evidence_note: >
  本地 GITHUB_TOKEN=<PAT> python3 scripts/validate_memory_structure.py → exit 0;
  CI run <run_id>（ci-generated）在同 head 上 conclusion=success。
```

## 5. 记录位置与生命周期

- **存放**：Issue 回报评论（主）/ PR body（有 PR 时）+ commit message 引用 `execution_id`。不新建任何存储。
- **验证**：ChatGPT Review 或另一实例复核非 `agent-declared` 证据后，Issue 状态 Label 迁移（`status:done` → `status:verified`），沿用 README「状态模型」。
- **归档**：Issue 关闭即自然归档；Receipt 不复制进 Hub 层记忆文件（保持 Hub 只存协议与指针）。

## 6. 与现有体系的关系

- **GMR v0.2 / MEMORY_MANIFEST.yaml**：零修改。Receipt 是 task-scope 过程记录，路由规则照旧（MEMORY_ROUTER.md）。
- **README「状态模型」**：`status:*` Label 仍是机器可查的 current status；`STATUS:` 评论降级为审计日志——Receipt 是审计日志的**结构化超集**。
- **CI（memory-structure.yml）**：绿 run 本身就是 `ci-generated` Evidence；required check 化（M0）后即为机器级完成依据。
- **演进**：本规范为 v1。字段变更走 ARCH-001 正常流程（Issue 提案 → Round 评审 → Human 决策），不得静默修改。
