- [react-use 库学习总结](#react-use-库学习总结)
  - [架构设计](#架构设计)
  - [自定义hook实现分析](#自定义hook实现分析)


# react-use 库学习总结

## 架构设计

- 语言：typescript
- 打包：tsc，支持 cjs 和 esm 两种格式
- 代码规范：prettier 和 eslint， 通过 hooks 在 pre-commit 和 pre-push 阶段进行检查
- 单测：jest
- 文档：storybook
- DEMO：storybook
- CI/CD：travis ci 和 circle ci

## 自定义hook实现分析