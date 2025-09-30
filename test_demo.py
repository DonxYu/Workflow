#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示分镜头生成功能
使用模拟的API响应来展示功能
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from typing import List

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class StoryboardScene:
    """分镜头场景数据结构"""
    scene_id: str
    scene_title: str
    scene_description: str
    duration: int  # 秒数
    visual_elements: List[str]
    text_overlay: str
    background_music: str
    transition_effect: str

class MockStoryboardGenerator:
    """模拟分镜头生成器"""
    
    def __init__(self):
        pass
    
    async def generate_storyboard(self, content: str, num_scenes: int = 3) -> List[StoryboardScene]:
        """
        模拟生成分镜头脚本
        
        Args:
            content: 小红书仿写内容
            num_scenes: 分镜头数量
            
        Returns:
            分镜头场景列表
        """
        # 模拟API调用延迟
        await asyncio.sleep(1)
        
        # 模拟生成的分镜头数据
        mock_scenes = [
            StoryboardScene(
                scene_id="scene_1",
                scene_title="开场引入",
                scene_description="画面从职场办公室开始，镜头缓缓推进到一位正在思考的职场人士，背景音乐轻柔，营造思考氛围。人物表情专注，周围环境整洁有序，体现专业感。",
                duration=8,
                visual_elements=["办公室环境", "思考的职场人士", "整洁的桌面", "柔和的灯光"],
                text_overlay="为什么聪明人都在'装傻'？",
                background_music="轻柔的思考音乐",
                transition_effect="淡入效果"
            ),
            StoryboardScene(
                scene_id="scene_2",
                scene_title="核心观点展示",
                scene_description="画面切换到会议室场景，展示不同的人在会议中的表现。聪明人低调观察，而急于表现的人在高谈阔论。通过对比展现'装傻'的智慧。",
                duration=8,
                visual_elements=["会议室场景", "不同性格的人物", "对比画面", "文字动画"],
                text_overlay="真正的智慧在于'藏拙'",
                background_music="渐强的背景音乐",
                transition_effect="切换转场"
            ),
            StoryboardScene(
                scene_id="scene_3",
                scene_title="总结升华",
                scene_description="画面回到个人特写，人物露出会心的微笑，背景逐渐虚化，突出人物形象。最后出现核心观点文字，配合优雅的动画效果。",
                duration=8,
                visual_elements=["人物特写", "会心微笑", "虚化背景", "文字动画"],
                text_overlay="真正的智慧，往往藏在'不争'之中",
                background_music="升华的音乐结尾",
                transition_effect="淡出效果"
            )
        ]
        
        return mock_scenes[:num_scenes]

async def demo_storyboard_generation():
    """演示分镜头生成功能"""
    try:
        # 创建模拟分镜头生成器
        storyboard_generator = MockStoryboardGenerator()
        
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
        print("🎬 分镜头生成功能演示")
        print("="*60)
        print("📝 输入内容：职场智慧类小红书笔记")
        print("🎯 目标：生成3个8秒分镜头脚本")
        print("⏱️  模拟API调用中...")
        
        # 生成分镜头
        scenes = await storyboard_generator.generate_storyboard(test_content, num_scenes=3)
        
        if scenes:
            print(f"\n✅ 成功生成 {len(scenes)} 个分镜头")
            print("\n" + "="*60)
            print("📋 分镜头脚本详情")
            print("="*60)
            
            for i, scene in enumerate(scenes, 1):
                print(f"\n🎬 分镜头 {i}: {scene.scene_title}")
                print(f"   🆔 ID: {scene.scene_id}")
                print(f"   ⏱️  时长: {scene.duration}秒")
                print(f"   📖 描述: {scene.scene_description}")
                print(f"   🎨 视觉元素: {', '.join(scene.visual_elements)}")
                print(f"   📝 文本覆盖: {scene.text_overlay}")
                print(f"   🎵 背景音乐: {scene.background_music}")
                print(f"   🔄 转场效果: {scene.transition_effect}")
                print("-" * 50)
            
            # 保存结果到JSON文件
            result_data = {
                "success": True,
                "total_scenes": len(scenes),
                "input_content": test_content[:200] + "...",
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
            
            with open('demo_storyboard_result.json', 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n💾 分镜头结果已保存到: demo_storyboard_result.json")
            
            # 显示视频生成流程说明
            print("\n" + "="*60)
            print("🎥 视频生成流程说明")
            print("="*60)
            print("1. 📝 分镜头脚本生成 ✅ (已完成)")
            print("2. 🤖 调用豆包Seedance API (需要真实API密钥)")
            print("3. 🎬 为每个分镜头生成8秒视频")
            print("4. 💾 下载并保存视频文件")
            print("5. 📊 生成完整的视频制作报告")
            
            print(f"\n🔧 要使用真实API，请：")
            print(f"   1. 设置环境变量: export LLM_API_KEY=your_deepseek_api_key")
            print(f"   2. 设置环境变量: export DOUBAO_API_KEY=your_doubao_api_key")
            print(f"   3. 运行: python3 test_video_generation.py")
            
        else:
            print("❌ 分镜头生成失败")
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        logger.exception("详细错误信息:")

async def main():
    """主函数"""
    print("🎬 视频生成功能演示")
    print("="*60)
    print("此演示使用模拟数据展示分镜头生成功能")
    print("不需要真实的API密钥")
    print("="*60)
    
    await demo_storyboard_generation()

if __name__ == "__main__":
    asyncio.run(main())
