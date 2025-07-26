#!/usr/bin/env python3
"""
Petechoes后端应用入口文件
放在根目录便于Zeabur部署
"""

import sys
import os

# 添加backend目录到Python路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

print("🚀 Petechoes后端启动中...")
print(f"📁 Backend目录: {backend_dir}")
print(f"🐍 Python路径: {sys.path[:3]}")

try:
    # 尝试导入完整的应用
    print("🔄 尝试导入完整应用...")
    import postgres_server
    app = postgres_server.app
    print("✅ 成功导入完整应用 (postgres_server)")
    
    # 验证关键路由是否存在
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    print(f"📋 可用路由: {routes}")
    
    if '/upload' in routes:
        print("✅ 确认包含/upload路由")
    else:
        print("❌ 警告: 缺少/upload路由")
        
except ImportError as e:
    print(f"❌ 导入完整应用失败: {e}")
    print("🔄 尝试导入简化版本...")
    try:
        from app import app as backup_app
        app = backup_app
        print("⚠️ 使用简化版本应用")
    except ImportError as e2:
        print(f"❌ 导入简化版本也失败: {e2}")
        # 创建最基本的应用
        from flask import Flask, jsonify
        app = Flask(__name__)
        
        @app.route('/')
        def emergency():
            return jsonify({"error": "应用启动失败", "message": "请检查依赖和配置"})
        
        print("🆘 使用紧急备用应用")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 启动服务器在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 