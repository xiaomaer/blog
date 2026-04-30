# 前端开发常用 Skills

本文整理前端开发中常用的 Skills，便于按任务快速选择，而不是临时回忆「该用哪个」。若你希望从概念上理解 Skill 是什么、团队如何沉淀自有技能，可配合阅读：[AI 辅助开发流程：Skill](./AI%20辅助开发流程-skill.md)。

---

## 快速选型

下表中的 **技能名** 以常见发布源（如 Vercel 工程实践、社区技能包）中的标识为例；你本地通过 `npx skills add` 安装后，**以 `npx skills list` 与包内 `SKILL.md` 的 `name` 字段为准**，对话里点名时使用列表里显示的名称即可。

| 任务场景 | 推荐 Skills |
| --- | --- |
| React 组件设计、渲染性能、数据流与副作用规范 | `vercel-react-best-practices` |
| 复合组件、布尔参数泛滥、组件 API 设计与重构 | `vercel-composition-patterns` |
| Next.js 路由、RSC 边界、数据获取、元数据与错误处理 | `next-best-practices` |
| 落地页、活动页、后台界面「做出来好看」 | `frontend-design` |
| 交互、信息架构、配色字体、响应式与无障碍的综合方案 | `ui-ux-pro-max` |
| 对照常见 Web 规范做 UI / a11y 评审与清单式问题罗列 | `web-design-guidelines` |
| Tailwind 设计令牌、主题、组件样式体系统一 | `tailwind-design-system` |
| 以「实现页面」为主、顺带要工程边界正确 | `next-best-practices` + `vercel-react-best-practices`（Next 项目） |
| 以「挑问题、改体验」为主、顺带要视觉提案 | `web-design-guidelines` + `frontend-design` 或 `ui-ux-pro-max` |
| 单元测试 / 组件测试（Vitest、Jest、React Testing Library） | 先用 `npx skills find vitest`（或 `testing-library`、`jest`）安装，再以 `npx skills list` 中的 **实际 name** 在对话里点名 |
| E2E / 浏览器自动化（Playwright、Cypress） | `npx skills find playwright` / `cypress`，以 list 结果为准 |
| TypeScript 严格类型、类型建模与重构 | `npx skills find typescript`，或团队自建「TS 规范」技能 |
| 客户端数据层（TanStack Query、SWR、与缓存失效策略） | `npx skills find tanstack` / `react-query`，与 `vercel-react-best-practices` 搭配时注意边界 |
| shadcn/ui、Radix + Tailwind 的无障碍组件拼装 | `npx skills find shadcn`；与 `tailwind-design-system` 常一起用 |
| Storybook（组件文档、交互用例、视觉回归辅助） | `npx skills find storybook` |
| Monorepo（Turborepo、Nx、pnpm workspace） | `npx skills find turbo` / `nx` / `monorepo` |
| 国际化（i18n、文案抽取、路由级语言） | `npx skills find i18n` / `lingui` / `formatjs` |
| 前端安全（XSS、CSP、依赖与供应链） | `npx skills find security` / `xss`；若无满意包可 **自建项目技能** |
| Vue / Nuxt、Svelte / SvelteKit 等 **非 React** 栈 | `npx skills find vue` / `nuxt` / `svelte`，勿套用 `vercel-react-best-practices` |
| Remix、Astro 等其它元框架 | `npx skills find remix` / `astro` |
| 不知道该装什么、想按描述搜一圈 | 已安装 CLI 时多用 `npx skills find <关键词>`；若使用 Agent 的 **find-skills** 类技能，按其说明检索可安装技能 |

**简单记**：偏 **工程与正确性** → React/Next 类技能；偏 **观感与体验** → design / ui-ux 类；偏 **审查与规范** → `web-design-guidelines`；偏 **样式体系** → `tailwind-design-system`；偏 **质量与交付证据** → 测试 / E2E 类（按 find 安装）；偏 **仓库结构** → Monorepo 类；偏 **栈别** → 用对应框架关键词检索，不要硬套 React 技能。

> **关于「find 关键词」行**：表中 Vitest、Playwright、shadcn 等行给出的是 **检索关键词**，社区包名与作者仓库会变化；**不要**把关键词当作对话里点名的技能标识。安装后一律以 `npx skills list` 与对应 `SKILL.md` 里的 `name` 为准。若某关键词暂无满意结果，可换同义词再搜，或 [自建技能](./AI%20辅助开发流程-skill.md)。

**与 Cursor 内置能力**：例如需在对话旁产出可交互的分析页、数据看板式界面时，可使用 Cursor 文档中的 **Canvas** 等工作流（通常走编辑器内置技能，不一定在 `npx skills` 同一套安装路径下）；与上表「前端工程技能」互补而非重复。

---

## 常用 Skills 说明

### `vercel-react-best-practices`

| 维度 | 说明 |
| --- | --- |
| 适用 | React 组件开发、列表与重渲染、状态与副作用、客户端性能相关重构。 |
| 不适用 | 非 React 技术栈；或只做视觉不改数据流时，可不必单独启用。 |
| 典型说法 | 「按 Vercel/React 团队建议优化这段组件」「减少不必要的重渲染」「这段 `useEffect` 有没有更稳妥的写法」。 |

### `vercel-composition-patterns`

| 维度 | 说明 |
| --- | --- |
| 适用 | 组件抽象、复合组件、布尔参数过多、对外 API 难维护、需要可扩展的组件结构。 |
| 不适用 | 一次性脚本、与组件结构无关的纯样式微调。 |
| 典型说法 | 「这个 Modal 参数太多了，帮我设计成 compound components」「抽一个可组合的 Tabs API」。 |

### `next-best-practices`

| 维度 | 说明 |
| --- | --- |
| 适用 | Next.js 目录与路由约定、服务端与客户端边界、数据获取、缓存与重新验证、错误与 loading UI。 |
| 不适用 | 纯 CRA/Vite SPA、Remix 等非 Next 项目（应换对应框架的实践或通用 React 技能）。 |
| 典型说法 | 「这个 page 应该放 Server 还是 Client」「`fetch` 在 RSC 里怎么写更合理」。 |

### `frontend-design`

| 维度 | 说明 |
| --- | --- |
| 适用 | 新页面视觉方案、现有页面改版、提升层次与「成品感」。 |
| 不适用 | 只想要无障碍清单而不需要视觉方向时，可优先 `web-design-guidelines`。 |
| 典型说法 | 「把这个后台首页做得不那么模板感」「活动页一屏内信息层级再清晰一点」。 |

### `ui-ux-pro-max`

| 维度 | 说明 |
| --- | --- |
| 适用 | 从布局、动效、配色、字体、响应式到无障碍等多维度一起推敲。 |
| 与 `frontend-design` | 前者更偏「全链路体验与设计语言」；后者更偏「直接产出界面级方案」。可二选一或组合，组合时注意控制上下文长度。 |
| 典型说法 | 「从 UX 角度看看这个注册流程哪里别扭」「移动端首屏怎么取舍信息」。 |

### `web-design-guidelines`

| 维度 | 说明 |
| --- | --- |
| 适用 | 对照常见 Web 界面与可用性规范做 review、列问题优先级、给可执行修改建议。 |
| 不适用 | 需要大量品牌视觉定制且尚无设计稿时，单靠它可能不够，需配合 `frontend-design`。 |
| 典型说法 | 「帮我 audit 这个表单的无障碍和键盘操作」「这个列表页有哪些明显的 UX 反模式」。 |

### `tailwind-design-system`

| 维度 | 说明 |
| --- | --- |
| 适用 | 基于 Tailwind 做设计令牌、间距与字号阶梯、语义化 class 策略、组件层样式规范。 |
| 不适用 | 未使用 Tailwind 的项目；或只做单次页面微调而无体系化需求。 |
| 典型说法 | 「把按钮、输入框、卡片抽成一套 token」「暗色主题和间距怎么和组件库对齐」。 |

---

## 推荐组合

| 目标 | 组合 | 备注 |
| --- | --- | --- |
| React 项目重构 | `vercel-react-best-practices` + `vercel-composition-patterns` | 先结构再性能，避免两头同时大改难以 review。 |
| Next.js 页面开发 | `next-best-practices` + `vercel-react-best-practices` | 先定数据与边界，再细化客户端组件。 |
| 页面视觉升级 | `frontend-design` + `ui-ux-pro-max` | 先定方向再展开细节；若上下文紧张可只保留其一。 |
| UI 评审与落地修正 | `web-design-guidelines` + `frontend-design` | 先清单化问题，再出改稿思路。 |
| Tailwind 组件库建设 | `tailwind-design-system` + `ui-ux-pro-max` | 令牌与组件 API 和交互状态一起考虑。 |
| 新功能带单测 | 业务技能任选其一 + **Vitest/RTL 等测试技能**（以 `npx skills list` 为准） | 先定可测行为再写实现，可与 Superpowers 的 TDD 流程对齐。 |
| 关键路径 E2E | **Playwright 或 Cypress 技能** + `web-design-guidelines`（可选） | E2E 管流程与选择器稳定；a11y 仍以专用审查或指南为准。 |
| shadcn 页面落地 | **shadcn 相关技能** + `tailwind-design-system` | 统一 token 与组件变体，避免 class 与主题分叉。 |

---

## 如何使用（安装、启用与对话）

### 1. 安装与更新

通过官方/社区提供的 **Skills CLI**（以你当前包版本帮助为准）可以搜索、安装与升级：

```bash
npx skills find [query]        # 按关键词搜索技能
npx skills add <owner/repo>    # 安装：支持 GitHub 简写、完整 URL、本地路径
npx skills list                # 查看已安装技能名称（对话里点名用这里显示的标识）
npx skills check               # 检查可用更新
npx skills update              # 升级已安装技能
npx skills remove [skill-name] # 卸载
```

**说明**：

- 安装通常需要能访问 GitHub 等源（网络或镜像策略按你所在环境配置）。
- 安装完成后，在 **Cursor** 中是否出现在 Agent 可选技能列表里，以 **Cursor 当前版本的 Skills 文档/设置** 为准；若列表里没有，可尝试重启 Cursor 或检查技能是否安装在 Cursor 扫描的用户技能目录（常见为 `~/.cursor/skills/` 下的子目录，与 [Skill 流程文档](./AI%20辅助开发流程-skill.md) 一致）。

### 2. 在对话里怎么用

| 方式 | 做法 | 适用 |
| --- | --- | --- |
| **显式点名** | 在需求里写清技能名，例如：「用 `next-best-practices` 重构下面这段路由与数据获取。」 | 任务边界清晰、希望强制按某套实践执行时。 |
| **自然语言触发** | 描述任务类型与栈（「Next RSC」「Tailwind 设计令牌」「无障碍 audit」），由 Agent 根据技能 `description` 自动选用。 | 日常开发、愿意接受自动匹配时。 |
| **项目规则里约定** | 在 Cursor **项目规则**或 `AGENTS.md` 中写：本仓库前端任务默认参考哪些技能或目录。 | 团队协作、减少每人重复说明。 |

**实操建议**：

1. **一次 1～3 个技能**：过多技能容易导致建议重叠、上下文浪费；表格里「推荐组合」已是上限参考。
2. **工程类与设计类分工**：实现功能时以 React/Next 技能为主；定稿前再开 `web-design-guidelines` 做一轮审查，往往比全程混开更清晰。
3. **栈要对齐**：非 Next 项目不要默认绑 `next-best-practices`；非 Tailwind 项目不要强绑 `tailwind-design-system`。
4. **与规则冲突时以你为准**：你在对话或项目规则里写的明确要求，应覆盖技能中的默认建议（与上游 Superpowers 等理念一致）。

### 3. 与自建团队 Skill 的关系

社区「常用技能」解决 **通用最佳实践**；你们仓库特有的目录、API、设计稿链接、发布 checklist，更适合放在 **项目内 `.cursor/skills/`** 自建技能中，并在规则里写「与 `vercel-react-best-practices` 同时生效时的优先级」。详见 [AI 辅助开发流程：Skill](./AI%20辅助开发流程-skill.md) 第 6 节。

---

## 使用建议（摘要）

- 按 **当前任务** 选 Skill，不要「能开全开」。
- **实现页面** → 优先工程类 + 视需要加设计类；**审查问题** → 优先 `web-design-guidelines`，再视情况加 `frontend-design`。
- 同一轮对话 **最多组合 2～3 个** Skills，避免模型在重叠建议中摇摆。
- 长任务可 **分会话**：一会话定架构与数据，另一会话做视觉与 a11y，便于控制上下文与 review 粒度。

---

## 示例提示词

```text
使用 next-best-practices，帮我重构这个 Next.js 页面的数据获取逻辑，说明 RSC 与 Client 边界。

使用 vercel-react-best-practices，检查这个列表组件是否存在不必要的重渲染，并给出最小改动方案。

使用 vercel-composition-patterns，把这个 Dialog 从「一堆 boolean props」改成可维护的复合组件 API。

使用 frontend-design 和 ui-ux-pro-max，优化这个后台首页的视觉层次和响应式布局；移动端首屏只保留最高优先级信息。

使用 web-design-guidelines，审查这个表单页面的可用性和无障碍问题，按严重程度列出清单。

使用 tailwind-design-system，整理这组按钮、卡片和表单控件的设计令牌，并给出在组件里的引用方式。

（将「以下技能名」替换为 `npx skills list` 中的实际名称）使用 <vitest-rtl 技能名>，为这个 hooks 写最小单测，覆盖成功与错误分支。

使用 <playwright 技能名>，为登录到下单写一条冒烟 E2E，优先用 role/data-testid 等稳定选择器。

用 npx skills find typescript 后安装到的技能，检查这个 API 客户端的类型是否过宽，并给出收紧类型的重构步骤。
```

---

## 相关文档

- [AI 辅助开发流程：Skill](./AI%20辅助开发流程-skill.md) — Skill 概念、创建与团队沉淀  
- [AI 辅助开发流程：Superpowers](./AI%20辅助开发流程-superpowers.md) — 与规格、计划、TDD 等流程型技能配合时的思路  
