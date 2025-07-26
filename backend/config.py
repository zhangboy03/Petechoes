import os
import time
import psycopg2
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# PostgreSQL数据库配置
# Zeabur会自动设置这些环境变量
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'hkg1.clusters.zeabur.com'),
    'port': int(os.getenv('POSTGRES_PORT', '30177')),  # 更新为新端口
    'database': os.getenv('POSTGRES_DATABASE', os.getenv('POSTGRES_DB', 'zeabur')),
    'user': os.getenv('POSTGRES_USERNAME', os.getenv('POSTGRES_USER', 'root')),
    'password': os.getenv('POSTGRES_PASSWORD', os.getenv('PASSWORD', 'laKs69d7AVXmTJ5H1wLGBrIqv0h43k28'))
}

# ModelScope API配置
MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY')

def get_db_connection_with_retry(max_retries=5, retry_delay=2):
    """
    带重试逻辑的数据库连接
    """
    for attempt in range(max_retries):
        try:
            print(f"🔄 尝试连接数据库 (第{attempt + 1}次/共{max_retries}次)...")
            print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
            print(f"   Database: {DB_CONFIG['database']}")
            print(f"   User: {DB_CONFIG['user']}")
            
            conn = psycopg2.connect(**DB_CONFIG)
            print("✅ 数据库连接成功！")
            return conn
            
        except psycopg2.OperationalError as e:
            print(f"❌ 数据库连接失败 (第{attempt + 1}次): {e}")
            if attempt < max_retries - 1:
                print(f"⏰ {retry_delay}秒后重试...")
                time.sleep(retry_delay)
            else:
                print("🚫 已达到最大重试次数，连接失败")
                raise e
        except Exception as e:
            print(f"❌ 其他数据库错误: {e}")
            raise e
    
    return None

# 打印配置信息（用于调试，生产环境中应该移除密码打印）
print("🔧 数据库配置:")
print(f"  Host: {DB_CONFIG['host']}")
print(f"  Port: {DB_CONFIG['port']}")
print(f"  Database: {DB_CONFIG['database']}")
print(f"  User: {DB_CONFIG['user']}")
print(f"  Password: {'***已设置***' if DB_CONFIG['password'] else '❌未设置'}")
print(f"🔑 ModelScope API Key: {'✅已设置' if MODELSCOPE_API_KEY else '❌未设置'}")

# 启动时测试数据库连接
print("\n🚀 启动时测试数据库连接...")
try:
    test_conn = get_db_connection_with_retry(max_retries=3, retry_delay=1)
    if test_conn:
        test_conn.close()
        print("✅ 数据库启动连接测试成功")
except Exception as e:
    print(f"⚠️ 数据库启动连接测试失败: {e}")
    print("📝 应用将继续启动，但数据库功能可能不可用") 