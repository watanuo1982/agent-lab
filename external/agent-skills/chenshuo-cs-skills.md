# 陈硕 `cs-skills` — External Memory

- 类型：开源 Agent Skills / 工作方法论
- 来源：https://github.com/ChenShuo2004/cs-skills
- 引用日期：2026-08-30
- 相关项目：`agent-lab`, `commercial-radar`, `ai-content`, `-quantitative-trading`
- 状态：`candidate` / 未正式采用

## 我们为什么关注

该项目把个人工作方法编译为可执行 Skill，重点机制包括统一入口/路由、研究型 Skill、交付收尾与验证。它与我们的 ChatGPT → GitHub → Buddy → Review 工作流存在明显交集，因此适合作为 Skill Architecture 的外部参考样本。

## 当前判断

1. `cs-run`：值得研究其「目标 → 路由 → 执行 → 验证」思想，但**不直接采用**；我们的项目路由与 Buddy 协作已有独立协议。
2. `cs-search-skill`：与 `commercial-radar` 的 Research / Evidence 思路高度相关，值得作为 Research Skill Benchmark 的对照样本。
3. `cs-ending-time`：其「执行完成 ≠ 交付完成」以及 commit / push / verification / closeout 思路与我们现有交付痛点高度相关，值得作为 Delivery Verification Benchmark 的对照样本。
4. 不建议整套安装。外部 Skill 必须经过真实任务 Benchmark 后再决定 `ADOPT / ADAPT / REJECT`。

## 与我们 Skill Architecture 的关系

本条目只记录外部项目本身及我们的采用判据；我们自己的 Skill Contract、Skill Audit、Skill Lifecycle 属于 `agent-lab` Global Memory，不在这里定义。

## 证据纪律

- 本条目不是我们已经验证这些 Skill 有效的证据。
- GitHub stars、作者描述、公开帖子不能单独构成 `[Experiment]`。
- 若未来进行真实 Benchmark，实验结果应记录在对应项目或 `agent-lab` 的研究/实验文件中，并由结果决定是否 Adopt。
