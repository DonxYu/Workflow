#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频生成模块
包含分镜头生成和豆包seedance模型调用功能
"""

import asyncio
import json
import logging
import os
import aiohttp
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

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

@dataclass
class VideoGenerationResult:
    """视频生成结果数据结构"""
    scene_id: str
    status: str  # success, failed, processing
    video_url: Optional[str] = None
    video_path: Optional[str] = None
    error_message: Optional[str] = None
    generation_time: Optional[float] = None

class StoryboardGenerator:
    """分镜头生成器"""
    
    def __init__(self, llm_api_key: str, llm_base_url: str = "https://api.deepseek.com"):
        self.llm_api_key = llm_api_key
        self.llm_base_url = llm_base_url
        self.headers = {
            'Authorization': f'Bearer {llm_api_key}',
            'Content-Type': 'application/json'
        }
    
    async def generate_storyboard(self, content: str, num_scenes: int = 3) -> List[StoryboardScene]:
        """
        基于内容生成分镜头脚本
        
        Args:
            content: 小红书仿写内容
            num_scenes: 分镜头数量
            
        Returns:
            分镜头场景列表
        """
        try:
            logger.info(f"开始生成分镜头脚本，目标场景数: {num_scenes}")
            
            prompt = f"""# 角色与背景
你是一位专业的视频制作导演和分镜头脚本专家，擅长将文字内容转化为视觉化的视频分镜头脚本。你需要将小红书笔记内容转化为多个8秒左右的视频分镜头。

# 任务
请根据以下小红书笔记内容，生成{num_scenes}个视频分镜头脚本，每个分镜头时长约8秒。

# 输入内容
{content}

# 核心要求
1. 每个分镜头必须约8秒时长
2. 分镜头要符合小红书视频的视觉风格和节奏
3. 内容要有逻辑性和连贯性
4. 每个分镜头要有明确的视觉元素和文本覆盖
5. 考虑背景音乐和转场效果

# 输出格式
请严格按照以下JSON格式输出，不要包含任何其他文字：

```json
{{
  "scenes": [
    {{
      "scene_id": "scene_1",
      "scene_title": "开场引入",
      "scene_description": "详细描述这个分镜头的视觉内容、动作、场景设置等",
      "duration": 8,
      "visual_elements": ["元素1", "元素2", "元素3"],
      "text_overlay": "屏幕上显示的主要文字内容",
      "background_music": "背景音乐风格描述",
      "transition_effect": "转场效果描述"
    }},
    {{
      "scene_id": "scene_2", 
      "scene_title": "核心观点",
      "scene_description": "详细描述这个分镜头的视觉内容、动作、场景设置等",
      "duration": 8,
      "visual_elements": ["元素1", "元素2", "元素3"],
      "text_overlay": "屏幕上显示的主要文字内容",
      "background_music": "背景音乐风格描述",
      "transition_effect": "转场效果描述"
    }},
    {{
      "scene_id": "scene_3",
      "scene_title": "总结升华", 
      "scene_description": "详细描述这个分镜头的视觉内容、动作、场景设置等",
      "duration": 8,
      "visual_elements": ["元素1", "元素2", "元素3"],
      "text_overlay": "屏幕上显示的主要文字内容",
      "background_music": "背景音乐风格描述",
      "transition_effect": "转场效果描述"
    }}
  ]
}}
```

请确保：
1. 分镜头数量为{num_scenes}个
2. 每个分镜头时长都是8秒
3. 内容连贯，符合小红书视频风格
4. 视觉元素具体可执行
5. 文本覆盖简洁有力"""

            # 调用LLM API生成分镜头脚本
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000
                }
                
                async with session.post(
                    f"{self.llm_base_url}/v1/chat/completions",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        storyboard_text = result['choices'][0]['message']['content']
                        
                        # 解析JSON响应
                        scenes = self._parse_storyboard_response(storyboard_text)
                        logger.info(f"成功生成 {len(scenes)} 个分镜头")
                        return scenes
                    else:
                        logger.error(f"LLM API调用失败: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"生成分镜头脚本时发生错误: {e}")
            return []
    
    def _parse_storyboard_response(self, response_text: str) -> List[StoryboardScene]:
        """
        解析LLM返回的分镜头脚本
        
        Args:
            response_text: LLM返回的文本
            
        Returns:
            分镜头场景列表
        """
        try:
            # 提取JSON部分
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error("无法找到有效的JSON格式")
                return []
            
            json_text = response_text[json_start:json_end]
            data = json.loads(json_text)
            
            scenes = []
            for scene_data in data.get('scenes', []):
                scene = StoryboardScene(
                    scene_id=scene_data.get('scene_id', ''),
                    scene_title=scene_data.get('scene_title', ''),
                    scene_description=scene_data.get('scene_description', ''),
                    duration=scene_data.get('duration', 8),
                    visual_elements=scene_data.get('visual_elements', []),
                    text_overlay=scene_data.get('text_overlay', ''),
                    background_music=scene_data.get('background_music', ''),
                    transition_effect=scene_data.get('transition_effect', '')
                )
                scenes.append(scene)
            
            return scenes
            
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON时发生错误: {e}")
            return []
        except Exception as e:
            logger.error(f"解析分镜头脚本时发生错误: {e}")
            return []

class DoubaoSeedanceAPI:
    """豆包Seedance视频生成API"""
    
    def __init__(self, api_key: str, base_url: str = "https://ark.cn-beijing.volces.com/api/v3"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def generate_video(self, scene: StoryboardScene, output_dir: str = "videos") -> VideoGenerationResult:
        """
        使用豆包Seedance生成视频
        
        Args:
            scene: 分镜头场景
            output_dir: 输出目录
            
        Returns:
            视频生成结果
        """
        try:
            logger.info(f"开始生成视频: {scene.scene_title}")
            start_time = datetime.now()
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            # 构建视频生成请求
            prompt = self._build_video_prompt(scene)
            
            # 调用豆包Seedance API
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "doubao-seedance",
                    "prompt": prompt,
                    "duration": scene.duration,
                    "resolution": "720p",
                    "style": "realistic",
                    "motion": "medium"
                }
                
                async with session.post(
                    f"{self.base_url}/video/generate",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # 处理视频下载
                        video_url = result.get('video_url')
                        if video_url:
                            video_path = await self._download_video(video_url, scene.scene_id, output_dir)
                            
                            generation_time = (datetime.now() - start_time).total_seconds()
                            
                            return VideoGenerationResult(
                                scene_id=scene.scene_id,
                                video_url=video_url,
                                video_path=video_path,
                                status="success",
                                generation_time=generation_time
                            )
                        else:
                            return VideoGenerationResult(
                                scene_id=scene.scene_id,
                                status="failed",
                                error_message="API返回的视频URL为空"
                            )
                    else:
                        error_text = await response.text()
                        return VideoGenerationResult(
                            scene_id=scene.scene_id,
                            status="failed",
                            error_message=f"API调用失败: {response.status} - {error_text}"
                        )
                        
        except Exception as e:
            logger.error(f"生成视频时发生错误: {e}")
            return VideoGenerationResult(
                scene_id=scene.scene_id,
                status="failed",
                error_message=str(e)
            )
    
    def _build_video_prompt(self, scene: StoryboardScene) -> str:
        """
        构建视频生成提示词
        
        Args:
            scene: 分镜头场景
            
        Returns:
            视频生成提示词
        """
        prompt = f"""Create a {scene.duration}-second video scene with the following specifications:

Title: {scene.scene_title}
Description: {scene.scene_description}

Visual Elements:
{', '.join(scene.visual_elements)}

Text Overlay: {scene.text_overlay}
Background Music: {scene.background_music}
Transition Effect: {scene.transition_effect}

Style Requirements:
- High quality, professional video
- Suitable for social media (Xiaohongshu style)
- Smooth transitions and movements
- Clear and readable text overlay
- Engaging visual composition
- Duration: exactly {scene.duration} seconds

Please generate a video that matches these specifications with high visual quality and smooth motion."""
        
        return prompt
    
    async def _download_video(self, video_url: str, scene_id: str, output_dir: str) -> str:
        """
        下载生成的视频
        
        Args:
            video_url: 视频URL
            scene_id: 场景ID
            output_dir: 输出目录
            
        Returns:
            本地视频文件路径
        """
        try:
            video_filename = f"{scene_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            video_path = os.path.join(output_dir, video_filename)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as response:
                    if response.status == 200:
                        with open(video_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        
                        logger.info(f"视频下载完成: {video_path}")
                        return video_path
                    else:
                        logger.error(f"下载视频失败: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"下载视频时发生错误: {e}")
            return None

class VideoWorkflowManager:
    """视频工作流管理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.storyboard_generator = StoryboardGenerator(
            config['llm_api_key'], 
            config.get('llm_base_url', 'https://api.deepseek.com')
        )
        self.doubao_api = DoubaoSeedanceAPI(
            config['doubao_api_key'],
            config.get('doubao_base_url', 'https://ark.cn-beijing.volces.com/api/v3')
        )
    
    async def process_video_workflow(self, content: str, num_scenes: int = 3) -> Dict[str, Any]:
        """
        处理完整的视频生成工作流
        
        Args:
            content: 小红书仿写内容
            num_scenes: 分镜头数量
            
        Returns:
            处理结果
        """
        try:
            logger.info(f"开始视频生成工作流，分镜头数量: {num_scenes}")
            
            # 1. 生成分镜头脚本
            scenes = await self.storyboard_generator.generate_storyboard(content, num_scenes)
            if not scenes:
                return {
                    "success": False,
                    "message": "分镜头脚本生成失败"
                }
            
            logger.info(f"成功生成 {len(scenes)} 个分镜头脚本")
            
            # 2. 生成视频
            video_results = []
            for scene in scenes:
                result = await self.doubao_api.generate_video(scene)
                video_results.append(result)
                
                if result.status == "success":
                    logger.info(f"视频生成成功: {scene.scene_title}")
                else:
                    logger.error(f"视频生成失败: {scene.scene_title} - {result.error_message}")
            
            # 3. 统计结果
            successful_videos = [r for r in video_results if r.status == "success"]
            failed_videos = [r for r in video_results if r.status == "failed"]
            
            return {
                "success": len(successful_videos) > 0,
                "message": f"成功生成 {len(successful_videos)} 个视频，失败 {len(failed_videos)} 个",
                "total_scenes": len(scenes),
                "successful_videos": len(successful_videos),
                "failed_videos": len(failed_videos),
                "scenes": [
                    {
                        "scene_id": scene.scene_id,
                        "scene_title": scene.scene_title,
                        "scene_description": scene.scene_description,
                        "duration": scene.duration,
                        "visual_elements": scene.visual_elements,
                        "text_overlay": scene.text_overlay
                    }
                    for scene in scenes
                ],
                "video_results": [
                    {
                        "scene_id": result.scene_id,
                        "status": result.status,
                        "video_url": result.video_url,
                        "video_path": result.video_path,
                        "error_message": result.error_message,
                        "generation_time": result.generation_time
                    }
                    for result in video_results
                ]
            }
            
        except Exception as e:
            logger.error(f"视频工作流处理时发生错误: {e}")
            return {
                "success": False,
                "message": f"视频工作流处理失败: {e}"
            }
