# Git 合并 commit 与 rebase 指南

这篇文档解决两个高频问题：

- 开发过程中产生了很多零散 commit，提交前想整理成更清晰的提交历史
- 远程分支更新了，想同步最新代码，但不希望额外生成 merge commit

## 1. 合并多个 commit

如果你在功能分支上提交了多次临时 commit，例如：

```bash
git commit -m "WIP: initial implementation"
git commit -m "fix typo"
git commit -m "add tests"
```

在发起 PR 前，通常可以把这些提交整理成 1 个或少量有意义的 commit。

### 操作步骤

1. 查看最近几次提交

```bash
git log --oneline -n 5
```

2. 对最近 3 个提交执行交互式 rebase

```bash
git rebase -i HEAD~3
```

3. 在打开的编辑界面中，保留第一条为 `pick`，其余改为 `squash` 或 `fixup`

```text
pick  abc1234 WIP: initial implementation
squash def5678 fix typo
fixup 789abcd add tests
```

常见指令含义：

- `pick`：保留该 commit
- `squash`：合并到上一条 commit，并保留提交说明，稍后可继续编辑
- `fixup`：合并到上一条 commit，直接丢弃当前提交说明
- `reword`：保留 commit 内容，但修改提交说明

4. 保存并退出后，按提示整理最终的 commit message

整理完成后，你的多次临时提交就会变成一条更易理解的提交记录。

## 2. 将功能分支 rebase 到最新 `main`

如果远程 `main` 已经更新，而你希望当前功能分支基于最新主干继续开发，推荐这样做：

```bash
git fetch origin
git rebase origin/main
```

这样会把你当前分支上的提交“重新应用”到最新的 `main` 之后，提交历史通常会更线性。

### 冲突处理

如果 rebase 过程中出现冲突：

1. 修改冲突文件
2. 标记为已解决

```bash
git add <resolved-files>
```

3. 继续 rebase

```bash
git rebase --continue
```

如果不想继续本次 rebase，可以直接放弃：

```bash
git rebase --abort
```

### 推送说明

如果该分支之前已经推送到远程，rebase 后提交历史会变化，通常需要强制推送：

```bash
git push --force-with-lease origin feature/new-feature
```

优先使用 `--force-with-lease`，不要直接使用 `--force`。前者会先检查远程分支是否有你未拉取的新变更，风险更低。

## 3. 拉取远程更新时使用 rebase

如果你只是想拉取当前分支对应远程分支的最新提交，同时避免额外生成 merge commit，可以使用：

```bash
git pull --rebase
```

也可以设置为默认行为：

```bash
git config --global pull.rebase true
```

这样以后执行 `git pull` 时，会默认按 rebase 方式同步远程更新。

## 4. `merge` 和 `rebase` 的区别

- `merge`：保留分叉历史，可能产生额外的 merge commit
- `rebase`：改写提交历史，让历史更线性、更易阅读

如果团队更重视提交历史的整洁，功能分支开发阶段通常更偏向使用 `rebase`。  
如果团队更重视保留真实分叉过程，或者当前分支已经多人协作，通常更适合用 `merge`。

## 5. 什么情况下不要随便 rebase

以下场景需要谨慎：

- 已经被多人共同使用的公共分支，不要随意 rebase
- 已经推送并被他人基于其继续开发的分支，不要在未沟通的情况下改写历史
- 对历史是否会被改写没有把握时，先确认分支是否只有你自己在使用

一句话判断：

> rebase 更适合整理自己的分支历史，不适合随意改写团队公共历史。

## 6. 常用命令速查

```bash
# 合并最近 3 个 commit
git rebase -i HEAD~3

# 将当前分支变基到最新 main
git fetch origin
git rebase origin/main

# 继续 / 放弃 rebase
git rebase --continue
git rebase --abort

# 拉取远程更新并使用 rebase
git pull --rebase

# rebase 后推送远程分支
git push --force-with-lease origin <branch-name>
```
