在 AI Agent 里，可以这样理解：

**Harness Engineering 是方法论 / 系统工程；Superpowers 是这个方法论在 AI 编码 Agent 里的一个具体实现。**

OpenAI 对 Harness Engineering 的核心表述是：当 Agent 成为主要执行者时，工程师的工作会从“亲自写代码”转向“设计环境、明确意图、构建反馈回路，让 Agent 稳定工作”。([OpenAI][1])
而 Superpowers 官方定位是：给 coding agent 的一套完整软件开发方法论，基于可组合的 skills 和初始指令，确保 Agent 使用这些流程。([GitHub][2])

## 关系一句话

**Superpowers = Harness Engineering 的一个工具化/技能化落地。**

不是：

> Harness Engineering = Superpowers

而是：

> Harness Engineering ⊃ Superpowers

## 类比

可以把一个 AI Agent 看成这样：

| 层               | 作用                 | 例子                                                 |
| --------------- | ------------------ | -------------------------------------------------- |
| **模型**          | 大脑                 | GPT、Claude、Gemini                                  |
| **Agent Loop**  | 会循环思考和行动           | 读文件、改代码、跑测试、再修                                     |
| **Harness**     | 约束、工具、上下文、验证、恢复机制  | AGENTS.md、测试、CI、sandbox、workflow、review、日志、权限      |
| **Superpowers** | Harness 的一组现成工作流技能 | brainstorming、planning、TDD、code review、debugging 等 |

所以 **Superpowers 不是让模型本身变强**，而是给 Agent 加了一套“工程纪律”。很多介绍也把它概括为 “Process over Prompt”，即流程大于提示词：先分析、再规划、再编码、再测试、再审查。([博客园][3])

## Superpowers 主要覆盖 Harness 的哪部分？

它主要覆盖这几块：

1. **流程 Harness**：强制 Agent 不要直接开写，而是先 brainstorm、design、plan。
2. **质量 Harness**：通过 TDD、review、debugging 流程减少“能跑但很烂”的代码。
3. **技能 Harness**：把软件工程最佳实践封装成 Agent 可调用的 skills。
4. **协作 Harness**：让不同 AI coding tools 使用相似的工程流程，比如 Claude Code、Cursor、Codex、OpenCode、Gemini CLI 等。([OpenClaw API][4])

## 但 Superpowers 不是完整的 Harness Engineering

完整的 Harness Engineering 还包括很多 Superpowers 不一定默认解决的东西：

| Harness Engineering 能力     | Superpowers 是否覆盖 |
| -------------------------- | ---------------- |
| 需求澄清 / 方案设计 / TDD / Review | 覆盖较多             |
| 项目级上下文组织                   | 部分覆盖             |
| 代码库结构约束                    | 需要你自己补           |
| CI/CD、自动验证流水线              | 需要你接入            |
| 权限、沙箱、安全边界                 | 不完全覆盖            |
| 观测、日志、失败恢复                 | 不完全覆盖            |
| 长任务状态管理、多 Agent 编排         | 需要额外框架或自建        |
| 业务知识库、产品原则、架构规则            | 需要团队自己沉淀         |

OpenAI 的 Harness Engineering 经验里特别强调：Agent 可读的 repo 知识、版本化计划、自动 lint/CI、结构测试、反馈循环和“垃圾回收”式的持续维护，都是让 Agent 长期稳定工作的关键。([OpenAI][5])

## 实践上怎么用？

比较合理的关系是：

**用 Superpowers 起步，用 Harness Engineering 补全。**

例如做 AI coding agent：

1. 用 **Superpowers** 管住基础开发流程：需求分析、计划、TDD、审查、调试。
2. 在项目里加 **AGENTS.md / CLAUDE.md / SPEC.md**，告诉 Agent 架构、边界、命名、禁止事项。
3. 用测试、lint、typecheck、CI 把规则机械化。
4. 给 Agent 明确“完成定义”：测试通过、文档更新、PR 描述、回归验证。
5. 对失败模式做 harness：失败时如何重试、何时停下、何时请求人类判断。

## 最简结论

**Harness Engineering 是“怎么驾驭 Agent”的系统工程。
Superpowers 是“把一部分驾驭方式封装成 Skills 和工作流”的工具。**

所以你可以把 Superpowers 看成 Harness Engineering 里的 **workflow harness / skills harness**，适合快速把 AI coding 从“随缘生成代码”推进到“按工程流程交付”。

[1]: https://openai.com/index/harness-engineering/?utm_source=chatgpt.com "Harness engineering: leveraging Codex in an agent-first world"
[2]: https://github.com/obra/superpowers?utm_source=chatgpt.com "GitHub - obra/superpowers: An agentic skills framework & software ..."
[3]: https://www.cnblogs.com/jinjiangongzuoshi/p/19863212?utm_source=chatgpt.com "2026 AI效率神器：Superpowers + Claude Code 保姆级教程"
[4]: https://openclawapi.org/en/blog/2026-03-14-superpowers?utm_source=chatgpt.com "Superpowers: Professional Development Workflow in Practice with AI ..."
[5]: https://openai.com/zh-Hans-CN/index/harness-engineering/?utm_source=chatgpt.com "工程技术：在智能体优先的世界中利用 Codex | OpenAI"
