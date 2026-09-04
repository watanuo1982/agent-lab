# IDENTITY_TOKEN_POLICY — 实例身份与凭证映射

> Canonical 层文档（ARCH-001 M6）。目的：让体系能回答「谁执行了什么」，
> 并保证不同执行体不共享高权限身份。本文件不记录任何 token 值。
> 状态模型 / GMR v0.2 不受本文件影响。

## 1. 实例身份登记表（2026-09-04 实测）

| 实例 ID | 载体 | 当前凭证 | 平台侧权限 | 归属可辨性 | 判定 |
|---|---|---|---|---|---|
| `buddy-cloud` | Cloudflare CoreAgent / Domain Runtime | GitHub App `ai-content-cloud-runtime`（App ID 4816080，2026-09-03 创建） | `contents:write` + `metadata:read` | **平台级**：push actor = `ai-content-cloud-runtime[bot]`，commit 带 GitHub GPG 签名（verified: valid） | ✅ 已分离，最小权限 |
| `buddy-local` | 本地 WorkBuddy（Human 的 Mac） | Human 的 classic PAT（唯一凭证条目） | 实测 20 项 scope（`repo, workflow, admin:org, delete_repo, audit_log…`） | 平台 actor = `watanuo1982`，与 Human 不可区分 | ❌ 共享凭证（Critical C1） |
| `Human` | watanuo1982 本人 | 同一枚 classic PAT | 同上 | 同上 | ❌ 与 buddy-local 共享 |

实测证据：`x-oauth-scopes` 响应头核查（2026-09-04）、
GitHub App 公开档案 `https://github.com/apps/ai-content-cloud-runtime`、
`-ai-content` push 事件 actor 记录、commit `2c016afb` 签名信息。

## 2. 归属判定规则（Evidence-first）

- Git commit 的 author/committer 字段是**自声明元数据，可伪造**，单独不构成身份证据。
- 平台级可辨身份 = 以下之一：
  1. **GitHub App bot 身份**：push actor 为 bot 账号 + GitHub 代签名（当前 `buddy-cloud` 即此形态）；
  2. **实例级 token**：fine-grained PAT 与实例一一绑定，push actor 归属 token 所有者账号（M6 目标形态）；
  3. Issue 评论等操作以操作者账号落痕，凭证分离后 actor 即实例。
- `EXECUTION_RECEIPT.md` 的 `executor` / `produced_by` 字段必须填写实例 ID
  （本表第 1 列），不得填写产品名或「AI」等类别词。

## 3. 目标凭证规格

### 3.1 buddy-cloud（已达成，登记为既有事实）

GitHub App `ai-content-cloud-runtime`：permissions = `contents:write`、`metadata:read`。
任何新增权限须先在本文件登记理由再操作。

### 3.2 buddy-local（[Blocked] 待 Human 创建）

GitHub 不提供 fine-grained PAT 的创建 API（实测 `POST /user/personal-access-tokens` → 404），
创建必须由 Human 在网页完成。规格（最小集）：

- **Token name**：`buddy-local (WorkBuddy local instance)`
- **Expiration**：90 days（到期轮换，轮换时更新本文件）
- **Repository access**：Only select repositories → `watanuo1982/agent-lab`、`watanuo1982/-ai-content`、`watanuo1982/-agent-runtime`
- **Permissions**：`Contents: Read and write`、`Pull requests: Read and write`、`Issues: Read and write`、`Metadata: Read-only`
- **明确不授予**：`workflows`（CI 变更走 Human）、`secrets`、`administration`、一切 `admin:*`
- **存放**：`~/.workbuddy/secrets/buddy_local_gh_pat`，`chmod 600`，绝不写入任何仓库/Issue/文档/对话
- **接线**：agent-lab / -ai-content 本地 clone 使用
  `git config credential.helper "store --file=<secrets 路径>"` 实现按仓库区分凭证；
  Human 其余 git 操作不受影响

创建后验证协议（由 buddy-local 执行并回报 Issue #15）：
1. `GET /user` 确认 actor = watanuo1982、token 为 fine-grained（无 `X-OAuth-Scopes` 头）；
2. 对授权范围内 repo 完成一次真实 PR 写入（正向）；
3. 对范围外 repo（如 `-quantitative-trading`）尝试访问 → 预期 403（负向）；
4. 尝试修改 `.github/workflows` → 预期被拒（负向，验证最小权限）。

## 4. 风险登记（分离完成前有效）

- **R-M6-1 [Conflict]**：classic PAT 在分离完成前仍被 Human 与 buddy-local 共享，
  Git 历史/操作日志无法区分二者，M0 的治理防线对此不可审计。
- **R-M6-2**：classic PAT 曾在历史对话与本地 stdout 输出中出现（前缀可溯），
  分离完成后 Human 应将其**轮换**（撤销旧 PAT 需网页操作，API 无法自删）。
- **R-M6-3**：持有 admin 权限的凭证理论上可先关闭分支保护再直推 main，
  GitHub 原生无解；凭证分离 + Human 对凭证的物理掌控是当前唯一缓解。

## 5. 变更记录

| 日期 | 实例 | 变更 |
|---|---|---|
| 2026-09-04 | buddy-local | 初版：登记实测状态、归属规则、目标规格、[Blocked] 项与风险 |
