import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# PostgreSQL数据库配置
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'database': os.getenv('POSTGRES_DATABASE'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('PASSWORD')
}

# ModelScope API配置
MODELSCOPE_API_KEY = os.getenv('MODELSCOPE_API_KEY') 