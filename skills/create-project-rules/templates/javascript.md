# JavaScript 项目规则

## 语言特定规范

### 现代 JavaScript（ES2020+）

**使用 const 和 let，避免 var：**
```javascript
// 推荐
const API_URL = 'https://api.example.com'
let counter = 0

// 避免
var API_URL = 'https://api.example.com'
var counter = 0
```

### 箭头函数

**优先使用箭头函数：**
```javascript
// 推荐：简洁的箭头函数
const double = x => x * 2
const add = (a, b) => a + b

// 多行箭头函数
const processUser = user => {
  const normalized = normalizeUser(user)
  return saveUser(normalized)
}

// 避免：传统函数表达式（除非需要 this 绑定）
const double = function(x) {
  return x * 2
}
```

### 解构赋值

**对象解构：**
```javascript
// 推荐
const { name, age, email } = user
const { data, error } = await fetchUser(id)

// 避免
const name = user.name
const age = user.age
const email = user.email
```

**数组解构：**
```javascript
// 推荐
const [first, second, ...rest] = numbers
const [x, y] = getCoordinates()

// 避免
const first = numbers[0]
const second = numbers[1]
```

### 展开运算符

**对象展开：**
```javascript
// 推荐：不可变更新
const updatedUser = {
  ...user,
  name: newName,
  updatedAt: Date.now()
}

// 避免：直接修改
user.name = newName
user.updatedAt = Date.now()
```

**数组展开：**
```javascript
// 推荐
const allItems = [...items1, ...items2]
const copy = [...original]

// 避免
const allItems = items1.concat(items2)
const copy = original.slice()
```

### 模板字符串

**使用模板字符串：**
```javascript
// 推荐
const message = `Hello, ${user.name}! You have ${count} messages.`
const url = `/api/users/${userId}/posts`

// 避免
const message = 'Hello, ' + user.name + '! You have ' + count + ' messages.'
const url = '/api/users/' + userId + '/posts'
```

### 可选链和空值合并

**可选链（?.）：**
```javascript
// 推荐
const city = user?.address?.city
const firstItem = items?.[0]
const result = obj.method?.()

// 避免
const city = user && user.address && user.address.city
```

**空值合并（??）：**
```javascript
// 推荐：只在 null/undefined 时使用默认值
const name = user.name ?? 'Anonymous'
const count = data.count ?? 0

// 避免：|| 会将 0、''、false 也视为假值
const name = user.name || 'Anonymous'
```

### 异步处理

**async/await：**
```javascript
// 推荐
async function fetchUser(id) {
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

// 避免：Promise 链
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      return response.json()
    })
    .catch(error => {
      console.error('Failed to fetch user:', error)
      return null
    })
}
```

**并行异步操作：**
```javascript
// 推荐：并行执行
const [users, posts, comments] = await Promise.all([
  fetchUsers(),
  fetchPosts(),
  fetchComments()
])

// 避免：串行执行
const users = await fetchUsers()
const posts = await fetchPosts()
const comments = await fetchComments()
```

### 数组方法

**使用函数式数组方法：**
```javascript
// map
const userNames = users.map(u => u.name)

// filter
const activeUsers = users.filter(u => u.isActive)

// reduce
const total = items.reduce((sum, item) => sum + item.price, 0)

// find
const user = users.find(u => u.id === userId)

// some/every
const hasAdmin = users.some(u => u.role === 'admin')
const allActive = users.every(u => u.isActive)
```

### 对象方法

**Object.entries/keys/values：**
```javascript
// 遍历对象
Object.entries(user).forEach(([key, value]) => {
  console.log(`${key}: ${value}`)
})

// 获取键
const keys = Object.keys(user)

// 获取值
const values = Object.values(user)
```

### 模块导入导出

**命名导出（推荐）：**
```javascript
// utils.js
export function calculateTotal(items) { }
export const TAX_RATE = 0.1

// main.js
import { calculateTotal, TAX_RATE } from './utils.js'
```

**默认导出（仅用于组件）：**
```javascript
// Button.jsx
export default function Button({ children }) {
  return <button>{children}</button>
}

// App.jsx
import Button from './Button.jsx'
```

### 错误处理

**自定义错误类：**
```javascript
class ValidationError extends Error {
  constructor(message, field) {
    super(message)
    this.name = 'ValidationError'
    this.field = field
  }
}

// 使用
if (!email.includes('@')) {
  throw new ValidationError('Invalid email format', 'email')
}
```

### JSDoc 注释

**函数文档：**
```javascript
/**
 * 计算购物车总价
 * @param {Array<{price: number, quantity: number}>} items - 购物车商品
 * @param {number} taxRate - 税率（0-1 之间）
 * @returns {number} 总价（含税）
 */
function calculateTotal(items, taxRate = 0.1) {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  return subtotal * (1 + taxRate)
}
```

### 代码质量检查清单

- [ ] 使用 const/let，没有 var
- [ ] 使用箭头函数
- [ ] 使用解构赋值
- [ ] 使用展开运算符（不可变更新）
- [ ] 使用模板字符串
- [ ] 使用可选链和空值合并
- [ ] 使用 async/await 而非 Promise 链
- [ ] 使用函数式数组方法
- [ ] 没有 console.log（生产代码）
- [ ] 通过 ESLint 检查

## 工具配置

### package.json

```json
{
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest",
    "lint": "eslint . --ext .js,.jsx",
    "format": "prettier --write \"src/**/*.{js,jsx}\""
  },
  "devDependencies": {
    "eslint": "^8.54.0",
    "prettier": "^3.1.0",
    "vitest": "^1.0.0"
  }
}
```

### ESLint 配置（.eslintrc.json）

```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended"
  ],
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "rules": {
    "no-var": "error",
    "prefer-const": "error",
    "prefer-arrow-callback": "warn",
    "prefer-template": "warn",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  }
}
```

### Prettier 配置（.prettierrc）

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

### .gitignore

```
node_modules/
dist/
build/
.env
.env.local
*.log
.DS_Store
coverage/
```
