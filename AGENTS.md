# AGENTS.md — Git Memory 运行时引导（Git Memory Runtime Bootstrap）

> GMR v0.2 运行时入口。本文件刻意保持精简；它不是记忆存储。

## 强制行为（Mandatory behavior）

1. 若读取本仓库或任何已注册的项目仓库，进入 **Git Memory Mode（Git 记忆模式）**。
2. 遵循 `architecture/AGENT_GIT_MEMORY_CONTRACT.md` 执行 Global Bootstrap（全局引导）、Project Bootstrap（项目引导）、Plan Continuity（计划延续）、Trigger Monitor（触发监视器）与 Memory Sync Gate（记忆同步闸门）。
3. 以 Git 为规范真相（canonical truth）；不要用会话 / 聊天上下文去覆盖 Git 中的事实。
4. 在每一轮对话中执行轻量的 **Session Trigger Scan（会话触发扫描）**。强触发进入 Memory Evaluation（记忆评估）；触发并不等于要写入。
5. 在工作单元 / 检查点边界，返回结果前运行完整的 Memory Sync Gate（记忆同步闸门）。
6. 当具有 Git 写入权限时，ChatGPT 是 Memory Owner（记忆所有者）。Buddy（执行智能体）仅负责执行，绝不需要作为记忆中介。
7. 项目范围必须明确。绝不要自动把 Project Memory（项目记忆）提升为 Global Memory（全局记忆）。
8. 绝不要静默删除或覆盖核心记忆；使用 canonical-owner（规范归属方）更新与 `SUPERSEDE`（取代）历史。
9. 若架构冲突或无法裁决的规范记忆冲突出现，则 fail closed（安全失败），并将其记录 / 路由为 `[Unknown]`，而不是猜测。

## 极简启动（Minimal startup）

`检查 Git 的记忆` / `CHECK_GIT_MEMORY` → Global Bootstrap（全局引导） → 识别项目 → Project Bootstrap（项目引导） → Plan Continuity Check（计划延续检查） → 任务解析（task resolution）。
