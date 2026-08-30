# Agent Skills Benchmark — 2026-08

> 外部研究记录。记录外部 Skill 体系及其对本体系的判据；不等同于已采用。

## 结论摘要

当前最值得吸收的不是某个具体 Skill，而是 **Skill 的选择、验证和生命周期机制**：

1. Skill 应按需发现/加载，而不是无差别全部注入。
2. Discipline/Workflow 类 Skill 应先做 baseline，再做 pressure test；Skill 本身应像代码一样测试。
3. Skill 的完成标准必须包含 evidence / verification，而不是 agent 自报完成。
4. Adversarial / pre-mortem 类 Skill 对 Commercial Radar、P02 选题和 Quant Research 都可能有高复用价值。
5. 任何 Skill 在进入正式体系前，应有真实任务上的收益证据；“看起来专业”不算采用依据。

## 样本 1：obra/superpowers

- 来源：https://github.com/obra/superpowers
- 引用日期：2026-08-30
- 类型：Agentic skills framework / 软件开发方法论
- 关键机制：mandatory workflow、verification-before-completion、writing-skills、skill evals、RED-GREEN-REFACTOR。
- 关键证据：其 writing-skills 要求先运行无 Skill baseline，观察 agent 实际失败与 rationalization，再写 Skill；随后 pressure test，继续 refactor 直到漏洞关闭。其 evals 使用真实 LLM session 驱动的行为测试，而不是只检查文档格式。
- 判据：**高度相关，建议 ADAPT 到我们的 Skill Contract。**
- 限制：原体系主要面向软件开发；不能直接假定其流程适用于商业研究或内容选题。

## 样本 2：anthropics/skills

- 来源：https://github.com/anthropics/skills
- 引用日期：2026-08-30
- 类型：Agent Skills 参考实现
- 关键机制：SKILL.md 入口、YAML metadata、progressive disclosure、scripts/references/assets 分层；skill-creator 明确支持创建、修改、性能测量、benchmark 与 trigger 优化。
- 判据：**作为结构规范参考，建议 ADOPT 其“metadata → SKILL.md → bundled resources”分层思想。**
- 限制：这是技能格式/作者工具的参考实现，不证明某个 Skill 本身有效。

## 样本 3：carlkibler/agent-skills

- 来源：https://github.com/carlkibler/agent-skills
- 引用日期：2026-08-30
- 类型：可复用 Agent Skills
- 关键机制：pre-mortem 让多个 agent 从不同失败角度攻击计划；empathy-audit 从 user/machine/developer/support 四个视角审查完成后的产品；另有 decision-log、release verification 等。
- 判据：**建议 ADAPT pre-mortem / adversarial review。**
- 限制：具体 Skill 的收益仍需在我们的真实任务上验证。

## 对我们的 Skill Contract 的新增原则

### Skill 必须有 Evaluation

最低要求：
- baseline（无 Skill）
- intervention（有 Skill）
- measurable outcome
- cost（tokens/time/tool calls/human review）
- decision：ADOPT / ADAPT / REJECT

### Discipline Skill 的测试方法

```text
RED: 无 Skill，观察真实失败
→ capture failure / rationalization
GREEN: 最小 Skill，重复同场景
→ verify compliance
REFACTOR: 压力测试，寻找新 loophole
→ re-test
```

### 当前采用状态

- `cs-skills`：CANDIDATE / 未正式采用
- `superpowers`：CANDIDATE / 方法论参考，未整体采用
- `anthropics/skills`：REFERENCE / 结构规范参考
- `carlkibler/agent-skills`：CANDIDATE / pre-mortem 候选

## 下一步

不创建 Buddy Issue。先在 ChatGPT 侧设计最小 Benchmark：

1. Commercial Radar：普通研究 vs research + adversarial/pre-mortem
2. P02：普通选题判断 vs 加入 evidence/kill-condition
3. Agent execution：普通完成声明 vs verification gate

只有 Benchmark 产生明确收益后，才把结论迁移到 Global Skill Contract 或具体 Project Memory。
