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

# Black Forest Lab API配置
BFL_API_URL = 'https://api.bfl.ai/v1/flux-kontext-max'

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'hkg1.clusters.zeabur.com'),
    'port': int(os.getenv('POSTGRES_PORT', '30177')),
    'database': os.getenv('POSTGRES_DATABASE', os.getenv('POSTGRES_DB', 'zeabur')),
    'user': os.getenv('POSTGRES_USERNAME', os.getenv('POSTGRES_USER', 'root')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('PASSWORD', 'laKs69d7AVXmTJ5H1wLGBrIqv0h43k28'))
}

BFL_API_KEY = os.getenv('BFL_API_KEY', '7b9e4ba5-8136-4a85-94e6-e1c45fd5d0c0')

print("🚀 Petechoes完整应用启动中...")
print(f"🔧 数据库配置: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
print(f"🔑 BFL API Key: {'✅已设置' if BFL_API_KEY else '❌未设置'}")

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
        
        # 创建照相馆背景图片表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS studio_backgrounds (
                id SERIAL PRIMARY KEY,
                image_data BYTEA NOT NULL,
                is_active BOOLEAN DEFAULT true,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 检查是否已有背景图片
        cursor.execute("SELECT COUNT(*) FROM studio_backgrounds WHERE is_active = true")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 如果没有背景图片，插入默认的图片2（需要从项目中读取）
            logger.info("📸 正在初始化照相馆背景图片...")
            init_studio_background(cursor)
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("✅ 数据库表初始化成功")
        return True
        
    except Exception as e:
        logger.error(f"❌ 数据库初始化失败: {e}")
        return False

def init_studio_background(cursor):
    """初始化照相馆背景图片"""
    try:
        # 这里需要读取项目中的图片2并插入数据库
        # 由于这是后端代码，我们需要从iOS项目的Assets中获取图片
        # 暂时先插入一个占位符，实际部署时需要手动上传图片2
        
        # 创建一个小的占位图片
        from PIL import Image as PILImage
        import io
        
        # 创建一个402x874的占位图片
        placeholder = PILImage.new('RGB', (402, 874), color='#F5DEB3')  # 浅黄色背景
        
        # 将图片转换为字节
        img_byte_arr = io.BytesIO()
        placeholder.save(img_byte_arr, format='JPEG', quality=90)
        img_byte_arr = img_byte_arr.getvalue()
        
        cursor.execute(
            "INSERT INTO studio_backgrounds (image_data, is_active) VALUES (%s, %s)",
            (img_byte_arr, True)
        )
        
        logger.info("📸 已插入占位符背景图片，请通过管理接口上传实际的图片2")
        
    except Exception as e:
        logger.error(f"❌ 初始化背景图片失败: {e}")

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
            '/upload-studio-background - 上传照相馆背景图片',
            '/upload-memory-photo - 上传记忆照片',
            '/studio-background - 获取照相馆背景图片',
            '/status/<id> - 查询状态',
            '/image/<id> - 获取图片',
            '/test - 测试接口',
            '/test-api - 测试BFL API'
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
        'BFL_API_KEY': 'Set' if os.getenv('BFL_API_KEY') else 'Not set',
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
def test_bfl_api():
    """测试Black Forest Lab API"""
    try:
        logger.info("🧪 测试BFL API...")
        
        # 使用BFL API格式
        headers = {
            'x-key': BFL_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': 'ein fantastisches bild',
            'input_image': 'https://resources.modelscope.cn/aigc/image_edit.png',
            'seed': 42,
            'aspect_ratio': '1:1',
            'output_format': 'jpeg',
            'prompt_upsampling': False,
            'safety_tolerance': 2
        }
        
        logger.info(f"🧪 测试payload: {payload}")
        logger.info(f"🧪 API Key: {BFL_API_KEY[:10]}...")
        
        response = requests.post(
            BFL_API_URL, 
            json=payload, 
            headers=headers,
            timeout=60
        )
        
        logger.info(f"🧪 API测试响应: {response.status_code}")
        logger.info(f"🧪 API测试内容: {response.text}")
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'BFL API测试成功',
                'response': response.json()
            })
        else:
            return jsonify({
                'success': False,
                'message': 'BFL API测试失败',
                'status_code': response.status_code,
                'response': response.text
            }), response.status_code
            
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

@app.route('/upload-studio-background', methods=['POST'])
def upload_studio_background():
    """上传照相馆背景图片（管理员接口）"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': '没有找到图片文件'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        # 读取图片数据
        image_data = file.read()
        logger.info(f"🖼️ 收到照相馆背景图片上传，大小: {len(image_data)} bytes")
        
        # 保存到数据库
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
        
        cursor = conn.cursor()
        
        # 先将所有背景图片设为非活跃状态
        cursor.execute("UPDATE studio_backgrounds SET is_active = false")
        
        # 插入新的背景图片
        cursor.execute(
            "INSERT INTO studio_backgrounds (image_data, is_active) VALUES (%s, %s)",
            (image_data, True)
        )
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info(f"✅ 照相馆背景图片上传成功")
        
        return jsonify({
            'success': True,
            'message': '照相馆背景图片上传成功'
        })
        
    except Exception as e:
        logger.error(f"❌ 背景图片上传失败: {e}")
        return jsonify({'error': f'背景图片上传失败: {str(e)}'}), 500

@app.route('/upload-memory-photo', methods=['POST'])
def upload_memory_photo():
    """上传记忆照片并进行AI风格化处理"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': '没有找到图片文件'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        photo_index = request.form.get('photo_index', '0')
        
        # 读取图片数据
        image_data = file.read()
        logger.info(f"📸 收到记忆照片上传，索引: {photo_index}，大小: {len(image_data)} bytes")
        
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
        
        logger.info(f"✅ 记忆照片保存成功，ID: {image_id}")
        
        # 在后台线程中进行AI风格化处理
        threading.Thread(target=stylize_memory_photo, args=(image_id, int(photo_index))).start()
        
        return jsonify({
            'success': True,
            'image_id': image_id,
            'message': '记忆照片上传成功，正在进行风格化处理...'
        })
        
    except Exception as e:
        logger.error(f"❌ 记忆照片上传失败: {e}")
        return jsonify({'error': f'记忆照片上传失败: {str(e)}'}), 500

def stylize_memory_photo(image_id, photo_index):
    """对记忆照片进行AI风格化处理"""
    try:
        logger.info(f"🎨 开始风格化记忆照片 {image_id} (索引: {photo_index})")
        
        # 构建用户图片的公开URL
        base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
        user_image_url = f"{base_url}/image/{image_id}?type=original"
        
        logger.info(f"✅ 构建记忆照片URL: {user_image_url}")
        
        # 记忆照片风格化提示词
        prompt = """Transform this photo into a warm, anime-style illustration with the same cozy atmosphere as a pet photography studio.

Requirements:
- Convert to soft anime/cartoon art style
- Maintain warm golden lighting and gentle atmosphere
- Keep all objects and details recognizable but stylized
- Use soft pastels and warm colors
- Create a heartwarming, memorial-like mood
- Style should match pet photography studio ambiance
- Output format: suitable for mobile app display

将这张照片转换成温馨的动漫风格插画，保持与宠物照相馆相同的舒适氛围。
使用柔和的动漫风格，温暖的色调，营造治愈系的纪念氛围。"""

        # 调用BFL API进行风格化
        headers = {
            'x-key': BFL_API_KEY,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'prompt': prompt,
            'input_image': user_image_url,
            'seed': 42,
            'aspect_ratio': '1:1',  # 记忆照片使用1:1比例
            'output_format': 'jpeg',
            'prompt_upsampling': False,
            'safety_tolerance': 2
        }
        
        logger.info(f"🎨 调用BFL API风格化记忆照片...")
        logger.info(f"📋 记忆照片索引: {photo_index}")
        
        response = requests.post(BFL_API_URL, json=payload, headers=headers, timeout=60)
        logger.info(f"📡 BFL API响应: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"✅ 记忆照片风格化任务提交成功")
            
            if 'id' in result:
                # 轮询结果
                polling_url = result.get('polling_url')
                if polling_url:
                    poll_memory_photo_result(image_id, polling_url, photo_index)
                else:
                    logger.error(f"❌ 未获得轮询URL")
                    update_image_status(image_id, 'failed')
            else:
                logger.error(f"❌ 未获得任务ID")
                update_image_status(image_id, 'failed')
        else:
            logger.error(f"❌ BFL API调用失败: {response.status_code}")
            update_image_status(image_id, 'failed')
            
    except Exception as e:
        logger.error(f"❌ 记忆照片风格化异常: {e}")
        update_image_status(image_id, 'failed')

def poll_memory_photo_result(image_id, polling_url, photo_index):
    """轮询记忆照片处理结果"""
    max_attempts = 60
    attempts = 0
    
    while attempts < max_attempts:
        attempts += 1
        
        try:
            response = requests.get(polling_url, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', 'unknown')
                
                logger.info(f"📊 记忆照片 {photo_index} 状态检查 {attempts}: {status}")
                
                if status == 'Ready' and 'sample' in result:
                    generated_image_url = result['sample']
                    logger.info(f"✅ 记忆照片 {photo_index} 风格化完成: {generated_image_url}")
                    
                    # 下载并保存风格化后的图片
                    img_response = requests.get(generated_image_url)
                    if img_response.status_code == 200:
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
                            logger.info(f"✅ 记忆照片 {photo_index} 风格化完成并保存")
                            return
                    
                elif status == 'failed':
                    logger.error(f"❌ 记忆照片 {photo_index} 风格化失败")
                    update_image_status(image_id, 'failed')
                    return
                    
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"❌ 轮询记忆照片 {photo_index} 失败: {e}")
            time.sleep(5)
    
    # 超时
    logger.error(f"⏰ 记忆照片 {photo_index} 风格化超时")
    update_image_status(image_id, 'failed')

def generate_new_image(image_id):
    """使用Black Forest Lab生成新图片"""
    try:
        logger.info(f"🔍 开始处理图片 {image_id}")
        
        # 构建用户上传图片的公开URL
        base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
        user_image_url = f"{base_url}/image/{image_id}?type=original"
        
        # 构建照相馆背景图片的公开URL
        studio_background_url = f"{base_url}/studio-background"
        
        logger.info(f"✅ 构建用户图片URL: {user_image_url}")
        logger.info(f"✅ 构建照相馆背景URL: {studio_background_url}")
        logger.info(f"🎨 将在payload中同时传递两张图片")
        
        # 调用BFL API
        headers = {
            'x-key': BFL_API_KEY,
            'Content-Type': 'application/json'
        }
        
        # 强调沿用照相馆风格的提示词
        prompt = """Create an anime-style pet memorial photo by combining the pet from the first image with the studio setting from the second image.
        
        Task: Place the anime-stylized pet sitting on the wooden chair in the exact same studio environment as shown in the background image.
        
        Requirements:
        - Keep the EXACT same studio layout, lighting, and atmosphere from the background image
        - Transform the pet into cute anime/cartoon style while maintaining its original characteristics  
        - The pet should sit calmly on the wooden chair, looking towards the camera
        - Preserve the warm golden lighting and cozy photography studio atmosphere
        - Maintain the camera, tripod, and all studio elements in their original positions
        - Style: Anime illustration with soft colors and heartwarming mood
        - Output format: 9:20 aspect ratio for mobile app background
        
        请将第一张图片中的宠物与第二张图片中的照相馆场景结合，创造温馨的动漫风格纪念照。
        保持照相馆的原有风格和布局，让动漫化的宠物自然地坐在椅子上等待拍照。
        沿用照相馆的温暖色调、灯光效果和整体氛围。"""
        
        payload = {
            'prompt': prompt,
            'input_image': user_image_url,  # 用户的宠物照片
            'background_image': studio_background_url,  # 照相馆背景图片
            'reference_image': studio_background_url,  # 尝试不同的字段名
            'studio_image': studio_background_url,  # 再尝试一个字段名
            'second_image': studio_background_url,  # 第二张图片
            'seed': 42,
            'aspect_ratio': '9:20',  # 接近402*874的比例，适合iPhone16Pro
            'output_format': 'jpeg',
            'prompt_upsampling': False,
            'safety_tolerance': 2
        }
        
        logger.info(f"🔄 调用BFL API...")
        logger.info(f"🌐 API URL: {BFL_API_URL}")
        logger.info(f"🔑 API Key: {BFL_API_KEY[:10]}...")
        logger.info(f"🎯 尝试多图片输入:")
        logger.info(f"   - 宠物图片: {user_image_url}")
        logger.info(f"   - 照相馆背景: {studio_background_url}")
        logger.info(f"📋 Payload字段: {list(payload.keys())}")
        logger.info(f"📝 提示词长度: {len(prompt)} 字符")
        
        # 首先测试我们的图片URL是否可以访问
        try:
            test_response = requests.head(user_image_url, timeout=10)
            logger.info(f"🔍 用户图片URL测试: {test_response.status_code}, Content-Type: {test_response.headers.get('content-type', 'unknown')}")
            
            studio_test_response = requests.head(studio_background_url, timeout=10)
            logger.info(f"🔍 照相馆背景URL测试: {studio_test_response.status_code}, Content-Type: {studio_test_response.headers.get('content-type', 'unknown')}")
        except Exception as e:
            logger.warning(f"⚠️ 图片URL测试失败: {e}")
        
        # 使用BFL API格式
        response = requests.post(
            BFL_API_URL, 
            json=payload, 
            headers=headers,
            timeout=60
        )
        
        logger.info(f"📡 API响应状态码: {response.status_code}")
        logger.info(f"📡 API响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"🔍 API返回结构: {list(result.keys())}")
            
            # BFL API响应格式可能不同，需要根据实际响应调整
            if 'id' in result:
                # BFL API返回任务ID，需要轮询结果
                task_id = result['id']
                polling_url = result.get('polling_url')
                logger.info(f"✅ 获得任务ID: {task_id}")
                logger.info(f"✅ 轮询URL: {polling_url}")
                
                # 开始轮询结果
                threading.Thread(target=poll_bfl_result, args=(image_id, task_id, polling_url)).start()
                logger.info(f"🔄 开始轮询任务结果，ID: {task_id}")
                
            elif 'url' in result:
                # 如果直接返回图片URL
                generated_image_url = result['url']
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
                logger.error(f"❌ API响应格式未知: {result}")
                update_image_status(image_id, 'failed')
        else:
            logger.error(f"❌ BFL API调用失败: {response.status_code}, 响应: {response.text}")
            update_image_status(image_id, 'failed')
            
    except Exception as e:
        logger.error(f"❌ 生成图片异常: {e}")
        update_image_status(image_id, 'failed')

def poll_bfl_result(image_id, task_id, polling_url):
    """轮询BFL API结果"""
    try:
        logger.info(f"🔄 开始轮询任务 {task_id} 的结果...")
        
        max_attempts = 60  # 最多轮询5分钟（60次 * 5秒）
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            logger.info(f"🔄 轮询第 {attempt} 次...")
            
            try:
                # 使用轮询URL获取结果
                headers = {
                    'x-key': BFL_API_KEY,
                    'Content-Type': 'application/json'
                }
                
                response = requests.get(polling_url, headers=headers, timeout=30)
                logger.info(f"📡 轮询响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 显示完整的BFL图片URL（如果存在）
                    if 'result' in result and 'sample' in result['result']:
                        bfl_image_url = result['result']['sample']
                        logger.info(f"🖼️ BFL完整图片URL: {bfl_image_url}")
                    
                    logger.info(f"📡 轮询响应摘要: 状态={result.get('status', 'unknown')}, 包含结果={bool(result.get('result'))}")
                    
                    # 检查任务状态
                    if 'status' in result:
                        status = result['status']
                        logger.info(f"📊 任务状态: {status}")
                        
                        if status == 'completed' or status == 'Ready':
                            # 任务完成，获取结果
                            if 'result' in result and 'sample' in result['result']:
                                generated_image_url = result['result']['sample']
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
                                        
                                        # 显示我们的简短URL
                                        base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
                                        our_image_url = f"{base_url}/image/{image_id}?type=generated"
                                        logger.info(f"✅ 图片 {image_id} 生成成功")
                                        logger.info(f"🔗 简短访问URL: {our_image_url}")
                                        logger.info(f"📱 iOS应用将使用此URL显示生成的图片")
                                        return  # 成功完成，退出轮询
                                    else:
                                        logger.error(f"❌ 数据库连接失败，无法保存生成的图片")
                                        update_image_status(image_id, 'failed')
                                        return
                                else:
                                    logger.error(f"❌ 下载生成图片失败: {img_response.status_code}")
                                    update_image_status(image_id, 'failed')
                                    return
                            else:
                                logger.error(f"❌ 任务完成但未找到结果URL: {result}")
                                update_image_status(image_id, 'failed')
                                return
                                
                        elif status == 'failed':
                            logger.error(f"❌ BFL任务失败: {result}")
                            update_image_status(image_id, 'failed')
                            return
                        elif status in ['pending', 'running', 'processing']:
                            logger.info(f"⏳ 任务进行中: {status}")
                            # 继续轮询
                        else:
                            logger.warning(f"⚠️ 未知任务状态: {status}，继续轮询...")
                    else:
                        # 旧格式响应，检查是否直接包含结果
                        if 'url' in result:
                            generated_image_url = result['url']
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
                                    
                                    # 显示我们的简短URL
                                    base_url = os.getenv('PUBLIC_URL', 'https://petecho.zeabur.app')
                                    our_image_url = f"{base_url}/image/{image_id}?type=generated"
                                    logger.info(f"✅ 图片 {image_id} 生成成功")
                                    logger.info(f"🔗 简短访问URL: {our_image_url}")
                                    logger.info(f"📱 iOS应用将使用此URL显示生成的图片")
                                    return  # 成功完成，退出轮询
                                else:
                                    logger.error(f"❌ 数据库连接失败，无法保存生成的图片")
                                    update_image_status(image_id, 'failed')
                                    return
                            else:
                                logger.error(f"❌ 下载生成图片失败: {img_response.status_code}")
                                update_image_status(image_id, 'failed')
                                return
                        else:
                            logger.info(f"⏳ 任务仍在处理中，等待下次轮询...")
                            
                elif response.status_code == 404:
                    logger.warning(f"⚠️ 任务未找到，可能已过期: {task_id}")
                    update_image_status(image_id, 'failed')
                    return
                else:
                    logger.warning(f"⚠️ 轮询响应异常: {response.status_code}")
                    logger.info(f"📡 错误响应内容: {response.text[:200]}...")
                    
            except Exception as e:
                logger.warning(f"⚠️ 轮询请求异常: {e}")
            
            # 等待5秒后继续轮询
            time.sleep(5)
        
        # 轮询超时
        logger.error(f"❌ 轮询超时，任务 {task_id} 未完成")
        update_image_status(image_id, 'failed')
        
    except Exception as e:
        logger.error(f"❌ 轮询异常: {e}")
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

@app.route('/studio-background', methods=['GET'])
def get_studio_background():
    """获取照相馆背景图片（图片2）"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': '数据库连接失败'}), 500
        
        cursor = conn.cursor()
        # 从数据库获取照相馆背景图片
        cursor.execute("SELECT image_data FROM studio_backgrounds WHERE is_active = true LIMIT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not result or not result[0]:
            # 如果数据库中没有背景图片，返回错误
            return jsonify({'error': '照相馆背景图片不存在，请先上传'}), 404
        
        return send_file(
            io.BytesIO(result[0]),
            mimetype='image/jpeg'
        )
        
    except Exception as e:
        logger.error(f"❌ 获取照相馆背景失败: {e}")
        return jsonify({'error': f'获取照相馆背景失败: {str(e)}'}), 500

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