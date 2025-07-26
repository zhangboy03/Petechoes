#!/usr/bin/env python3
"""
Zeabur部署配置检查脚本
用于验证所有必要的环境变量和服务是否正确配置
"""

import os
import psycopg2
import requests
from config import DB_CONFIG, MODELSCOPE_API_KEY

def check_environment_variables():
    """检查环境变量配置"""
    print("🔍 检查环境变量...")
    
    required_vars = {
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'POSTGRES_PORT': os.getenv('POSTGRES_PORT'), 
        'POSTGRES_DATABASE': os.getenv('POSTGRES_DATABASE') or os.getenv('POSTGRES_DB'),
        'POSTGRES_USER': os.getenv('POSTGRES_USERNAME') or os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD') or os.getenv('PASSWORD'),
        'MODELSCOPE_API_KEY': MODELSCOPE_API_KEY,
        'PUBLIC_URL': os.getenv('PUBLIC_URL'),
        'PORT': os.getenv('PORT')
    }
    
    all_good = True
    for var_name, var_value in required_vars.items():
        status = "✅" if var_value else "❌"
        print(f"  {status} {var_name}: {'已设置' if var_value else '未设置'}")
        if not var_value and var_name in ['POSTGRES_HOST', 'POSTGRES_PASSWORD', 'MODELSCOPE_API_KEY']:
            all_good = False
    
    return all_good

def check_database_connection():
    """检查数据库连接"""
    print("\n🗄️ 检查数据库连接...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"  ✅ 数据库连接成功")
        print(f"  📊 PostgreSQL版本: {version}")
        return True
        
    except Exception as e:
        print(f"  ❌ 数据库连接失败: {e}")
        return False

def check_modelscope_api():
    """检查ModelScope API配置"""
    print("\n🤖 检查ModelScope API...")
    
    if not MODELSCOPE_API_KEY:
        print("  ❌ ModelScope API密钥未设置")
        return False
    
    # 这里可以添加实际的API测试，但为了避免不必要的API调用，我们只检查密钥格式
    if len(MODELSCOPE_API_KEY) > 10:  # 简单的长度检查
        print("  ✅ ModelScope API密钥已设置")
        return True
    else:
        print("  ❌ ModelScope API密钥格式可能不正确")
        return False

def initialize_database_tables():
    """初始化数据库表"""
    print("\n📋 初始化数据库表...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
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
        
        print("  ✅ 数据库表创建成功")
        return True
        
    except Exception as e:
        print(f"  ❌ 数据库表创建失败: {e}")
        return False

def main():
    """主检查流程"""
    print("🚀 Petechoes Zeabur部署配置检查")
    print("=" * 50)
    
    # 检查环境变量
    env_ok = check_environment_variables()
    
    # 检查数据库连接
    db_ok = check_database_connection()
    
    # 初始化数据库表
    if db_ok:
        table_ok = initialize_database_tables()
    else:
        table_ok = False
    
    # 检查ModelScope API
    api_ok = check_modelscope_api()
    
    print("\n" + "=" * 50)
    print("📊 检查结果汇总:")
    print(f"  环境变量: {'✅' if env_ok else '❌'}")
    print(f"  数据库连接: {'✅' if db_ok else '❌'}")
    print(f"  数据库表: {'✅' if table_ok else '❌'}")
    print(f"  ModelScope API: {'✅' if api_ok else '❌'}")
    
    if all([env_ok, db_ok, table_ok, api_ok]):
        print("\n🎉 所有检查通过！部署配置正确。")
        return True
    else:
        print("\n⚠️ 有些配置需要修复，请检查上述错误。")
        return False

if __name__ == "__main__":
    main() 