# 🐾 PetEchoes - 宠物回声

<div align="center">

![iOS](https://img.shields.io/badge/iOS-17.6+-007AFF?style=for-the-badge&logo=ios)
![Swift](https://img.shields.io/badge/Swift-5.9-FA7343?style=for-the-badge&logo=swift)
![SwiftUI](https://img.shields.io/badge/SwiftUI-4.0-0066CC?style=for-the-badge&logo=swift)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask)

*一款温暖治愈的宠物纪念iOS应用*

[功能特色](#-功能特色) • [技术架构](#-技术架构) • [安装使用](#-安装使用) • [设计理念](#-设计理念) • [贡献指南](#-贡献指南)

</div>

## 📱 项目简介

PetEchoes（宠物回声）是一款专为纪念逝去宠物而设计的治愈系iOS应用。通过温暖的界面设计、AI图像生成技术和互动体验，为用户提供一个缅怀和纪念爱宠的数字空间。

### 🎨 设计哲学

- **治愈系美学**：采用温柔的色调和柔和的界面设计
- **情感连接**：通过AI技术重现与宠物的美好回忆
- **简约交互**：直观的手势和点击操作，专注于情感体验
- **个性化纪念**：为每只宠物创造独特的数字纪念空间

## ✨ 功能特色

### 🎬 沉浸式体验
- **开机动画**：支持自定义MOV视频启动页面
- **背景音乐**：循环播放的治愈系背景音乐
- **平滑转场**：页面间的自然过渡动画

### 📸 AI照相馆
- **智能合成**：将宠物照片与照相馆场景合成
- **动漫风格化**：使用AI将真实照片转换为动漫风格
- **实时预览**：即时查看生成效果

### 🖼️ 记忆相册
- **多图上传**：支持同时上传4张纪念照片
- **AI美化**：自动优化照片质量和风格
- **网格布局**：精心设计的照片展示布局

### 💌 情感信件
- **写信功能**：向逝去的宠物写信表达思念
- **键盘支持**：友好的文本输入体验
- **信件投递**：模拟寄信的仪式感

### 🌍 探索世界
- **手势导航**：左右滑动探索不同场景
- **交互热区**：点击建筑物发现隐藏内容
- **多层导航**：复杂而直观的页面跳转逻辑

### 🔮 未来功能（规划中）
- **相似动物匹配**：基于AI视觉识别，寻找与逝去宠物相似的其他动物，提供心理慰藉
- **社区分享**：与其他用户分享宠物回忆
- **个性化定制**：更多主题和风格选择

## 🛠 技术架构

### 前端技术栈
- **SwiftUI 4.0+**：现代化的iOS界面框架
- **AVFoundation**：音视频播放管理
- **PhotosUI**：系统照片选择器集成
- **Combine**：响应式编程和状态管理

### 后端技术栈
- **Flask 2.0+**：轻量级Python Web框架
- **PostgreSQL**：可靠的关系型数据库
- **psycopg2**：Python PostgreSQL适配器
- **Pillow**：Python图像处理库

### AI服务集成
- **BFL Flux API**：图像生成和风格转换
- **RESTful API**：标准化的服务接口

### 部署和运维
- **Zeabur**：现代化云平台部署
- **GitHub Actions**：自动化CI/CD流程
- **环境变量管理**：安全的配置管理

### 项目架构
```
petechoes/
├── iOS App (SwiftUI)
│   ├── Views/           # 页面视图组件
│   ├── Models/          # 数据模型
│   ├── Services/        # 网络和图像服务
│   └── Resources/       # 图片和音频资源
│
├── Backend (Flask)
│   ├── API endpoints    # RESTful接口
│   ├── Database models  # 数据库模型
│   └── AI integration   # AI服务集成
│
└── Assets
    ├── UI Images        # 界面背景图片
    ├── Audio Files      # 背景音乐
    └── Animations       # 启动动画视频
```

## 🚀 安装使用

### 环境要求
- **iOS开发**：
  - Xcode 15.0+
  - iOS 17.6+
  - macOS 14.0+

- **后端开发**：
  - Python 3.8+
  - PostgreSQL 12+

### 快速开始

1. **克隆项目**
```bash
git clone https://github.com/zhangboy03/Petechoes.git
cd Petechoes
```

2. **iOS应用设置**
```bash
# 打开Xcode项目
open petechoes.xcodeproj

# 在Xcode中选择模拟器或真机运行
```

3. **后端服务部署**
```bash
cd backend
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，填入数据库和API密钥

# 启动服务
python app.py
```

### 配置说明

#### 环境变量配置
```env
# 数据库配置
DATABASE_URL=postgresql://username:password@host:port/database

# AI服务配置
BFL_API_KEY=your_bfl_api_key_here

# 服务器配置
FLASK_ENV=development
FLASK_DEBUG=True
```

#### 资源文件
- 将启动动画视频命名为 `startup_animation.mov` 并放置在 `petechoes/` 目录
- 将背景音乐命名为 `bgm.MP3` 并放置在 `petechoes/` 目录
- 确保Assets.xcassets中包含编号为1-11的界面图片

## 📖 使用指南

### 基本操作流程
1. **启动应用** → 观看开机动画
2. **进入主页** → 点击房子图标进入拍摄场景
3. **上传照片** → 点击椅子上传宠物照片
4. **AI生成** → 等待AI合成照相馆风格图片
5. **记忆相册** → 上传多张纪念照片
6. **写信功能** → 向宠物表达思念
7. **探索世界** → 通过手势发现更多内容

### 手势操作
- **点击**：页面跳转和功能触发
- **左右滑动**：在不同场景间切换
- **长按**：某些特殊交互（未来功能）

## 🎯 设计理念

### 情感体验优先
PetEchoes相信技术应该服务于情感表达。每一个界面元素、每一次交互都经过精心设计，旨在为用户提供温暖、治愈的体验。

### AI赋能回忆
通过先进的AI图像生成技术，我们能够：
- 重现与宠物的美好时光
- 创造新的视觉回忆
- 提供情感慰藉和支持

### 未来愿景：相似动物匹配
我们正在开发一项创新功能：基于用户上传的宠物照片，使用AI视觉识别技术寻找其他长相相似的动物。这不仅是技术展示，更是一种心理慰藉——让用户感受到爱宠的"回声"在世界的某个角落依然存在。

### 社区共鸣
虽然每个人的失宠经历都是独特的，但悲伤和思念是共通的。PetEchoes希望成为一个温暖的社区，让用户在这里找到理解和支持。

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

### 贡献类型
- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 🎨 UI/UX优化
- 🧪 测试用例
- 🌐 国际化支持

### 开发规范
- 遵循Swift编码规范
- 保持代码简洁和可读性
- 添加必要的注释和文档
- 确保新功能包含测试用例

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

- 感谢所有为宠物纪念而努力的开发者和设计师
- 特别感谢AI技术让这种温暖的体验成为可能
- 致敬所有曾经陪伴我们的毛孩子们

## 📞 联系我们

- **Issue**：[GitHub Issues](https://github.com/zhangboy03/Petechoes/issues)
- **讨论**：[GitHub Discussions](https://github.com/zhangboy03/Petechoes/discussions)

---

<div align="center">

**用技术传递温暖，让爱永远回响** 💕

Made with ❤️ for our beloved pets

</div>