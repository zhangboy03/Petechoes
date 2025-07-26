# 📊 PetEchoes 技术栈详解

## 🍎 前端技术栈 (iOS)

### 核心框架
- **SwiftUI 4.0+** - 现代化声明式UI框架
- **UIKit** - 系统级UI组件支持
- **Combine** - 响应式编程框架
- **Foundation** - 核心系统框架

### 多媒体处理
- **AVFoundation** - 音视频播放管理
  - `AVAudioPlayer` - 背景音乐播放
  - `AVAudioSession` - 音频会话管理
- **AVKit** - 视频播放组件
  - `VideoPlayer` - 开机动画播放

### 系统集成
- **PhotosUI** - 系统照片选择器
  - `PhotosPicker` - 多图片选择
  - `PhotosPickerItem` - 图片项目处理
- **CoreImage** - 图像处理框架
- **UIKit** - 图片显示和处理

### 网络和数据
- **URLSession** - HTTP网络请求
- **JSONSerialization** - JSON数据解析
- **UserDefaults** - 本地数据存储

## 🐍 后端技术栈 (Python)

### Web框架
- **Flask 2.0+** - 轻量级Web应用框架
- **Flask-CORS** - 跨域资源共享支持
- **Werkzeug** - WSGI工具库

### 数据库
- **PostgreSQL 12+** - 主数据库
- **psycopg2-binary** - Python PostgreSQL适配器
- **SQLAlchemy** (可选) - ORM框架

### 图像处理
- **Pillow (PIL) 8.0+** - Python图像处理库
  - 图像格式转换
  - 图像压缩和优化
  - 图像尺寸调整

### 外部API集成
- **requests 2.25+** - HTTP客户端库
- **BFL Flux API** - AI图像生成服务
- **RESTful API** - 标准化接口设计

### 配置管理
- **python-dotenv** - 环境变量管理
- **os.environ** - 系统环境变量

## ☁️ 部署和运维

### 云平台
- **Zeabur** - 现代化云平台
  - 自动化部署
  - 环境变量管理
  - 数据库托管
  - SSL证书自动配置

### 版本控制
- **Git** - 版本控制系统
- **GitHub** - 代码托管平台
- **GitHub Actions** (可选) - CI/CD自动化

### 监控和日志
- **Flask内置日志** - 应用日志记录
- **Zeabur监控** - 服务监控和告警

## 🤖 AI服务集成

### 图像生成
- **BFL Flux Kontext Max API**
  - 图像到图像转换
  - 风格迁移
  - 动漫风格化处理

### API规范
- **RESTful API** - 标准化接口设计
- **JSON** - 数据交换格式
- **HTTP/HTTPS** - 通信协议

## 📱 iOS开发环境

### 开发工具
- **Xcode 15.0+** - 集成开发环境
- **iOS Simulator** - 应用测试
- **Instruments** - 性能分析工具

### 支持版本
- **iOS 17.6+** - 最低支持版本
- **iPhone 16 Pro** - 主要适配机型
- **Universal App** - 支持所有iPhone设备

### 构建配置
- **Swift 5.9** - 编程语言版本
- **Deployment Target** - iOS 17.6
- **Architecture** - arm64, x86_64

## 🛠 开发工具链

### 代码编辑
- **Xcode** - iOS开发
- **Visual Studio Code** - 后端开发
- **Swift Package Manager** - 依赖管理

### 调试工具
- **Xcode Debugger** - iOS调试
- **Python Debugger** - 后端调试
- **Network Inspector** - 网络请求调试

### 性能优化
- **Instruments** - iOS性能分析
- **Memory Graph** - 内存泄漏检测
- **Time Profiler** - 性能瓶颈分析

## 📦 项目依赖

### iOS依赖 (Swift Package Manager)
```swift
// 系统框架，无需额外依赖
import SwiftUI
import AVFoundation
import PhotosUI
import Combine
```

### Python依赖 (requirements.txt)
```python
Flask>=2.0.0
Flask-CORS>=3.0.0
psycopg2-binary>=2.9.0
requests>=2.25.0
Pillow>=8.0.0
python-dotenv>=0.19.0
```

## 🔧 配置要求

### 开发环境
- **macOS 14.0+** - 开发机系统要求
- **Xcode 15.0+** - iOS开发工具
- **Python 3.8+** - 后端运行环境
- **PostgreSQL 12+** - 数据库环境

### 生产环境
- **Zeabur云平台** - 应用部署
- **PostgreSQL云数据库** - 数据存储
- **CDN** (可选) - 静态资源加速

## 📊 架构特点

### 前端架构
- **MVVM模式** - Model-View-ViewModel
- **响应式编程** - Combine框架
- **声明式UI** - SwiftUI框架
- **状态管理** - ObservableObject

### 后端架构
- **RESTful API** - 标准化接口
- **MVC模式** - Model-View-Controller
- **中间件** - 跨域和错误处理
- **异步处理** - 图像生成任务

### 数据流
```
iOS App → HTTP Request → Flask API → PostgreSQL
    ↑                                      ↓
UI Update ← JSON Response ← AI Processing ← Data Storage
```

## 🚀 性能优化

### 前端优化
- **图片懒加载** - 按需加载图片资源
- **异步网络请求** - 非阻塞UI操作
- **内存管理** - ARC自动引用计数
- **缓存策略** - 图片和数据缓存

### 后端优化
- **数据库连接池** - 复用数据库连接
- **图片压缩** - 减少传输大小
- **异步处理** - AI任务后台处理
- **错误重试** - 网络请求容错

这个技术栈确保了PetEchoes能够提供流畅、稳定、高质量的用户体验，同时保证了代码的可维护性和扩展性。 