#!/usr/bin/env python3
"""
数据库连接诊断脚本
用于调试Zeabur PostgreSQL连接问题
"""

import os
import socket
import time
import psycopg2
from config import DB_CONFIG

def test_network_connectivity(host, port):
    """测试网络连通性"""
    print(f"🌐 测试网络连通性: {host}:{port}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ 网络连接正常")
            return True
        else:
            print(f"❌ 网络连接失败，错误代码: {result}")
            return False
    except Exception as e:
        print(f"❌ 网络连接测试异常: {e}")
        return False

def test_postgres_connection():
    """测试PostgreSQL连接"""
    print(f"\n🗄️ 测试PostgreSQL连接")
    print(f"配置信息:")
    print(f"  Host: {DB_CONFIG['host']}")
    print(f"  Port: {DB_CONFIG['port']}")
    print(f"  Database: {DB_CONFIG['database']}")
    print(f"  User: {DB_CONFIG['user']}")
    print(f"  Password: {'已设置' if DB_CONFIG['password'] else '未设置'}")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ PostgreSQL连接成功")
        print(f"📊 版本信息: {version}")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ PostgreSQL操作错误: {e}")
        return False
    except Exception as e:
        print(f"❌ PostgreSQL连接异常: {e}")
        return False

def test_alternative_connections():
    """测试不同的连接配置"""
    print(f"\n🔄 尝试替代连接配置...")
    
    # 尝试不同的环境变量组合
    alternatives = [
        {
            'host': os.getenv('POSTGRES_HOST'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'database': os.getenv('POSTGRES_DATABASE'),
            'user': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD')
        },
        {
            'host': os.getenv('POSTGRES_HOST'),
            'port': int(os.getenv('POSTGRES_PORT', '5432')),
            'database': os.getenv('POSTGRES_DB'),
            'user': os.getenv('POSTGRES_USERNAME'),
            'password': os.getenv('PASSWORD')
        }
    ]
    
    for i, config in enumerate(alternatives):
        if not all(config.values()):
            print(f"⏭️ 配置{i+1}: 缺少必要参数，跳过")
            continue
            
        print(f"🧪 测试配置{i+1}: {config['host']}:{config['port']}")
        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            cursor.close()
            conn.close()
            print(f"✅ 配置{i+1}连接成功！")
            return config
        except Exception as e:
            print(f"❌ 配置{i+1}连接失败: {e}")
    
    return None

def check_environment_variables():
    """检查所有相关环境变量"""
    print(f"\n📋 检查环境变量:")
    
    env_vars = [
        'POSTGRES_HOST', 'POSTGRES_PORT', 'POSTGRES_DATABASE', 'POSTGRES_DB',
        'POSTGRES_USER', 'POSTGRES_USERNAME', 'POSTGRES_PASSWORD', 'PASSWORD',
        'POSTGRES_URI', 'POSTGRES_CONNECTION_STRING'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        status = "✅" if value else "❌"
        print(f"  {status} {var}: {'已设置' if value else '未设置'}")
        if value and len(value) > 50:
            print(f"      值: {value[:50]}...")
        elif value:
            print(f"      值: {value}")

def main():
    """主诊断流程"""
    print("🔍 PostgreSQL数据库连接诊断")
    print("=" * 50)
    
    # 检查环境变量
    check_environment_variables()
    
    # 测试网络连通性
    network_ok = test_network_connectivity(DB_CONFIG['host'], DB_CONFIG['port'])
    
    # 测试PostgreSQL连接
    postgres_ok = test_postgres_connection()
    
    # 如果标准连接失败，尝试替代配置
    if not postgres_ok:
        print("\n🔧 标准配置失败，尝试替代配置...")
        alternative_config = test_alternative_connections()
        if alternative_config:
            print(f"🎉 找到有效配置: {alternative_config}")
    
    print("\n" + "=" * 50)
    print("📊 诊断结果:")
    print(f"  网络连通性: {'✅' if network_ok else '❌'}")
    print(f"  PostgreSQL连接: {'✅' if postgres_ok else '❌'}")
    
    if not postgres_ok:
        print("\n💡 建议的解决方案:")
        print("1. 检查Zeabur中的PostgreSQL服务是否正在运行")
        print("2. 验证数据库环境变量是否正确")
        print("3. 检查数据库服务的网络配置")
        print("4. 等待几分钟后重试（可能是服务启动延迟）")

if __name__ == "__main__":
    main() 