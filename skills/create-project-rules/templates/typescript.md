# TypeScript 项目规则

## 语言特定规范

### TypeScript 配置

**tsconfig.json 推荐配置：**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "lib": ["ES2020", "DOM"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### 类型定义

**优先使用类型推断：**
```typescript
// 推荐：让 TypeScript 推断类型
const user = { name: 'Alice', age: 30 }

// 避免：不必要的类型注解
const user: { name: string; age: number } = { name: 'Alice', age: 30 }
```

**使用 interface 而非 type（对象类型）：**
```typescript
// 推荐
interface User {
  name: string
  age: number
}

// 避免（除非需要联合类型或其他高级特性）
type User = {
  name: string
  age: number
}
```

**使用严格的 null 检查：**
```typescript
// 推荐：明确处理 null/undefined
function getUser(id: string): User | null {
  const user = findUser(id)
  return user ?? null
}

// 避免：使用 any 或忽略 null
function getUser(id: string): any {
  return findUser(id)
}
```

### 命名规范

- **接口（Interface）**：PascalCase，不使用 I 前缀
  ```typescript
  interface User { }  // 推荐
  interface IUser { } // 避免
  ```

- **类型别名（Type Alias）**：PascalCase
  ```typescript
  type UserId = string
  type UserRole = 'admin' | 'user' | 'guest'
  ```

- **枚举（Enum）**：PascalCase，成员使用 PascalCase
  ```typescript
  enum UserRole {
    Admin = 'ADMIN',
    User = 'USER',
    Guest = 'GUEST'
  }
  ```

- **泛型参数**：单个大写字母或 PascalCase
  ```typescript
  function identity<T>(value: T): T { return value }
  function map<TInput, TOutput>(fn: (x: TInput) => TOutput): TOutput { }
  ```

### 函数式编程

**优先使用函数式组件（React）：**
```typescript
// 推荐
const UserCard: React.FC<{ user: User }> = ({ user }) => {
  return <div>{user.name}</div>
}

// 避免
class UserCard extends React.Component<{ user: User }> {
  render() {
    return <div>{this.props.user.name}</div>
  }
}
```

**使用不可变数据操作：**
```typescript
// 推荐
const updatedUsers = users.map(u =>
  u.id === userId ? { ...u, name: newName } : u
)

// 避免
const user = users.find(u => u.id === userId)
user.name = newName  // 直接修改！
```

### 异步处理

**优先使用 async/await：**
```typescript
// 推荐
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`)
  return response.json()
}

// 避免：Promise 链
function fetchUser(id: string): Promise<User> {
  return fetch(`/api/users/${id}`)
    .then(response => response.json())
}
```

**错误处理：**
```typescript
async function fetchUser(id: string): Promise<User | null> {
  try {
    const response = await fetch(`/api/users/${id}`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Failed to fetch user:', error)
    return null
  }
}
```

### 导入导出

**使用命名导出（Named Exports）：**
```typescript
// 推荐
export function calculateTotal(items: Item[]): number { }
export const TAX_RATE = 0.1

// 避免：默认导出（除非是组件）
export default function calculateTotal(items: Item[]): number { }
```

**导入顺序：**
```typescript
// 1. 外部依赖
import React from 'react'
import { z } from 'zod'

// 2. 内部模块（绝对路径）
import { User } from '@/types'
import { api } from '@/lib/api'

// 3. 相对路径
import { Button } from './Button'
import styles from './styles.module.css'
```

### 代码质量检查清单

- [ ] 所有函数都有明确的返回类型
- [ ] 没有使用 `any` 类型（除非绝对必要）
- [ ] 所有 Promise 都有错误处理
- [ ] 使用 `const` 而非 `let`（除非需要重新赋值）
- [ ] 接口和类型定义在单独的文件中
- [ ] 没有未使用的导入
- [ ] 通过 `tsc --noEmit` 检查
- [ ] 通过 ESLint 检查

## 工具配置

### ESLint 配置

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
  }
}
```

### Prettier 配置

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "avoid"
}
```
