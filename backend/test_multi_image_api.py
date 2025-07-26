#!/usr/bin/env python3
"""
测试多图片API调用的脚本
验证BFL API是否支持多图片字段
"""

import requests
import json
import os
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 直接从环境变量获取API key
BFL_API_KEY = os.getenv('BFL_API_KEY', '7b9e4ba5-8136-4a85-94e6-e1c45fd5d0c0')

def test_multi_image_api():
    """测试多图片API调用"""
    
    # BFL API配置
    BFL_API_URL = 'https://api.bfl.ai/v1/flux-kontext-max'
    
    # 测试用的图片URL
    pet_image_url = "https://resources.modelscope.cn/aigc/image_edit.png"  # 宠物图片
    studio_image_url = "https://petecho.zeabur.app/studio-background"  # 照相馆背景
    
    # 多图片提示词
    prompt = """Create an anime-style pet memorial photo by combining the pet from the first image with the studio setting from the second image.
    
    Task: Place the anime-stylized pet sitting on the wooden chair in the exact same studio environment as shown in the background image.
    
    Requirements:
    - Keep the EXACT same studio layout, lighting, and atmosphere from the background image
    - Transform the pet into cute anime/cartoon style while maintaining its original characteristics  
    - The pet should sit calmly on the wooden chair, looking towards the camera
    - Preserve the warm golden lighting and cozy photography studio atmosphere
    - Maintain the camera, tripod, and all studio elements in their original positions
    - Style: Anime illustration with soft colors and heartwarming mood
    - Output format: 9:20 aspect ratio for mobile app background"""
    
    # 尝试不同的payload配置
    test_configs = [
        {
            "name": "多字段配置",
            "payload": {
                'prompt': prompt,
                'input_image': pet_image_url,
                'background_image': studio_image_url,
                'reference_image': studio_image_url,
                'studio_image': studio_image_url,
                'second_image': studio_image_url,
                'seed': 42,
                'aspect_ratio': '9:20',
                'output_format': 'jpeg',
                'prompt_upsampling': False,
                'safety_tolerance': 2
            }
        },
        {
            "name": "标准单图配置",
            "payload": {
                'prompt': prompt,
                'input_image': pet_image_url,
                'seed': 42,
                'aspect_ratio': '9:20',
                'output_format': 'jpeg',
                'prompt_upsampling': False,
                'safety_tolerance': 2
            }
        }
    ]
    
    headers = {
        'x-key': BFL_API_KEY,
        'Content-Type': 'application/json'
    }
    
    print("🧪 开始测试多图片API调用...")
    print("=" * 60)
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n📋 测试配置 {i}: {config['name']}")
        print(f"🔑 API Key: {BFL_API_KEY[:10]}...")
        print(f"📤 Payload字段: {list(config['payload'].keys())}")
        
        try:
            response = requests.post(
                BFL_API_URL,
                json=config['payload'],
                headers=headers,
                timeout=60
            )
            
            print(f"📡 响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API调用成功!")
                print(f"📋 响应字段: {list(result.keys())}")
                
                if 'id' in result:
                    print(f"🆔 任务ID: {result['id']}")
                if 'polling_url' in result:
                    print(f"🔄 轮询URL: {result['polling_url']}")
                    
            else:
                print(f"❌ API调用失败")
                print(f"📄 错误响应: {response.text[:200]}...")
                
        except Exception as e:
            print(f"💥 请求异常: {e}")
        
        print("-" * 40)
    
    print("\n🎯 测试总结:")
    print("- 如果多字段配置成功，说明API支持多图片输入")
    print("- 如果只有标准配置成功，说明API只支持单图片")
    print("- 检查日志中的响应内容了解具体支持情况")

if __name__ == "__main__":
    if not BFL_API_KEY:
        print("❌ 请设置BFL_API_KEY环境变量")
        exit(1)
    
    test_multi_image_api() 