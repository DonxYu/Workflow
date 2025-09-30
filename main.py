#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书笔记搜索与内容处理工作流
基于Coze工作流实现的Python版本

主要功能：
1. 根据关键词搜索小红书笔记
2. 读取笔记详细内容
3. 使用大语言模型处理内容
4. 将结果存储到Notion数据库
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import aiohttp
import requests
from dataclasses import dataclass
from notion_client import Client as NotionClient
from config import load_config_dict, ConfigManager
from video_generator import VideoWorkflowManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class XHSNote:
    """小红书笔记数据结构"""
    note_id: str
    note_display_title: str
    note_url: str
    auther_nick_name: str
    auther_user_id: str
    auther_avatar: str
    auther_home_page_url: str
    note_liked_count: str
    note_cover_url_pre: str
    note_cover_url_default: str
    note_cover_width: str
    note_cover_height: str
    note_model_type: str
    note_card_type: str
    note_xsec_token: str
    note_liked: bool

@dataclass
class NoteContent:
    """笔记内容数据结构"""
    title: str
    desc: str
    video_url: Optional[str] = None

class XHSSearchAPI:
    """小红书搜索API"""
    
    def __init__(self, cookie_str: str):
        self.cookie_str = cookie_str
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Cookie': cookie_str,
            'Referer': 'https://www.xiaohongshu.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
    
    async def search_notes(self, keywords: str, note_type: int = 2, sort: int = 2, total_number: int = 2) -> List[XHSNote]:
        """
        搜索小红书笔记
        
        Args:
            keywords: 搜索关键词
            note_type: 笔记类型 (0=全部，1=视频，2=图文)
            sort: 排序方式 (0=综合，1=最新，2=最热)
            total_number: 要抓取的笔记总数
            
        Returns:
            笔记列表
        """
        try:
            # 这里需要根据实际的小红书API接口进行调整
            # 由于小红书的反爬机制，这里提供一个模拟的实现
            logger.info(f"搜索关键词: {keywords}, 类型: {note_type}, 排序: {sort}, 数量: {total_number}")
            
            # 模拟返回数据（实际使用时需要替换为真实的API调用）
            mock_notes = [
                XHSNote(
                    note_id="mock_note_1",
                    note_display_title=f"关于{keywords}的精彩分享",
                    note_url="https://www.xiaohongshu.com/explore/mock_note_1",
                    auther_nick_name="测试用户1",
                    auther_user_id="user_1",
                    auther_avatar="https://example.com/avatar1.jpg",
                    auther_home_page_url="https://www.xiaohongshu.com/user/profile/user_1",
                    note_liked_count="100",
                    note_cover_url_pre="https://example.com/cover1.jpg",
                    note_cover_url_default="https://example.com/cover1.jpg",
                    note_cover_width="400",
                    note_cover_height="300",
                    note_model_type="normal",
                    note_card_type="normal",
                    note_xsec_token="mock_token_1",
                    note_liked=False
                ),
                XHSNote(
                    note_id="mock_note_2",
                    note_display_title=f"{keywords}的深度解析",
                    note_url="https://www.xiaohongshu.com/explore/mock_note_2",
                    auther_nick_name="测试用户2",
                    auther_user_id="user_2",
                    auther_avatar="https://example.com/avatar2.jpg",
                    auther_home_page_url="https://www.xiaohongshu.com/user/profile/user_2",
                    note_liked_count="200",
                    note_cover_url_pre="https://example.com/cover2.jpg",
                    note_cover_url_default="https://example.com/cover2.jpg",
                    note_cover_width="400",
                    note_cover_height="300",
                    note_model_type="normal",
                    note_card_type="normal",
                    note_xsec_token="mock_token_2",
                    note_liked=False
                )
            ]
            
            return mock_notes[:total_number]
            
        except Exception as e:
            logger.error(f"搜索笔记时发生错误: {e}")
            return []

class XHSReaderAPI:
    """小红书笔记内容读取API"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    
    async def read_note_content(self, note_url: str) -> Optional[NoteContent]:
        """
        读取笔记详细内容
        
        Args:
            note_url: 笔记链接
            
        Returns:
            笔记内容
        """
        try:
            logger.info(f"读取笔记内容: {note_url}")
            
            # 这里需要根据实际的小红书内容解析逻辑进行调整
            # 由于小红书的反爬机制，这里提供一个模拟的实现
            mock_content = NoteContent(
                title=f"笔记标题 - {note_url.split('/')[-1]}",
                desc=f"这是关于{note_url}的详细内容描述。在实际使用中，这里应该是从网页中解析出的真实内容。",
                video_url=None
            )
            
            return mock_content
            
        except Exception as e:
            logger.error(f"读取笔记内容时发生错误: {e}")
            return None

class LLMProcessor:
    """大语言模型处理器"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    
    async def process_content(self, content: str) -> Optional[str]:
        """
        使用大语言模型处理内容
        
        Args:
            content: 原始内容
            
        Returns:
            处理后的内容
        """
        try:
            logger.info("开始使用LLM处理内容")
            
            prompt = f"""# 角色与背景 (Persona)
你是一位兼具战略视野和人文关怀的职场思想家、高级管理者。你在 [国内一线互联网大厂，如腾讯/阿里/字节] 身居高位超过 [10年]，你的职场人设是 "冷静的观察者、深刻的思考者、真诚的布道者"。你早已跳出具体执行的细节，更擅长洞察商业和职场的底层逻辑。你的分享，旨在提升读者的认知维度，帮助他们建立更宏大的职业格局和长远的个人发展观，实现从"优秀"到"卓越"的跃迁。

# 任务 (Task)
请根据我提供的 [内容原文]，以"仿写"和"再创作"的方式，将其改写为一篇符合上述【角色与背景】的、适合在小红书平台发布的、立意高远且富有深度的职场洞察笔记。

核心目标： 你的任务不是简单地总结或润色原文，而是要用指定的"人设"和"思维框架"对原文进行脱胎换骨的重塑，提取其核心内核，并以更高维度的视角和更深刻的逻辑进行全新演绎。

# 核心要求 (Core Requirements)
1.  输入内容 (Input):
    * {content}

2.  核心转化动作 (Core Transformation Actions):
    * 提炼升维 (Elevate & Reframe): 深入分析 {content} 的核心思想，找到一个最能颠覆固有认知的 "反直觉切入点" 作为笔记的"钩子"。即使原文观点平和，你也要挖掘出其背后隐藏的、挑战常识的洞见。
    * 重构逻辑 (Restructure Logic): 将原文的逻辑，强力重塑为 "提出颠覆性观点 → 拆解底层逻辑/引入思维模型 → 给出可行路径/心法" 的深度叙事结构。你要做的不是复述原文，而是借用原文的"料"，搭建起一个更具结构性和说服力的逻辑框架。
    * 拔高立意与赋能 (Conceptualize & Empower): 为原文的核心观点匹配并引入1-2个高级商业或思维模型（例如：系统思维、第一性原理、价值杠杆、非对称优势、认知飞轮等）。用通俗易懂的语言和精妙的比喻，将这些模型与原文内容无缝融合，最终输出一个能让读者举一反三、直接应用的思考框架或"心法"。

# 风格与语调 (Style & Tone)
1.  整体风格: 格局宏大、洞察深刻、逻辑严密，同时保持真诚和易读性。用"我"的第一人称分享洞见。
2.  开头: 用一个从原文观点中提炼出的、振聋发聩的问题或颠覆性的观点开场，直接抓住高认知人群的注意力。
3.  正文:
    * 结构清晰，严格遵循上述"重构逻辑"的路径。
    * 语言精准有力，多用比喻、类比来解释复杂概念。可以适当出现一些"金句"，引发读者思考和共鸣。
    * 保持小红书的易读性，多用分点叙述（1️⃣ 2️⃣ 3️⃣）、emoji 和小标题，形成视觉节奏感。
4.  结尾: 不仅是总结，更要提供一个开放性的思考题或一句充满哲理的寄语，引导读者进行深度互动和反思，将思考引向更深处。

# 输出格式 (Output Format)
请严格按照以下小红书笔记格式输出：

---
小红书标题：（基于原文核心，生成一个有深度、能引发思考的爆款标题，可以用设问或颠覆性观点）

正文内容：
（开头段落，提出从原文提炼的反直觉观点或深刻问题）

（正文，拆解底层逻辑，提供思维框架，分点叙述，逻辑清晰）

（结尾总结&升华 + 引导深度思考）

Hashtags:
（生成5-8个精准、有格调的标签，包含核心赛道词、主题关键词和认知提升类标签）"""

            # 调用DeepSeek API
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.8,
                    "max_tokens": 2200
                }
                
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        processed_content = result['choices'][0]['message']['content']
                        logger.info("LLM处理内容完成")
                        return processed_content
                    else:
                        logger.error(f"LLM API调用失败: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"LLM处理内容时发生错误: {e}")
            return None

class NotionManager:
    """Notion数据库管理器"""
    
    def __init__(self, notion_token: str):
        self.client = NotionClient(auth=notion_token)
    
    async def add_database_item(self, database_id: str, properties: List[Dict[str, Any]]) -> bool:
        """
        向Notion数据库添加新行
        
        Args:
            database_id: 数据库ID
            properties: 属性列表
            
        Returns:
            是否成功
        """
        try:
            logger.info(f"向Notion数据库 {database_id} 添加新行")
            
            # 转换属性格式为Notion API格式
            notion_properties = {}
            for prop in properties:
                name = prop['name']
                prop_type = prop['type']
                value = prop['value']
                
                if prop_type == 'title':
                    notion_properties[name] = {
                        "title": [{"text": {"content": str(value)}}]
                    }
                elif prop_type == 'rich_text':
                    notion_properties[name] = {
                        "rich_text": [{"text": {"content": str(value)}}]
                    }
                elif prop_type == 'url':
                    notion_properties[name] = {
                        "url": str(value)
                    }
                elif prop_type == 'date':
                    notion_properties[name] = {
                        "date": {"start": str(value)}
                    }
            
            # 添加新行
            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=notion_properties
            )
            
            logger.info(f"成功添加Notion数据库行: {response['id']}")
            return True
            
        except Exception as e:
            logger.error(f"添加Notion数据库行时发生错误: {e}")
            return False

class WorkflowProcessor:
    """工作流处理器"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.xhs_search = XHSSearchAPI(config['xhs_cookie'])
        self.xhs_reader = XHSReaderAPI()
        self.llm_processor = LLMProcessor(config['llm_api_key'], config.get('llm_base_url'))
        self.notion_manager = NotionManager(config['notion_token'])
        self.video_manager = VideoWorkflowManager(config)
    
    async def process_workflow(self, keyword: str) -> Dict[str, Any]:
        """
        处理完整的工作流
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            处理结果
        """
        try:
            logger.info(f"开始处理工作流，关键词: {keyword}")
            
            # 1. 搜索小红书笔记
            notes = await self.xhs_search.search_notes(
                keywords=keyword,
                note_type=self.config.get('note_type', 2),
                sort=self.config.get('sort', 2),
                total_number=self.config.get('total_number', 2)
            )
            
            if not notes:
                logger.warning("未找到任何笔记")
                return {"success": False, "message": "未找到任何笔记"}
            
            logger.info(f"找到 {len(notes)} 条笔记")
            
            results = []
            
            # 2. 循环处理每个笔记
            for note in notes:
                try:
                    # 2.1 读取笔记内容
                    note_content = await self.xhs_reader.read_note_content(note.note_url)
                    if not note_content:
                        logger.warning(f"无法读取笔记内容: {note.note_url}")
                        continue
                    
                    # 2.2 使用LLM处理内容
                    processed_content = await self.llm_processor.process_content(note_content.desc)
                    if not processed_content:
                        logger.warning(f"LLM处理内容失败: {note.note_url}")
                        continue
                    
                    # 2.2.1 生成视频分镜头和视频
                    video_result = None
                    try:
                        logger.info(f"开始为笔记生成视频: {note.note_display_title}")
                        video_result = await self.video_manager.process_video_workflow(
                            processed_content, 
                            self.config.get('default_scene_count', 3)
                        )
                        if video_result['success']:
                            logger.info(f"视频生成成功: {video_result['successful_videos']} 个视频")
                        else:
                            logger.warning(f"视频生成失败: {video_result['message']}")
                    except Exception as e:
                        logger.error(f"视频生成过程中发生错误: {e}")
                        video_result = {"success": False, "message": str(e)}
                    
                    # 2.3 准备Notion数据
                    current_date = datetime.now().strftime('%Y-%m-%d')
                    
                    # 原始笔记数据
                    original_properties = [
                        {
                            "name": "note_display_title",
                            "type": "title",
                            "value": note.note_display_title or "无标题"
                        },
                        {
                            "name": "auther_nick_name",
                            "type": "rich_text",
                            "value": note.auther_nick_name or "未知作者"
                        },
                        {
                            "name": "note_liked_count",
                            "type": "rich_text",
                            "value": note.note_liked_count or "0"
                        },
                        {
                            "name": "note_url",
                            "type": "url",
                            "value": note.note_url or "无链接"
                        },
                        {
                            "name": "created_date",
                            "type": "date",
                            "value": current_date
                        }
                    ]
                    
                    # 处理后的内容数据
                    processed_properties = [
                        {
                            "name": "Content",
                            "type": "title",
                            "value": processed_content[:1997] + "..." if len(processed_content) > 2000 else processed_content
                        },
                        {
                            "name": "Date",
                            "type": "date",
                            "value": current_date
                        }
                    ]
                    
                    # 2.4 存储到Notion数据库
                    original_success = await self.notion_manager.add_database_item(
                        self.config['original_database_id'], 
                        original_properties
                    )
                    
                    processed_success = await self.notion_manager.add_database_item(
                        self.config['processed_database_id'], 
                        processed_properties
                    )
                    
                    result = {
                        "note_id": note.note_id,
                        "note_title": note.note_display_title,
                        "note_url": note.note_url,
                        "author": note.auther_nick_name,
                        "likes": note.note_liked_count,
                        "original_content": note_content.desc,
                        "processed_content": processed_content,
                        "original_saved": original_success,
                        "processed_saved": processed_success,
                        "video_generation": video_result
                    }
                    
                    results.append(result)
                    logger.info(f"成功处理笔记: {note.note_display_title}")
                    
                except Exception as e:
                    logger.error(f"处理笔记时发生错误: {e}")
                    continue
            
            return {
                "success": True,
                "message": f"成功处理 {len(results)} 条笔记",
                "results": results
            }
            
        except Exception as e:
            logger.error(f"工作流处理时发生错误: {e}")
            return {"success": False, "message": f"工作流处理失败: {e}"}

async def main():
    """主函数"""
    try:
        # 加载配置
        config_manager = ConfigManager('.env')
        config = config_manager.get_config_dict()
        
        # 打印配置摘要
        config_manager.print_config_summary()
        
    except ValueError as e:
        print(f"配置错误: {e}")
        print("请检查环境变量配置或.env文件")
        return
    except Exception as e:
        print(f"加载配置时发生错误: {e}")
        return
    
    # 获取搜索关键词
    keyword = input("请输入搜索关键词: ").strip()
    if not keyword:
        print("关键词不能为空")
        return
    
    # 创建工作流处理器
    processor = WorkflowProcessor(config)
    
    # 执行工作流
    result = await processor.process_workflow(keyword)
    
    # 输出结果
    print("\n" + "="*50)
    print("工作流执行结果:")
    print("="*50)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
