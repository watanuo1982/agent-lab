# PROJECTS — 项目注册表

| Project ID | Repository | 类型 | 状态 | Project Memory | 说明 |
|---|---|---|---|---|---|
| quantitative-trading | `watanuo1982/-quantitative-trading` | 量化研究 / 实盘策略 | ACTIVE | **ADOPTED**（P1-A, commit `51696258698ff2c29f903f7986ee4e9f40f47004`） | 独立项目，所有策略、数据、实验、报告留在本仓库 |
| ai-content | `watanuo1982/-ai-content` | AI 内容生产 | ACTIVE | **ADOPTED**（P1-B, commit `fad8b740f8ee4041049c18999edccde642a56d30`） | 独立项目，内容、任务、Review、平台实验留在本仓库 |
| commercial-radar | `watanuo1982/-commercial-radar` | 商业机会雷达 / ToC 选品 | ACTIVE | **ADOPTED**（Issue #9, `b29eebf`） | 独立项目，任务走本仓库 GitHub Issues；选品流水线、评分模型、实验记录留在本仓库。**已验证参考实现** |
| agent-runtime | `watanuo1982/agent-runtime` | Cloud Runtime / Agent 执行基础设施 | ACTIVE | **PENDING**（新项目，待初始化） | 独立 Runtime 项目；负责 Cloudflare runtime 实现。首个运行目标为 `core-agent`。**不承载 Global Memory / Agent Hub 治理** |
| agent-hub | `watanuo1982/agent-lab` | 跨项目协作基础设施 | ACTIVE | **不适用**（本层即 Global Memory v0.1，Issue #2） | 项目注册、跨项目通知、协作协议、记忆架构 |

> `Project Memory` 列记录该项目是否已建立 `PROJECT_CONTEXT.md` / `CURRENT_STATE.md` / `NEXT_WORK.md` 等最小记忆集合。
> `quantitative-trading` 与 `ai-content` 的 Project Memory 现状原在 agent-lab Issue #2 因 Non-goals 不迁移业务仓库而标 `[Unknown]` 未核实；**已于 P1-C（agent-lab Issue #3）经 P1-A（qt，commit `5169625`）与 P1-B（ai-content，commit `fad8b740`）核实并标 RESOLVED**，见 `UNKNOWN_REGISTRY.md` U-B / U-C，本表对应行改为 **ADOPTED**。

> `-work-buddy-lab` 已从 GitHub 账户的当前仓库列表中消失，已确认删除。本注册表不再把它作为项目记录。若与其他 Hub 文件发生冲突，统一登记到 `UNKNOWN_REGISTRY.md`，不得在本表自行选边。

## 新项目接入最小规范

新项目必须建立**独立 repository**，然后在本文件登记，并建立最小 Project Memory。

**必须（缺一不可）**

> ⚠️ **P0.6 跨会话恢复实测产物独立归档于 `memory-tests/`**（`run-2026-08-30/` 含 s1/s2/s3 冷启动答案 + `summary.md`），不依赖任何 GitHub Issue 作载体；当时 Issue #3 尚不存在。

1. `README.md` —— 项目是什么、怎么跑、边界在哪。
2. `PROJECT_CONTEXT.md` —— 定位、边界、长期原则、**事实唯一归属表**、证据语义、新会话恢复路径。
3. `CURRENT_STATE.md` —— 当前阶段与当前已证实结论。
4. `NEXT_WORK.md` —— 当前导航与待办摘要。
5. `GITHUB_WORKFLOW.md`（可直接沿用 `-commercial-radar` 的协议）—— Issue 生命周期、状态元数据与 `STATUS:` 审计日志、DoD 模板。
6. 在本表登记，并把 `Project Memory` 列标为 `ADOPTED`。

建议：`DECISIONS.md`、`MEMORY_INDEX.md`、`CHANGELOG.md`。

**不需要**：数据库、向量检索、记忆服务。文件-first 基线的效果没被测量之前，不引入这些依赖。

完整规范见 `MEMORY_ARCHITECTURE.md` §8；已落地的参考实现见 `-commercial-radar`（Issue #9）。

## 项目 repository 自己负责

- README / 项目目标
- PROJECT_CONTEXT.md
- CURRENT_STATE.md
- NEXT_WORK.md
- 项目规范、代码与数据
- 实验记录、Evidence、Review、CHANGELOG

Agent Hub 不复制上述内容，只保存跨项目的任务指针、项目地图和协作协议。

## 仓库边界原则

**一个真实项目 = 一个独立 repository；Agent Hub = 唯一跨项目通知入口。**

## Cloud Runtime 项目边界

`agent-runtime` 是 Agent System 的独立 Runtime implementation project。

- `agent-lab`：Governance / Agent Hub / Global Memory
- `agent-runtime`：Cloud Runtime implementation / deployment
- Cloudflare：运行时平台
- `core-agent`：第一个 Runtime Agent
- Buddy：在明确 Issue 合同下执行实现
- ChatGPT：负责 Runtime 架构、研究、方案、任务合同与 Review

不得把 Runtime implementation code、部署配置或运行时项目 Memory 搬入 `agent-lab`，除非未来发生经过 Evidence → Evaluation → Change Proposal → Approval 的架构变更。
