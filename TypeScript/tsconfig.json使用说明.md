- [tsconfig.json 使用说明](#tsconfigjson-使用说明)
  - [作用](#作用)
  - [使用 tsconfig.json](#使用-tsconfigjson)
  - [常用配置](#常用配置)
  - [常用编译选项](#常用编译选项)
  - [发布声明文件](#发布声明文件)
    - [方案](#方案)
    - [将声明文件和源码放在一起](#将声明文件和源码放在一起)
    - [将声明文件发布到 @types 下](#将声明文件发布到-types-下)
  - [typeRoots 和 types 的区别](#typeroots-和-types-的区别)

# tsconfig.json 使用说明

## 作用

指定用来编译这个项目的根文件和编译选项

## 使用 tsconfig.json

- 不带任何输入文件的情况下调用 tsc，编译器会从当前目录开始去查找 tsconfig.json 文件，逐级向上搜索父目录。
- 不带任何输入文件的情况下调用 tsc，且使用命令行参数--project（或-p）指定一个包含 tsconfig.json 文件的目录。
- 当命令行上指定了输入文件时，tsconfig.json 文件会被忽略。

## 常用配置

- extends：从另一个配置文件里继承配置
- files：指定编译文件列表
- compilerOptions：配置编译选项
- compileOnSave：保存时，是否自动重新编译
- include：指定编译文件或目录列表（支持文件 glob 匹配模式）
- exclude：指定排除的编译文件或目录列表（支持文件 glob 匹配模式）

`注意：`如果"files"和"include"都没有被指定，编译器默认包含当前目录和子目录下所有的 TypeScript 文件（.ts, .d.ts 和 .tsx），排除在"exclude"里指定的文件。

## 常用编译选项

详细参考：https://www.tslang.cn/docs/handbook/compiler-options.html

```
"compilerOptions": {
  "incremental": true, // TS编译器在第一次编译之后会生成一个存储编译信息的文件，第二次编译会在第一次的基础上进行增量编译，可以提高编译的速度
  "tsBuildInfoFile": "./buildFile", // 增量编译文件的存储位置
  "diagnostics": true, // 打印诊断信息
  "target": "ES5", // 目标语言的版本
  "module": "CommonJS", // 生成代码的模板标准
  "outFile": "./app.js", // 将多个相互依赖的文件生成一个文件，可以用在AMD模块中，即开启时应设置"module": "AMD",
  "lib": ["DOM", "ES2015", "ScriptHost", "ES2019.Array"], // TS需要引用的库，即声明文件，es5 默认引用dom、es5、scripthost,如需要使用es的高级版本特性，通常都需要配置，如es8的数组新特性需要引入"ES2019.Array",
  "allowJS": true, // 允许编译器编译JS，JSX文件
  "checkJs": true, // 允许在JS文件中报错，通常与allowJS一起使用
  "outDir": "./dist", // 指定输出目录
  "rootDir": "./", // 指定输出文件目录(用于输出)，用于控制输出目录结构
  "declaration": true, // 生成声明文件，开启后会自动生成声明文件
  "declarationDir": "./file", // 指定生成声明文件存放目录
  "emitDeclarationOnly": true, // 只生成声明文件，而不会生成js文件
  "sourceMap": true, // 生成目标文件的sourceMap文件
  "inlineSourceMap": true, // 生成目标文件的inline SourceMap，inline SourceMap会包含在生成的js文件中
  "declarationMap": true, // 为声明文件生成sourceMap
  "typeRoots": [], // 声明文件目录，默认时node_modules/@types
  "types": [], // 加载的声明文件包
  "removeComments":true, // 删除注释
  "noEmit": true, // 不输出文件,即编译后不会生成任何js文件
  "noEmitOnError": true, // 发送错误时不输出任何文件
  "noEmitHelpers": true, // 不生成helper函数，减小体积，需要额外安装，常配合importHelpers一起使用
  "importHelpers": true, // 通过tslib引入helper函数，文件必须是模块
  "downlevelIteration": true, // 降级遍历器实现，如果目标源是es3/5，那么遍历器会有降级的实现
  "strict": true, // 开启所有严格的类型检查
  "alwaysStrict": true, // 在代码中注入'use strict'
  "noImplicitAny": true, // 不允许隐式的any类型
  "strictNullChecks": true, // 不允许把null、undefined赋值给其他类型的变量
  "strictFunctionTypes": true, // 不允许函数参数双向协变
  "strictPropertyInitialization": true, // 类的实例属性必须初始化
  "strictBindCallApply": true, // 严格的bind/call/apply检查
  "noImplicitThis": true, // 不允许this有隐式的any类型
  "noUnusedLocals": true, // 检查只声明、未使用的局部变量(只提示不报错)
  "noUnusedParameters": true, // 检查未使用的函数参数(只提示不报错)
  "noFallthroughCasesInSwitch": true, // 防止switch语句贯穿(即如果没有break语句后面不会执行)
  "noImplicitReturns": true, //每个分支都会有返回值
  "esModuleInterop": true, // 允许export=导出，由import from 导入
  "allowUmdGlobalAccess": true, // 允许在模块中全局变量的方式访问umd模块
  "moduleResolution": "node", // 模块解析策略，ts默认用node的解析策略，即相对的方式导入
  "baseUrl": "./", // 解析非相对模块的基地址，默认是当前目录
  "paths": { // 路径映射，相对于baseUrl
    // 如使用jq时不想使用默认版本，而需要手动指定版本，可进行如下配置
    "jquery": ["node_modules/jquery/dist/jquery.min.js"]
  },
  "rootDirs": ["src","out"], // 将多个目录放在一个虚拟目录下，用于运行时，即编译后引入文件的位置可能发生变化，这也设置可以虚拟src和out在同一个目录下，不用再去改变路径也不会报错
  "listEmittedFiles": true, // 打印输出文件
  "listFiles": true// 打印编译的文件(包括引用的声明文件)
}
```

## 发布声明文件

### 方案

- 将声明文件和源码放在一起（建议这种）
- 将声明文件发布到 @types 下

### 将声明文件和源码放在一起

- 如果声明文件是通过 tsc 自动生成的，那么无需做任何其他配置，只需要把编译好的文件也发布到 npm 上，使用方就可以获取到类型提示了。
- 如果是手动写的声明文件，那么需要满足以下条件之一，才能被正确的识别
  - 给 package.json 中的 types 或 typings 字段指定一个类型声明文件地址
  - 在项目根目录下，编写一个 index.d.ts 文件
  - 针对入口文件（package.json 中的 main 字段指定的入口文件），编写一个同名不同后缀的 .d.ts 文件
  ```
  {
    "name": "foo",
    "version": "1.0.0",
    "main": "lib/index.js",
    "types": "foo.d.ts",
  }
  ```
  - 指定了 types 为 foo.d.ts 之后，导入此库的时候，就会去找 foo.d.ts 作为此库的类型声明文件了。
- 如果没有指定 types 或 typings，那么就会在根目录下寻找 index.d.ts 文件，将它视为此库的类型声明文件。
- 如果没有找到 index.d.ts 文件，那么就会寻找入口文件（package.json 中的 main 字段指定的入口文件）是否存在对应同名不同后缀的 .d.ts 文件。

### 将声明文件发布到 @types 下

- 如果我们是在给别人的仓库添加类型声明文件，但原作者不愿意合并 pull request，那么就需要将声明文件发布到 @types 下。
- 与普通的 npm 模块不同，@types 是统一由 DefinitelyTyped 管理的。要将声明文件发布到 @types 下，就需要给 DefinitelyTyped 创建一个 pull-request，其中包含了类型声明文件，测试代码，以及 tsconfig.json 等。
- pull-request 需要符合它们的规范，并且通过测试，才能被合并，稍后就会被自动发布到 @types 下。

## typeRoots 和 types 的区别

- 默认所有可见的"@types"包会在编译过程中被包含进来。 node_modules/@types 文件夹下以及它们子文件夹下的所有包都是可见的； 也就是说， ./node_modules/@types/，../node_modules/@types/和../../node_modules/@types/等等。

- 如果指定了 typeRoots，只有 typeRoots 下面的包才会被包含进来。 比如：

```
{
   "compilerOptions": {
       "typeRoots" : ["./typings"]
   }
}
```

这个配置文件会包含所有./typings 下面的包，而不包含./node_modules/@types 里面的包。

- 如果指定了 types，只有被列出来的包才会被包含进来。 比如：

```
{
   "compilerOptions": {
        "types" : ["node", "lodash", "express"]
   }
}
```

这个 tsconfig.json 文件将仅会包含 ./node_modules/@types/node，./node_modules/@types/lodash 和./node_modules/@types/express。`./node_modules/@types/*`里面的其它包不会被引入进来。
