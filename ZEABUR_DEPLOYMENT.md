# Zeabur部署指南

## 1. 准备工作

### 1.1 注册Zeabur账号
1. 访问 [zeabur.com](https://zeabur.com)
2. 使用GitHub账号注册登录

### 1.2 准备GitHub仓库
确保您的代码已推送到GitHub仓库

## 2. 部署步骤

### 2.1 创建项目
1. 登录Zeabur控制台
2. 点击"New Project"创建新项目
3. 选择"Deploy from GitHub"
4. 选择您的petechoes仓库

### 2.2 添加PostgreSQL数据库
1. 在项目中点击"Add Service"
2. 选择"PostgreSQL"
3. 等待数据库创建完成
4. 记录数据库连接信息（Zeabur会自动生成环境变量）

### 2.3 配置环境变量
在后端服务的环境变量中添加：

```
POSTGRES_HOST=<数据库主机地址>
POSTGRES_PORT=5432
POSTGRES_DATABASE=<数据库名>
POSTGRES_USER=<用户名>
PASSWORD=<密码>
MODELSCOPE_API_KEY=<您的ModelScope API密钥>
PUBLIC_URL=<您的应用公网URL>
PORT=8080
```

**注意**：
- PostgreSQL相关变量通常会自动生成
- 您需要手动添加 `MODELSCOPE_API_KEY`
- `PUBLIC_URL` 在首次部署后获取

### 2.4 获取ModelScope API密钥
1. 访问 [ModelScope官网](https://www.modelscope.cn/)
2. 注册并登录账号
3. 进入API管理页面
4. 创建API密钥
5. 将密钥添加到Zeabur环境变量中

### 2.5 更新iOS应用配置
部署完成后：
1. 获取Zeabur分配的公网域名
2. 更新iOS应用中的 `backendUrl`：

```swift
let backendUrl = "https://your-app-name.zeabur.app"
```

## 3. 验证部署

### 3.1 测试后端接口
访问以下URL验证：
- `https://your-app-name.zeabur.app/health` - 健康检查
- `https://your-app-name.zeabur.app/test` - 环境变量检查

### 3.2 测试完整流程
1. 使用iOS应用上传图片
2. 检查后端日志
3. 验证图片生成流程

## 4. 常见问题

### 4.1 数据库连接失败
- 检查PostgreSQL服务是否正常运行
- 验证环境变量是否正确配置

### 4.2 ModelScope API调用失败
- 确认API密钥是否有效
- 检查账户余额和调用限制

### 4.3 图片上传失败
- 检查网络连接
- 验证后端URL是否正确
- 查看应用日志了解具体错误

## 5. 监控和维护

### 5.1 查看日志
在Zeabur控制台中可以实时查看应用日志

### 5.2 扩容配置
根据用户量调整服务器规格

### 5.3 域名配置
可以绑定自定义域名替换默认的zeabur.app域名 