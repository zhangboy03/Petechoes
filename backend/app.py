#!/usr/bin/env python3
"""
简化的Flask应用 - 用于Zeabur部署
如果主应用有问题，可以使用这个作为备用
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': 'Petechoes后端服务器运行正常',
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def home():
    """根路径"""
    return jsonify({
        'name': 'Petechoes Backend',
        'description': '宠物纪念APP后端服务',
        'endpoints': [
            '/health - 健康检查',
            '/upload - 图片上传',
            '/status/<id> - 查询状态',
            '/image/<id> - 获取图片'
        ]
    })

@app.route('/test', methods=['GET'])
def test():
    """测试接口"""
    env_info = {
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST', 'Not set'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT', 'Not set'),
        'POSTGRES_DATABASE': os.getenv('POSTGRES_DATABASE', 'Not set'),
        'POSTGRES_USER': os.getenv('POSTGRES_USER', 'Not set'),
        'MODELSCOPE_API_KEY': 'Set' if os.getenv('MODELSCOPE_API_KEY') else 'Not set',
        'PUBLIC_URL': os.getenv('PUBLIC_URL', 'Not set'),
        'PORT': os.getenv('PORT', '5001')
    }
    
    return jsonify({
        'message': '测试接口正常',
        'environment': env_info
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    logger.info(f"🚀 启动简化服务器在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 