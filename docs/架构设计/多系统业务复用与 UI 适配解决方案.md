# 多系统业务复用与 UI 适配解决方案

## 1. 背景

同一套业务能力需要接入多个系统时，前端通常会遇到两个核心差异点：

- `UI 差异`
  - 需要内置一套标准实现，保证开箱即用
  - 不同系统又需要支持主题覆盖、局部替换，甚至整页重写
- `权限差异`
  - 不同系统的页面入口、按钮可见性、操作执行规则可能不同

在 `Next.js + Tailwind CSS` 技术栈下，目标不是做一套“写死”的公共页面，而是沉淀一套既能复用业务逻辑，又能适配不同系统差异的前端方案。

## 2. 设计目标

这份文档整理原始讨论中提到的所有方案，并按层次进行归类，目标是回答三个问题：

- 业务逻辑如何只维护一份
- 标准 UI 如何提供默认实现并允许替换
- 权限差异如何做到统一接入而不污染组件代码

## 3. 设计原则

- `逻辑与表现分离`
  - 业务逻辑、权限判断、数据处理尽量不和具体 DOM 结构耦合
- `默认实现优先`
  - 公共模块先提供标准 UI，降低接入成本
- `插件化扩展`
  - 对局部或整体差异，通过扩展点、配置和 Provider 注入，不在公共代码中堆大量系统判断
- `权限集中治理`
  - 权限不只控制按钮展示，还要覆盖页面入口和请求执行
- `适配 Next.js 边界`
  - 服务端负责获取用户与权限快照，客户端负责交互与展示控制

## 4. 方案总览

原始文档中提到的方案可以分成三类：

### 4.1 架构级方案

这类方案决定“整体怎么复用”：

- `Headless UI + Logic Hook`
- `Monorepo + Component Library`
- `Composition via Slot / Render Props`

### 4.2 组件扩展级方案

这类方案决定“默认实现如何被替换”：

- `CSS Variables + Tailwind`
- `Tailwind Config + CVA 变体`
- `Render Props / Render Functions`
- `Named Slots / Composition`
- `Component Registry / Factory`
- `Build-time Alias`

### 4.3 权限适配方案

这类方案决定“不同系统的权限逻辑如何统一接入”：

- `Strategy Pattern`
- `Dependency Injection`
- `Provider + Hook`

下面逐一整理。

## 5. 架构级方案整理

### 5.1 方案一：Headless UI + Logic Hook

#### 核心思路

将业务逻辑完全抽到 Hook 或纯函数中，UI 层只负责渲染。公共模块可以提供一套默认 UI，也可以只暴露无样式能力。

#### 实现方式

- `Logic Layer`
  - 封装 API 调用、状态管理、数据转换、流程控制
- `UI Layer`
  - 提供标准组件，或者只暴露 Headless 组件和 Hook
- `Theme Layer`
  - 通过 `Tailwind` 类名、CSS Variables、`variant` 承接视觉差异

#### 示例

```tsx
export type BizAction = 'view' | 'edit' | 'submit' | 'export'

export function useOrderFeature(initialData: OrderDetail) {
  const [formData, setFormData] = useState(initialData)
  const [loading, setLoading] = useState(false)

  async function submit() {
    setLoading(true)
    try {
      await updateOrder(formData)
    } finally {
      setLoading(false)
    }
  }

  return {
    formData,
    setFormData,
    loading,
    submit,
  }
}
```

```tsx
type OrderSubmitButtonProps = {
  className?: string
  action?: BizAction
  onClick: () => void
  disabled?: boolean
}

export function OrderSubmitButton({
  className,
  action = 'submit',
  onClick,
  disabled,
}: OrderSubmitButtonProps) {
  const canSubmit = usePermission(action)
  if (!canSubmit) return null

  return (
    <button
      className={cn('rounded-md px-4 py-2 text-sm font-medium', className)}
      onClick={onClick}
      disabled={disabled}
    >
      提交
    </button>
  )
}
```

#### 适用场景

- 业务逻辑高度一致
- UI 差异较大
- 不同系统希望保留自己的设计体系

#### 优点

- 复用粒度最灵活
- 逻辑和 UI 解耦最彻底
- 最适合“只复用逻辑，不复用页面”的场景

#### 缺点

- 对公共模块设计能力要求高
- 如果没有标准 UI，接入方初始开发成本会更高

### 5.2 方案二：Monorepo + Component Library

#### 核心思路

将业务逻辑、标准 UI、系统接入工程拆成独立 workspace，通过 monorepo 管理版本和依赖。

#### 实现方式

推荐拆分为：

- `packages/biz-core`
  - 业务逻辑、类型定义、API、权限契约
- `packages/biz-ui`
  - 基于 `Tailwind CSS` 的标准组件与标准页面
- `apps/system-a`
  - 系统 A 的主题、权限、接入页面
- `apps/system-b`
  - 系统 B 的主题、权限、接入页面

#### 示例目录

```text
packages/
  biz-core/
    src/
      api/
      hooks/
      permissions/
      types/
  biz-ui/
    src/
      components/
      pages/
      providers/
      styles/

apps/
  system-a/
    app/
    src/
      biz-adapter/
        permission.ts
        components.tsx
        theme.css
        config.ts
  system-b/
    app/
    src/
      biz-adapter/
        permission.ts
        components.tsx
        theme.css
        config.ts
```

#### 适用场景

- 多个系统长期演进
- 公共模块需要持续维护
- 希望统一构建、发布和版本管理

#### 优点

- 工程边界清晰
- 便于沉淀公共能力
- 最适合长期复用和团队协作

#### 缺点

- 前期搭建成本更高
- 需要团队具备 monorepo 维护能力

### 5.3 方案三：Composition via Slot / Render Props

#### 核心思路

页面流程和主体结构复用，局部区域通过插槽或渲染函数交给接入系统自定义。

#### 实现方式

- 定义“骨架组件”承接流程和状态
- 把头部、搜索区、操作区、底部按钮等开放为扩展点
- 默认不传时，使用公共模块内置实现

#### 示例

```tsx
type UserPageProps = {
  renderActions?: (ctx: { selectedIds: string[] }) => React.ReactNode
}

export function UserManagerPage({ renderActions }: UserPageProps) {
  const { selectedIds } = useUserManager()

  return (
    <section className="space-y-4">
      <UserSearchPanel />
      <UserTable />
      {renderActions
        ? renderActions({ selectedIds })
        : <DefaultActionBar selectedIds={selectedIds} />}
    </section>
  )
}
```

#### 适用场景

- 页面结构大体一致
- 只有部分区域需要定制
- 接入系统希望复用默认页面而不是完全重写

#### 优点

- 扩展点清晰
- 默认实现和定制实现可以共存
- 类型安全，调试成本低

#### 缺点

- 插槽设计不合理时，容易不断加 props
- 复杂页面下需要提前规划扩展边界

## 6. 默认实现 + 插件化替换方案整理

这一类方案是对“公共模块内置一套标准 UI，同时允许接入系统按需替换”的进一步细化。可以按替换粒度从小到大理解。

### 6.1 方案 A：CSS Variables + Tailwind

#### 核心思路

如果差异只是颜色、圆角、阴影、字号、间距，优先通过设计 token 解决，而不是重写组件。

#### 实现方式

- 在系统侧提供主题变量文件
- 在 `Tailwind` 配置中映射到 `colors`、`borderRadius`、`boxShadow`
- 公共组件只消费 token，不写死品牌风格

#### 示例

```css
:root {
  --biz-color-primary: 37 99 235;
  --biz-radius-md: 12px;
  --biz-shadow-card: 0 8px 24px rgba(15, 23, 42, 0.08);
}
```

```ts
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      primary: 'rgb(var(--biz-color-primary) / <alpha-value>)',
    },
    borderRadius: {
      md: 'var(--biz-radius-md)',
    },
    boxShadow: {
      card: 'var(--biz-shadow-card)',
    },
  },
}
```

#### 适用场景

- 品牌色不同
- 按钮圆角不同
- 卡片样式不同

#### 优点

- 成本最低
- 不影响组件结构
- 最容易规模化维护

#### 缺点

- 只适合视觉参数差异
- 无法处理结构差异

### 6.2 方案 B：Tailwind Config + CVA 变体

#### 核心思路

当组件结构相同，但多个系统需要预置不同风格组合时，使用 `variant` 比单纯 `className` 更稳定。

#### 示例

```tsx
import { cva } from 'class-variance-authority'

const buttonStyles = cva('inline-flex items-center px-4 py-2 text-sm font-medium transition', {
  variants: {
    intent: {
      systemA: 'rounded-none bg-indigo-600 text-white',
      systemB: 'rounded-full bg-emerald-500 text-white shadow-md',
      default: 'rounded-md bg-primary text-white',
    },
  },
  defaultVariants: {
    intent: 'default',
  },
})
```

#### 适用场景

- 标准组件较多
- 需要稳定的视觉变体体系
- 想避免大量零散 `className` 拼接

#### 优点

- 变体集中管理
- 组件 API 更清晰
- 更适合组件库沉淀

#### 缺点

- 只适合结构基本不变的场景
- 变体过多时需要控制规模

### 6.3 方案 C：Render Props / Render Functions

#### 核心思路

公共组件提供默认 UI，同时暴露渲染函数，让接入方替换某个具体节点。

#### 示例

```tsx
type UserTableProps = {
  data: User[]
  renderActions?: (user: User) => React.ReactNode
}

function DefaultActions(user: User) {
  return (
    <div className="space-x-2">
      <button>编辑</button>
      <button>删除</button>
    </div>
  )
}

export function UserTable({
  data,
  renderActions = DefaultActions,
}: UserTableProps) {
  return (
    <table className="min-w-full">
      <tbody>
        {data.map((user) => (
          <tr key={user.id}>
            <td>{user.name}</td>
            <td>{renderActions(user)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
```

#### 适用场景

- 只替换按钮、操作列、表头、自定义空态等局部节点

#### 优点

- 灵活度高
- 实现简单
- 接入成本低

#### 缺点

- 渲染函数太多时，组件会变复杂
- 不适合大块结构替换

### 6.4 方案 D：Named Slots / Composition

#### 核心思路

将页面拆成多个具名区域，接入方选择复用默认部分，或覆盖某个指定区域。

#### 示例

```tsx
type UserManagerSkeletonProps = {
  header?: React.ReactNode
  search?: React.ReactNode
  footer?: React.ReactNode
  children: React.ReactNode
}

export function UserManagerSkeleton({
  header,
  search,
  footer,
  children,
}: UserManagerSkeletonProps) {
  return (
    <div className="space-y-4">
      {header ?? <DefaultHeader title="用户管理" />}
      {search ?? <DefaultSearch />}
      <div>{children}</div>
      {footer ?? <DefaultFooter />}
    </div>
  )
}
```

#### 适用场景

- 页面结构整体一致
- 个别板块需要重写
- 需要比 `renderProps` 更清晰的扩展边界

#### 优点

- 结构化更强
- 语义清晰
- 更适合页面级骨架组件

#### 缺点

- 扩展点设计需要提前规划
- 过多 slot 会使组件 API 冗长

### 6.5 方案 E：Component Registry / Factory

#### 核心思路

在公共模块内部维护默认组件映射表，接入系统通过 Provider 注入替换实现。

#### 示例

```tsx
type BizComponentRegistry = {
  PrimaryButton: React.ComponentType<React.ButtonHTMLAttributes<HTMLButtonElement>>
  SearchInput: React.ComponentType<React.InputHTMLAttributes<HTMLInputElement>>
}

const defaultRegistry: BizComponentRegistry = {
  PrimaryButton: (props) => <button className="rounded-md bg-primary px-4 py-2 text-white" {...props} />,
  SearchInput: (props) => <input className="rounded-md border px-3 py-2" {...props} />,
}

const BizComponentRegistryContext = createContext<BizComponentRegistry>(defaultRegistry)

export function BizComponentRegistryProvider({
  components,
  children,
}: {
  components?: Partial<BizComponentRegistry>
  children: React.ReactNode
}) {
  const value = { ...defaultRegistry, ...components }
  return (
    <BizComponentRegistryContext.Provider value={value}>
      {children}
    </BizComponentRegistryContext.Provider>
  )
}
```

#### 适用场景

- 希望全局替换某类基础组件
- 多个页面都要统一替换按钮、输入框、弹窗等

#### 优点

- 系统级接入非常方便
- 适合做全局默认替换

#### 缺点

- 调试时需要明确当前实际注入的是谁
- 组件契约需要稳定，否则替换成本高

### 6.6 方案 F：Build-time Alias

#### 核心思路

在构建阶段通过 alias，把公共模块内部的默认组件路径重定向到系统自己的实现。

#### 示例

```js
// next.config.js
const path = require('path')

module.exports = {
  webpack: (config) => {
    config.resolve.alias['@provider-kit/default-button'] = path.resolve(
      __dirname,
      'src/components/SystemAButton.tsx',
    )
    return config
  },
}
```

#### 适用场景

- 极少数底层原子组件替换
- 接入系统对构建链路可控

#### 优点

- 业务代码看起来最“无侵入”
- 纯配置即可切换

#### 缺点

- IDE 和调试体验差
- 静态分析能力变弱
- 不适合业务高频变动场景

#### 结论

这个方案一般不作为首选，更适合作为少量底层能力的兜底手段。

## 7. 权限适配方案整理

权限差异是第二个核心问题。原始文档中提到的 `Strategy Pattern`、`Dependency Injection`、`Provider` 本质上是同一套设计链路，可以整理为一套统一方案。

### 7.1 策略模式

先抽象统一权限契约，不同系统提供各自实现。

```ts
export type PermissionInput = {
  action: BizAction
  resource: string
  data?: unknown
}

export interface PermissionPolicy {
  can(input: PermissionInput): boolean
}
```

系统 A 和系统 B 的差异，不应该散落在按钮组件里，而应该体现在不同的 `PermissionPolicy` 实现里。

### 7.2 依赖注入

通过 Provider 把权限策略注入到业务模块，组件内部统一通过 Hook 使用。

```tsx
const PermissionContext = createContext<PermissionPolicy | null>(null)

export function BizProvider({
  permission,
  children,
}: {
  permission: PermissionPolicy
  children: React.ReactNode
}) {
  return (
    <PermissionContext.Provider value={permission}>
      {children}
    </PermissionContext.Provider>
  )
}

export function usePermission(action: BizAction, resource = 'order') {
  const policy = useContext(PermissionContext)
  return policy?.can({ action, resource }) ?? false
}
```

### 7.3 三层权限控制

权限不要只做前端按钮隐藏，建议至少分三层：

- `页面入口层`
  - 能否访问页面、模块或路由
- `操作展示层`
  - 是否展示按钮、菜单、Tab、批量操作入口
- `请求执行层`
  - 提交、删除、导出等动作执行前再次校验

其中真正的安全边界仍然应该在服务端。

### 7.4 Next.js 中的落点建议

结合 `Next.js` 的服务端/客户端边界，推荐这样处理：

- `服务端页面入口`
  - 获取用户信息、系统标识、权限快照
- `客户端组件`
  - 根据权限快照控制按钮展示、禁用状态、交互反馈
- `服务端动作或接口`
  - 在提交、删除、导出等关键操作前再次校验

注意点：

- 服务端获取到的权限数据应尽量序列化后再传给客户端
- 不要把不可序列化对象直接跨边界传递
- 页面拦截和操作校验都要做，不能只选其一

## 8. 组合落地建议

如果要在多个系统中长期复用，推荐采用下面这套组合，而不是单独使用某一个方案：

### 8.1 推荐组合

- `工程组织`
  - `Monorepo + Component Library`
- `逻辑复用`
  - `Headless UI + Logic Hook`
- `标准页面扩展`
  - `Named Slots / Render Props`
- `样式差异`
  - `CSS Variables + Tailwind`，必要时配合 `CVA`
- `权限差异`
  - `Strategy Pattern + Provider`

### 8.2 推荐原因

- 业务逻辑沉淀在 `biz-core`
- 默认 UI 沉淀在 `biz-ui`
- 各系统只维护自己的适配层
- 既能低成本复用标准实现，也能支持局部和整体替换

## 9. 参考落地结构

```text
packages/
  biz-core/
    src/
      api/
      hooks/
      permissions/
      types/
      utils/
  biz-ui/
    src/
      components/
      pages/
      providers/
      theme/
      hooks/

apps/
  system-a/
    app/
    src/
      biz-adapter/
        permission.ts
        registry.tsx
        theme.css
        config.ts

  system-b/
    app/
    src/
      biz-adapter/
        permission.ts
        registry.tsx
        theme.css
        config.ts
```

### 各层职责

- `biz-core`
  - 业务逻辑、权限契约、接口层、类型定义
- `biz-ui`
  - 默认 UI、骨架组件、Provider、扩展点
- `biz-adapter`
  - 系统主题、权限实现、组件替换、接入配置

## 10. 方案选型建议

| 场景 | 推荐方案 |
| --- | --- |
| UI 结构完全不同，只想复用业务逻辑 | `Headless UI + Logic Hook` |
| 多系统长期维护，需要清晰工程边界 | `Monorepo + Component Library` |
| 页面大体一致，局部区域差异明显 | `Named Slots / Render Props` |
| 只是颜色、圆角、阴影等视觉差异 | `CSS Variables + Tailwind` |
| 结构不变，但组件需要多套视觉变体 | `CVA variant` |
| 需要系统级替换某类基础组件 | `Component Registry / Factory` |
| 仅少量底层原子组件需要构建期替换 | `Build-time Alias` |
| 不同系统权限规则不同 | `Strategy Pattern + Provider` |

## 11. 不建议的做法

- 每个系统复制一份完整页面，再各自改样式和权限
- 在公共组件中写大量 `if (system === 'A')`
- 把权限控制简化为“按钮隐藏”
- 一上来就使用 `Build-time Alias` 替换大量业务组件

这些做法短期快，但长期会导致：

- 逻辑分叉越来越多
- 公共模块不可维护
- 调试和排查问题成本不断升高

## 12. 总结

原始文档中提到的方案并不是互斥关系，而是分布在不同层级：

- `Headless UI + Logic Hook`
  - 解决逻辑复用问题
- `Monorepo + Component Library`
  - 解决工程组织问题
- `Slot / Render Props / Registry`
  - 解决默认实现的扩展问题
- `CSS Variables / CVA`
  - 解决样式差异问题
- `Strategy Pattern + Provider`
  - 解决权限适配问题

因此，真正可落地的方案通常不是“只选一个”，而是组合使用：

- 用 `Monorepo` 管理公共模块
- 用 `Headless Hook` 沉淀业务逻辑
- 用 `标准 UI + Slot / Render Props` 提供默认实现和局部扩展
- 用 `Tailwind Token + CVA` 处理视觉差异
- 用 `Permission Provider` 处理权限差异

这套组合既适合当前“内置标准实现 + 支持自定义”的需求，也适合后续新增更多系统时继续扩展。
