from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import requests
from PIL import Image
import io
import threading
from config import DB_CONFIG, MODELSCOPE_API_KEY

app = Flask(__name__)
CORS(app)

# ModelScope API配置
MODELSCOPE_API_URL = 'https://api.modelscope.cn/v1/models/black-forest-labs/FLUX.1-Kontext-dev/inference'

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def init_database():
    """初始化数据库表"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # 创建图片表
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
        
        print("✅ 数据库表初始化成功")
        return True
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

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
        
        # 在后台线程中生成新图片
        threading.Thread(target=generate_new_image, args=(image_id,)).start()
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'message': '图片上传成功，正在生成新图片...'
        })
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        return jsonify({'error': f'上传失败: {str(e)}'}), 500

def generate_new_image(image_id):
    """使用ModelScope生成新图片"""
    try:
        print(f"🔍 开始处理图片 {image_id}")
        
        # 构建图片的公开URL
        base_url = os.getenv('PUBLIC_URL', 'http://localhost:5001')
        image_url = f"{base_url}/image/{image_id}?type=original"
        print(f"✅ 构建图片URL: {image_url}")
        
        # 调用ModelScope API
        headers = {
            'Authorization': f'Bearer {MODELSCOPE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'black-forest-labs/FLUX.1-Kontext-dev',
            'prompt': '根据用户上传的宠物图片，生成宠物坐在椅子上等待被拍照的图片，温馨的宠物纪念风格，温暖的色调，适合作为手机应用背景',
            'image_url': image_url
        }
        
        print(f"🔄 调用ModelScope API...")
        print(f"URL: {MODELSCOPE_API_URL}")
        print(f"Headers: {headers}")
        print(f"Payload keys: {list(payload.keys())}")
        
        response = requests.post(MODELSCOPE_API_URL, json=payload, headers=headers)
        
        print(f"📡 API响应状态码: {response.status_code}")
        print(f"📡 API响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            generated_image_url = result.get('output', {}).get('generated_image_url')
            
            if generated_image_url:
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
                        print(f"✅ 图片 {image_id} 生成成功")
                    else:
                        print(f"❌ 数据库连接失败，无法保存生成的图片")
                else:
                    print(f"❌ 下载生成图片失败: {img_response.status_code}")
                    update_image_status(image_id, 'failed')
            else:
                print(f"❌ 未收到生成图片URL")
                update_image_status(image_id, 'failed')
        else:
            print(f"❌ ModelScope API调用失败: {response.status_code}")
            update_image_status(image_id, 'failed')
            
    except Exception as e:
        print(f"❌ 生成图片异常: {e}")
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
        print(f"❌ 更新状态失败: {e}")

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
        print(f"❌ 获取图片失败: {e}")
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
            base_url = os.getenv('PUBLIC_URL', 'http://localhost:5001')
            response_data['generated_image_url'] = f"{base_url}/image/{image_id}?type=generated"
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ 获取状态失败: {e}")
        return jsonify({'error': f'获取状态失败: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def home():
    """根路径"""
    return jsonify({
        'name': 'Petechoes Backend',
        'description': '宠物纪念APP后端服务',
        'status': 'running',
        'version': '1.0.0',
        'endpoints': [
            '/health - 健康检查',
            '/upload - 图片上传',
            '/status/<id> - 查询状态', 
            '/image/<id> - 获取图片',
            '/test - 测试接口'
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

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'healthy', 'message': 'PostgreSQL服务器运行正常'})

if __name__ == '__main__':
    if init_database():
        print("🌐 PostgreSQL服务器启动在 http://localhost:5001")
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        print("❌ 数据库初始化失败") 