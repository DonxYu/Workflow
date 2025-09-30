#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频生成功能测试脚本
用于测试分镜头生成和豆包Seedance视频生成功能
"""

import asyncio
import json
import logging
from config import ConfigManager
from video_generator import VideoWorkflowManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_video_generation():
    """测试视频生成功能"""
    try:
        # 加载配置
        config_manager = ConfigManager('.env')
        config = config_manager.get_config_dict()
        
        # 打印配置摘要
        config_manager.print_config_summary()
        
        # 创建视频工作流管理器
        video_manager = VideoWorkflowManager(config)
        
        # 测试内容（模拟小红书仿写内容）
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
        print("开始测试视频生成功能")
        print("="*60)
        
        # 执行视频生成工作流
        result = await video_manager.process_video_workflow(test_content, num_scenes=3)
        
        # 输出结果
        print("\n" + "="*60)
        print("视频生成测试结果")
        print("="*60)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        # 分析结果
        if result['success']:
            print(f"\n✅ 测试成功！")
            print(f"📊 统计信息：")
            print(f"   - 总分镜头数: {result['total_scenes']}")
            print(f"   - 成功生成视频: {result['successful_videos']}")
            print(f"   - 失败视频: {result['failed_videos']}")
            
            print(f"\n🎬 分镜头详情：")
            for i, scene in enumerate(result['scenes'], 1):
                print(f"   {i}. {scene['scene_title']} ({scene['duration']}秒)")
                print(f"      描述: {scene['scene_description'][:100]}...")
                print(f"      文本覆盖: {scene['text_overlay']}")
                print()
            
            print(f"\n🎥 视频生成结果：")
            for video_result in result['video_results']:
                status_emoji = "✅" if video_result['status'] == 'success' else "❌"
                print(f"   {status_emoji} {video_result['scene_id']}: {video_result['status']}")
                if video_result['status'] == 'success':
                    print(f"      视频路径: {video_result['video_path']}")
                    print(f"      生成时间: {video_result['generation_time']:.2f}秒")
                else:
                    print(f"      错误信息: {video_result['error_message']}")
                print()
        else:
            print(f"\n❌ 测试失败: {result['message']}")
        
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请检查环境变量配置或.env文件")
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        logger.exception("详细错误信息:")

async def test_storyboard_only():
    """仅测试分镜头生成功能"""
    try:
        # 加载配置
        config_manager = ConfigManager('.env')
        config = config_manager.get_config_dict()
        
        # 创建分镜头生成器
        from video_generator import StoryboardGenerator
        storyboard_generator = StoryboardGenerator(
            config['llm_api_key'], 
            config.get('llm_base_url', 'https://api.deepseek.com')
        )
        
        # 测试内容
        test_content = "这是一个关于职场智慧的测试内容，包含深度思考和实用建议。"
        
        print("\n" + "="*60)
        print("测试分镜头生成功能")
        print("="*60)
        
        # 生成分镜头
        scenes = await storyboard_generator.generate_storyboard(test_content, num_scenes=3)
        
        if scenes:
            print(f"✅ 成功生成 {len(scenes)} 个分镜头")
            for i, scene in enumerate(scenes, 1):
                print(f"\n{i}. {scene.scene_title}")
                print(f"   ID: {scene.scene_id}")
                print(f"   时长: {scene.duration}秒")
                print(f"   描述: {scene.scene_description}")
                print(f"   视觉元素: {', '.join(scene.visual_elements)}")
                print(f"   文本覆盖: {scene.text_overlay}")
                print(f"   背景音乐: {scene.background_music}")
                print(f"   转场效果: {scene.transition_effect}")
        else:
            print("❌ 分镜头生成失败")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        logger.exception("详细错误信息:")

async def main():
    """主函数"""
    print("视频生成功能测试")
    print("="*60)
    print("1. 完整视频生成测试（包含分镜头生成和视频生成）")
    print("2. 仅分镜头生成测试")
    print("3. 退出")
    
    choice = input("\n请选择测试类型 (1-3): ").strip()
    
    if choice == "1":
        await test_video_generation()
    elif choice == "2":
        await test_storyboard_only()
    elif choice == "3":
        print("退出测试")
    else:
        print("无效选择")

if __name__ == "__main__":
    asyncio.run(main())
