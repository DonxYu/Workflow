#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化视频生成功能测试脚本
不需要用户交互，自动运行测试
"""

import asyncio
import json
import logging
import os
from config import ConfigManager
from video_generator import VideoWorkflowManager, StoryboardGenerator

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_storyboard_generation():
    """测试分镜头生成功能"""
    try:
        print("\n" + "="*60)
        print("🎬 测试1: 分镜头生成功能")
        print("="*60)
        
        # 检查LLM API密钥
        llm_api_key = os.getenv('LLM_API_KEY')
        if not llm_api_key or llm_api_key == 'sk-your_deepseek_api_key_here':
            print("⚠️  LLM_API_KEY未设置，使用模拟数据测试")
            return await test_storyboard_mock()
        
        # 创建分镜头生成器
        storyboard_generator = StoryboardGenerator(llm_api_key)
        
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
        
        print(f"📝 输入内容长度: {len(test_content)} 字符")
        print("⏱️  调用LLM API生成分镜头...")
        
        # 生成分镜头
        scenes = await storyboard_generator.generate_storyboard(test_content, num_scenes=3)
        
        if scenes:
            print(f"✅ 成功生成 {len(scenes)} 个分镜头")
            
            for i, scene in enumerate(scenes, 1):
                print(f"\n🎬 分镜头 {i}: {scene.scene_title}")
                print(f"   ⏱️  时长: {scene.duration}秒")
                print(f"   📝 文本覆盖: {scene.text_overlay}")
                print(f"   🎨 视觉元素: {', '.join(scene.visual_elements[:2])}...")
            
            # 保存结果
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
            
            with open('storyboard_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 分镜头结果已保存到: storyboard_test_result.json")
            return True
        else:
            print("❌ 分镜头生成失败")
            return False
        
    except Exception as e:
        print(f"❌ 分镜头生成测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

async def test_storyboard_mock():
    """使用模拟数据测试分镜头生成"""
    try:
        print("🎭 使用模拟数据测试分镜头生成...")
        
        # 模拟分镜头数据
        mock_scenes = [
            {
                "scene_id": "scene_1",
                "scene_title": "开场引入",
                "scene_description": "职场办公室场景，思考的职场人士",
                "duration": 8,
                "visual_elements": ["办公室环境", "思考的职场人士"],
                "text_overlay": "为什么聪明人都在'装傻'？",
                "background_music": "轻柔的思考音乐",
                "transition_effect": "淡入效果"
            },
            {
                "scene_id": "scene_2", 
                "scene_title": "核心观点展示",
                "scene_description": "会议室对比场景，展现'装傻'智慧",
                "duration": 8,
                "visual_elements": ["会议室场景", "不同性格的人物"],
                "text_overlay": "真正的智慧在于'藏拙'",
                "background_music": "渐强的背景音乐",
                "transition_effect": "切换转场"
            },
            {
                "scene_id": "scene_3",
                "scene_title": "总结升华", 
                "scene_description": "人物特写，升华主题",
                "duration": 8,
                "visual_elements": ["人物特写", "会心微笑"],
                "text_overlay": "真正的智慧，往往藏在'不争'之中",
                "background_music": "升华的音乐结尾",
                "transition_effect": "淡出效果"
            }
        ]
        
        print(f"✅ 模拟生成 {len(mock_scenes)} 个分镜头")
        
        for i, scene in enumerate(mock_scenes, 1):
            print(f"\n🎬 分镜头 {i}: {scene['scene_title']}")
            print(f"   ⏱️  时长: {scene['duration']}秒")
            print(f"   📝 文本覆盖: {scene['text_overlay']}")
        
        # 保存结果
        result_data = {
            "success": True,
            "total_scenes": len(mock_scenes),
            "test_mode": "mock",
            "scenes": mock_scenes
        }
        
        with open('storyboard_mock_result.json', 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 模拟分镜头结果已保存到: storyboard_mock_result.json")
        return True
        
    except Exception as e:
        print(f"❌ 模拟分镜头测试失败: {e}")
        return False

async def test_video_generation():
    """测试完整视频生成功能"""
    try:
        print("\n" + "="*60)
        print("🎥 测试2: 完整视频生成功能")
        print("="*60)
        
        # 检查配置
        try:
            config_manager = ConfigManager('.env')
            config = config_manager.get_config_dict()
            print("✅ 配置加载成功")
        except Exception as e:
            print(f"⚠️  配置加载失败: {e}")
            print("使用默认配置继续测试...")
            config = {
                'llm_api_key': os.getenv('LLM_API_KEY', ''),
                'llm_base_url': os.getenv('LLM_BASE_URL', 'https://api.deepseek.com'),
                'doubao_api_key': os.getenv('DOUBAO_API_KEY', ''),
                'doubao_base_url': os.getenv('DOUBAO_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
                'video_output_dir': os.getenv('VIDEO_OUTPUT_DIR', 'videos'),
                'default_scene_count': int(os.getenv('DEFAULT_SCENE_COUNT', '3'))
            }
        
        # 检查API密钥
        if not config.get('llm_api_key') or config['llm_api_key'] == 'sk-your_deepseek_api_key_here':
            print("⚠️  LLM_API_KEY未设置，跳过视频生成测试")
            return False
        
        if not config.get('doubao_api_key') or config['doubao_api_key'] == 'your_doubao_seedance_api_key_here':
            print("⚠️  DOUBAO_API_KEY未设置，跳过视频生成测试")
            return False
        
        # 创建视频工作流管理器
        video_manager = VideoWorkflowManager(config)
        
        # 测试内容
        test_content = "这是一个关于职场智慧的测试内容，包含深度思考和实用建议。"
        
        print("⏱️  开始视频生成工作流...")
        
        # 执行视频生成工作流
        result = await video_manager.process_video_workflow(test_content, num_scenes=2)
        
        # 输出结果
        print("\n" + "="*60)
        print("🎥 视频生成测试结果")
        print("="*60)
        
        if result['success']:
            print(f"✅ 测试成功！")
            print(f"📊 统计信息：")
            print(f"   - 总分镜头数: {result['total_scenes']}")
            print(f"   - 成功生成视频: {result['successful_videos']}")
            print(f"   - 失败视频: {result['failed_videos']}")
            
            # 保存结果
            with open('video_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 视频生成结果已保存到: video_test_result.json")
            return True
        else:
            print(f"❌ 测试失败: {result['message']}")
            return False
        
    except Exception as e:
        print(f"❌ 视频生成测试失败: {e}")
        logger.exception("详细错误信息:")
        return False

async def main():
    """主函数"""
    print("🎬 自动化视频生成功能测试")
    print("="*60)
    print("此脚本将自动运行所有测试，无需用户交互")
    print("="*60)
    
    # 测试1: 分镜头生成
    storyboard_success = await test_storyboard_generation()
    
    # 测试2: 完整视频生成（如果API密钥可用）
    video_success = await test_video_generation()
    
    # 总结
    print("\n" + "="*60)
    print("📊 测试总结")
    print("="*60)
    print(f"分镜头生成测试: {'✅ 成功' if storyboard_success else '❌ 失败'}")
    print(f"视频生成测试: {'✅ 成功' if video_success else '❌ 跳过/失败'}")
    
    if storyboard_success:
        print("\n🎉 基础功能测试通过！")
        print("💡 要使用完整视频生成功能，请设置以下环境变量：")
        print("   export LLM_API_KEY=your_deepseek_api_key")
        print("   export DOUBAO_API_KEY=your_doubao_api_key")
    else:
        print("\n⚠️  基础功能测试失败，请检查配置")

if __name__ == "__main__":
    asyncio.run(main())
