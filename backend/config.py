import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# PostgreSQL数据库配置
# Zeabur会自动设置这些环境变量
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'hkg1.clusters.zeabur.com'),
    'port': os.getenv('POSTGRES_PORT', '30206'),
    'database': os.getenv('POSTGRES_DATABASE', os.getenv('POSTGRES_DB', 'zeabur')),
    'user': os.getenv('POSTGRES_USERNAME', os.getenv('POSTGRES_USER', 'root')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('PASSWORD', ''))
}

# ModelScope API配置
MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY')

# 打印配置信息（用于调试，生产环境中应该移除密码打印）
print("🔧 数据库配置:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  Database: {DB_CONFIG['database']}")
print(f"  User: {DB_CONFIG['user']}")
print(f"  Password: {'***已设置***' if DB_CONFIG['password'] else '❌未设置'}")
print(f"🔑 ModelScope API Key: {'✅已设置' if MODELSCOPE_API_KEY else '❌未设置'}") 