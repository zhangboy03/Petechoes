#!/usr/bin/env python3
"""
上传照相馆背景图片到数据库的脚本
用于将iOS项目中的图片2上传到后端数据库
"""

import requests
import sys
import os

def upload_studio_background(image_path, server_url="https://petecho.zeabur.app"):
    """上传照相馆背景图片"""
    try:
        if not os.path.exists(image_path):
            print(f"❌ 图片文件不存在: {image_path}")
            return False
        
        print(f"📤 正在上传照相馆背景图片: {image_path}")
        print(f"🌐 服务器地址: {server_url}")
        
        with open(image_path, 'rb') as f:
            files = {'image': ('studio_background.jpg', f, 'image/jpeg')}
            
            response = requests.post(
                f"{server_url}/upload-studio-background",
                files=files,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 上传成功: {result['message']}")
            return True
        else:
            print(f"❌ 上传失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 上传异常: {e}")
        return False

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("使用方法: python upload_studio_image.py <图片路径>")
        print("示例: python upload_studio_image.py /path/to/studio_image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    # 可以通过环境变量设置服务器地址
    server_url = os.getenv('SERVER_URL', 'https://petecho.zeabur.app')
    
    print("🚀 照相馆背景图片上传工具")
    print("=" * 40)
    
    success = upload_studio_background(image_path, server_url)
    
    if success:
        print("\n🎉 照相馆背景图片上传完成！")
        print("现在iOS应用可以正常生成宠物纪念照了。")
    else:
        print("\n💥 上传失败，请检查网络连接和服务器状态。")
        sys.exit(1)

if __name__ == "__main__":
    main() 