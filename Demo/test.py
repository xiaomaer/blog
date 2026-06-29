# 写一个函数接收一个 user_dict（包含 name, role, status）。
# 如果 status 不是 "active"，抛出异常或返回特定错误。
# 如果是 "admin"，返回一个包含他名字和大写状态的元组。
# 使用 Type Hints 标注所有的输入输出。

from typing import Any
from pydantic import BaseModel, ValidationError

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

# --- 测试用例 ---
if __name__ == "__main__":
    # 测试 Admin 分支 (返回 tuple)
    admin_data = {"name": "Alex", "role": "admin", "status": "active"}
    print(check_user(admin_data))  # 输出: ('Alex', 'ACTIVE')

    # 测试普通用户分支 (返回 User 实例)
    user_data = {"name": "Bob", "role": "user", "status": "active"}
    print(check_user(user_data))   # 输出: name='Bob' role='user' status='active'

    # 测试输入字段缺失 (Pydantic 会自动捕获并抛出 ValidationError)
    try:
        invalid_data = {"name": "Charlie", "role": "user"} # 缺 status
        check_user(invalid_data)
    except ValidationError as e:
        print("Pydantic 成功拦截了非法数据！")
