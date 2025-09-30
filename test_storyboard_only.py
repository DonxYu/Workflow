#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅测试分镜头生成功能
不需要豆包Seedance API，只需要LLM API
"""

import asyncio
import json
import logging
import os
from video_generator import StoryboardGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_storyboard_generation():
    """测试分镜头生成功能"""
    try:
        # 从环境变量或直接设置LLM配置
        llm_api_key = os.getenv('LLM_API_KEY', 'sk-your_deepseek_api_key_here')
        llm_base_url = os.getenv('LLM_BASE_URL', 'https://api.deepseek.com')
        
        if llm_api_key == 'sk-your_deepseek_api_key_here':
            print("⚠️  请设置LLM_API_KEY环境变量")
            print("方法1: 在终端中运行: export LLM_API_KEY=your_actual_api_key")
            print("方法2: 创建.env文件并设置LLM_API_KEY")
            return
        
        # 创建分镜头生成器
        storyboard_generator = StoryboardGenerator(llm_api_key, llm_base_url)
        
        # 测试内容
        test_content = """
小红书标题：职场真相：为什么聪明人都在"装傻"？

正文内容：

你有没有发现，职场里那些真正厉害的人，往往看起来"不太聪明"？

他们不会在会议上抢着发言，不会炫耀自己的成就，甚至有时候会"装傻"问一些基础问题。

但奇怪的是，这些人往往升职最快，人缘最好，资源最多。

为什么？

1️⃣ 真正的聪明人懂得"示弱"

在《道德经》里有一句话："大智若愚，大巧若拙。"

真正的高手，从来不会让自己显得过于聪明。因为他们知道，过度的聪明会带来嫉妒、防备和孤立。

而适当的"示弱"，反而能获得更多的帮助和支持。

2️⃣ 装傻是一种高级的社交智慧

当你表现得"不太懂"的时候，别人会更愿意教你、帮你、分享资源给你。

这就是心理学上的"互惠原理"——人们更愿意帮助那些看起来需要帮助的人。

3️⃣ 真正的智慧在于"藏拙"

《易经》说："君子藏器于身，待时而动。"

真正的高手，不是没有能力，而是知道什么时候该展现，什么时候该隐藏。

他们会在关键时刻一鸣惊人，而不是在平时就锋芒毕露。

所以，下次当你觉得自己很聪明的时候，不妨问问自己：我是不是太急于证明自己了？

真正的智慧，往往藏在"不争"之中。

Hashtags:
#职场智慧 #情商修炼 #职场心理学 #成长思维 #人生感悟
"""
        
        print("\n" + "="*60)
        print("开始测试分镜头生成功能")
        print("="*60)
        print(f"LLM API Key: {llm_api_key[:10]}...")
        print(f"LLM Base URL: {llm_base_url}")
        
        # 生成分镜头
        scenes = await storyboard_generator.generate_storyboard(test_content, num_scenes=3)
        
        if scenes:
            print(f"\n✅ 成功生成 {len(scenes)} 个分镜头")
            print("\n" + "="*60)
            print("分镜头详情")
            print("="*60)
            
            for i, scene in enumerate(scenes, 1):
                print(f"\n🎬 分镜头 {i}: {scene.scene_title}")
                print(f"   ID: {scene.scene_id}")
                print(f"   时长: {scene.duration}秒")
                print(f"   描述: {scene.scene_description}")
                print(f"   视觉元素: {', '.join(scene.visual_elements)}")
                print(f"   文本覆盖: {scene.text_overlay}")
                print(f"   背景音乐: {scene.background_music}")
                print(f"   转场效果: {scene.transition_effect}")
                print("-" * 40)
            
            # 保存结果到JSON文件
            result_data = {
                "success": True,
                "total_scenes": len(scenes),
                "scenes": [
                    {
                        "scene_id": scene.scene_id,
                        "scene_title": scene.scene_title,
                        "scene_description": scene.scene_description,
                        "duration": scene.duration,
                        "visual_elements": scene.visual_elements,
                        "text_overlay": scene.text_overlay,
                        "background_music": scene.background_music,
                        "transition_effect": scene.transition_effect
                    }
                    for scene in scenes
                ]
            }
            
            with open('storyboard_result.json', 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 分镜头结果已保存到: storyboard_result.json")
            
        else:
            print("❌ 分镜头生成失败")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        logger.exception("详细错误信息:")

async def main():
    """主函数"""
    print("分镜头生成功能测试")
    print("="*60)
    print("此测试只需要LLM API密钥，不需要豆包Seedance API")
    print("="*60)
    
    await test_storyboard_generation()

if __name__ == "__main__":
    asyncio.run(main())
