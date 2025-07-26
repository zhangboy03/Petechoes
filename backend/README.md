# Petechoes 后端服务器

## 项目简介

这是一个用于宠物纪念APP的后端服务器，使用Flask框架构建，支持图片上传、存储和AI图片生成功能。

## 技术栈

- **框架**: Flask
- **数据库**: PostgreSQL
- **图片处理**: Pillow
- **AI服务**: ModelScope FLUX.1-Kontext-dev
- **部署**: Zeabur

## 主要功能

1. **图片上传**: 接收iOS应用上传的宠物照片
2. **数据库存储**: 将原始图片和生成图片存储在PostgreSQL中
3. **AI图片生成**: 调用ModelScope API生成温馨的宠物纪念照
4. **图片服务**: 提供图片访问API
5. **状态查询**: 提供图片处理状态查询

## API接口

### 1. 图片上传
- **路径**: `POST /upload`
- **参数**: `image` (multipart/form-data)
- **返回**: 
  ```json
  {
    "success": true,
    "image_id": 123,
    "message": "图片上传成功，正在生成新图片..."
  }
  ```

### 2. 获取图片
- **路径**: `GET /image/<image_id>`
- **参数**: `type=original|generated`
- **返回**: 图片文件

### 3. 查询状态
- **路径**: `GET /status/<image_id>`
- **返回**:
  ```json
  {
    "status": "completed",
    "has_generated_image": true,
    "generated_image_url": "https://petecho.zeabur.app/image/123?type=generated"
  }
  ```

### 4. 健康检查
- **路径**: `GET /health`
- **返回**:
  ```json
  {
    "status": "healthy",
    "message": "PostgreSQL服务器运行正常"
  }
  ```

## 环境变量配置

在Zeabur部署时需要设置以下环境变量：

```bash
# PostgreSQL 数据库配置
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=your_postgres_port
POSTGRES_DATABASE=your_database_name
POSTGRES_USER=your_username
PASSWORD=your_password

# ModelScope API 配置
MODELSCOPE_API_KEY=your_modelscope_api_key

# 公网URL配置（部署后获得）
PUBLIC_URL=https://your-app-name.zeabur.app
```

## 本地开发

1. 安装依赖：
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. 配置环境变量（创建.env文件）

3. 启动服务器：
   ```bash
   python start_server.py
   ```

## 部署

项目已配置为在Zeabur平台部署：

1. 连接GitHub仓库
2. 选择`backend`目录作为构建路径
3. 配置环境变量
4. 自动部署

## 数据库结构

### images表
```sql
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    original_image BYTEA NOT NULL,
    generated_image BYTEA,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 注意事项

- 图片文件使用BYTEA类型存储在PostgreSQL中
- AI生成过程是异步的，使用轮询机制查询状态
- 支持JPG、PNG、HEIC等常见图片格式
- 生成过程通常需要1-3分钟

## 联系方式

如有问题，请联系开发团队。 