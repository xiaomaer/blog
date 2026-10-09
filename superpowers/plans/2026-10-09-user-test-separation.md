# 用户校验测试分离实施计划

关联设计：`../specs/2026-10-09-user-test-separation-design.md`。

## 1. 建立行为基线

- 在 `python_backend_scaffold/tests/test_user.py` 中导入原模块的 `User` 和 `check_user()`。
- 将管理员、普通用户和字段缺失示例改为断言，补充非 active 用户用例。
- 验证命令：在 `python_backend_scaffold/` 下执行 `poetry run python -B -m pytest -p no:cacheprovider -o pythonpath=src`。

## 2. 分离业务模块

- 将模型与函数移动到 `src/python_backend_scaffold/user.py`。
- 移除打印式测试、测试专用导入及原 `test.py`。
- 将测试导入更新为 `python_backend_scaffold.user`。
- 再次运行同一 pytest 命令，核对结果一致。
- 按用户确认，在 `pyproject.toml` 添加 `[tool.pytest.ini_options]` 和 `pythonpath = ["src"]`，然后执行不带临时路径参数的 `poetry run python -B -m pytest -p no:cacheprovider`。

## 3. 检查交付

- 执行 `poetry run ruff check --no-cache src/python_backend_scaffold/user.py tests/test_user.py`。
- 执行 `poetry run ruff format --check --no-cache src/python_backend_scaffold/user.py tests/test_user.py`。
- 人工确认业务代码无测试入口、返回值和异常规则未变、已有工作区改动得到保留。
- 汇报实际命令、退出码、文件职责和提交状态。

## 执行记录

- 首次未指定源码路径时，pytest 收集失败，退出码 `2`，原因是当前 Poetry 环境未安装项目包，无法导入 `src/` 下的模块。
- 使用命令行参数 `-o pythonpath=src` 后，重构前、重构后均为 `7 passed`，退出码均为 `0`。
- Ruff lint 输出 `All checks passed!`，退出码 `0`。
- Ruff 格式检查输出 `2 files already formatted`，退出码 `0`。
- 已人工核对业务模块只保留模型与函数，原有返回值、校验顺序和异常信息未改动。
- 用户已选择项目级 pytest 路径配置；已在 `pyproject.toml` 添加 `pythonpath = ["src"]`，未增加依赖。
- 配置生效后执行 `poetry run python -B -m pytest -p no:cacheprovider`，输出 `7 passed in 0.12s`，退出码 `0`，不再需要临时源码路径参数。
