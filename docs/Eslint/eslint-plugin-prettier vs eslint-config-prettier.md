# eslint-plugin-prettier vs eslint-config-prettier

- [eslint-plugin-prettier vs eslint-config-prettier](#eslint-plugin-prettier-vs-eslint-config-prettier)
  - [一句话区别](#一句话区别)
  - [核心差异对比](#核心差异对比)
  - [eslint-config-prettier 是什么](#eslint-config-prettier-是什么)
  - [eslint-plugin-prettier 是什么](#eslint-plugin-prettier-是什么)
  - [两者是什么关系](#两者是什么关系)
  - [推荐用法](#推荐用法)
  - [配置示例](#配置示例)
  - [常见误区](#常见误区)
  - [总结](#总结)
  - [参考资料](#参考资料)

很多人在接入 Prettier 时，会把 `eslint-plugin-prettier` 和 `eslint-config-prettier` 当成“二选一”的关系。

实际上这两个包解决的不是同一个问题：

- `eslint-config-prettier`：负责关闭和 Prettier 冲突的 ESLint 规则
- `eslint-plugin-prettier`：负责把 Prettier 当成一条 ESLint 规则来运行

如果只记一条结论：

> 大多数项目优先选择 `Prettier + eslint-config-prettier`；只有在你明确希望“通过 ESLint 报出格式问题”时，再考虑 `eslint-plugin-prettier`。

## 一句话区别

- `eslint-config-prettier` 是“关规则”的
- `eslint-plugin-prettier` 是“跑格式化检查”的

## 核心差异对比

| 包名 | 主要作用 | 会不会执行 Prettier 格式化逻辑 | 会不会关闭冲突规则 | 典型用途 |
| --- | --- | --- | --- | --- |
| `eslint-config-prettier` | 关闭和 Prettier 冲突或无意义的 ESLint 格式规则 | 不会 | 会 | 让 ESLint 和 Prettier 和平共处 |
| `eslint-plugin-prettier` | 把 Prettier 作为 ESLint 规则执行 | 会 | 不会直接负责，但推荐配置会顺带启用 `eslint-config-prettier` | 希望通过 ESLint 直接报格式错误 |

## eslint-config-prettier 是什么

它的职责非常单一：**关闭那些和 Prettier 有冲突的 ESLint 规则**。

比如你已经使用 Prettier 管理缩进、分号、引号、逗号换行等格式问题，那么 ESLint 里对应的风格规则就没有必要继续开着，否则很容易出现：

- ESLint 要求一种写法
- Prettier 又格式化成另一种写法
- 两个工具互相打架

`eslint-config-prettier` 的价值就在这里：

- 它不会帮你格式化代码
- 它不会新增 lint 检查能力
- 它只是让 ESLint 不再管那些应该交给 Prettier 的事

所以它更像一个“协调层”。

## eslint-plugin-prettier 是什么

它会把 Prettier 作为 ESLint 规则执行，对应规则名是 `prettier/prettier`。

这意味着你运行 `eslint` 的时候，Prettier 也会一起跑；如果代码格式不符合 Prettier 规则，ESLint 会直接报错或警告。

它的特点是：

- 可以把格式问题统一收敛到 ESLint 输出里
- 执行 `eslint --fix` 时，也能顺手按 Prettier 的规则修复格式
- 适合想把“代码质量检查”和“格式检查”都放进同一条命令的人

但它也有明显代价：

- 编辑器里会出现很多格式类报错，噪音比较大
- 通常比直接运行 Prettier 更慢
- 多了一层 ESLint -> Prettier 的间接调用，排查问题更绕

## 两者是什么关系

两者不是替代关系，而是不同层次的工具：

- `eslint-config-prettier` 解决“规则冲突”问题
- `eslint-plugin-prettier` 解决“是否通过 ESLint 执行 Prettier”问题

它们可以一起用，而且 `eslint-plugin-prettier` 的推荐配置本身就会启用 `eslint-config-prettier`。

也就是说：

- 你用了 `eslint-plugin-prettier` 的推荐配置，通常也等于用了 `eslint-config-prettier`
- 你只用了 `eslint-config-prettier`，则不会自动运行 Prettier

## 推荐用法

### 方案一：大多数项目推荐

使用：

- `prettier`
- `eslint`
- `eslint-config-prettier`

执行方式：

- 编辑器保存时运行 Prettier
- 命令行使用 `prettier --write` 或 `prettier --check`
- ESLint 只负责潜在 bug、代码质量、最佳实践

这种方式的优点：

- 角色分工清晰
- 速度更快
- 编辑器噪音更少
- 更符合 Prettier 官方现在的推荐方向

### 方案二：确实需要统一进 ESLint 时再用

如果你的团队就是希望：

- 只跑一条 `eslint` 命令
- 只看 ESLint 报告
- 在 CI 里统一用 ESLint 的退出码控制检查结果

那就可以使用：

- `eslint-plugin-prettier`
- `eslint-config-prettier`

这时要接受一个现实：**格式问题会变成 lint 问题**，开发体验通常不如直接运行 Prettier 清爽。

## 配置示例

### 推荐方案：Prettier 直接负责格式化

`eslint.config.js`

```js
import js from '@eslint/js';
import eslintConfigPrettier from 'eslint-config-prettier/flat';

export default [
  js.configs.recommended,
  {
    rules: {
      'no-unused-vars': 'error',
      eqeqeq: 'error',
    },
  },
  eslintConfigPrettier,
];
```

`package.json`

```json
{
  "scripts": {
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "format": "prettier . --write",
    "format:check": "prettier . --check"
  }
}
```

说明：

- `eslint-config-prettier` 要尽量放在后面
- Prettier 配置建议放在 `.prettierrc`、`prettier.config.js` 这类专用文件里

### 需要把 Prettier 作为 ESLint 规则执行

`eslint.config.js`

```js
import js from '@eslint/js';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';

export default [
  js.configs.recommended,
  eslintPluginPrettierRecommended,
];
```

`.eslintrc.js`

```js
module.exports = {
  extends: ['plugin:prettier/recommended'],
};
```

这个推荐配置会同时做三件事：

- 启用 `prettier/prettier`
- 关闭和该插件配合时容易出问题的部分规则
- 启用 `eslint-config-prettier`

## 常见误区

### 1. `eslint-config-prettier` 会帮我格式化代码

不会。

它只会关闭冲突规则，不负责改代码格式。真正格式化代码的仍然是 `prettier`。

### 2. 只装 `eslint-plugin-prettier` 就够了

通常不够。

如果你让 ESLint 去执行 Prettier，但又没有关闭 ESLint 里的格式规则，还是会发生规则冲突。所以官方推荐配置会把 `eslint-config-prettier` 一起带上。

### 3. Prettier 选项写进 ESLint 规则里更集中

不推荐。

更稳妥的做法是把 Prettier 选项放到 `.prettierrc` 或 `prettier.config.js` 中，这样 CLI、编辑器插件、CI 使用的是同一份配置。

### 4. 用了 Prettier 之后，ESLint 就没用了

不是。

Prettier 主要处理“格式”，例如缩进、引号、换行。
ESLint 主要处理“代码质量”，例如未使用变量、危险写法、不合理依赖。

它们关注点不同，通常应该一起使用。

### 5. `eslint-plugin-prettier` 一定是最佳实践

不一定。

它的主要价值是“统一入口”，不是“更先进”。如果你的编辑器、命令行和 CI 已经能直接运行 Prettier，那么很多项目并不需要它。

## 总结

可以直接这样理解：

- 想解决“ESLint 和 Prettier 打架”的问题，用 `eslint-config-prettier`
- 想让 “Prettier 通过 ESLint 报错”，用 `eslint-plugin-prettier`
- 大多数情况下，推荐 `Prettier + eslint-config-prettier`
- 只有在你明确需要“统一到 ESLint 流程”时，再加上 `eslint-plugin-prettier`

## 参考资料

- [Prettier: Integrating with Linters](https://prettier.io/docs/next/integrating-with-linters.html)
- [Prettier: Prettier vs. Linters](https://prettier.io/docs/comparison)
- [eslint-config-prettier README](https://github.com/prettier/eslint-config-prettier)
- [eslint-plugin-prettier README](https://github.com/prettier/eslint-plugin-prettier)
