# IDENTITY_TOKEN_POLICY — 实例身份与凭证映射

> Canonical 层文档（ARCH-001 M6）。目的：让体系能回答「谁执行了什么」，
> 并保证不同执行体不共享高权限身份。本文件不记录任何 token 值。
> 状态模型 / GMR v0.2 不受本文件影响。

## 1. 实例身份登记表（2026-09-04 H4 收口后实测）

| 实例 ID | 载体 | 当前凭证 | 平台侧权限 | 归属可辨性 | 判定 |
|---|---|---|---|---|---|
| `buddy-cloud` | Cloudflare CoreAgent / Domain Runtime | GitHub App `ai-content-cloud-runtime`（App ID 4816080，2026-09-03 创建） | `contents:write` + `metadata:read` | **平台级**：push actor = `ai-content-cloud-runtime[bot]`，commit 带 GitHub GPG 签名（verified: valid） | ✅ 已分离，最小权限 |
| `buddy-local` | 本地 WorkBuddy（Human 的 Mac） | fine-grained PAT `buddy-local (WorkBuddy local instance)`（2026-09-04 H1–H3 接线） | 五仓库 agent-lab / -ai-content / -agent-runtime / -quantitative-trading / -commercial-radar（2026-09-04 扩展，见 §4 R-POST-D2-1）：Contents/PR/Issues RW + Metadata R（实测 workflows 403、范围外 repo 404） | 实例级 token（M6 目标形态），与 Human 凭证分离 | ✅ 已分离，最小权限 |
| `Human` | watanuo1982 本人 | classic PAT 已于 2026-09-04 H4 **撤销**（钥匙串条目实测 401，已清除）；当前无常驻本地 GitHub 凭证 | — | Human 平台动作均经本人账号/网页 | ✅ 不再与任何实例共享 |

实测证据：`x-oauth-scopes` 响应头核查（2026-09-04）、GitHub App 公开档案
`https://github.com/apps/ai-content-cloud-runtime`、`-ai-content` push 事件 actor 记录、
commit `2c016afb` 签名信息、fine-grained 四步验证回执 `archive/fine-grained-pat-verification-20260904.md`。

## 2. 归属判定规则（Evidence-first）

- Git commit 的 author/committer 字段是**自声明元数据，可伪造**，单独不构成身份证据。
- 平台级可辨身份 = 以下之一：
  1. **GitHub App bot 身份**：push actor 为 bot 账号 + GitHub 代签名（当前 `buddy-cloud` 即此形态）；
  2. **实例级 token**：fine-grained PAT 与实例一一绑定，push actor 归属 token 所有者账号（当前 `buddy-local` 即此形态）；
  3. Issue 评论等操作以操作者账号落痕，凭证分离后 actor 即实例。
- `EXECUTION_RECEIPT.md` 的 `executor` / `produced_by` 字段必须填写实例 ID
  （本表第 1 列），不得填写产品名或「AI」等类别词。

## 3. 目标凭证规格

### 3.1 buddy-cloud（已达成，登记为既有事实）

GitHub App `ai-content-cloud-runtime`：permissions = `contents:write`、`metadata:read`。
任何新增权限须先在本文件登记理由再操作。

### 3.2 buddy-local（✅ 2026-09-04 已分离接线，H1–H3 完成）

GitHub 不提供 fine-grained PAT 的创建 API（实测 `POST /user/personal-access-tokens` → 404），
创建必须由 Human 在网页完成。规格（最小集）：

> **2026-09-04 D-2 H3 状态更新**：token 已由 Human 创建并落地于本节规定存放路径；四步验证协议全部通过
>（回执 `archive/fine-grained-pat-verification-20260904.md`，PR #31，全程由该 token 经 REST API 完成）。
> 本地 agent-lab / -ai-content / -agent-runtime clone 的 credential.helper 均已切换为
> `store --file=<secrets>/github-credential-store`（600；repo 级先置空再 add，覆盖全局 osxkeychain）。
> **2026-09-04 补充**：Human 已在 UI 将 Repository access 扩入 `-quantitative-trading` / `-commercial-radar`
>（两仓 API 实测 200），`-quantitative-trading` clone 已接线同一 store（R-POST-D2-1 关闭）。
> Expiration 90 天——**约 2026-12-03 到期，轮换时更新本文件**。

- **Token name**：`buddy-local (WorkBuddy local instance)`
- **Expiration**：90 days（到期轮换，轮换时更新本文件）
- **Repository access**：Only select repositories → `watanuo1982/agent-lab`、`watanuo1982/-ai-content`、`watanuo1982/-agent-runtime`（创建时最小集；2026-09-04 经 Human UI 扩入 `-quantitative-trading`、`-commercial-radar`，共五仓）
- **Permissions**：`Contents: Read and write`、`Pull requests: Read and write`、`Issues: Read and write`、`Metadata: Read-only`
- **明确不授予**：`workflows`（CI 变更走 Human）、`secrets`、`administration`、一切 `admin:*`
- **存放**：`~/.workbuddy/secrets/buddy_local_gh_pat`，`chmod 600`，绝不写入任何仓库/Issue/文档/对话
- **接线**：agent-lab / -ai-content / -agent-runtime / -quantitative-trading 本地 clone 使用
  `git config credential.helper "store --file=<secrets 路径>"` 实现按仓库区分凭证
  （-commercial-radar 无本地 clone，暂无需接线）；
  Human 其余 git 操作不受影响

创建后验证协议（由 buddy-local 执行并回报 Issue #15）：
1. `GET /user` 确认 actor = watanuo1982、token 为 fine-grained（无 `X-OAuth-Scopes` 头）；
2. 对授权范围内 repo 完成一次真实 PR 写入（正向）；
3. 对范围外 repo 尝试访问 → 预期 403（负向）；
4. 尝试修改 `.github/workflows` → 预期被拒（负向，验证最小权限）。

## 4. 风险登记（分离完成前有效）

- **R-M6-1 [Conflict]（✅ 2026-09-04 CLOSED）**：classic PAT 曾被 Human 与 buddy-local 共享，
  Git 历史/操作日志无法区分二者。**2026-09-04 收口**：buddy-local 切换至 fine-grained PAT（§3.2），
  Human 撤销 classic PAT（钥匙串实测 401），共享状态不复存在。
- **R-M6-2（✅ 2026-09-04 已完成）**：classic PAT 曾在历史对话与本地 stdout 输出中出现（前缀可溯），
  Human 已于 2026-09-04 H4 将其撤销，暴露面关闭。
- **R-M6-3**：持有 admin 权限的凭证理论上可先关闭分支保护再直推 main，
  GitHub 原生无解；凭证分离（已完成）+ Human 对凭证的物理掌控是当前缓解。
- **R-POST-D2-1 [Conflict]（✅ 2026-09-04 CLOSED）**：classic PAT 撤销后 `-quantitative-trading` /
  `-commercial-radar` 本地 clone 一度无可用凭证。**收口**：Human 于 UI 将两仓扩入 fine-grained PAT
  仓库范围（API 实测两仓 `GET /repos` → 200），`-quantitative-trading` clone 已接线同一 store。
  注：收口当日 git 端点（github.com:443）正处网络故障期（双代理 502 / 直连超时），
  凭据有效性由 API 200 证明；网络恢复后 git pull/push 即可用（同凭证在 agent-lab 已实测通过）。

## 5. D-2 收口复核（2026-09-04，agent-lab#29）

executor: `buddy-local` ｜ 结论：**PASS WITH CONDITIONS**
（机器可验证项全部通过；剩余项均需 Human GitHub UI 操作，已登记为显式 blocker）
**2026-09-04 更新：H1–H4 已全部完成，条件全部解除，D-2 完全收口（见 §6 变更记录）。**

### 5.1 实测结果（全部为 [Fact]，附复现方式）

| # | 检查项 | 结果 | 证据 |
|---|---|---|---|
| F1 | buddy-local / Human 共享的 classic PAT 仍在用，scope 未收窄 | ❌ 未变 | osxkeychain（github.com）凭据为 `ghp_` 前缀 40 字符；`GET /user` → actor=`watanuo1982`；`x-oauth-scopes` 实测 20 项：admin:enterprise, admin:gpg_key, admin:org, admin:org_hook, admin:public_key, admin:repo_hook, audit_log, codespace, copilot, delete:packages, delete_repo, gist, notifications, project, repo, user, workflow, write:discussion, write:network_configurations, write:packages |
| F2 | fine-grained PAT 无法经 API / 工具链创建 | ❌ 确认不可能 | `POST /user/personal-access-tokens` → HTTP 404（2026-09-04 D-2 复测，与 M6 初测一致） |
| F3 | buddy-cloud 仍绑定 GitHub App 身份，未回归 classic PAT | ✅ 通过 | `-ai-content` commit `2c016afb`（2026-09-04T08:02:12Z）author=`ai-content-cloud-runtime[bot]`（id 324436493），committer=`GitHub / web-flow`（GitHub 代签名）；App 档案页 `github.com/apps/ai-content-cloud-runtime` 在线（private App） |
| F4 | 执行回执 / commit 溯源可区分执行实例 | ✅ App 侧 / ⚠️ local 侧 | `EXECUTION_RECEIPT.md` §2 强制 `executor` ∈ {buddy-local, buddy-cloud, core-agent, chatgpt, human}；`-ai-content` M5 handoff（issue 10 / #15）实测 runtime A（buddy-local）与 runtime B（bot）在 commit 层可区分。buddy-local 与 Human 在平台层仍同 actor（= C1 / R-M6-1，分离完成前无解） |
| F5 | WorkBuddy GitHub MCP 连接器通道独立于 classic PAT | ✅ | 连接器为本地 connector-proxy（`http://127.0.0.1:<port>/…/mcp`），鉴权 = 平台签发 `Authorization` header + `X-WorkBuddy-MCP-Context`（值不记录），不读取 osxkeychain PAT |
| F6 | 本地凭证接线现状 | [Fact] | 4 个本地 clone（agent-lab / -ai-content / -agent-runtime / -quantitative-trading）`credential.helper` 均为 `osxkeychain`，全部解析到同一枚 classic PAT；`-commercial-radar` 无本地 clone。另：agent-lab 本地目录为 codeload 快照基线（分支 master），非 git clone 历史 |

### 5.2 本轮已完成动作（buddy-local，可经工具链执行的部分）

1. F1–F6 全量复核并登记（本节）。
2. 创建 PAT 落地目录 `~/.workbuddy/secrets/`（`chmod 700`）——§3.2 存放路径就绪，等待 H1/H2。
3. 本 Policy 更新随 D-2 PR 落盘。

### 5.3 Human 动作清单（2026-09-04 全部完成）

| # | 动作 | Owner | 状态 |
|---|---|---|---|
| H1 | GitHub UI 创建 fine-grained PAT，规格 = §3.2：name `buddy-local (WorkBuddy local instance)`、90 天、仅 agent-lab / -ai-content / -agent-runtime 三仓库、Contents/PR/Issues RW + Metadata R、不授 workflows/admin | **Human** | ✅ 2026-09-04 完成 |
| H2 | 将新 token 直接写入 `~/.workbuddy/secrets/buddy_local_gh_pat`（`chmod 600`）。**不得经过对话 / Issue / 任何被提交的文件** | **Human** | ✅ 2026-09-04 完成（buddy-local 规范化为 600 并清理 RTF 源文件） |
| H3 | buddy-local 完成按仓库 credential.helper 区分接线，并执行 §3.2 四步验证协议（GET /user 无 X-OAuth-Scopes 头 + 范围内真实 PR 写入 + 范围外 repo 403 + workflows 写入被拒） | buddy-local | ✅ 2026-09-04 完成（PR #31 / #32） |
| H4 | H3 验证通过后，Human 轮换/撤销 classic PAT（Settings → Developer settings → Personal access tokens (classic)），并更新本文件变更记录 | **Human** | ✅ 2026-09-04 完成（钥匙串实测 401，条目已清除） |

### 5.4 判定依据

PASS WITH CONDITIONS：F3 / F4(App 侧) / F5 机器可验证通过，buddy-cloud 侧无回归；
buddy-local 侧分离（H1–H4）严格依赖 GitHub 仅有的网页操作入口，均已登记 owner/action，
无架构漂移、无业务仓库改动、无新增基础设施。

## 6. 变更记录

| 日期 | 实例 | 变更 |
|---|---|---|
| 2026-09-04 | buddy-local | 初版：登记实测状态、归属规则、目标规格、[Blocked] 项与风险 |
| 2026-09-04 | buddy-local | D-2（agent-lab#29）：F1–F6 复核登记、创建 secrets 落地目录、登记 H1–H4 blocker；结论 PASS WITH CONDITIONS |
| 2026-09-04 | buddy-local | D-2 H3（PR #31）：fine-grained PAT 创建落地 + 四步验证全过 + 本地接线完成；剩 **H4（Human 轮换 classic PAT）**，完成后 R-M6-1 关闭、D-2 完全收口 |
| 2026-09-04 | buddy-local | D-2 H4 收口（PR #33）：Human 撤销 classic PAT（钥匙串实测 401，死条目已清除）；§1 登记表、§4 R-M6-1/R-M6-2 更新；-agent-runtime clone 接线；**R-M6-1 CLOSED，D-2 完全收口**；新开 R-POST-D2-1（-quantitative-trading / -commercial-radar 本地凭证待 Human 决策） |
| 2026-09-04 | buddy-local | R-POST-D2-1 收口（PR #34）：Human 在 UI 将 -quantitative-trading / -commercial-radar 扩入 token 仓库范围（API 实测 200），-quantitative-trading clone 接线完成；token 现覆盖五仓库 |
