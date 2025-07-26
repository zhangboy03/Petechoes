#!/usr/bin/env python3
"""
启动PostgreSQL服务器的脚本
适用于Zeabur部署环境
"""

import os
import sys
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_environment_variables():
    """检查必需的环境变量"""
    required_vars = [
        'POSTGRES_HOST',
        'POSTGRES_PORT', 
        'POSTGRES_DATABASE',
        'POSTGRES_USER',
        'PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ 缺少必需的环境变量: {missing_vars}")
        logger.error("请在Zeabur控制台中设置这些环境变量")
        return False
    
    logger.info("✅ 所有必需的环境变量都已设置")
    return True

def main():
    """主函数"""
    logger.info("🚀 启动Petechoes后端服务器...")
    
    # 检查环境变量
    if not check_environment_variables():
        logger.error("❌ 环境变量检查失败，退出")
        sys.exit(1)
    
    # 显示环境信息
    logger.info(f"📊 数据库主机: {os.getenv('POSTGRES_HOST')}")
    logger.info(f"🔌 数据库端口: {os.getenv('POSTGRES_PORT')}")
    logger.info(f"📁 数据库名称: {os.getenv('POSTGRES_DATABASE')}")
    logger.info(f"🌐 公网URL: {os.getenv('PUBLIC_URL', 'http://localhost:5001')}")
    
    try:
        # 导入应用模块
        from postgres_server import app, init_database
        
        # 初始化数据库
        logger.info("📂 正在初始化数据库...")
        if init_database():
            logger.info("✅ 数据库初始化成功")
        else:
            logger.warning("⚠️ 数据库初始化失败，但继续启动服务器")
        
        # 获取端口
        port = int(os.getenv('PORT', 5001))
        logger.info(f"🌐 服务器将在端口 {port} 启动")
        
        # 启动Flask应用
        app.run(host='0.0.0.0', port=port, debug=False)
        
    except ImportError as e:
        logger.error(f"❌ 导入模块失败: {e}")
        logger.error("请确保所有依赖都已正确安装")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 启动服务器失败: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 