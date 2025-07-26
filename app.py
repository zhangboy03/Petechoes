#!/usr/bin/env python3
"""
Petechoes后端应用入口文件
放在根目录便于Zeabur部署
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    # 尝试导入完整的应用
    from postgres_server import app
    print("✅ 成功导入完整应用")
except ImportError as e:
    print(f"⚠️ 导入完整应用失败: {e}")
    print("🔄 使用简化版本...")
    # 使用简化版本
    from backend.app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 启动服务器在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 