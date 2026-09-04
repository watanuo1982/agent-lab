# buddy-local fine-grained PAT 接线验证回执（H1–H3）

- date: 2026-09-04（D-2 / agent-lab#29 H3）
- executor: buddy-local
- token: fine-grained PAT `buddy-local (WorkBuddy local instance)`（值不入库）
- 本 commit / PR / merge 全部由该 fine-grained token 经 REST API 完成（正向写入验证）

## 验证结果

| 步骤 | 结果 |
|---|---|
| 1. GET /user | ✅ actor=watanuo1982，无 `x-oauth-scopes:` 头（fine-grained 属性确认） |
| 2. 范围内真实 PR 写入 | ✅ 本 PR 即正向验证 |
| 3. 范围外 repo（-quantitative-trading）GET | ✅ 404 Not Found（不可见） |
| 4. `.github/workflows` 写入 | ✅ 403 Resource not accessible by personal access token（最小权限确认） |

## 接线

- 存放：`~/.workbuddy/secrets/buddy_local_gh_pat`（chmod 600；来源 RTF 已移入废纸篓）
- 本地 clone（agent-lab / -ai-content）credential.helper 切换为
  `store --file=/Users/howard/.workbuddy/secrets/github-credential-store`（600）

## 剩余

- H4（Human）：轮换/撤销 classic PAT 后，R-M6-1 关闭，D-2 完全收口
