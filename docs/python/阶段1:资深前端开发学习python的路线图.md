为你整理的 **阶段一：概念映射与语法“翻译”** 的完整学习资料。这份资料摒弃了面向零基础的繁琐叙述，专门以 **JavaScript/TypeScript 为参照物**，帮你实现知识的无缝迁移。

---

## 🎯 核心认知转变与语法对照

### 1. 块级作用域与强制缩进

* **JS/TS:** 使用 `{}` 定义块级作用域，缩进只是团队规范（靠 Prettier 维持）。
* **Python:** **没有大括号，缩进即作用域**。4 个空格是绝对标准。
* **避坑：** 不要混用 Tab 和空格，否则会触发 `IndentationError`。

```python
# Python 示例
def calculate_discount(price: float) -> float:
    if price > 100:
        final_price = price * 0.9
        return final_price
    return price

```

### 2. 变量声明与变量提升

* **JS/TS:** 有 `const`、`let`、`var`。严格区分常量和变量，存在变量提升。
* **Python:** **不需要关键字声明**，直接赋值即创建。
* **没有原生的 `const**`。通常用全大写字母表示约定俗成的常量（如 `MAX_CONNECTIONS = 10`）。
* 命名规范：前端习惯 `camelCase`，Python 必须用 **`snake_case`**（下划线命名）。



### 3. “虚值” (Falsy Values) 的巨大差异

Python 的条件判断比 JS 更加干净，因为**空容器在 Python 中自带 Falsy 属性**。

| 概念 | JavaScript / TypeScript | Python | 关键差异 |
| --- | --- | --- | --- |
| **空/无值** | `null` / `undefined` | `None` | Python 只有一个表示空的值：`None`。 |
| **布尔值** | `true` / `false` | `True` / `False` | Python 必须**大写首字母**。 |
| **空数组/列表** | `[]` (处于 if 中为 **Truthy**) | `[]` (处于 if 中为 **Falsy**) | **高危点：** JS 中 `if([])` 成立；Python 中 `if []:` 不成立！ |
| **空对象/字典** | `{}` (处于 if 中为 **Truthy**) | `{}` (处于 if 中为 **Falsy**) | 同上，Python 不需要像 JS 那样用 `Object.keys(obj).length === 0` 来判断空对象。 |

---

## ⚡ 核心数据结构“平移翻译”

### 1. Array vs List （数组与列表）

Python 的 `list` 对应 JS 的数组，但配合 **列表推导式 (List Comprehension)**，操作会极度优雅。

```typescript
// TypeScript: 过滤并翻倍
const nums = [1, 2, 3, 4, 5];
const doubledEvens = nums.filter(n => n % 2 === 0).map(n => n * 2); 
// 结果: [4, 8]

```

```python
# Python: 列表推导式
nums = [1, 2, 3, 4, 5]
doubled_evens = [n * 2 for n in nums if n % 2 == 0]
# 结果: [4, 8]
# 语法结构: [返回值 for 迭代对象 if 条件]

```

### 2. Object/Map vs Dict （对象与字典）

Python 的 `dict` 类似于 JS 的对象或 Map。

* **高危点：** 在 JS 中访问不存在的属性会返回 `undefined`。但在 Python 中，通过 `dict['key']` 访问不存在的键会直接**抛出 `KeyError` 异常崩溃**！
* **解决方案：** 始终使用 `.get()` 方法。

```python
user_info = {"name": "Alex", "role": "admin"}

# 危险写法（如果 age 不存在会报错）
# age = user_info["age"] 

# 安全写法（不存在时返回 None，或者设置默认值）
age = user_info.get("age")          # 返回 None
age = user_info.get("age", 18)      # 返回 18

```

### 3. 解构赋值与高级展开

```typescript
// TypeScript 解构与展开
const [first, ...rest] = [1, 2, 3, 4];
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };

```

```python
# Python 解构与展开 (使用 * 和 **)
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]

dict1 = {"a": 1}
dict2 = {**dict1, "b": 2}    # 合并字典

```

---

## 🛠️ 从 TypeScript 到 Python Type Hints

既然你是资深前端，写 Python 时请**直接开启强类型模式**。Python 3.10+ 的现代类型系统与 TS 契合度极高。

### 基础类型对照表

```typescript
// TypeScript
let username: string = "Tom";
let age: number = 25;
let isReady: boolean = true;
let scores: number[] = [90, 85];
let user: { id: number; name: string } = { id: 1, name: "Tom" };

```

```python
# Python (3.10+)
username: str = "Tom"
age: int = 25
is_ready: bool = True
scores: list[int] = [90, 85]  # 3.10+ 直接用原生小写 list/dict
user: dict[str, int | str] = {"id": 1, "name": "Tom"}

```

### 高级类型对照（联合类型、可选、别名）

```typescript
// TypeScript
type ID = string | number;
interface User {
    id: ID;
    email?: string; // 可选属性
}

```

```python
# Python (3.10+)
from typing import TypeAlias

ID: TypeAlias = str | int  # 类型别名

# 对于复杂的结构体，Python 不用 dict 表示，而是用 Pydantic 或 Class
from pydantic import BaseModel

class User(BaseModel):
    id: ID
    email: str | None = None  # 对应可选属性，赋予默认值 None

```

---

## 🔄 异步编程与异常处理心智对齐

### 1. 异常处理 (Error Handling)

* Python 更加倾向于 **EAFP 风格** (Easier to Ask for Forgiveness than Permission —— 抓异常比提前判断好)。

```typescript
// TypeScript
try {
    const data = JSON.parse(rawString);
} catch (error) {
    console.error("解析失败", error);
}

```

```python
# Python
import json

try:
    data = json.loads(raw_string)
except json.JSONDecodeError as error:
    print(f"解析失败: {error}")

```

### 2. Async / Await 与事件循环

Python 的 `asyncio` 库提供了与 JS 极其类似的并发心智模型。

```typescript
// TypeScript 异步并发
async function fetchData() {
    const [res1, res2] = await Promise.all([
        fetch("/api/1"),
        fetch("/api/2")
    ]);
    return { res1, res2 };
}

```

```python
# Python 异步并发 (需要引入 asyncio)
import asyncio

async def fetch_data():
    # 假设 get_api 是一个 async 异步函数
    # asyncio.gather 完美对应 Promise.all
    res1, res2 = await asyncio.gather(
        get_api("/api/1"),
        get_api("/api/2")
    )
    return {"res1": res1, "res2": res2}

```

---

## 🚀 练习任务：完成你的第一段 Pythonic 代码

在你的电脑上创建一个 `test.py`，尝试把以下前端常见的 **Token 校验与用户信息提取** 逻辑改写为 Python：

> **业务需求：**
> 1. 写一个函数接收一个 `user_dict`（包含 `name`, `role`, `status`）。
> 2. 如果 `status` 不是 `"active"`，抛出异常或返回特定错误。
> 3. 如果是 `"admin"`，返回一个包含他名字和大写状态的元组。
> 4. 使用 **Type Hints** 标注所有的输入输出。
> 
> 

完成这段代码的编写，你的 Python 语法第一关就已经顺利通关了！