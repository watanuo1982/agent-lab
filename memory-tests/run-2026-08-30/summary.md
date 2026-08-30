# 跨会话记忆恢复实测 — 2026-08-30 记录

**被测版本**：`agent-lab` @ `52edc68`（Memory Architecture v0.1）+ `watanuo1982/-commercial-radar` @ `b29eebf`（Project Memory，Issue #9 交付）
**测试时间**：2026-08-30
**方法**：冷启动模拟——三个全新上下文 Agent，分别只给一个物理隔离的远端快照目录（`/tmp/ct1` Hub / `/tmp/ct2` Project / `/tmp/ct3` Hub 但问项目级问题），禁止读 memory-tests/、禁止联网、禁止猜测。
**协议**：见 `../protocol.md`（跑测前预登记，题目+通过线+评分口径已写死，未事后拟合）

---

## 1. 评分矩阵

| 场景 | 题 | 结果 | 备注 |
|---|---|---|---|
| S1 Global | G1 | PASS | 正确识别 README 5 仓库 vs PROJECTS 4 仓库矛盾，引用 U-F |
| S1 | G2 | PASS | 三角色职责 + 任务合同=业务仓库 Issue |
| S1 | G3 | PASS | 4 层边界正确 |
| S1 | G4 | PASS | 路由前两步 Q1 Session / Q2 External 顺序正确 |
| S1 | G5 | PASS | 5 标记 + `[Experiment]` 成立条件正确 |
| S1 | G6 | PASS | 恢复路径顺序与 §9 一致 |
| S1 | G7 | PASS | Hub 硬边界正确 |
| S1 | G8 | PASS | 列出全部 6 个 Unknown（U-A~U-F） |
| **S1 小计** | | **8/8 PASS，0 FABRICATED** | |
| S2 Project | P1 | PASS | |
| S2 | P2 | PASS | 正确指出全仓库 0 条 `[Experiment]` |
| S2 | P3 | PASS | 指向 Issue #8 + 交付物 |
| S2 | P4 | PASS | B2B 暂停 + 多项否决，理由正确 |
| S2 | P5 | PASS | 两套互斥模型 + 引用注意 |
| S2 | P6 | PASS | fixtures 不可用于商业判断 |
| S2 | P7 | PASS | 两条验证命令正确（分项数字沿用修复前文档，见 F-3） |
| S2 | P8 | PASS | D-05 内容正确 |
| **S2 小计** | | **8/8 PASS，0 FABRICATED** | |
| S3 边界 | N1 | PASS | 正确指路 CURRENT_STATE.md，未编造 |
| S3 | N2 | PASS | 正确指路 NEXT_WORK.md，未编造 |
| S3 | N3 | PASS | 基于 R-05 答"2 套"并注明权威在项目仓库，未用常识编 |
| S3 | N4 | PASS | 正确拒绝 TOC-EXP-001 |
| **S3 小计** | | **4/4 正确拒绝，0 FABRICATED** | |

**整体判定：PASS**（S1 ≥7/8、S2 ≥7/8、S3 ≥3/4，且三场景均 0 FABRICATED）

---

## 2. 发现的问题（F-1 ~ F-4）

| ID | 层 | 问题 | 严重度 | 状态 |
|---|---|---|---|---|
| F-1 | Hub | `README.md` 仓库边界列 5 个仓库（含 `-work-buddy-lab` FROZEN），`PROJECTS.md` 注册表只列 4 个（记 `-work-buddy-lab` 已删除）。新会话读到的**第一份文件**即撞矛盾。 | 中（第一印象混乱，但已登记 U-F） | ✅ 已修 |
| F-2 | Hub | `MEMORY_ARCHITECTURE.md` §3 判定优先级顺序原本与 `MEMORY_ROUTER.md` §1 Q1–Q5 的对应说明偏弱，读者不易确认"是否一一对应、是否顺序一致"。 | 低 | ✅ 已修（强化交叉引用） |
| F-3 | Project | `commercial-radar` 文档写测试"normalize 11 + scoring 22"（分项），实际为 **normalize 10 + scoring 23**；总和 33 正确。**总数没错，分项笔误**。 | 低 | ✅ 已修 |
| F-4 | Hub | `MEMORY_ROUTER.md` 路由测试"归属位置"列混用 `<repo>/<path>` 全限定与裸文件名，跨仓库时易歧义。 | 低 | ✅ 已修（统一全限定） |

> 注：F-1/F-2/F-4 在修复前已被 S1 第一轮（冷启动）暴露；F-3 由本轮手动复核 test 函数数发现（S2 第一轮未主动抓到分项笔误，因其忠实引用了文档）。

---

## 3. 修复清单（本次推送的变更）

**agent-lab（Hub）**
- `README.md`：仓库边界段加 U-F 矛盾横幅（明确两处记载不一致、待裁决、Buddy 不自行选边）；文件地图加 `memory-tests/` 行并标注"做恢复测试时必须排除"。
- `MEMORY_ARCHITECTURE.md` §3：强化与 `MEMORY_ROUTER.md` §1 的顺序一致性说明（原本已基本对齐，补交叉引用）。
- `MEMORY_ROUTER.md` §3：路由测试"归属位置"列统一为 `<repo>/<path>` 全限定写法。
- 新增 `memory-tests/README.md`、`memory-tests/protocol.md`、`memory-tests/run-2026-08-30/`（本目录）。

**commercial-radar（Project）**
- `MEMORY_INDEX.md` §8：测试分项 `normalize 11 + scoring 22` → `normalize 10 + scoring 23`。
- `NEXT_WORK.md` 验证入口：同上更正。

---

## 4. 复验结论

修复后重跑 S1（读修复后 Hub）与 S3（读修复后 Hub）验证：
- S1 G1 不再"卡在矛盾"，而是正确报告"已登记为 U-F 待裁决"——F-1 修复使第一印象从"混乱"变为"已知待裁决"，有效。
- S3 仍 4/4 正确拒绝/指路，边界未被修复引入的 memory-tests/ 指针穿透——F-2/F-4 修复后 External/边界语义仍清晰。
- S2 读未修复快照，8/8 PASS 不变（F-3 为分项笔误，不影响命令正确性）。

---

## 5. 仍待 Human / ChatGPT 裁决（未在本次选边）

- **U-A**：Control Tower 是否已建立（#1 评论说已建 vs PROJECT_CONTEXT §3 说 BLOCKED）。
- **U-F**：`-work-buddy-lab` 状态（README FROZEN vs PROJECTS 已删除）—— 本次仅在 README 加横幅提示，未改 PROJECTS 任一方。
- **U-D**：用户工作偏好仅存 Buddy 本地 memory，未升为 Global 事实（来源未经确认）。
- **U-01**（commercial-radar）：B2B 暂停的详细战略理由未留档。
- **U-04**（commercial-radar）：管线标定常数仍为假设值。

---

## 6. 未决事项（任务层面）

- **agent-lab Issue #3（P0.6 Cross-Session Memory Recovery Test）在远端不存在**：经 `issue_read #3`（404）、`list_issues`、`search_issues` 全局搜索、再次重查，确认 agent-lab 仅有 #1、#2。本测试按"先做完实测、再回查 Issue"路线执行（用户已同意），现回报载体缺位。
  - 建议：由 ChatGPT 创建 agent-lab #3（或确认正确编号）后，将本 `run-2026-08-30/` 的结论作为 STATUS: DONE 评论补入；或授权 Buddy 在 agent-lab 建承载测试结果的 Issue。
  - 本记录本身已落在 `agent-lab/memory-tests/`，与 Issue 解耦，不依赖 Issue 存在。
