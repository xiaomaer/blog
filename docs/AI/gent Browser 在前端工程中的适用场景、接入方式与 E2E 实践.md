# Agent Browser 在前端工程中的适用场景、接入方式与 E2E 实践

## 一、Agent Browser 是什么

Agent Browser 可以理解为一个 **面向 AI Agent 的浏览器自动化工具**。

它本身不是大模型，也不是完整的 AI 系统。它的核心作用是：把真实浏览器包装成一个 AI Agent 可以理解、可以操作、可以调试的工具接口。

也就是说：

```text
AI Agent = 大脑
Agent Browser = 眼睛 + 手 + 浏览器调试工具
Chrome / Chromium = 真实运行环境
```

AI Agent 负责理解任务、规划步骤、判断页面状态；Agent Browser 负责打开网页、读取页面结构、点击按钮、填写表单、截图、查看网络请求、读取 console error 等。

---

## 二、Agent Browser 的核心工作方式

Agent Browser 的典型工作流程是：

```text
AI Agent 接收任务
  ↓
调用 Agent Browser 打开页面
  ↓
Agent Browser 返回页面 snapshot / screenshot / network / console 信息
  ↓
AI Agent 根据页面状态判断下一步
  ↓
调用 Agent Browser 执行 click / fill / navigate 等操作
  ↓
页面变化后重新观察
  ↓
循环直到任务完成
```

它最关键的设计是 **snapshot + ref**。

普通网页 DOM 非常大，直接丢给大模型会浪费大量 token，而且 AI 很难稳定地选择元素。Agent Browser 会把页面压缩成更适合 AI 使用的结构化文本，例如：

```text
@e1 [heading] "Login"
@e2 [input type="email"] placeholder="Email"
@e3 [input type="password"] placeholder="Password"
@e4 [button] "Sign in"
```

AI 看到这个结构后，就能判断：

```text
邮箱输入框是 @e2
密码输入框是 @e3
登录按钮是 @e4
```

然后执行：

```bash
agent-browser fill @e2 "user@example.com"
agent-browser fill @e3 "password"
agent-browser click @e4
```

这种方式比让 AI 猜 CSS selector 更稳定，也更节省上下文。

---

## 三、Agent Browser 适用场景

### 1. AI 操作真实网页

Agent Browser 适合让 AI 像真实用户一样操作网页：

```text
打开页面 → 点击按钮 → 填写表单 → 跳转页面 → 读取结果 → 汇总信息
```

常见场景包括：

* 自动检查后台配置是否正确
* 自动完成登录、onboarding、checkout 等流程
* 帮运营批量查看页面状态
* 在没有 API 的内部系统中提取页面信息
* 自动复现某个前端问题

它的优势是可以处理真实浏览器环境，包括 JS 渲染、动态加载、弹窗、按钮点击、表单输入、页面跳转等。

---

### 2. 前端调试与页面巡检

对于前端工程，Agent Browser 很适合做自动化巡检。

例如在一个页面中自动检查：

```text
页面是否正常渲染
console 是否有 error
关键按钮是否存在
静态资源是否 404
接口是否 5xx
页面截图是否正常
network 请求是否异常
```

尤其是在多 store、多 path、多环境的前端架构里，它可以帮助批量发现问题。

例如：

```text
/store-a
/store-b
/store-c

/products/foo
/collections/main
/cart
/checkout
```

Agent Browser 可以自动打开这些页面，记录截图、console、network、HAR，帮助工程师快速定位异常样本。

---

### 3. 页面内容抽取

当页面内容依赖浏览器渲染时，Agent Browser 也很有用。

适合的页面包括：

* SPA 页面
* 登录后页面
* 需要点击 tab 才能看到内容的页面
* 需要分页、筛选、下拉加载的页面
* 没有稳定 API 的内部系统页面

但对于简单静态 HTML 页面，直接用 HTTP 请求或 API 通常更快、更稳定。

---

### 4. AI 辅助生成 E2E 测试

Agent Browser 很适合让 AI 先探索页面，再把真实操作步骤转换成 Playwright 测试。

流程可以是：

```text
AI 打开页面
  ↓
Agent Browser 返回 snapshot
  ↓
AI 找到按钮和输入框
  ↓
AI 点击、输入、观察页面变化
  ↓
AI 总结用户路径
  ↓
生成 Playwright E2E case
```

也就是说，Agent Browser 更适合做 **测试生成和测试调试的辅助工具**，而不是正式的 E2E 测试框架。

---

### 5. 低频运营自动化

Agent Browser 也适合一些低频、半自动化的运营任务：

* 每天检查几个后台页面状态
* 批量查看商品页是否展示正常
* 检查某些配置是否生效
* 自动填写重复性表单
* 提交前让人确认

这种任务通常页面结构会变，但变化不大。相比写死脚本，AI + Agent Browser 会更灵活。

---

## 四、不适合使用 Agent Browser 的场景

### 1. 高并发、大规模爬虫

浏览器自动化成本高、速度慢、资源占用大。

大规模数据采集的优先级应该是：

```text
API > 静态 HTML 抓取 > 浏览器自动化
```

Agent Browser 不适合高并发抓取。

---

### 2. 核心生产操作全自动化

涉及以下操作时要非常谨慎：

```text
付款
下单
删除数据
发布内容
修改生产配置
发送邮件
权限变更
```

因为浏览器 Agent 容易受到页面变化、弹窗、误识别、提示注入等影响。

更安全的方式是：

```text
只读优先
提交前人工确认
使用最小权限账号
先在测试环境验证
关键操作加确认步骤
```

---

### 3. 已经有稳定 API 的系统

如果系统已经有稳定 API，优先使用 API。

API 的优势是：

```text
更快
更稳定
可观测性更强
错误更明确
不依赖 UI 结构
```

Agent Browser 更适合“没有 API”或者“必须验证真实 UI”的场景。

---

### 4. 精准性能诊断

Agent Browser 可以发现页面慢、资源异常、console 报错、接口失败，但它不应该作为唯一的性能分析工具。

例如这些问题：

```text
request queueing time 长
waiting for first byte 长
document parsing 长
静态资源没走 CDN
某些资源 TTFB 不稳定
```

根因分析仍然需要依赖：

```text
Chrome DevTools
Performance trace
HAR
Envoy access log
Next.js server log
RUM
Synthetic monitoring
Origin metrics
CDN metrics
```

Agent Browser 更适合做自动复现和异常样本收集。

---

## 五、如何接入 Agent Browser

### 1. 安装

推荐安装到前端项目中，便于固定版本：

```bash
npm install -D agent-browser
npx agent-browser install
npx agent-browser doctor
```

也可以全局安装：

```bash
npm install -g agent-browser
agent-browser install
agent-browser doctor
```

Linux 环境如果缺少浏览器依赖，可以使用：

```bash
agent-browser install --with-deps
```

---

### 2. 接入 Coding Agent

如果团队使用 Cursor、Claude Code、Codex、Gemini CLI、Copilot、Windsurf 等 AI Coding Agent，可以在项目中加入 Agent Browser 的使用说明。

例如在项目根目录添加 `AGENTS.md`：

```md
## Browser Automation

Use `agent-browser` for browser automation and frontend verification.

Core workflow:

1. Open target page with `agent-browser open <url>`
2. Run `agent-browser snapshot -i` to get interactive element refs
3. Use refs like `@e1`, `@e2` for click/fill operations
4. Re-run snapshot after page changes
5. Collect network, console, errors, screenshot, and HAR for debugging
```

这样 AI Agent 在处理前端问题时，就知道可以调用 Agent Browser。

---

### 3. 添加配置文件

可以在项目根目录添加 `agent-browser.json`：

```json
{
  "headed": false,
  "ignoreHttpsErrors": true,
  "profile": "./.agent-browser/profile",
  "hideScrollbars": false
}
```

如果需要走本地代理：

```json
{
  "proxy": "http://localhost:8080",
  "ignoreHttpsErrors": true,
  "profile": "./.agent-browser/profile"
}
```

---

## 六、前端巡检脚本示例

可以创建一个基础巡检脚本：

```bash
mkdir -p scripts
touch scripts/ab-check.sh
chmod +x scripts/ab-check.sh
```

`scripts/ab-check.sh`：

```bash
#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:3000}"
OUT="${OUT:-./.agent-browser-artifacts}"

mkdir -p "$OUT"

agent-browser close --all || true

agent-browser open
agent-browser network har start
agent-browser navigate "$URL"

agent-browser wait --load networkidle

agent-browser snapshot -i > "$OUT/snapshot.txt"
agent-browser network requests > "$OUT/network.txt"
agent-browser console > "$OUT/console.txt"
agent-browser errors > "$OUT/errors.txt"
agent-browser screenshot "$OUT/page.png" --full
agent-browser network har stop "$OUT/network.har"

agent-browser close
```

在 `package.json` 里添加：

```json
{
  "scripts": {
    "ab:install": "agent-browser install",
    "ab:doctor": "agent-browser doctor",
    "ab:check": "bash scripts/ab-check.sh"
  }
}
```

使用方式：

```bash
npm run ab:check -- "https://your-domain.com/store-a"
```

这个脚本可以产出：

```text
snapshot.txt
network.txt
console.txt
errors.txt
page.png
network.har
```

这些文件可以用于 AI 分析，也可以用于工程师排查问题。

---

## 七、结合 Next.js + Envoy 架构的使用方式

假设当前架构是：

```text
Next.js frontend 自己 host 静态资源
每个 store 有自己的 Envoy proxy
按 path 分流到 frontend
静态资源没有走 CDN
同一时间访问时，部分资源快，部分资源 TTFB 高
```

Agent Browser 可以用来批量巡检不同 store 和 path。

示例脚本：

```bash
#!/usr/bin/env bash
set -euo pipefail

BASE="https://your-domain.com"
OUT="./.agent-browser-artifacts"

stores=(
  "store-a"
  "store-b"
  "store-c"
)

paths=(
  "/"
  "/products"
  "/collections/main"
)

mkdir -p "$OUT"

for store in "${stores[@]}"; do
  for path in "${paths[@]}"; do
    safe_name="${store}${path}"
    safe_name="${safe_name//\//_}"

    url="${BASE}/${store}${path}"
    dir="${OUT}/${safe_name}"
    mkdir -p "$dir"

    echo "Checking $url"

    agent-browser close --all || true
    agent-browser open
    agent-browser network har start
    agent-browser navigate "$url"
    agent-browser wait --load networkidle

    agent-browser network requests > "$dir/network.txt"
    agent-browser console > "$dir/console.txt"
    agent-browser errors > "$dir/errors.txt"
    agent-browser screenshot "$dir/page.png" --full
    agent-browser network har stop "$dir/network.har"

    agent-browser close
  done
done
```

这个脚本可以帮助回答：

```text
哪些 store/path 更容易慢？
哪些静态资源返回 404/5xx？
同一个资源在不同 store 下是否表现不同？
是否有 console error？
页面首屏是否正常？
是否存在某些路径分流异常？
```

但它只能辅助发现现象。最终根因还是要结合：

```text
Envoy access log
Next.js server log
origin metrics
Chrome HAR
RUM 数据
server CPU / memory / connection pool
```

---

## 八、E2E 应该怎么处理

Agent Browser 不建议作为正式 E2E 测试框架。

更合理的分工是：

```text
Playwright = 正式 E2E 测试框架
Agent Browser = AI 辅助探索 / 复现 / 失败诊断 / 生成测试步骤
```

也就是：

```text
开发阶段：
AI + Agent Browser 打开页面、点击流程、看 console/network、生成 Playwright case

CI 阶段：
Playwright 跑稳定 E2E，失败时保留 trace、截图、video

排障阶段：
Agent Browser 复现失败页面，收集 HAR、snapshot、screenshot，辅助定位
```

---

## 九、Playwright E2E 接入建议

初始化：

```bash
npm init playwright@latest
```

`package.json`：

```json
{
  "scripts": {
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "e2e:debug": "playwright test --debug",
    "e2e:report": "playwright show-report"
  }
}
```

`playwright.config.ts`：

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 60_000,
  expect: {
    timeout: 10_000,
  },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI
    ? [['html'], ['github']]
    : [['html'], ['list']],
  use: {
    baseURL: process.env.E2E_BASE_URL || 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'desktop-chrome',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 7'] },
    },
  ],
  webServer: process.env.CI
    ? undefined
    : {
        command: 'npm run dev',
        url: 'http://localhost:3000',
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
```

---

## 十、E2E 测试重点

E2E 不要覆盖太多细节，应该少而稳。

对于电商或 store 类型前端，建议覆盖：

```text
首页能打开
collection 页面能渲染
product page 能渲染
加购
cart 页面
checkout 入口
登录态页面
关键静态资源没有 404/5xx
关键配置正确展示
```

不要把所有业务规则都放到 E2E。价格计算、库存、权限、复杂业务逻辑，优先用 unit test、integration test 或 API test 覆盖。

---

## 十一、E2E 示例：store 首页 smoke test

```ts
import { test, expect } from '@playwright/test';

const stores = [
  'store-a',
  'store-b',
  'store-c',
];

for (const store of stores) {
  test(`${store} home page renders`, async ({ page }) => {
    const response = await page.goto(`/${store}`, {
      waitUntil: 'domcontentloaded',
    });

    expect(response?.status()).toBeLessThan(500);

    await expect(page.locator('body')).toBeVisible();
    await expect(page).toHaveTitle(/.+/);

    const pageErrors: string[] = [];

    page.on('pageerror', error => {
      pageErrors.push(error.message);
    });

    await page.waitForLoadState('networkidle');

    expect(pageErrors).toEqual([]);
  });
}
```

---

## 十二、E2E 示例：检查静态资源错误

```ts
import { test, expect } from '@playwright/test';

test('static assets should not return 4xx/5xx', async ({ page }) => {
  const badResponses: string[] = [];

  page.on('response', response => {
    const url = response.url();
    const status = response.status();

    const isStaticAsset =
      url.includes('/_next/static/') ||
      url.endsWith('.js') ||
      url.endsWith('.css') ||
      url.endsWith('.woff2') ||
      url.endsWith('.png') ||
      url.endsWith('.jpg') ||
      url.endsWith('.webp');

    if (isStaticAsset && status >= 400) {
      badResponses.push(`${status} ${url}`);
    }
  });

  await page.goto('/store-a', { waitUntil: 'networkidle' });

  expect(badResponses).toEqual([]);
});
```

这个测试非常适合你们这种静态资源没有走 CDN、由 Next.js server 自 host 的场景。

---

## 十三、E2E 示例：加购流程

```ts
import { test, expect } from '@playwright/test';

test('user can add product to cart', async ({ page }) => {
  await page.goto('/store-a/products/example-product');

  await expect(
    page.getByRole('heading', { name: /example product/i })
  ).toBeVisible();

  await page.getByRole('button', { name: /add to cart/i }).click();

  await expect(
    page.getByText(/added to cart|cart/i)
  ).toBeVisible();

  await page.getByRole('link', { name: /cart/i }).click();

  await expect(page).toHaveURL(/cart/);
  await expect(page.getByText(/example product/i)).toBeVisible();
});
```

---

## 十四、Selector 规范

稳定的 selector 是 E2E 成败的关键。

推荐优先级：

```text
1. getByRole
2. getByLabel
3. getByText
4. getByTestId
5. CSS selector
6. XPath，尽量不用
```

前端组件中可以补充：

```tsx
<button data-testid="add-to-cart-button">
  Add to cart
</button>
```

测试中使用：

```ts
await page.getByTestId('add-to-cart-button').click();
```

避免使用脆弱 selector：

```ts
page.locator('.css-1abc23 > div:nth-child(2) > button')
```

这种 selector 很容易因为样式或 DOM 结构变化而失效。

---

## 十五、Agent Browser 在 E2E 中的定位

可以在 `AGENTS.md` 中加入 E2E 相关说明：

```md
## E2E Workflow

When creating or debugging E2E tests:

1. Use `agent-browser open <url>` to inspect the real page.
2. Use `agent-browser snapshot -i` to identify interactive elements.
3. Interact with refs using `agent-browser click @e1` or `agent-browser fill @e2 "value"`.
4. Re-run snapshot after every navigation or major UI change.
5. Convert the observed flow into Playwright tests.
6. Prefer Playwright role/text/testid locators over fragile CSS selectors.
7. Do not commit agent-browser scripts as the primary E2E suite unless explicitly needed for diagnostics.
```

也可以准备一个失败诊断脚本：

```bash
#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:3000/store-a}"
OUT="${OUT:-./artifacts/agent-browser}"

mkdir -p "$OUT"

agent-browser close --all || true

agent-browser batch --bail \
  "open $URL" \
  "wait --load networkidle" \
  "snapshot -i" \
  "screenshot $OUT/page.png --full" \
  "network requests" \
  "console" \
  "errors" \
  > "$OUT/diagnostics.txt"

agent-browser close
```

使用方式：

```bash
bash scripts/ab-diagnose.sh "https://preview.example.com/store-a/products/foo"
```

---

## 十六、CI 策略

推荐分层跑测试：

### PR 必跑

```text
核心 smoke tests
少量 store
Chromium only
控制在 5-10 分钟以内
```

### Nightly 全量跑

```text
多 store
多 locale
desktop + mobile
完整 checkout 链路
静态资源 404/5xx 检查
```

### 线上 synthetic 巡检

```text
定时访问核心路径
记录 TTFB、LCP、JS error、资源错误
异常时报警
```

GitHub Actions 示例：

```yaml
name: e2e

on:
  pull_request:
  push:
    branches:
      - main

jobs:
  e2e:
    runs-on: ubuntu-latest

    strategy:
      fail-fast: false
      matrix:
        shard: [1, 2, 3, 4]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - run: npm ci

      - run: npx playwright install --with-deps chromium

      - run: npm run build

      - run: npx playwright test --shard=${{ matrix.shard }}/4
        env:
          E2E_BASE_URL: ${{ secrets.E2E_BASE_URL }}

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report-${{ matrix.shard }}
          path: |
            playwright-report
            test-results
```

---

## 十七、整体落地建议

推荐按这个顺序推进：

```text
1. 先接入 Playwright
2. 写 3-5 条核心 smoke tests
3. 开启 trace / screenshot / video on failure
4. 统一 selector 规范
5. 补充 data-testid
6. 加 store/path matrix
7. 引入 Agent Browser 辅助测试生成和问题复现
8. 增加 Agent Browser 巡检脚本
9. 接入 CI 和 nightly
10. 再考虑线上 synthetic monitoring
```

---

## 十八、总结

Agent Browser 的核心价值不是替代 Playwright，也不是替代 Chrome DevTools，而是让 AI Agent 拥有真实浏览器操作能力。

它适合做：

```text
页面探索
AI 自动操作网页
前端问题复现
页面巡检
console/network/error 收集
辅助生成 E2E 测试
失败诊断
```

它不适合做：

```text
高并发爬虫
核心生产操作全自动化
已有 API 的稳定业务调用
精准性能根因分析
正式 E2E 主框架
```

对于你们这种 **Next.js frontend + store 级 Envoy proxy + path 分流 + 静态资源自 host** 的架构，推荐定位是：

```text
Playwright 负责稳定 E2E
Agent Browser 负责 AI 辅助探索、巡检和失败诊断
DevTools / HAR / Envoy log / Next.js log 负责性能根因分析
```

一句话概括：

```text
Agent Browser 不是 AI 大脑，而是 AI 的浏览器眼睛和手。
Playwright 是测试系统，Agent Browser 是 AI 辅助调试系统。
```
