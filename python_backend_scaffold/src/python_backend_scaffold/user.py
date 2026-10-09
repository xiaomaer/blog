# 写一个函数接收一个 user_dict（包含 name, role, status）。
# 如果 status 不是 "active"，抛出异常或返回特定错误。
# 如果是 "admin"，返回一个包含他名字和大写状态的元组。
# 使用 Type Hints 标注所有的输入输出。

from typing import Any

from pydantic import BaseModel


# 1. 定义数据模型
class User(BaseModel):
    name: str
    role: str
    status: str


# 2. 业务逻辑函数
# 显式声明返回类型为 tuple 或 User 实例
def check_user(user_dict: dict[str, Any]) -> tuple[str, str] | User:
    # 使用 Pydantic v2 推荐的验证方式
    user = User.model_validate(user_dict)

    if user.status != "active":
        raise ValueError("User is not active")

    if user.role == "admin":
        return (user.name, user.status.upper())

    return user
