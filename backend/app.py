#!/usr/bin/env python3
"""
完整的Flask应用 - 集成所有功能
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import requests
from PIL import Image
import io
import threading
import time
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# ModelScope API配置
MODELSCOPE_API_URL = 'https://api-inference.modelscope.cn/v1/images/generations'

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'hkg1.clusters.zeabur.com'),
    'port': int(os.getenv('POSTGRES_PORT', '30177')),
    'database': os.getenv('POSTGRES_DATABASE', os.getenv('POSTGRES_DB', 'zeabur')),
    'user': os.getenv('POSTGRES_USERNAME', os.getenv('POSTGRES_USER', 'root')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('PASSWORD', 'laKs69d7AVXmTJ5H1wLGBrIqv0h43k28'))
}

MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY', 'ms-6ab8bbf1-8fbd-4859-9a93-742f4edc5da8')

print("🚀 Petechoes完整应用启动中...")
print(f"🔧 数据库配置: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"🔑 ModelScope API Key: {'✅已设置' if MODELSCOPE_API_KEY else '❌未设置'}")

def get_db_connection_with_retry(max_retries=3, retry_delay=1):
    """带重试逻辑的数据库连接"""
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"数据库连接失败 (第{attempt + 1}次): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e
    return None

def get_db_connection():
    """获取数据库连接"""
    try:
        return get_db_connection_with_retry(max_retries=3, retry_delay=1)
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        return None

def init_database():
    """初始化数据库表"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                original_image BYTEA NOT NULL,
                generated_image BYTEA,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("✅ 数据库表初始化成功")
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    """根路径"""
    return jsonify({
        'name': 'Petechoes Backend',
        'description': '宠物纪念APP后端服务',
        'status': 'running',
        'version': '2.0.0',
        'endpoints': [
            '/health - 健康检查',
            '/upload - 图片上传',
            '/status/<id> - 查询状态',
            '/image/<id> - 获取图片',
            '/test - 测试接口',
            '/test-api - 测试ModelScope API'
        ]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'message': 'Petechoes后端服务器运行正常',
        'version': '2.0.0'
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
        'PORT': os.getenv('PORT', '8080')
    }
    
    return jsonify({
        'message': '测试接口正常',
        'environment': env_info,
        'database_config': {
            'host': DB_CONFIG['host'],
            'port': DB_CONFIG['port'],
            'database': DB_CONFIG['database'],
            'user': DB_CONFIG['user'],
            'password_set': bool(DB_CONFIG['password'])
        }
    })

@app.route('/test-api', methods=['GET'])
def test_modelscope_api():
    """测试ModelScope API"""
    try:
        logger.info("🧪 测试ModelScope API...")
        
        # 使用示例图片测试API  
        headers = {
            'Authorization': 'Bearer ms-6ab8bbf1-8fbd-4859-9a93-742f4edc5da8',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'black-forest-labs/FLUX.1-Kontext-dev',
            'prompt': '把女孩的头发变成蓝色',
            'image_url': "https://resources.modelscope.cn/aigc/image_edit.png"
        }
        
        logger.info(f"🧪 测试payload: {payload}")
        logger.info(f"🧪 API Key: ms-6ab8bbf...")
        
        import json
        response = requests.post(
            MODELSCOPE_API_URL, 
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
            headers=headers,
            timeout=60
        )
        
        logger.info(f"🧪 API测试响应: {response.status_code}")
        logger.info(f"🧪 API测试内容: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'ModelScope API测试成功',
                'response': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'ModelScope API测试失败',
                'status_code': response.status_code,
                'response': response.text
            }), 400
            
    except Exception as e:
        logger.error(f"🧪 API测试异常: {e}")
        return jsonify({
            'success': False,
            'message': f'API测试异常: {str(e)}'
        }), 500

@app.route('/upload', methods=['POST'])
def upload_image():
    """上传图片并触发AI生成"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': '没有找到图片文件'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 读取图片数据
        image_data = file.read()
        logger.info(f"📸 收到图片上传，大小: {len(image_data)} bytes")
        
        # 保存到数据库
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
        
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO images (original_image, status) VALUES (%s, %s) RETURNING id",
            (image_data, 'processing')
        )
        image_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ 图片保存成功，ID: {image_id}")
        
        # 在后台线程中生成新图片
        threading.Thread(target=generate_new_image, args=(image_id,)).start()
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'message': '图片上传成功，正在生成新图片...'
        })
        
    except Exception as e:
        logger.error(f"❌ 上传失败: {e}")
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

def generate_new_image(image_id):
    """使用ModelScope生成新图片"""
    try:
        logger.info(f"🔍 开始处理图片 {image_id}")
        
        # 构建图片的公开URL
        base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
        image_url = f"{base_url}/image/{image_id}?type=original"
        logger.info(f"✅ 构建图片URL: {image_url}")
        
        # 调用ModelScope API（完全按照官方示例）
        headers = {
            'Authorization': 'Bearer ms-6ab8bbf1-8fbd-4859-9a93-742f4edc5da8',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'black-forest-labs/FLUX.1-Kontext-dev',
            'prompt': '根据用户上传的宠物图片，生成宠物坐在椅子上等待被拍照的图片，温馨的宠物纪念风格，温暖的色调，适合作为手机应用背景',
            'image_url': image_url
        }
        
        logger.info(f"🔄 调用ModelScope API...")
        logger.info(f"🌐 API URL: {MODELSCOPE_API_URL}")
        logger.info(f"🔑 API Key: ms-6ab8bbf...")
        logger.info(f"📋 Payload: {payload}")
        
        # 首先测试我们的图片URL是否可以访问
        try:
            test_response = requests.head(image_url, timeout=10)
            logger.info(f"🔍 图片URL测试: {test_response.status_code}, Content-Type: {test_response.headers.get('content-type', 'unknown')}")
        except Exception as e:
            logger.warning(f"⚠️ 图片URL测试失败: {e}")
        
        # 使用正确的请求格式
        import json
        response = requests.post(
            MODELSCOPE_API_URL, 
            data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), 
            headers=headers,
            timeout=60
        )
        
        logger.info(f"📡 API响应状态码: {response.status_code}")
        logger.info(f"📡 API响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"🔍 API返回结构: {list(result.keys())}")
            
            # 使用正确的响应格式
            if 'images' in result and len(result['images']) > 0:
                generated_image_url = result['images'][0]['url']
                logger.info(f"✅ 获得生成图片URL: {generated_image_url}")
                
                # 下载生成的图片
                img_response = requests.get(generated_image_url)
                if img_response.status_code == 200:
                    # 保存生成的图片到数据库
                    conn = get_db_connection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            "UPDATE images SET generated_image = %s, status = %s WHERE id = %s",
                            (img_response.content, 'completed', image_id)
                        )
                        conn.commit()
                        cursor.close()
                        conn.close()
                        logger.info(f"✅ 图片 {image_id} 生成成功")
                    else:
                        logger.error(f"❌ 数据库连接失败，无法保存生成的图片")
                else:
                    logger.error(f"❌ 下载生成图片失败: {img_response.status_code}")
                    update_image_status(image_id, 'failed')
            else:
                logger.error(f"❌ API响应中未找到images字段")
                update_image_status(image_id, 'failed')
        else:
            logger.error(f"❌ ModelScope API调用失败: {response.status_code}, 响应: {response.text}")
            update_image_status(image_id, 'failed')
            
    except Exception as e:
        logger.error(f"❌ 生成图片异常: {e}")
        update_image_status(image_id, 'failed')

def update_image_status(image_id, status):
    """更新图片状态"""
    try:
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE images SET status = %s WHERE id = %s", (status, image_id))
            conn.commit()
            cursor.close()
            conn.close()
    except Exception as e:
        logger.error(f"❌ 更新状态失败: {e}")

@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    """获取图片"""
    try:
        image_type = request.args.get('type', 'generated')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
        
        cursor = conn.cursor()
        
        if image_type == 'original':
            cursor.execute("SELECT original_image FROM images WHERE id = %s", (image_id,))
        else:
            cursor.execute("SELECT generated_image FROM images WHERE id = %s", (image_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result or not result[0]:
            return jsonify({'error': '图片不存在'}), 404
        
        return send_file(
            io.BytesIO(result[0]),
            mimetype='image/jpeg'
        )
        
    except Exception as e:
        logger.error(f"❌ 获取图片失败: {e}")
        return jsonify({'error': f'获取图片失败: {str(e)}'}), 500

@app.route('/status/<int:image_id>', methods=['GET'])
def get_status(image_id):
    """获取图片处理状态"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT status, (generated_image IS NOT NULL) as has_generated_image FROM images WHERE id = %s",
            (image_id,)
        )
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result:
            return jsonify({'error': '图片不存在'}), 404
        
        response_data = {
            'status': result['status'],
            'has_generated_image': result['has_generated_image']
        }
        
        if result['status'] == 'completed' and result['has_generated_image']:
            base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
            response_data['generated_image_url'] = f"{base_url}/image/{image_id}?type=generated"
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ 获取状态失败: {e}")
        return jsonify({'error': f'获取状态失败: {str(e)}'}), 500

# 初始化数据库
if init_database():
    logger.info("✅ 应用初始化成功")
else:
    logger.warning("⚠️ 数据库初始化失败，但应用继续启动")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"🚀 启动完整服务器在端口 {port}")
    app.run(host='0.0.0.0', port=port, debug=False) 