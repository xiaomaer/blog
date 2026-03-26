# Next.js 项目构建优化

本文记录项目升级到 `Next.js 16.1.1` 后，在包体积、构建速度和 Docker 构建链路上的几项优化实践。目标不是堆配置项，而是解决下面几类实际问题：

- 图标库或大包导入方式不当，导致无效代码进入构建产物
- monorepo 中内部包重复构建，拉长本地和 CI 构建时间
- Dockerfile 层级设计不合理，缓存命中率低
- 缺少可视化工具，难以快速定位包体积问题

## 前提

- 将项目升级到 `Next.js 16.1.1`
- 增加 `next experimental-analyze` 命令，用于分析构建产物体积

```bash
next experimental-analyze
```

如果需要保留分析结果用于前后对比，也可以输出到本地目录：

```bash
next experimental-analyze --output
```

## 1. 依赖包体积优化

### 1.1 `lucide-react` 按需引入

对于图标名称在编码阶段已经确定的场景，优先使用具名导入：

```tsx
import { Download } from 'lucide-react'
```

不要把下面这种动态导入方式作为默认方案：

```tsx
import { DynamicIcon } from 'lucide-react/dynamic'
```

`DynamicIcon` 更适合“运行时根据字符串决定图标名”的场景。对于普通业务页面，具名导入更容易被优化，构建产物也更可控。

### 1.2 统一依赖版本

在 monorepo 中尽量保证 `lucide-react` 只有一个版本，避免出现以下问题：

- 重复安装同一个库
- 客户端产物中出现重复代码
- 构建分析时难以判断真实体积来源

## 2. `next.config.js` 优化

### 2.1 使用 `optimizePackageImports`

对于带有大量 barrel export 的包，可以开启 `optimizePackageImports`：

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    optimizePackageImports: ['lucide-react', 'shiki'],
  },
}

module.exports = nextConfig
```

适用场景：

- 图标库、语法高亮等导出项很多的包
- 项目仍然需要显式控制包导入优化策略

补充说明：

- 如果开发环境已经全面使用 Turbopack，很多导入优化会自动完成，这个配置不一定是必须项
- 即使配置了该选项，也仍然建议优先使用清晰的按需导入写法

### 2.2 生产环境移除无用 `console`

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  compiler: {
    removeConsole:
      process.env.NODE_ENV === 'production'
        ? { exclude: ['error', 'warn'] }
        : false,
  },
}

module.exports = nextConfig
```

这项配置的价值主要体现在两个方面：

- 减少客户端产物中的无用日志代码
- 避免线上保留过多调试输出

### 2.3 使用 `transpilePackages` 接管内部包编译

如果 `packages/ui`、`packages/lib` 这类内部包是被 Next.js 应用直接消费的，可以让 Next.js 在应用构建阶段统一处理，而不是先单独执行一次包构建。

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@dragonfruit/ui'],
}

module.exports = nextConfig
```

这样做的好处是：

- 减少 `packages/ui`、`packages/lib` 的独立 build 步骤
- 简化 CI 和 Dockerfile
- 避免应用构建和包构建重复做同一份转译工作

说明：

- `Next.js 16` 已默认使用 Rust/SWC 工具链，因此这里不再把 `swcMinify` 作为单独的核心优化项强调
- 文档里的重点应放在“减少无效打包”和“减少重复构建”这两类更直接的收益上

## 3. Dockerfile 优化

### 3.1 使用 BuildKit 缓存挂载

在安装依赖时缓存 `pnpm store`，可以显著减少重复安装时间：

```dockerfile
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
```

在执行构建时继续缓存 Turbo 和 Next.js 的构建结果：

```dockerfile
RUN --mount=type=cache,id=turbo-build,target=/app/.turbo \
    --mount=type=cache,id=next-cache-${APP_NAME},target=/app/apps/${APP_NAME}/.next/cache \
    pnpm --filter @dragonfruit/${APP_NAME} build
```

建议为不同应用使用独立的缓存 ID，例如 `next-cache-${APP_NAME}`，避免多个应用之间相互污染缓存。

### 3.2 按变更频率拆分 `COPY` 层

Docker 层缓存是否稳定，核心在于哪些文件会导致层失效。推荐按“变更频率”拆分复制顺序：

- 先复制根目录配置文件
- 再复制共享包源码
- 最后复制当前应用源码

示例：

```dockerfile
COPY --from=deps /app/node_modules ./node_modules

# Layer 1: Root configs
COPY pnpm-workspace.yaml package.json pnpm-lock.yaml ./
COPY turbo.json tsconfig.json ./
COPY scripts/ ./scripts/

# Layer 2: Shared packages
COPY packages/ui/ ./packages/ui/
COPY packages/lib/ ./packages/lib/

# Layer 3: Current app
COPY apps/${APP_NAME}/ ./apps/${APP_NAME}/
```

这样做的收益是：

- 当业务代码变更时，不会让共享包或根配置对应的缓存层一起失效
- Docker 构建过程更容易命中缓存
- CI 中重复构建的耗时更稳定

### 3.3 构建环境变量优化

建议在构建阶段显式声明以下环境变量：

```dockerfile
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
```

作用分别是：

- `NEXT_TELEMETRY_DISABLED=1`：禁用遥测，减少无关构建开销
- `NODE_ENV=production`：确保生产构建按生产模式执行

### 3.4 如果使用 Docker 部署，建议评估 `standalone` 输出

如果最终运行方式是容器化部署，可以进一步评估：

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
}

module.exports = nextConfig
```

这样可以输出更适合容器运行的最小化产物，降低运行镜像体积。是否采用，需要结合当前 monorepo 结构和部署方式一起评估。

## 4. 验证方式

优化完成后，建议从下面几个维度验证效果：

### 4.1 包体积

使用 `next experimental-analyze` 对比优化前后的结果，重点观察：

- `lucide-react` 是否仍然出现大面积打包
- `@dragonfruit/ui` 等内部包是否存在重复产物
- 客户端与服务端 bundle 是否出现异常增长

### 4.2 Docker 缓存命中率

关注 Docker 构建日志中以下几类变化：

- `pnpm install` 是否经常命中缓存
- 仅修改业务页面时，共享包层是否仍然复用
- 不同应用之间是否存在缓存串用现象

### 4.3 CI 构建耗时

对比优化前后的 CI 数据，重点看：

- 依赖安装时间是否下降
- 单应用构建时间是否下降
- 重复触发流水线时，整体耗时是否更稳定
