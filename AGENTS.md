## 与 Superpowers 共存（本仓库：blog / 文档为主）

### 优先级

- **当前对话里用户的明确指令** > 本文件 > Superpowers 技能默认行为。
- 用户写清「跳过某技能 / 不落盘 / 不写测试」时，以用户为准。

### 产物路径（与 `docs/AI/AI 辅助开发流程-superpowers.md` 对齐时可改）

- 设计/规格：`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- 实现计划：`docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`  
若改用其他目录，请在本文件或首条消息里写清新路径。

### 何时走完整 Superpowers 流程

- **brainstorming → writing-plans →（subagent-driven-development 或 executing-plans）**：新功能、改行为、多文件/多步实现、需要可追溯规格与计划时。
- **test-driven-development**：涉及可测代码或可自动化校验逻辑时；本仓库若暂无真实测试套件，以「约定验证方式」替代（见下）。
- **systematic-debugging**：非一眼能定的失败、多轮乱改无效、构建/脚本异常时。
- **verification-before-completion**：在对话中声称「完成 / 通过 / 无问题」之前，须已执行并**贴出**本任务相关的命令与退出码（或等价证据）。
- **requesting-code-review / receiving-code-review**：合并或大范围改动前、处理 PR/CI 评论时。
- **finishing-a-development-branch**：分支/计划内任务全部完成且验证通过后，再谈合并、PR、清理 worktree。
- **using-git-worktrees**：与主分支并行大改、需要干净工作区执行计划时（可选）。
- **dispatching-parallel-agents**：多问题域独立、无强共享可变状态时再并行分派。

### 何时可缩短流程（不必落盘设计/长计划）

同时满足「任务性质简单」且用户未要求完整流程时，可仅在对话里一两句确认后直接改：

- 单文件、且不改变对外约定或读者可见语义；或
- 仅限 typo、格式化、纯目录调整、注释-only。

**纯 Markdown 文档**（新建/改一篇博客或 AI 笔记）：默认**不写**单元测试；仍建议在收尾用 `pnpm exec prettier --write` / `--check`（若项目已配置）或用户指定的校验，并在声称完成前贴命令输出。

### 本仓库测试脚本的现实约定

- `package.json` 中 `npm test` / `pnpm test` 当前为占位，**不得**用它作为「测试已通过」的证据。
- 若任务需要可重复验证，由用户在需求中写明命令（例如 Prettier、自定义脚本）；否则在对话中说明采用的**人工检查项**。

### 单次对话快速收口（示例句式）

在首条消息写明，例如：「仅改 `docs/xxx.md` 一节内容；跳过 brainstorming 与独立计划文件；完成后运行 `pnpm exec prettier --write <路径>`。」