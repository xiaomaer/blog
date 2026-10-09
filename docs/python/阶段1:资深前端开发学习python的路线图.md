These notes cover **Stage One: Concept Mapping and Syntax Translation**. They use **JavaScript and TypeScript as reference points** so experienced frontend developers can transfer existing knowledge without repeating a beginner programming course.

---

## 🎯 Core Concepts and Syntax Comparisons

### 1. 语句块、作用域与强制缩进

* **JS/TS:** 语句块通常用 `{}` 包围；`let`、`const` 具有块级作用域，`var` 不遵循同样的规则。缩进主要用于可读性。
* **Python:** **缩进划分语句块，不等于创建新作用域**。普通 `if`、`for`、`while` 不会创建独立的局部作用域；函数定义会引入函数局部作用域。通常使用 4 个空格缩进。
* **避坑：** 不要混用 Tab 和空格，否则会触发 `IndentationError`。

例如，在函数内的 `if` 分支中赋值，只要该分支已经执行，之后仍可在同一函数中读取该变量；若分支没有执行，读取尚未绑定的局部变量可能抛出 `UnboundLocalError`。详见 [Python 执行模型](https://docs.python.org/3.14/reference/executionmodel.html)；闭包和变量绑定的练习见[阶段三](./阶段3:硬核进阶与底层差异.md#22-作用域与闭包变量在什么时候被读取)。

```python
# Python example
def calculate_discount(price: float) -> float:
    if price > 100:
        final_price = price * 0.9
        return final_price
    return price

```

### 2. Variable Declarations and Hoisting

* **JS/TS:** `const`, `let`, and `var` have different binding and hoisting behavior.
* **Python:** **No declaration keyword is required**; assignment creates a binding.
* **There is no native `const`.** Conventionally, constants use uppercase names, such as `MAX_CONNECTIONS = 10`.
* Naming conventions: frontend code commonly uses `camelCase`; Python conventionally uses **`snake_case`**.



### 3. Important Differences in Falsy Values

Python conditionals handle empty containers directly because **empty containers are falsy**.

| Concept | JavaScript / TypeScript | Python | Key difference |
| --- | --- | --- | --- |
| **Missing or empty value** | `null` / `undefined` | `None` | Python uses `None` for the absence of a value. |
| **Boolean values** | `true` / `false` | `True` / `False` | Python requires the initial **capital letter**. |
| **Empty array/list** | `[]` is **truthy** in a conditional | `[]` is **falsy** in a conditional | `if ([])` takes the branch in JS; `if []:` does not in Python. |
| **Empty object/dictionary** | `{}` is **truthy** in a conditional | `{}` is **falsy** in a conditional | Python does not need an equivalent of `Object.keys(obj).length === 0` to check an empty dictionary. |

---

## ⚡ Translating Core Data Structures

### 1. Arrays and Lists

Python's `list` corresponds to a JS array; **list comprehensions** provide a concise way to transform and filter values.

```typescript
// TypeScript: filter and double
const nums = [1, 2, 3, 4, 5];
const doubledEvens = nums.filter(n => n % 2 === 0).map(n => n * 2); 
// Result: [4, 8]

```

```python
# Python: list comprehension
nums = [1, 2, 3, 4, 5]
doubled_evens = [n * 2 for n in nums if n % 2 == 0]
# Result: [4, 8]
# Syntax: [expression for item in iterable if condition]

```

### 2. Objects, Maps, and Dictionaries

Python's `dict` plays a role similar to a JS object or Map.

* **Pitfall:** Accessing a missing property in JS returns `undefined`. In Python, accessing a missing key with `dict['key']` raises **`KeyError`**.
* **Suggested approach:** Use `.get()` when a missing key should produce a fallback value.

```python
user_info = {"name": "Alex", "role": "admin"}

# Direct lookup raises an error if age is missing.
# age = user_info["age"] 

# A missing key can return None or an explicit default.
age = user_info.get("age")          # Returns None
age = user_info.get("age", 18)      # Returns 18

```

### 3. Destructuring and Unpacking

```typescript
// TypeScript destructuring and spread
const [first, ...rest] = [1, 2, 3, 4];
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 };

```

```python
# Python unpacking with * and **
first, *rest = [1, 2, 3, 4]  # first=1, rest=[2, 3, 4]

dict1 = {"a": 1}
dict2 = {**dict1, "b": 2}    # Merge dictionaries

```

---

## 🛠️ From TypeScript to Python Type Hints

As an experienced frontend developer, start using **type hints** in your Python code. Modern Python 3.10+ typing has many familiar counterparts in TypeScript.

### Basic Type Comparisons

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
scores: list[int] = [90, 85]  # Use built-in lowercase list/dict in modern Python.
user: dict[str, int | str] = {"id": 1, "name": "Tom"}

```

### Advanced Types: Unions, Optional Values, and Aliases

```typescript
// TypeScript
type ID = string | number;
interface User {
    id: ID;
    email?: string; // Optional property
}

```

```python
# Python (3.10+)
from typing import TypeAlias

ID: TypeAlias = str | int  # Type alias

# For structured data, consider Pydantic models or classes instead of a plain dict.
from pydantic import BaseModel

class User(BaseModel):
    id: ID
    email: str | None = None  # Optional value with a default of None

```

---

## 🔄 Async Programming and Exception Handling

### 1. Error Handling

* Python often follows **EAFP**: Easier to Ask for Forgiveness than Permission, handling an operation's exception rather than checking every precondition first.

```typescript
// TypeScript
try {
    const data = JSON.parse(rawString);
} catch (error) {
    console.error("Parsing failed", error);
}

```

```python
# Python
import json

try:
    data = json.loads(raw_string)
except json.JSONDecodeError as error:
    print(f"Parsing failed: {error}")

```

### 2. Async / Await and the Event Loop

Python's `asyncio` library offers a concurrency model with many similarities to JS.

```typescript
// TypeScript asynchronous concurrency
async function fetchData() {
    const [res1, res2] = await Promise.all([
        fetch("/api/1"),
        fetch("/api/2")
    ]);
    return { res1, res2 };
}

```

```python
# Python asynchronous concurrency requires asyncio.
import asyncio

async def fetch_data():
    # Assume get_api is an async function.
    # asyncio.gather collects concurrent results, similar to Promise.all.
    res1, res2 = await asyncio.gather(
        get_api("/api/1"),
        get_api("/api/2")
    )
    return {"res1": res1, "res2": res2}

```

---

## 🚀 Exercise: Write Your First Pythonic Function

Create a `test.py` file and translate this familiar frontend **token validation and user information extraction** task into Python:

> **Requirements:**
> 1. Write a function that accepts a `user_dict` containing `name`, `role`, and `status`.
> 2. If `status` is not `"active"`, raise an exception or return a defined error.
> 3. If the role is `"admin"`, return a tuple containing the user's name and uppercase status.
> 4. Add **type hints** to every input and output.
> 
> 

Completing this exercise gives you a practical checkpoint for the first stage of Python syntax.