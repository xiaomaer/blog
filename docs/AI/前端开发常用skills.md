# 前端开发常用 Skills

本文整理前端开发中常用的 Skills，便于按任务快速选择，而不是临时回忆“该用哪个”。

## 快速选型

| 任务场景 | 推荐 Skills |
| --- | --- |
| React 组件设计、性能优化、代码规范 | `vercel-react-best-practices`、`vercel-composition-patterns` |
| Next.js 路由、数据获取、服务端边界设计 | `next-best-practices` |
| 落地页、活动页、后台界面视觉优化 | `frontend-design`、`ui-ux-pro-max` |
| UI 评审、可用性检查、无障碍审查 | `web-design-guidelines` |
| Tailwind 设计令牌、组件库、样式体系建设 | `tailwind-design-system` |

## 常用 Skills 说明

### `vercel-react-best-practices`
适用于 React 组件开发、渲染性能优化、状态与副作用处理等场景。  
当你需要“按现代 React 最佳实践重构代码”时优先使用。

### `vercel-composition-patterns`
适用于组件抽象、复合组件设计、布尔参数过多、组件 API 难维护等问题。  
当你发现组件不断堆参数、复用性差时，优先用它梳理组件结构。

### `next-best-practices`
适用于 Next.js 项目的目录设计、路由约定、服务端与客户端边界、数据获取与错误处理。  
当任务明确发生在 Next.js 项目中时，通常应优先启用。

### `frontend-design`
适用于新页面设计、现有页面改版、提升视觉层次与落地质量。  
它更偏“直接产出界面方案”，适合做页面和组件的视觉重构。

### `ui-ux-pro-max`
适用于从交互、布局、配色、字体、响应式和无障碍等多个维度给出综合建议。  
当你需要“设计 + 体验”一起优化时，它比单纯视觉类 Skill 更全面。

### `web-design-guidelines`
适用于审查现有 UI 是否符合常见 Web 界面规范，尤其适合做 review。  
当需求是“帮我看看这个页面/组件有哪些问题”时很合适。

### `tailwind-design-system`
适用于用 Tailwind 构建设计令牌、规范化组件样式、统一主题与间距体系。  
如果项目已经基于 Tailwind，且目标是“做体系化沉淀”，应优先使用。

## 推荐组合

* React 项目重构：`vercel-react-best-practices` + `vercel-composition-patterns`
* Next.js 页面开发：`next-best-practices` + `vercel-react-best-practices`
* 页面视觉升级：`frontend-design` + `ui-ux-pro-max`
* UI 评审与修正：`web-design-guidelines` + `frontend-design`
* Tailwind 组件库建设：`tailwind-design-system` + `ui-ux-pro-max`

## 使用建议

* 优先按“当前任务”选 Skill，不要一次启用过多。
* 如果目标是“实现页面”，优先选设计或工程类 Skill；如果目标是“审查问题”，优先选 review 类 Skill。
* 同一任务最多组合 2 到 3 个 Skills，避免建议重叠。

## 常用命令

```bash
npx skills find [query]        # 搜索相关技能
npx skills add <owner/repo>    # 安装技能，支持 GitHub 简写、完整 URL、本地路径
npx skills list                # 列出已安装的技能
npx skills check               # 检查可用更新
npx skills update              # 升级所有技能
npx skills remove [skill-name] # 卸载技能
```

## 示例提示词

```text
使用 next-best-practices，帮我重构这个 Next.js 页面的数据获取逻辑。

使用 frontend-design 和 ui-ux-pro-max，优化这个后台首页的视觉层次和响应式布局。

使用 web-design-guidelines，审查这个表单页面的可用性和无障碍问题。

使用 tailwind-design-system，整理这组按钮、卡片和表单控件的设计令牌。
```
