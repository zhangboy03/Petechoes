# 🐾 Petechoes - 宠物纪念APP

一个温馨的iOS应用，帮助用户为他们的宠物创建美好的纪念照片。

## 📱 项目简介

Petechoes是一个基于AI图像生成技术的宠物纪念应用。用户可以上传宠物照片，应用会使用AI技术生成温馨的宠物纪念照，展现宠物坐在椅子上等待拍照的温馨场景。

## ✨ 主要功能

- 🖼️ **精美的UI设计**: 基于图片的页面设计，支持流畅的页面转场
- 📸 **智能图片选择**: 支持从相册选择各种格式的宠物照片
- 🤖 **AI图片生成**: 使用ModelScope FLUX.1-Kontext-dev模型生成温馨纪念照
- 💾 **数据持久化**: 后端PostgreSQL数据库存储，确保数据安全
- ⏱️ **实时状态反馈**: 生成过程中显示动态等待消息

## 🏗️ 技术架构

### 前端 (iOS)
- **语言**: Swift
- **框架**: SwiftUI
- **最低版本**: iOS 16.0+
- **主要特性**: PhotosPicker、动画转场、异步网络请求

### 后端 (Python)
- **框架**: Flask
- **数据库**: PostgreSQL
- **AI服务**: ModelScope FLUX.1-Kontext-dev
- **部署平台**: Zeabur
- **主要库**: psycopg2、Pillow、requests

## 🚀 快速开始

### iOS应用开发

1. **环境要求**:
   - Xcode 14.0+
   - iOS 16.0+

2. **运行应用**:
   ```bash
   # 克隆项目
   git clone https://github.com/zhangboy03/Petechoes.git
   
   # 打开Xcode项目
   open petechoes.xcodeproj
   
   # 在Xcode中运行
   ```

3. **添加背景图片**:
   - 将你的背景图片添加到 `petechoes/Assets.xcassets/1.imageset/1.png`
   - 将第二页背景图片添加到 `petechoes/Assets.xcassets/2.imageset/2.png`

### 后端部署

1. **Zeabur部署** (推荐):
   - 连接GitHub仓库到Zeabur
   - 选择`backend`目录作为构建路径
   - 配置环境变量（见下方）
   - 自动部署

2. **环境变量配置**:
   ```bash
   POSTGRES_HOST=your_postgres_host
   POSTGRES_PORT=your_postgres_port
   POSTGRES_DATABASE=your_database_name
   POSTGRES_USER=your_username
   PASSWORD=your_password
   MODELSCOPE_API_KEY=your_modelscope_api_key
   PUBLIC_URL=https://your-app-name.zeabur.app
   ```

3. **本地开发**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python start_server.py
   ```

## 📡 API文档

### 主要接口

- `POST /upload` - 上传宠物照片
- `GET /image/<id>` - 获取图片文件
- `GET /status/<id>` - 查询处理状态
- `GET /health` - 健康检查

详细API文档请查看 [backend/README.md](backend/README.md)

## 🎨 应用流程

1. **启动页面**: 显示精美的欢迎图片
2. **上传页面**: 点击或滑动进入，选择宠物照片
3. **处理过程**: 显示动态等待消息和进度指示器
4. **结果展示**: 生成的纪念照作为新的背景展示

## 🌟 特色功能

- **温馨的等待体验**: 生成过程中显示可爱的等待消息
- **流畅的动画**: 页面转场和状态变化都有平滑动画
- **智能图片处理**: 自动压缩和格式转换
- **安全的数据存储**: 所有图片安全存储在后端数据库

## 🔧 项目结构

```
petechoes/
├── petechoes/                 # iOS应用源码
│   ├── ContentView.swift      # 主界面
│   ├── petechoesApp.swift     # 应用入口
│   └── Assets.xcassets/       # 图片资源
├── backend/                   # 后端服务器
│   ├── postgres_server.py     # Flask服务器
│   ├── config.py             # 配置文件
│   ├── start_server.py       # 启动脚本
│   ├── requirements.txt      # Python依赖
│   └── zeabur.json          # 部署配置
└── README.md                 # 项目说明
```

## 📝 开发注意事项

- iOS应用需要iOS 16.0+支持
- 后端URL需要在`ContentView.swift`中正确配置
- 图片文件较大，请确保网络连接稳定
- AI生成过程通常需要1-3分钟

## 🎯 未来计划

- [ ] 支持更多图片风格选择
- [ ] 添加图片编辑功能
- [ ] 支持批量处理
- [ ] 添加社交分享功能
- [ ] 支持用户账户系统

## 🤝 贡献

欢迎提交Issues和Pull Requests来改进这个项目！

## 📄 许可证

本项目采用MIT许可证 - 详见LICENSE文件

## 💝 致谢

感谢ModelScope提供的AI图像生成服务，让这个项目成为可能。