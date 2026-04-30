官网：https://openspec.dev/  
GitHub：https://github.com/Fission-AI/OpenSpec

## 1. 什么是 OpenSpec？

OpenSpec 是一个轻量级、规范驱动（Spec-Driven）的开发框架，核心目标是在写代码前先明确需求意图，并把需求长期沉淀在仓库中。  
它不是某个单一 AI IDE 的功能，而是一个可跨工具使用的规划层，支持 Cursor、Claude Code、Codex、GitHub Copilot 等多种 AI 开发工具。

从官方定位看，OpenSpec 强调几件事：

- **轻量流程**：避免重流程和过度文档化，尽快进入实现。
- **迭代式推进**：反对瀑布式一次性规划，允许边做边更新规范。
- **面向存量项目（Brownfield）**：重点解决“已有系统难理解、需求容易漂移”的问题。
- **规范与代码同仓库管理**：规范不是临时聊天记录，而是可审阅、可追踪的工程资产。

## 2. 为什么需要 OpenSpec？

AI 编码助手在“生成代码”层面很强，但如果需求只存在于聊天上下文，常见问题是：

- 上下文一长就丢失关键约束；
- 不同会话之间难以保持一致；
- 评审时只能看代码 diff，难理解“需求为何变化”。

OpenSpec 的解决方式是：每次变更先生成变更提案与规范增量，再进入实现。这样可以把“为什么改、改什么、如何验收”结构化下来。

官方强调的价值可以概括为三点：

- **先对齐再编码**：先在提案和 specs 上达成一致，降低返工。
- **变更可审阅**：不仅审代码，还能审“需求 delta（变化）”。
- **上下文可持续**：规范长期存在仓库，成员更替或会话结束后仍可复用。

## 3. 适用场景

OpenSpec 不是只适合新项目，反而更适合复杂存量系统。典型场景：

- **功能迭代频繁的业务系统**：每次需求变更都能沉淀为可追溯规范。
- **多人协作与代码评审**：在 PR 前先评审提案与任务分解，减少沟通偏差。
- **跨 AI 工具协作**：团队成员使用不同 AI 工具时，依然共享同一套规范资产。
- **中大型代码库**：通过 capability 维度组织 specs，降低认知负担。
- **需要长期维护的项目**：规范与代码同仓，避免“口口相传”的隐性知识。

## 4. 准备工作

根据官方 README，使用前建议完成以下准备：

1. **Node.js 版本要求**：`20.19.0` 或更高。  
2. **全局安装 OpenSpec**：

```bash
npm install -g @fission-ai/openspec@latest
```

3. **进入你的项目目录并初始化**：

```bash
cd your-project
openspec init
```

4. （建议）初始化后执行 `openspec update`，同步最新 AI 指令与命令配置。  
5. （可选）按团队偏好选择 profile（例如 expanded workflow），再执行 update 生效。

## 5. 快速开始

OpenSpec 当前推荐以 `/opsx` 命令流开始（新工作流）：

1. **提出需求**：在 AI 工具中输入 `/opsx:propose "你的需求"`。  
   OpenSpec 会生成当前变更目录，通常包含：
   - `proposal.md`：为什么要改、改动范围
   - `design.md`：技术方案与关键决策
   - `tasks.md`：可执行任务清单
   - `specs/`：需求与场景的规范增量

2. **执行任务**：输入 `/opsx:apply`，按任务清单逐步实现。  
3. **归档变更**：完成后输入 `/opsx:archive`，将变更归档并同步规范状态。

这一流程的核心是：**先把需求与设计讲清楚，再让 AI 编码**，避免“直接提示词写代码”导致的不可控结果。

## 6. 完整工作流程

结合官网与 README，可整理为以下完整闭环：

### 阶段 A：提出变更（Propose）

- 明确一个需求点（例如“新增记住登录 30 天”）。
- 运行 `/opsx:propose` 生成变更资产。
- 与团队评审 `proposal/design/specs/tasks`，确认目标和边界。

### 阶段 B：实现变更（Apply）

- 运行 `/opsx:apply` 开始按 `tasks.md` 执行。
- 执行中可迭代修改 proposal/design/specs（OpenSpec 强调 fluid、iterative）。
- 同步更新代码与规范，保持实现与需求一致。

### 阶段 C：归档沉淀（Archive）

- 实现与验收完成后运行 `/opsx:archive`。
- 将变更归档到历史目录，形成可追溯记录。
- 规范库持续增长，成为团队长期上下文。

### 阶段 D：持续维护（Update）

- 升级 CLI：`npm install -g @fission-ai/openspec@latest`
- 每个项目执行：`openspec update`，刷新 AI 指令与模板
- 在后续需求中重复 A-B-C，形成稳定节奏。

## 7. 常用命令

以下是实际高频命令（以官方 README 与官网示例为准）：

| 命令 | 用途 | 典型时机 |
| --- | --- | --- |
| `npm install -g @fission-ai/openspec@latest` | 安装/升级 OpenSpec CLI | 初次接入或版本升级 |
| `openspec init` | 在项目中初始化 OpenSpec 目录与配置 | 项目首次接入 |
| `openspec update` | 更新项目内 AI 指令与命令配置 | 升级后或命令变更后 |
| `openspec config profile` | 选择工作流 profile（如 expanded） | 团队切换流程策略 |
| `/opsx:propose "idea"` | 生成变更提案与规范增量 | 需求进入规划时 |
| `/opsx:apply` | 按任务清单执行实现 | 方案评审通过后 |
| `/opsx:archive` | 归档变更并沉淀规范 | 开发与验收完成后 |

> 说明：官网中你也可能看到早期 `/openspec:*` 风格示例；README 当前主推的是 `/opsx:*` 新工作流。实践中优先以当前版本文档与 `openspec update` 结果为准。
