#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作流测试脚本
用于测试各个组件的功能
"""

import asyncio
import json
import logging
from typing import Dict, Any
from main import (
    XHSSearchAPI, XHSReaderAPI, LLMProcessor, 
    NotionManager, WorkflowProcessor, XHSNote, NoteContent
)
from config import ConfigManager
from utils import PerformanceMonitor, DataValidator, SecurityUtils

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WorkflowTester:
    """工作流测试器"""
    
    def __init__(self):
        self.config_manager = None
        self.config = None
        self.performance_monitor = PerformanceMonitor()
    
    async def setup(self):
        """设置测试环境"""
        try:
            self.config_manager = ConfigManager('.env')
            self.config = self.config_manager.get_config_dict()
            logger.info("测试环境设置完成")
        except Exception as e:
            logger.error(f"设置测试环境失败: {e}")
            raise
    
    async def test_xhs_search(self):
        """测试小红书搜索功能"""
        logger.info("开始测试小红书搜索功能")
        self.performance_monitor.start()
        
        try:
            search_api = XHSSearchAPI(self.config['xhs_cookie'])
            notes = await search_api.search_notes(
                keywords="测试关键词",
                note_type=2,
                sort=2,
                total_number=2
            )
            
            self.performance_monitor.checkpoint("xhs_search")
            
            if notes:
                logger.info(f"搜索成功，找到 {len(notes)} 条笔记")
                for i, note in enumerate(notes):
                    logger.info(f"笔记 {i+1}: {note.note_display_title}")
                    # 验证数据
                    note_data = {
                        'note_id': note.note_id,
                        'note_display_title': note.note_display_title,
                        'note_url': note.note_url,
                        'auther_nick_name': note.auther_nick_name
                    }
                    if DataValidator.validate_note_data(note_data):
                        logger.info("笔记数据验证通过")
                    else:
                        logger.warning("笔记数据验证失败")
                return notes
            else:
                logger.warning("未找到任何笔记")
                return []
                
        except Exception as e:
            logger.error(f"小红书搜索测试失败: {e}")
            return []
    
    async def test_xhs_reader(self, notes: list):
        """测试小红书内容读取功能"""
        if not notes:
            logger.info("跳过内容读取测试（无笔记数据）")
            return []
        
        logger.info("开始测试小红书内容读取功能")
        
        try:
            reader_api = XHSReaderAPI()
            contents = []
            
            for note in notes:
                content = await reader_api.read_note_content(note.note_url)
                if content:
                    contents.append(content)
                    logger.info(f"成功读取笔记内容: {content.title}")
                    
                    # 验证内容数据
                    content_data = {
                        'title': content.title,
                        'desc': content.desc
                    }
                    if DataValidator.validate_content_data(content_data):
                        logger.info("内容数据验证通过")
                    else:
                        logger.warning("内容数据验证失败")
                else:
                    logger.warning(f"读取笔记内容失败: {note.note_url}")
            
            self.performance_monitor.checkpoint("xhs_reader")
            logger.info(f"内容读取测试完成，成功读取 {len(contents)} 条内容")
            return contents
            
        except Exception as e:
            logger.error(f"小红书内容读取测试失败: {e}")
            return []
    
    async def test_llm_processor(self, contents: list):
        """测试LLM处理功能"""
        if not contents:
            logger.info("跳过LLM处理测试（无内容数据）")
            return []
        
        logger.info("开始测试LLM处理功能")
        
        try:
            llm_processor = LLMProcessor(
                self.config['llm_api_key'], 
                self.config['llm_base_url']
            )
            processed_contents = []
            
            for content in contents:
                processed = await llm_processor.process_content(content.desc)
                if processed:
                    processed_contents.append(processed)
                    logger.info(f"LLM处理成功，内容长度: {len(processed)}")
                else:
                    logger.warning("LLM处理失败")
            
            self.performance_monitor.checkpoint("llm_processor")
            logger.info(f"LLM处理测试完成，成功处理 {len(processed_contents)} 条内容")
            return processed_contents
            
        except Exception as e:
            logger.error(f"LLM处理测试失败: {e}")
            return []
    
    async def test_notion_manager(self, processed_contents: list):
        """测试Notion管理功能"""
        if not processed_contents:
            logger.info("跳过Notion测试（无处理后的内容）")
            return False
        
        logger.info("开始测试Notion管理功能")
        
        try:
            notion_manager = NotionManager(self.config['notion_token'])
            
            # 测试添加数据到处理后数据库
            test_properties = [
                {
                    "name": "Content",
                    "type": "title",
                    "value": f"测试内容 - {SecurityUtils.generate_request_id()}"
                },
                {
                    "name": "Date",
                    "type": "date",
                    "value": "2024-01-01"
                }
            ]
            
            success = await notion_manager.add_database_item(
                self.config['processed_database_id'],
                test_properties
            )
            
            self.performance_monitor.checkpoint("notion_manager")
            
            if success:
                logger.info("Notion测试成功")
                return True
            else:
                logger.warning("Notion测试失败")
                return False
                
        except Exception as e:
            logger.error(f"Notion测试失败: {e}")
            return False
    
    async def test_full_workflow(self):
        """测试完整工作流"""
        logger.info("开始测试完整工作流")
        
        try:
            processor = WorkflowProcessor(self.config)
            result = await processor.process_workflow("测试关键词")
            
            self.performance_monitor.checkpoint("full_workflow")
            
            if result.get('success'):
                logger.info("完整工作流测试成功")
                logger.info(f"处理结果: {result.get('message')}")
                return True
            else:
                logger.warning(f"完整工作流测试失败: {result.get('message')}")
                return False
                
        except Exception as e:
            logger.error(f"完整工作流测试失败: {e}")
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        logger.info("=" * 60)
        logger.info("开始运行工作流测试套件")
        logger.info("=" * 60)
        
        await self.setup()
        
        # 测试各个组件
        notes = await self.test_xhs_search()
        contents = await self.test_xhs_reader(notes)
        processed_contents = await self.test_llm_processor(contents)
        notion_success = await self.test_notion_manager(processed_contents)
        
        # 测试完整工作流
        workflow_success = await self.test_full_workflow()
        
        # 输出性能摘要
        performance_summary = self.performance_monitor.get_summary()
        logger.info("=" * 60)
        logger.info("性能摘要:")
        logger.info("=" * 60)
        for key, value in performance_summary.items():
            logger.info(f"{key}: {value:.2f}秒")
        
        # 输出测试结果摘要
        logger.info("=" * 60)
        logger.info("测试结果摘要:")
        logger.info("=" * 60)
        logger.info(f"小红书搜索: {'✓' if notes else '✗'}")
        logger.info(f"内容读取: {'✓' if contents else '✗'}")
        logger.info(f"LLM处理: {'✓' if processed_contents else '✗'}")
        logger.info(f"Notion集成: {'✓' if notion_success else '✗'}")
        logger.info(f"完整工作流: {'✓' if workflow_success else '✗'}")
        
        # 计算成功率
        total_tests = 5
        passed_tests = sum([
            bool(notes),
            bool(contents),
            bool(processed_contents),
            notion_success,
            workflow_success
        ])
        
        success_rate = (passed_tests / total_tests) * 100
        logger.info(f"测试成功率: {success_rate:.1f}% ({passed_tests}/{total_tests})")
        
        return success_rate >= 80  # 80%以上认为测试通过

async def main():
    """主测试函数"""
    tester = WorkflowTester()
    
    try:
        success = await tester.run_all_tests()
        if success:
            print("\n🎉 所有测试通过！工作流可以正常使用。")
        else:
            print("\n❌ 部分测试失败，请检查配置和网络连接。")
    except Exception as e:
        print(f"\n💥 测试过程中发生错误: {e}")
        logger.exception("测试异常详情:")

if __name__ == "__main__":
    asyncio.run(main())
