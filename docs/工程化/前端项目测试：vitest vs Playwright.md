# vitest vs Playwright

**Vitest 和 Playwright 不是替代关系，而是分工不同。**

| 对比   | Vitest                             | Playwright                   |
| ---- | ---------------------------------- | ---------------------------- |
| 主要用途 | 单元测试 / 组件逻辑测试                      | E2E / 浏览器自动化测试               |
| 跑在哪里 | Node / jsdom / happy-dom           | 真实浏览器                        |
| 测什么  | 函数、hooks、组件逻辑                      | 用户完整操作流程                     |
| 速度   | 快                                  | 相对慢                          |
| 稳定性  | 高                                  | 容易受环境、网络、数据影响                |
| 适合频率 | 每次保存、每个 PR                         | PR smoke / 主干 / 发布前          |
| 典型工具 | `expect`, `vi.fn`, Testing Library | `page`, `locator`, `browser` |

## 怎么选

### 用 Vitest 测这些

```text
utils 函数
hooks
状态管理
表单校验
权限判断
数据转换
组件渲染逻辑
边界条件
```

示例：

```ts
import { describe, it, expect } from 'vitest'
import { formatPrice } from '@/utils/formatPrice'

describe('formatPrice', () => {
  it('formats price correctly', () => {
    expect(formatPrice(1234)).toBe('$1,234.00')
  })
})
```

## 用 Playwright 测这些

```text
登录
注册
下单
支付
创建/编辑/删除核心业务对象
权限跳转
关键页面可用性
多页面流程
```

示例：

```ts
import { test, expect } from '@playwright/test'

test('user can login', async ({ page }) => {
  await page.goto('/login')
  await page.getByLabel('Email').fill('test@example.com')
  await page.getByLabel('Password').fill('password123')
  await page.getByRole('button', { name: 'Login' }).click()

  await expect(page).toHaveURL(/dashboard/)
})
```

## 推荐组合

对于 Next.js 项目：

```text
Vitest：覆盖 70%~80% 的逻辑测试
Playwright：覆盖 10%~20% 的核心链路
人工测试：覆盖体验、视觉、复杂边界
```

## 最佳实践

```text
Vitest 跑得快，放在每次 PR 必跑
Playwright 跑得慢，PR 只跑 smoke，主干/发布前跑完整 E2E
```

推荐 scripts：

```json
{
  "scripts": {
    "test": "vitest",
    "test:unit": "vitest run",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui"
  }
}
```

## 一句话结论

**Vitest 保证代码逻辑正确，Playwright 保证用户流程真的能跑通。**

实际项目里应该两个都用：

```text
Vitest = 防止代码写错
Playwright = 防止产品流程坏掉
```
