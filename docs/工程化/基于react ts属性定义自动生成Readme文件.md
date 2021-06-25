# 基于react ts属性定义自动生成Readme文件

## 背景
* 组件库中，手动编写和维护组件readme，不但浪费时间，不好维护，还风格不统一。
* 目前组件库是基于react ts开发的，是否可以根据ts属性定义自动生成readme，解决上面问题呢？

## 调研
在调研过程中，主要有如下几个方案：
* api-extractor
  * 基于react-docgen库，扩展支持子组件，增强对JSDoc的支持，如支持@default、@enumdesc等注释
  * 使用remark生成markdown
* ts-props-gen
  * 基于react-docgen，扩展了对多文件的处理，并且对各文件导出的interface做分类，但不支持从其它文件引入ts类型
* styleguidist
  * 基于react-docgen-typescript和webpack，动态生成组件文档

目前方案主要使用react-docgen或react-docgen-typescript，两者区别如下：
* react-docgen
  * 来自Facebook开源
  * 基于Babel解析源码，对propTypes支持良好
  * 虽然新版本支持 TypeScript，但从其它文件导入的类型信息无法被获取
  * 不解析JSDoc部分，整个注释都作为描述部分，不过可以添加自己handler来补充解析
* react-docgen-typescript
  * 来自styleguidist开源，主要目标是服务TS React组件的API文档生成
  * 基于TS解析源码，不支持propTypes，Props interface继承的类型都可以拿到
  * 会读取JSDoc的@type、@default作为类型和默认值信息

基于我们的技术展考虑，选择基于react-docgen-typescript实现自动生成readme文件的命令行工具

## 实现
使用react-docgen-typescript解析react ts，然后通过react-docgen-typescript-markdown-render生成readme文件。主要代码如下：
```
const path = require('path');
const docgen = require('react-docgen-typescript');
const markdown = require('react-docgen-typescript-markdown-render');
const fs = require('fs');
const ora = require('ora');

const root = process.cwd();
const spinner = ora('正在生成readme...').start();

if (!dir) {
  // 遍历src/components下的组件，为所有组件生成readme
  const dirPath = path.resolve(root, base);
  fileDisplay(dirPath);
} else {
  // 为指定组件生成readme
  const componentPath = path.resolve(root, base, dir);
  genDoc(componentPath, file);
}

/**
 * 根据react组件ts类型定义生成readme
 * @param {string} base
 * @param {string} dir
 * @param {string} file
 */
function genDoc(path, file = 'src/index.tsx') {
  const componentFile = `${path}/${file}`;
  const componentDoc = `${path}/README.md`;
  if (!/.tsx/.test(componentFile)) {
    spinner.warn('请指定react组件的文件名，文件类型需为tsx格式');
    return;
  }
  try {
    if (fs.existsSync(componentFile)) {
      const options = {
        savePropValueAsString: true,
        componentNameResolver: dir ? () => dir : undefined,
      };
      const content = docgen.parse(componentFile, options);
      const renderContent = markdown.markdownRender(content);
      try {
        fs.writeFileSync(componentDoc, renderContent);
        spinner.succeed(`${componentFile}组件readme生成完成`);
      } catch (error) {
        spinner.fail(`${componentFile}组件：${err}`);
      }
    } else {
      spinner.warn('路径不存在');
    }
  } catch {
    spinner.fail('执行错误');
  }
}
```

## 结果
* 开发了`react-ts-to-markdown`命令行工具，[点击这里](https://github.com/xiaomaer/react-ts-to-markdown)查看完整代码和使用。

## 使用
* 安装命令行工具
  ```
    npm i react-ts-to-markdown
  ```
* 按照规范编写react ts组件，如下：
  ```
    import React from "react";
    import { IColumnProps } from './interface'

    /**
    * Form column.
    */
    export function Column2(props: IColumnProps) {
    return <div>{props.name || ''}</div>;
    }

    import { OmitCustomProps } from './custom';

    /**
    * Column properties.
    */
    export interface IColumnProps extends OmitCustomProps {
        /**
        * 设置名称
        * @default "red"
        */
        name?: string;
        /** 设置性别 */
        sex: number;
        /**
        * 获取年龄
        */
        getAge: () => number;
        /** 设置分类
        * @default "option1"
        */
        category: "option1" | "option2" | "option3";
    }

  ```
* 执行命令自动生成readme，命令如下：
  ```
    docgen [options]
    options:
        -b,--base <baseName> 指定组件根目录，默认为src/components
        -d,--dir <dirName> 指定react组件所在文件夹
        -f,--file <fileName> 指定react组件的文件名（包含后缀）
  ``` 
  默认情况下，将为项目根目录下，满足该src/components/**/src/index.tsx路径的所有组件生成readme。
*  生成的remade文件如下：
  ```
    ### Column

    Form column.

    #### Props

    | Name                  | Type                                | Default value | Description  |
    | --------------------- | ----------------------------------- | ------------- | ------------ |
    | name                  | string                              | "red"         | 设置名称     |
    | sex _(required)_      | number                              |               | 设置性别     |
    | getAge _(required)_   | () => number                        |               | 获取年龄     |
    | category _(required)_ | "option1" \| "option2" \| "option3" | "option1"     | 设置分类     |
    | b                     | number                              |               | 设置b        |
    | c                     | boolean                             |               | 设置c        |
    | d                     | keyof Point                         | "x"           | 设置d        |
    | e                     | Point                               |               | 设置e        |
    | test                  | string\[]                           |               | 设置test属性 |
    | method                | (arr: string\[]) => void            |               | 我是一个方法 |

  ```
