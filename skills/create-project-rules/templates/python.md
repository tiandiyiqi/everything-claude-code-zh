# Python 项目规则

## 语言特定规范

### Python 版本

**推荐使用 Python 3.10+**
- 支持类型提示的最新特性
- 更好的错误消息
- 性能改进

### 代码风格（PEP 8）

**缩进和空格：**
```python
# 推荐：4 个空格缩进
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price
    return total

# 避免：使用 Tab
def calculate_total(items):
	total = 0  # Tab 缩进
	return total
```

**命名规范：**
```python
# 变量和函数：snake_case
user_name = "Alice"
def get_user_by_id(user_id): pass

# 类：PascalCase
class UserRepository: pass

# 常量：UPPER_SNAKE_CASE
MAX_RETRY_COUNT = 3
API_BASE_URL = "https://api.example.com"

# 私有成员：前缀 _
class User:
    def __init__(self):
        self._password = None  # 私有属性

    def _validate(self):  # 私有方法
        pass
```

### 类型提示（Type Hints）

**函数类型提示：**
```python
# 推荐：使用类型提示
def calculate_total(items: list[Item]) -> float:
    return sum(item.price for item in items)

# 避免：没有类型提示
def calculate_total(items):
    return sum(item.price for item in items)
```

**复杂类型：**
```python
from typing import Optional, Union, Dict, List, Tuple

# Optional（可能为 None）
def find_user(user_id: str) -> Optional[User]:
    return users.get(user_id)

# Union（多种类型）
def process_input(value: Union[str, int]) -> str:
    return str(value)

# 字典和列表
def get_user_scores() -> Dict[str, int]:
    return {"alice": 100, "bob": 95}

def get_coordinates() -> Tuple[float, float]:
    return (10.5, 20.3)
```

**类型别名：**
```python
from typing import TypeAlias

UserId: TypeAlias = str
UserRole: TypeAlias = Literal["admin", "user", "guest"]

def get_user(user_id: UserId) -> User:
    pass
```

### 数据类（Dataclasses）

**优先使用 dataclass：**
```python
from dataclasses import dataclass

# 推荐
@dataclass
class User:
    id: str
    name: str
    age: int
    email: str | None = None

# 避免：手动编写 __init__
class User:
    def __init__(self, id: str, name: str, age: int, email: str | None = None):
        self.id = id
        self.name = name
        self.age = age
        self.email = email
```

**不可变数据类：**
```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# point.x = 10  # 错误：无法修改
```

### 错误处理

**具体的异常类型：**
```python
# 推荐：捕获具体异常
try:
    user = get_user(user_id)
except UserNotFoundError:
    return None
except DatabaseError as e:
    logger.error(f"Database error: {e}")
    raise

# 避免：捕获所有异常
try:
    user = get_user(user_id)
except Exception:  # 太宽泛
    return None
```

**自定义异常：**
```python
class UserNotFoundError(Exception):
    """用户未找到异常"""
    def __init__(self, user_id: str):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")
```

### 上下文管理器

**使用 with 语句：**
```python
# 推荐：自动关闭文件
with open('data.txt', 'r') as f:
    content = f.read()

# 避免：手动关闭
f = open('data.txt', 'r')
content = f.read()
f.close()
```

**自定义上下文管理器：**
```python
from contextlib import contextmanager

@contextmanager
def database_transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# 使用
with database_transaction() as conn:
    conn.execute("INSERT INTO users ...")
```

### 列表推导式和生成器

**列表推导式：**
```python
# 推荐：简洁的列表推导
squared = [x**2 for x in range(10) if x % 2 == 0]

# 避免：冗长的循环
squared = []
for x in range(10):
    if x % 2 == 0:
        squared.append(x**2)
```

**生成器表达式（大数据集）：**
```python
# 推荐：节省内存
total = sum(x**2 for x in range(1000000))

# 避免：创建完整列表
total = sum([x**2 for x in range(1000000)])
```

### 函数式编程

**使用内置函数：**
```python
# map, filter, reduce
from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map
squared = list(map(lambda x: x**2, numbers))

# filter
evens = list(filter(lambda x: x % 2 == 0, numbers))

# reduce
total = reduce(lambda acc, x: acc + x, numbers, 0)
```

**装饰器：**
```python
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

### 异步编程

**使用 async/await：**
```python
import asyncio

async def fetch_user(user_id: str) -> User:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/api/users/{user_id}') as response:
            return await response.json()

async def main():
    users = await asyncio.gather(
        fetch_user('1'),
        fetch_user('2'),
        fetch_user('3')
    )
```

### 代码质量检查清单

- [ ] 所有函数都有类型提示
- [ ] 所有公共函数都有 docstring
- [ ] 使用 dataclass 而非普通类（数据对象）
- [ ] 使用 with 语句管理资源
- [ ] 异常处理具体且有意义
- [ ] 没有使用 `except Exception`（除非必要）
- [ ] 通过 `mypy` 类型检查
- [ ] 通过 `pylint` 或 `flake8` 检查
- [ ] 通过 `black` 格式化

## 工具配置

### pyproject.toml

```toml
[tool.black]
line-length = 100
target-version = ['py310']

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pylint.messages_control]
max-line-length = 100
disable = [
    "C0111",  # missing-docstring
    "R0903",  # too-few-public-methods
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term"
```

### requirements.txt 结构

```
# requirements.txt - 生产依赖
fastapi==0.104.1
pydantic==2.5.0
sqlalchemy==2.0.23

# requirements-dev.txt - 开发依赖
pytest==7.4.3
pytest-cov==4.1.0
black==23.11.0
mypy==1.7.1
pylint==3.0.2
```

### 虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt
```
