# 多系统业务复用与 UI 适配解决方案-样板代码

## 1. 样板说明

这份样板代码对应 [多系统业务复用与 UI 适配解决方案-落地版](./多系统业务复用与%20UI%20适配解决方案-落地版本.md) 中的推荐组合：

- `biz-core`
  - 沉淀统一领域模型、服务契约、权限契约、业务策略契约、工作流契约
- `biz-ui`
  - 提供默认页面、默认基础组件、Slot 扩展点、组件注册表
- `apps/system-a`
  - 使用默认页面，少量替换基础组件，直接提交
- `apps/system-b`
  - 页面结构基本复用，但业务规则和提交流程存在差异

样板场景统一使用 `订单详情页`，分别演示：

- `UI 差异`
  - 两个系统使用不同的按钮和输入框风格
- `业务逻辑差异`
  - 系统 A 和系统 B 的编辑规则、校验规则、提交流程不同
- `权限差异`
  - 页面入口和客户端操作受权限快照控制
- `API 差异`
  - 两个系统实现不同的 `OrderService`

## 2. 目录结构

```text
packages/
  biz-core/
    src/order/
      types.ts
      permission.ts
      contracts.ts
      use-order-detail-controller.ts

  biz-ui/
    src/runtime/
      registry.tsx
      provider.tsx
    src/pages/order-detail/
      order-detail-page.tsx

apps/
  system-a/
    app/orders/[id]/page.tsx
    src/biz-adapter/
      config.ts
      permission.ts
      api/order-service.ts
      policies/order-policy.ts
      workflows/submit-workflow.ts
      registry.tsx
    src/entries/order-detail-entry.tsx

  system-b/
    app/orders/[id]/page.tsx
    src/biz-adapter/
      config.ts
      permission.ts
      api/order-service.ts
      policies/order-policy.ts
      workflows/submit-workflow.ts
      registry.tsx
    src/entries/order-detail-entry.tsx
```

## 3. `packages/biz-core`

### 3.1 `packages/biz-core/src/order/types.ts`

```ts
export type SystemCode = 'system-a' | 'system-b'
export type UserRole = 'viewer' | 'editor' | 'admin'
export type OrderStatus = 'draft' | 'submitted' | 'approved'

export type Order = {
  id: string
  code: string
  customerName: string
  amount: number
  remark: string
  tags: string[]
  status: OrderStatus
  sourceSystem: SystemCode
}

export type OrderForm = {
  amount: number
  remark: string
  tags: string[]
}

export type PermissionSnapshot = {
  canView: boolean
  canEdit: boolean
  canSubmit: boolean
  canExport: boolean
}

export type SubmitOrderInput = {
  id: string
  amount: number
  remark: string
  tags: string[]
  extra?: Record<string, unknown>
}

export type OrderContext = {
  system: SystemCode
  userId: string
  order: Order
  form: OrderForm
  permission: PermissionSnapshot
}
```

### 3.2 `packages/biz-core/src/order/permission.ts`

```ts
import type { Order, PermissionSnapshot } from './types'

export type BizAction = 'view' | 'edit' | 'submit' | 'export'

export type PermissionInput = {
  action: BizAction
  order: Pick<Order, 'status'>
}

export interface PermissionPolicy {
  can(input: PermissionInput): boolean
}

export function createPermissionSnapshot(
  policy: PermissionPolicy,
  order: Pick<Order, 'status'>,
): PermissionSnapshot {
  return {
    canView: policy.can({ action: 'view', order }),
    canEdit: policy.can({ action: 'edit', order }),
    canSubmit: policy.can({ action: 'submit', order }),
    canExport: policy.can({ action: 'export', order }),
  }
}
```

### 3.3 `packages/biz-core/src/order/contracts.ts`

```ts
import type { Order, OrderContext, OrderForm, SubmitOrderInput, SystemCode } from './types'

export type OrderFeatureConfig = {
  enableDraftBadge: boolean
  requireRemarkOnSubmit: boolean
}

export interface OrderService {
  submit(input: SubmitOrderInput): Promise<void>
  precheck?(input: SubmitOrderInput): Promise<void>
  syncAfterSubmit?(orderId: string): Promise<void>
}

export interface OrderPolicy {
  createInitialForm(order: Order): OrderForm
  canEdit(ctx: OrderContext): boolean
  validate(ctx: OrderContext, config: OrderFeatureConfig): string[]
  buildSubmitInput(ctx: OrderContext, config: OrderFeatureConfig): SubmitOrderInput
}

export interface SubmitWorkflow {
  submit(
    ctx: OrderContext,
    deps: {
      config: OrderFeatureConfig
      policy: OrderPolicy
      service: OrderService
    },
  ): Promise<void>
}

export type OrderFeatureRuntime = {
  system: SystemCode
  config: OrderFeatureConfig
  service: OrderService
  policy: OrderPolicy
  workflow: SubmitWorkflow
}
```

### 3.4 `packages/biz-core/src/order/use-order-detail-controller.ts`

```tsx
'use client'

import { useState, useTransition } from 'react'
import type { Order, OrderForm, PermissionSnapshot } from './types'
import type { OrderFeatureRuntime } from './contracts'

type UseOrderDetailControllerOptions = {
  initialOrder: Order
  userId: string
  permission: PermissionSnapshot
  runtime: OrderFeatureRuntime
}

export function useOrderDetailController({
  initialOrder,
  userId,
  permission,
  runtime,
}: UseOrderDetailControllerOptions) {
  const [order, setOrder] = useState(initialOrder)
  const [form, setForm] = useState(() => runtime.policy.createInitialForm(initialOrder))
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [isSubmitting, startTransition] = useTransition()

  const ctx = {
    system: runtime.system,
    userId,
    order,
    form,
    permission,
  } as const

  const canEdit = permission.canEdit && runtime.policy.canEdit(ctx)
  const canSubmit = permission.canSubmit && canEdit

  function patchForm(patch: Partial<OrderForm>) {
    setForm((current) => ({ ...current, ...patch }))
  }

  function setAmount(value: number) {
    patchForm({ amount: Number.isNaN(value) ? 0 : value })
  }

  function setRemark(value: string) {
    patchForm({ remark: value })
  }

  function setTags(value: string[]) {
    patchForm({ tags: value })
  }

  function submit() {
    if (!canSubmit) {
      setSubmitError('当前状态不可提交或无提交权限')
      return
    }

    startTransition(() => {
      void (async () => {
        try {
          const errors = runtime.policy.validate(ctx, runtime.config)
          if (errors.length > 0) {
            setSubmitError(errors[0])
            return
          }

          setSubmitError(null)

          await runtime.workflow.submit(ctx, {
            config: runtime.config,
            policy: runtime.policy,
            service: runtime.service,
          })

          setOrder((current) => ({
            ...current,
            amount: form.amount,
            remark: form.remark,
            tags: form.tags,
            status: 'submitted',
          }))
        } catch (error) {
          setSubmitError(
            error instanceof Error ? error.message : '提交失败，请稍后重试',
          )
        }
      })()
    })
  }

  return {
    order,
    form,
    config: runtime.config,
    permission,
    canEdit,
    canSubmit,
    isSubmitting,
    submitError,
    setAmount,
    setRemark,
    setTags,
    submit,
  }
}
```

## 4. `packages/biz-ui`

### 4.1 `packages/biz-ui/src/runtime/registry.tsx`

```tsx
'use client'

import { createContext, useContext } from 'react'

export type CardProps = {
  title: string
  extra?: React.ReactNode
  children: React.ReactNode
}

export type TextFieldProps = {
  label: string
  value: string | number
  disabled?: boolean
  multiline?: boolean
  onChange: (value: string) => void
}

export type PrimaryButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  loading?: boolean
}

export type BizComponentRegistry = {
  Card: React.ComponentType<CardProps>
  TextField: React.ComponentType<TextFieldProps>
  PrimaryButton: React.ComponentType<PrimaryButtonProps>
}

function DefaultCard({ title, extra, children }: CardProps) {
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-base font-semibold text-slate-900">{title}</h2>
        {extra}
      </div>
      <div className="space-y-4">{children}</div>
    </section>
  )
}

function DefaultTextField({
  label,
  value,
  disabled,
  multiline,
  onChange,
}: TextFieldProps) {
  if (multiline) {
    return (
      <label className="block space-y-2">
        <span className="text-sm font-medium text-slate-700">{label}</span>
        <textarea
          className="min-h-28 w-full rounded-xl border border-slate-300 px-3 py-2 text-sm outline-none ring-0 transition focus:border-slate-900"
          value={String(value)}
          disabled={disabled}
          onChange={(event) => onChange(event.target.value)}
        />
      </label>
    )
  }

  return (
    <label className="block space-y-2">
      <span className="text-sm font-medium text-slate-700">{label}</span>
      <input
        className="h-11 w-full rounded-xl border border-slate-300 px-3 text-sm outline-none ring-0 transition focus:border-slate-900"
        value={String(value)}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
      />
    </label>
  )
}

function DefaultPrimaryButton({
  loading,
  children,
  className,
  disabled,
  ...rest
}: PrimaryButtonProps) {
  return (
    <button
      className={[
        'inline-flex h-11 items-center justify-center rounded-xl bg-slate-900 px-5 text-sm font-medium text-white transition',
        'disabled:cursor-not-allowed disabled:bg-slate-400',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? '提交中...' : children}
    </button>
  )
}

const defaultRegistry: BizComponentRegistry = {
  Card: DefaultCard,
  TextField: DefaultTextField,
  PrimaryButton: DefaultPrimaryButton,
}

const BizRegistryContext = createContext<BizComponentRegistry>(defaultRegistry)

export function BizRegistryProvider({
  registry,
  children,
}: {
  registry?: Partial<BizComponentRegistry>
  children: React.ReactNode
}) {
  return (
    <BizRegistryContext.Provider value={{ ...defaultRegistry, ...registry }}>
      {children}
    </BizRegistryContext.Provider>
  )
}

export function useBizRegistry() {
  return useContext(BizRegistryContext)
}
```

### 4.2 `packages/biz-ui/src/runtime/provider.tsx`

```tsx
'use client'

import { createContext, useContext } from 'react'
import type { OrderFeatureRuntime } from '@repo/biz-core/src/order/contracts'
import type { PermissionSnapshot } from '@repo/biz-core/src/order/types'
import type { BizComponentRegistry } from './registry'
import { BizRegistryProvider } from './registry'

type BizRuntimeValue = {
  runtime: OrderFeatureRuntime
  permission: PermissionSnapshot
}

const BizRuntimeContext = createContext<BizRuntimeValue | null>(null)

export function BizRuntimeProvider({
  runtime,
  permission,
  registry,
  children,
}: {
  runtime: OrderFeatureRuntime
  permission: PermissionSnapshot
  registry?: Partial<BizComponentRegistry>
  children: React.ReactNode
}) {
  return (
    <BizRuntimeContext.Provider value={{ runtime, permission }}>
      <BizRegistryProvider registry={registry}>{children}</BizRegistryProvider>
    </BizRuntimeContext.Provider>
  )
}

export function useBizRuntime() {
  const value = useContext(BizRuntimeContext)

  if (!value) {
    throw new Error('useBizRuntime must be used inside BizRuntimeProvider')
  }

  return value
}

export function usePermission(action: keyof PermissionSnapshot) {
  const { permission } = useBizRuntime()
  return permission[action]
}
```

### 4.3 `packages/biz-ui/src/pages/order-detail/order-detail-page.tsx`

```tsx
'use client'

import { useOrderDetailController } from '@repo/biz-core/src/order/use-order-detail-controller'
import type { Order } from '@repo/biz-core/src/order/types'
import { useBizRegistry } from '../../runtime/registry'
import { useBizRuntime } from '../../runtime/provider'

type OrderDetailSlots = {
  renderHeaderExtra?: (ctx: OrderDetailSlotContext) => React.ReactNode
  renderSummaryExtra?: (ctx: OrderDetailSlotContext) => React.ReactNode
  renderFooterExtra?: (ctx: OrderDetailSlotContext) => React.ReactNode
}

type OrderDetailSlotContext = {
  order: Order
  canEdit: boolean
  canSubmit: boolean
}

export function OrderDetailPage({
  initialOrder,
  userId,
  slots,
}: {
  initialOrder: Order
  userId: string
  slots?: OrderDetailSlots
}) {
  const { runtime, permission } = useBizRuntime()
  const { Card, TextField, PrimaryButton } = useBizRegistry()

  const controller = useOrderDetailController({
    initialOrder,
    userId,
    permission,
    runtime,
  })

  const slotContext: OrderDetailSlotContext = {
    order: controller.order,
    canEdit: controller.canEdit,
    canSubmit: controller.canSubmit,
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <div className="space-y-1">
          <p className="text-sm text-slate-500">订单详情</p>
          <h1 className="text-2xl font-semibold text-slate-950">
            {controller.order.code}
          </h1>
        </div>
        {slots?.renderHeaderExtra?.(slotContext)}
      </header>

      <Card
        title="基本信息"
        extra={
          controller.config.enableDraftBadge && controller.order.status === 'draft' ? (
            <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-700">
              草稿
            </span>
          ) : null
        }
      >
        <div className="grid gap-4 md:grid-cols-2">
          <div className="rounded-xl bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">客户</p>
            <p className="mt-2 text-sm font-medium text-slate-900">
              {controller.order.customerName}
            </p>
          </div>
          <div className="rounded-xl bg-slate-50 p-4">
            <p className="text-xs uppercase tracking-wide text-slate-500">来源系统</p>
            <p className="mt-2 text-sm font-medium text-slate-900">
              {controller.order.sourceSystem}
            </p>
          </div>
        </div>

        {slots?.renderSummaryExtra?.(slotContext)}
      </Card>

      <Card title="编辑区域">
        <div className="grid gap-4 md:grid-cols-2">
          <TextField
            label="订单金额"
            value={controller.form.amount}
            disabled={!controller.canEdit}
            onChange={(value) => controller.setAmount(Number(value))}
          />
          <TextField
            label="标签（逗号分隔）"
            value={controller.form.tags.join(',')}
            disabled={!controller.canEdit}
            onChange={(value) =>
              controller.setTags(
                value
                  .split(',')
                  .map((item) => item.trim())
                  .filter(Boolean),
              )
            }
          />
        </div>

        <TextField
          label="备注"
          value={controller.form.remark}
          disabled={!controller.canEdit}
          multiline
          onChange={controller.setRemark}
        />

        {controller.submitError ? (
          <p className="text-sm text-rose-600">{controller.submitError}</p>
        ) : null}
      </Card>

      <Card title="操作">
        <div className="flex flex-wrap items-center gap-3">
          <PrimaryButton
            loading={controller.isSubmitting}
            disabled={!controller.canSubmit}
            onClick={controller.submit}
          >
            提交订单
          </PrimaryButton>

          {slots?.renderFooterExtra?.(slotContext)}
        </div>
      </Card>
    </div>
  )
}
```

## 5. `apps/system-a`

### 5.1 `apps/system-a/src/biz-adapter/config.ts`

```ts
import type { OrderFeatureConfig } from '@repo/biz-core/src/order/contracts'

export const systemAFeatureConfig: OrderFeatureConfig = {
  enableDraftBadge: true,
  requireRemarkOnSubmit: true,
}
```

### 5.2 `apps/system-a/src/biz-adapter/permission.ts`

```ts
import type { PermissionPolicy } from '@repo/biz-core/src/order/permission'
import type { UserRole } from '@repo/biz-core/src/order/types'

export function createSystemAPermissionPolicy(role: UserRole): PermissionPolicy {
  return {
    can({ action, order }) {
      if (role === 'admin') return true
      if (role === 'viewer') return action === 'view'

      if (action === 'view' || action === 'export') return true
      if (action === 'edit') return order.status === 'draft'
      if (action === 'submit') return order.status === 'draft'

      return false
    },
  }
}
```

### 5.3 `apps/system-a/src/biz-adapter/api/order-service.ts`

```ts
import type { OrderService } from '@repo/biz-core/src/order/contracts'

function wait(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export const systemAOrderService: OrderService = {
  async submit(input) {
    await wait(300)
    console.info('[system-a] submit order', input)
  },
}
```

### 5.4 `apps/system-a/src/biz-adapter/policies/order-policy.ts`

```ts
import type { OrderPolicy } from '@repo/biz-core/src/order/contracts'

export const systemAOrderPolicy: OrderPolicy = {
  createInitialForm(order) {
    return {
      amount: order.amount,
      remark: order.remark,
      tags: order.tags,
    }
  },

  canEdit(ctx) {
    return ctx.permission.canEdit && ctx.order.status === 'draft'
  },

  validate(ctx, config) {
    const errors: string[] = []

    if (ctx.form.amount <= 0) {
      errors.push('系统 A 要求订单金额必须大于 0')
    }

    if (config.requireRemarkOnSubmit && !ctx.form.remark.trim()) {
      errors.push('系统 A 提交前必须填写备注')
    }

    return errors
  },

  buildSubmitInput(ctx) {
    return {
      id: ctx.order.id,
      amount: ctx.form.amount,
      remark: ctx.form.remark,
      tags: ctx.form.tags,
      extra: {
        channel: 'system-a-web',
      },
    }
  },
}
```

### 5.5 `apps/system-a/src/biz-adapter/workflows/submit-workflow.ts`

```ts
import type { SubmitWorkflow } from '@repo/biz-core/src/order/contracts'

export const systemASubmitWorkflow: SubmitWorkflow = {
  async submit(ctx, deps) {
    const input = deps.policy.buildSubmitInput(ctx, deps.config)
    await deps.service.submit(input)
  },
}
```

### 5.6 `apps/system-a/src/biz-adapter/registry.tsx`

```tsx
import type { BizComponentRegistry } from '@repo/biz-ui/src/runtime/registry'

export const systemARegistry: Partial<BizComponentRegistry> = {
  PrimaryButton: ({ loading, children, className, disabled, ...rest }) => (
    <button
      className={[
        'inline-flex h-11 items-center justify-center rounded-lg bg-sky-600 px-5 text-sm font-medium text-white transition hover:bg-sky-700',
        'disabled:cursor-not-allowed disabled:bg-slate-300',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? '系统 A 提交中...' : children}
    </button>
  ),
}
```

### 5.7 `apps/system-a/src/entries/order-detail-entry.tsx`

```tsx
'use client'

import type { Order, PermissionSnapshot } from '@repo/biz-core/src/order/types'
import { BizRuntimeProvider } from '@repo/biz-ui/src/runtime/provider'
import { OrderDetailPage } from '@repo/biz-ui/src/pages/order-detail/order-detail-page'
import { systemAFeatureConfig } from '../biz-adapter/config'
import { systemAOrderService } from '../biz-adapter/api/order-service'
import { systemAOrderPolicy } from '../biz-adapter/policies/order-policy'
import { systemASubmitWorkflow } from '../biz-adapter/workflows/submit-workflow'
import { systemARegistry } from '../biz-adapter/registry'

export function SystemAOrderDetailEntry({
  userId,
  initialOrder,
  permission,
}: {
  userId: string
  initialOrder: Order
  permission: PermissionSnapshot
}) {
  return (
    <BizRuntimeProvider
      permission={permission}
      registry={systemARegistry}
      runtime={{
        system: 'system-a',
        config: systemAFeatureConfig,
        service: systemAOrderService,
        policy: systemAOrderPolicy,
        workflow: systemASubmitWorkflow,
      }}
    >
      <OrderDetailPage
        initialOrder={initialOrder}
        userId={userId}
        slots={{
          renderHeaderExtra: ({ order }) => (
            <span className="rounded-full bg-sky-100 px-3 py-1 text-xs font-medium text-sky-700">
              系统 A / {order.status}
            </span>
          ),
        }}
      />
    </BizRuntimeProvider>
  )
}
```

### 5.8 `apps/system-a/app/orders/[id]/page.tsx`

```tsx
import { notFound } from 'next/navigation'
import { createPermissionSnapshot } from '@repo/biz-core/src/order/permission'
import type { Order, UserRole } from '@repo/biz-core/src/order/types'
import { createSystemAPermissionPolicy } from '@/src/biz-adapter/permission'
import { SystemAOrderDetailEntry } from '@/src/entries/order-detail-entry'

async function getCurrentUser() {
  return {
    id: 'user-system-a-001',
    role: 'editor' as UserRole,
  }
}

async function getOrderById(id: string): Promise<Order | null> {
  return {
    id,
    code: `A-${id}`,
    customerName: 'Acme Inc.',
    amount: 3200,
    remark: '',
    tags: ['vip', 'web'],
    status: 'draft',
    sourceSystem: 'system-a',
  }
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const [user, order] = await Promise.all([getCurrentUser(), getOrderById(id)])

  if (!order) {
    notFound()
  }

  const permission = createPermissionSnapshot(
    createSystemAPermissionPolicy(user.role),
    order,
  )

  if (!permission.canView) {
    notFound()
  }

  return (
    <SystemAOrderDetailEntry
      userId={user.id}
      initialOrder={order}
      permission={permission}
    />
  )
}
```

## 6. `apps/system-b`

### 6.1 `apps/system-b/src/biz-adapter/config.ts`

```ts
import type { OrderFeatureConfig } from '@repo/biz-core/src/order/contracts'

export const systemBFeatureConfig: OrderFeatureConfig = {
  enableDraftBadge: false,
  requireRemarkOnSubmit: false,
}
```

### 6.2 `apps/system-b/src/biz-adapter/permission.ts`

```ts
import type { PermissionPolicy } from '@repo/biz-core/src/order/permission'
import type { UserRole } from '@repo/biz-core/src/order/types'

export function createSystemBPermissionPolicy(role: UserRole): PermissionPolicy {
  return {
    can({ action, order }) {
      if (role === 'admin') return true
      if (role === 'viewer') return action === 'view'

      if (action === 'view' || action === 'export') return true
      if (action === 'edit') return order.status !== 'approved'
      if (action === 'submit') return order.status === 'draft' || order.status === 'submitted'

      return false
    },
  }
}
```

### 6.3 `apps/system-b/src/biz-adapter/api/order-service.ts`

```ts
import type { OrderService } from '@repo/biz-core/src/order/contracts'

function wait(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export const systemBOrderService: OrderService = {
  async precheck(input) {
    await wait(200)

    if (input.amount > 100000) {
      throw new Error('系统 B 预校验失败：金额超过限制')
    }
  },

  async submit(input) {
    await wait(300)
    console.info('[system-b] submit order', input)
  },

  async syncAfterSubmit(orderId) {
    await wait(150)
    console.info('[system-b] sync after submit', orderId)
  },
}
```

### 6.4 `apps/system-b/src/biz-adapter/policies/order-policy.ts`

```ts
import type { OrderPolicy } from '@repo/biz-core/src/order/contracts'

export const systemBOrderPolicy: OrderPolicy = {
  createInitialForm(order) {
    return {
      amount: order.amount,
      remark: order.remark || '系统 B 默认备注',
      tags: order.tags,
    }
  },

  canEdit(ctx) {
    if (!ctx.permission.canEdit) return false
    return ctx.order.status === 'draft' || ctx.order.status === 'submitted'
  },

  validate(ctx) {
    const errors: string[] = []

    if (ctx.form.amount < 100) {
      errors.push('系统 B 要求订单金额不能小于 100')
    }

    if (ctx.form.tags.length === 0) {
      errors.push('系统 B 提交前至少需要一个标签')
    }

    return errors
  },

  buildSubmitInput(ctx) {
    return {
      id: ctx.order.id,
      amount: ctx.form.amount,
      remark: ctx.form.remark,
      tags: ctx.form.tags,
      extra: {
        approvalMode: 'manual',
        labelString: ctx.form.tags.join('|'),
      },
    }
  },
}
```

### 6.5 `apps/system-b/src/biz-adapter/workflows/submit-workflow.ts`

```ts
import type { SubmitWorkflow } from '@repo/biz-core/src/order/contracts'

export const systemBSubmitWorkflow: SubmitWorkflow = {
  async submit(ctx, deps) {
    const input = deps.policy.buildSubmitInput(ctx, deps.config)

    await deps.service.precheck?.(input)
    await deps.service.submit(input)
    await deps.service.syncAfterSubmit?.(ctx.order.id)
  },
}
```

### 6.6 `apps/system-b/src/biz-adapter/registry.tsx`

```tsx
import type { BizComponentRegistry } from '@repo/biz-ui/src/runtime/registry'

export const systemBRegistry: Partial<BizComponentRegistry> = {
  PrimaryButton: ({ loading, children, className, disabled, ...rest }) => (
    <button
      className={[
        'inline-flex h-11 items-center justify-center rounded-full bg-emerald-600 px-6 text-sm font-semibold text-white transition hover:bg-emerald-700',
        'disabled:cursor-not-allowed disabled:bg-slate-300',
        className,
      ]
        .filter(Boolean)
        .join(' ')}
      disabled={disabled || loading}
      {...rest}
    >
      {loading ? '系统 B 提交中...' : children}
    </button>
  ),

  TextField: ({ label, value, disabled, multiline, onChange }) => {
    if (multiline) {
      return (
        <label className="block space-y-2">
          <span className="text-sm font-semibold text-emerald-800">{label}</span>
          <textarea
            className="min-h-28 w-full rounded-2xl border border-emerald-300 bg-emerald-50 px-4 py-3 text-sm text-slate-900 outline-none transition focus:border-emerald-600"
            value={String(value)}
            disabled={disabled}
            onChange={(event) => onChange(event.target.value)}
          />
        </label>
      )
    }

    return (
      <label className="block space-y-2">
        <span className="text-sm font-semibold text-emerald-800">{label}</span>
        <input
          className="h-11 w-full rounded-2xl border border-emerald-300 bg-emerald-50 px-4 text-sm text-slate-900 outline-none transition focus:border-emerald-600"
          value={String(value)}
          disabled={disabled}
          onChange={(event) => onChange(event.target.value)}
        />
      </label>
    )
  },
}
```

### 6.7 `apps/system-b/src/entries/order-detail-entry.tsx`

```tsx
'use client'

import type { Order, PermissionSnapshot } from '@repo/biz-core/src/order/types'
import { BizRuntimeProvider } from '@repo/biz-ui/src/runtime/provider'
import { OrderDetailPage } from '@repo/biz-ui/src/pages/order-detail/order-detail-page'
import { systemBFeatureConfig } from '../biz-adapter/config'
import { systemBOrderService } from '../biz-adapter/api/order-service'
import { systemBOrderPolicy } from '../biz-adapter/policies/order-policy'
import { systemBSubmitWorkflow } from '../biz-adapter/workflows/submit-workflow'
import { systemBRegistry } from '../biz-adapter/registry'

export function SystemBOrderDetailEntry({
  userId,
  initialOrder,
  permission,
}: {
  userId: string
  initialOrder: Order
  permission: PermissionSnapshot
}) {
  return (
    <BizRuntimeProvider
      permission={permission}
      registry={systemBRegistry}
      runtime={{
        system: 'system-b',
        config: systemBFeatureConfig,
        service: systemBOrderService,
        policy: systemBOrderPolicy,
        workflow: systemBSubmitWorkflow,
      }}
    >
      <OrderDetailPage
        initialOrder={initialOrder}
        userId={userId}
        slots={{
          renderHeaderExtra: ({ order }) => (
            <span className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-medium text-emerald-700">
              系统 B / {order.status}
            </span>
          ),
          renderFooterExtra: ({ canEdit }) =>
            canEdit ? (
              <span className="text-sm text-emerald-700">
                系统 B 会在提交成功后自动触发同步
              </span>
            ) : null,
        }}
      />
    </BizRuntimeProvider>
  )
}
```

### 6.8 `apps/system-b/app/orders/[id]/page.tsx`

```tsx
import { notFound } from 'next/navigation'
import { createPermissionSnapshot } from '@repo/biz-core/src/order/permission'
import type { Order, UserRole } from '@repo/biz-core/src/order/types'
import { createSystemBPermissionPolicy } from '@/src/biz-adapter/permission'
import { SystemBOrderDetailEntry } from '@/src/entries/order-detail-entry'

async function getCurrentUser() {
  return {
    id: 'user-system-b-001',
    role: 'editor' as UserRole,
  }
}

async function getOrderById(id: string): Promise<Order | null> {
  return {
    id,
    code: `B-${id}`,
    customerName: 'Beta Corp.',
    amount: 6800,
    remark: '',
    tags: ['manual-approval'],
    status: 'submitted',
    sourceSystem: 'system-b',
  }
}

export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params
  const [user, order] = await Promise.all([getCurrentUser(), getOrderById(id)])

  if (!order) {
    notFound()
  }

  const permission = createPermissionSnapshot(
    createSystemBPermissionPolicy(user.role),
    order,
  )

  if (!permission.canView) {
    notFound()
  }

  return (
    <SystemBOrderDetailEntry
      userId={user.id}
      initialOrder={order}
      permission={permission}
    />
  )
}
```

## 7. 这份样板代码怎么对应方案

### 7.1 `biz-core`

负责沉淀稳定能力：

- `types.ts`
  - 统一领域模型
- `permission.ts`
  - 统一权限契约
- `contracts.ts`
  - 统一服务、策略、工作流契约
- `use-order-detail-controller.ts`
  - 共享主干逻辑

### 7.2 `biz-ui`

负责默认 UI 和扩展机制：

- `registry.tsx`
  - 默认基础组件 + 组件替换入口
- `provider.tsx`
  - Runtime 注入
- `order-detail-page.tsx`
  - 默认页面 + Slot 扩展点

### 7.3 `system-a / system-b`

只负责自己的适配层：

- `config.ts`
  - 轻差异走配置
- `permission.ts`
  - 权限差异
- `order-policy.ts`
  - 规则差异
- `submit-workflow.ts`
  - 流程差异
- `order-service.ts`
  - API 差异
- `registry.tsx`
  - 基础组件差异
- `page.tsx`
  - Next.js 服务端入口，获取数据和权限快照

## 8. 落地时怎么扩展

如果你要把这份样板改成真实项目，建议按下面顺序替换：

1. 把 `getOrderById`、`getCurrentUser` 替换成真实服务端查询。
2. 把 `systemAOrderService`、`systemBOrderService` 里的 mock 实现替换成真实 SDK 或 `fetch`。
3. 把 `registry.tsx` 中的默认组件替换成你们自己的 `@heyrevia/ui-kit` 封装。
4. 继续沿用 `policy / workflow / service` 这三个边界，不要把系统差异重新写回页面组件。

## 9. 一句话总结

这份样板代码真正想表达的不是“订单详情页怎么写”，而是这条分层边界：

- `页面结构` 归 `biz-ui`
- `主干流程` 归 `biz-core`
- `系统差异` 归 `biz-adapter`

只要这个边界守住，后面新增系统 C、系统 D 时，就不会重新陷入“复制一份页面再改”的老路。
