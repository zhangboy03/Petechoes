#!/usr/bin/env python3
"""
启动PostgreSQL服务器的脚本
"""

import os
import sys
from postgres_server import app, init_database

def main():
    # 检查是否在Zeabur环境中（通过环境变量判断）
    if not os.getenv('POSTGRES_HOST'):
        # 本地开发环境的默认配置
        print("🔧 检测到本地开发环境，请设置环境变量")
        print("💡 建议创建 .env 文件并设置以下变量：")
        print("   POSTGRES_HOST=your_host")
        print("   POSTGRES_PORT=your_port")
        print("   POSTGRES_DATABASE=your_db")
        print("   POSTGRES_USER=your_user")
        print("   PASSWORD=your_password")
        print("   MODELSCOPE_API_KEY=your_api_key")
        return
    
    print("🚀 启动PostgreSQL服务器...")
    print(f"📊 数据库主机: {os.getenv('POSTGRES_HOST')}")
    print(f"🔌 数据库端口: {os.getenv('POSTGRES_PORT')}")
    print(f"📁 数据库名称: {os.getenv('POSTGRES_DATABASE')}")
    
    # 初始化数据库
    if init_database():
        print("✅ 数据库初始化成功")
        print("🌐 服务器启动中...")
        print("⏹️  按 Ctrl+C 停止服务器")
        
        # 启动Flask应用
        port = int(os.getenv('PORT', 5001))
        app.run(host='0.0.0.0', port=port)
    else:
        print("❌ 数据库初始化失败，请检查连接配置")
        sys.exit(1)

if __name__ == '__main__':
    main() 