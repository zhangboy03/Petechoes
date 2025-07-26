#!/usr/bin/env python3
"""
后端服务器测试脚本
用于验证API接口和数据库连接
"""

import requests
import json
import os
import sys
from config import DB_CONFIG
import psycopg2

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"✅ 数据库连接成功: {version[0]}")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def test_health_endpoint(base_url="http://localhost:5001"):
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查成功: {data}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_image_upload(base_url="http://localhost:5001"):
    """测试图片上传接口（需要服务器运行）"""
    print("🔍 测试图片上传接口...")
    
    # 创建一个测试图片数据
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    
    try:
        files = {'image': ('test.png', test_image_data, 'image/png')}
        response = requests.post(f"{base_url}/upload", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 图片上传成功: {data}")
            return data.get('image_id')
        else:
            print(f"❌ 图片上传失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 图片上传异常: {e}")
        return None

def test_image_status(image_id, base_url="http://localhost:5001"):
    """测试图片状态查询接口"""
    if not image_id:
        print("⚠️ 跳过状态查询测试：没有有效的图片ID")
        return False
        
    print(f"🔍 测试图片状态查询接口 (ID: {image_id})...")
    try:
        response = requests.get(f"{base_url}/status/{image_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 状态查询成功: {data}")
            return True
        else:
            print(f"❌ 状态查询失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 状态查询异常: {e}")
        return False

def test_environment_variables():
    """测试环境变量配置"""
    print("🔍 测试环境变量配置...")
    
    required_vars = [
        'POSTGRES_HOST',
        'POSTGRES_PORT', 
        'POSTGRES_DATABASE',
        'POSTGRES_USER',
        'PASSWORD',
        'MODELSCOPE_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少环境变量: {missing_vars}")
        return False
    else:
        print("✅ 所有必需的环境变量都已设置")
        return True

def main():
    """运行所有测试"""
    print("🚀 开始后端服务器测试...")
    print("=" * 50)
    
    results = []
    
    # 测试环境变量
    results.append(("环境变量配置", test_environment_variables()))
    
    # 测试数据库连接
    results.append(("数据库连接", test_database_connection()))
    
    # 测试API接口（需要服务器运行）
    server_url = os.getenv('PUBLIC_URL', 'http://localhost:5001')
    print(f"📡 使用服务器地址: {server_url}")
    
    results.append(("健康检查接口", test_health_endpoint(server_url)))
    
    # 测试图片上传
    image_id = test_image_upload(server_url)
    results.append(("图片上传接口", image_id is not None))
    
    # 测试状态查询
    results.append(("状态查询接口", test_image_status(image_id, server_url)))
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！后端服务器运行正常。")
        sys.exit(0)
    else:
        print("⚠️ 部分测试失败，请检查配置。")
        sys.exit(1)

if __name__ == '__main__':
    main() 