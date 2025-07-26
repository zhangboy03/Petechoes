# 环境变量配置指南

## 本地开发环境设置

### 1. 创建 `.env` 文件

在 `backend/` 目录下创建 `.env` 文件，内容如下：

```bash
# PostgreSQL 数据库配置
# 从Zeabur PostgreSQL实例获取这些值
POSTGRES_HOST=hkg1.clusters.zeabur.com
POSTGRES_PORT=32747
POSTGRES_DATABASE=zeabur
POSTGRES_USER=root
PASSWORD=你的PostgreSQL密码

# ModelScope API 配置
# 从 https://modelscope.cn/ 获取API密钥
MODELSCOPE_API_KEY=你的ModelScope API密钥

# 公网URL配置（本地开发时使用localhost）
PUBLIC_URL=http://localhost:5001

# 端口配置（可选，默认5001）
PORT=5001
```

### 2. Zeabur 环境变量配置

在Zeabur控制台中设置以下环境变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `POSTGRES_HOST` | `hkg1.clusters.zeabur.com` | PostgreSQL主机地址 |
| `POSTGRES_PORT` | `32747` | PostgreSQL端口 |
| `POSTGRES_DATABASE` | `zeabur` | 数据库名称 |
| `POSTGRES_USER` | `root` | 用户名 |
| `PASSWORD` | `bl58Aa79pRMC14u6Zsz3kgcfT20INBYE` | 数据库密码 |
| `MODELSCOPE_API_KEY` | `ms-6ab8bbf1-8fbd-4859-9a93-742f4edc5da8` | ModelScope API密钥 |
| `PUBLIC_URL` | `https://petecho.zeabur.app` | 部署后的公网URL |

### 3. 获取API密钥

#### ModelScope API密钥
1. 访问 [ModelScope](https://modelscope.cn/)
2. 注册并登录账户
3. 进入控制台获取API密钥
4. 确保有足够的信用额度使用FLUX.1-Kontext-dev模型

#### PostgreSQL连接信息
1. 在Zeabur控制台创建PostgreSQL服务
2. 在服务详情中获取连接信息
3. 记录主机、端口、数据库名、用户名和密码

### 4. 验证配置

运行以下命令验证配置是否正确：

```bash
cd backend
python start_server.py
```

如果看到以下输出说明配置成功：
```
✅ 数据库初始化成功
🌐 服务器启动中...
```

### 5. 注意事项

- **不要**将 `.env` 文件提交到Git仓库
- 确保API密钥有足够的额度
- 数据库连接失败时检查网络和防火墙设置
- 本地开发时可以使用 `http://localhost:5001` 作为PUBLIC_URL 