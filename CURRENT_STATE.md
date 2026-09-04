# CURRENT_STATE.md — Agent Hub

> `agent-lab` 是 Global Memory / Agent Hub，不是普通业务项目；本文件记录 Hub 自身的当前治理状态。

## 当前状态

- **治理基线**：GMR v0.2 已实施；Git-native、文件优先，无数据库/向量库/第二套任务系统。
- **Universal Agent entrypoint**：`AGENTS.md` + `architecture/AGENT_GIT_MEMORY_CONTRACT.md` v1.1；所有新工作 Session 默认先进入 Git Memory Mode。
- **Mandatory bootstrap**：Global Bootstrap 已明确为**每个新 Session 的强制启动动作**，不依赖 Human 是否说“检查 Git 的记忆”。Session memory / 旧聊天不能替代 Git Bootstrap。
- **Memory architecture**：四层模型已建立；`architecture/MEMORY_ARCHITECTURE.md` 定义模型，`architecture/MEMORY_ROUTER.md` §1 是唯一操作性路由规则源。
- **Runtime manifest**：`MEMORY_MANIFEST.yaml` v0.3 已建立，提供机器可读的 mandatory-every-new-session Bootstrap、路由、生命周期、写入策略与 Health 检查入口。
- **Plan continuity**：`architecture/PLAN_PROTOCOL.md` 定义已确认计划的 canonical ownership、版本与变更控制；新 Session 默认继续 Active Plan。
- **Session bootstrap**：`architecture/SESSION_BOOTSTRAP.md` v0.3 规定 Global Bootstrap → Project Bootstrap → Plan Continuity → Task Resolution。
- **Session Trigger Monitor**：GMR v0.2 已正式建立；每轮对话进行轻量 Trigger Scan，强 Trigger 与自然检查点进入 Memory Evaluation。
- **Automatic Memory Sync**：已正式纳入 Universal Agent Contract 与 GMR v0.2；产生 durable change 时 Agent 必须自动执行 Memory Sync Gate，并在需要时写回 canonical owner；无 durable change 则不产生无意义提交。
- **Memory Owner**：ChatGPT 在具备 Git 写权限时直接负责 durable-memory 的判断、路由、写回与验证；Buddy 仅负责执行，不是 Memory Owner，也不是 ChatGPT 写回的必要中介。
- **Promotion policy**：L0 不写、L1 自动写、L2 提案、L3 Human 确认；Project 不自动升级 Global。
- **History semantics**：核心记忆不删除；变化采用 `SUPERSEDE`，保留 provenance 与历史。
- **Unknown governance**：`UNKNOWN_REGISTRY.md` 是唯一登记与生命周期入口。
- **Project registry**：`PROJECTS.md` 是跨项目注册表；业务项目的详细事实留在各自仓库。
- **Task protocol**：GitHub Issue 是正式任务载体；`STATUS:` 评论是审计日志，机器 current status 使用 `status:*` Label。
- **Cloud Runtime architecture**：Cloud Runtime 是后续演进层，不是原始 AI 协作设计的一部分；当前 canonical architecture 见 `architecture/CLOUD_RUNTIME_ARCHITECTURE.md` v0.3，定义 CoreAgent 为统一 Runtime/orchestration 层、Domain Runtime 为受控领域执行层。
- **Control Tower**：仍只作为设计概念，不在未裁决情况下猜测其实际建立状态。

## 治理状态
- **M5 Cross-Runtime Handoff**：2026-09-04 完成 buddy-local → core-agent 最小接力实验（-ai-content `005_m5_handoff/`，B 以 `ai-content-cloud-runtime[bot]` 身份仅凭 GitHub 冷启动接手并落笔）；机制链路 PASS，content_revise 下游 4xx 与产出质量偏差已登记（见 Issue #15 M5 回报）。
- **M6 Identity / Token Separation（D-2 收口，Issue #29，VERIFIED）**：三执行体身份完全分离——buddy-cloud = GitHub App `ai-content-cloud-runtime`（bot actor + 平台代签名）；buddy-local = fine-grained PAT（四步验证全过：无 scope 头 / 范围内真实 PR / 范围外 404 / workflows 403），classic PAT 已撤销（401 实测）、钥匙串死条目清除，token 覆盖五注册仓库；R-M6-1 / R-M6-2 关闭。规格、验证协议与风险登记见 `architecture/IDENTITY_TOKEN_POLICY.md`。
- **ARCH-001 Round 5 候选落盘**：2026-09-04 将 Final Architecture Candidate（评论 5537869348）忠实转录为 `architecture/ARCH-001_FINAL_ARCHITECTURE.md`（CANDIDATE 未冻结，冻结待 Human 批准）；buddy-local 独立审查结论见 Issue #15。
- **ARCH-001 Freeze Prep**：2026-09-04 按 buddy-local 最终审查（评论 5537995684）的 5 项 Required Changes 完成 Freeze Candidate 修正：M6 表述如实改为 PARTIAL 并登记 open items（buddy-local fine-grained PAT 创建 / classic PAT 轮换）、Phase A 撤销 -agent-runtime 未注册误判（commit 28a181f8 已注册）、Phase B 清单补全三个新 canonical 文件并加入 README 文件地图规则、Phase C 增加 quantitative-trading 只读先行与 commercial-radar [Unknown] 先盘点护栏；文件状态 `READY FOR HUMAN FINAL APPROVAL`，未冻结。
- **ARCH-001 已冻结**：2026-09-04 Human Final Approval（Issue #15 评论 5538205132）——`architecture/ARCH-001_FINAL_ARCHITECTURE.md` 为 canonical architecture baseline（FROZEN）；GMR v0.2 不变，仍为 memory baseline；open items（buddy-local fine-grained PAT 创建 / classic PAT 轮换）继续按 `architecture/IDENTITY_TOKEN_POLICY.md` 跟踪，不因冻结自动完成。
- **ARCH-001-IMPL-01（Phase A + Phase B）**：Issue #23 完成并 VERIFIED——Hub 自身 canonical 收敛与协议对齐（ARCH 状态改写、README 文件地图收敛、CURRENT_STATE/NEXT_WORK 登记、协议文件一致性修正）。
- **Phase C 核心目标（状态元数据对齐）**：由 D-3 覆盖（Issue #35，VERIFIED）——三业务仓 open issues 全部对齐 canonical `status:*` Label、label 定义补齐、`GITHUB_WORKFLOW.md` 状态元数据章节、validator 跨仓库检查；agent-runtime 定位审计由 D-5（Issue #39）覆盖。逐项目深度审计不再单独立项。
- **Phase D Governance Hardening（D-2 ~ D-6，2026-09-04 全部收口）**：D-2 身份/凭证分离（#29）、D-3 状态元数据统一（#35）、D-4 权限治理（#37，五执行体 permission matrix + least-privilege 实测）、D-5 runtime 仓库定位审计（#39）、D-6 收口审计（#40，判定 PASS——Phase D 正式结束，停止架构治理转回业务执行）。全部 ChatGPT VERIFIED。
- **其他（2026-09-04）**：agent-lab 由 public 转为 private（D-4 U2 解决）；五仓关键文档中文化、12 个架构/协议文档归位 `architecture/`；fine-grained PAT 约 2026-12-03 到期需轮换（届时更新 `architecture/IDENTITY_TOKEN_POLICY.md`）。
- **M0 Governance Enforcement**：2026-09-04 起 main 分支保护已启用（PR-only + required check `validate-memory` + enforce_admins + 禁 force push/删除）；CODEOWNERS 已声明 canonical 文件 owner = Human；验收实验（直推 main 被 GH006 拒绝 / 违规 PR merge 被 405 拒绝）见 Issue #15 M0 回报。

- Issue #4：已完成并关闭；`status:verified`。
- GMR v0.2 implementation issue：Issue #14，规格已执行；实现变更已直接由 ChatGPT 写入 `agent-lab`，Buddy 未承担 Memory Owner 角色。
- Current governance priority：以真实新 Session cold-start 验收 GMR v0.2（Issue #14，IMPLEMENTED / PENDING COLD-START ACCEPTANCE）；架构治理已随 Phase D 收口进入稳态维护，仅在新执行实例 / 新仓库 / token 轮换 / 漂移迹象时重启。

## 已知开放风险

1. Plan continuity 的跨仓库自动一致性检查尚未完全工程化。
2. `PROJECTS.md` 跨私有仓库 existence/accessibility 校验需要 `PROJECT_REGISTRY_TOKEN` 才能在 CI 实际执行。
3. External Memory freshness 目前只有规则层要求，尚无自动检查。
4. 并发目前采用 Issue ownership + 避免同时修改同一 canonical file；暂不引入 distributed lock。
5. **真实 cold-start 的“模型自动调用 GitHub 工具”属于 Agent 执行能力问题，协议层已改为 mandatory；需要后续新 Session 实测验收。**
6. Trigger Monitor 的语义判断目前主要由遵约 Agent runtime 执行；后续如需要机器化检测，可增加 validator，但不得改变 canonical policy。

## 恢复路径

每个新 Session 的标准恢复路径为：

`New Session → AGENT_GIT_MEMORY_CONTRACT → Global Bootstrap → 项目识别 → Project Bootstrap → Active Plan → Issue → Review → Trigger Monitor / Memory Sync`

Human 不需要提供启动文件清单，也不需要提醒“上传记忆”。

