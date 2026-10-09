# 用户校验逻辑与测试分离

## 目标与范围

将 `python_backend_scaffold/src/python_backend_scaffold/test.py` 中的业务代码与打印式测试分离，保持 `User` 和 `check_user()` 的行为及类型标注不变。

## 目录与职责

- `python_backend_scaffold/src/python_backend_scaffold/user.py`：保留 `User` 模型和 `check_user()`，不包含测试数据、打印或测试入口。
- `python_backend_scaffold/tests/test_user.py`：通过 pytest 导入并验证业务代码。
- 移除原 `src/python_backend_scaffold/test.py`；仓库内未找到其他文件引用该模块。

模型与函数继续放在同一个业务模块中，不增加额外分层。使用项目已有的 pytest 和 Ruff，不修改依赖配置。

按用户确认，在 `pyproject.toml` 的 `[tool.pytest.ini_options]` 中配置 `pythonpath = ["src"]`，使 pytest 可直接导入源码包，不再需要命令行路径参数。

## 行为约定

- active 管理员返回 `(name, "ACTIVE")`。
- active 普通用户返回字段保持不变的 `User` 实例。
- 非 active 用户抛出 `ValueError("User is not active")`，管理员同样适用。
- 缺少任一必填字段时抛出 Pydantic `ValidationError`。

## 验证与交付

先针对原模块运行断言测试，再移动业务代码并更新测试导入，使用同一组测试验证重构前后行为一致。随后运行 Ruff lint 和格式检查，并人工核对变更范围。

保留工作区原有改动。按用户最新要求，文档保留中文，无需翻译成英文；在用户明确要求后提交。
