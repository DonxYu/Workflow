#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
负责加载和管理环境变量配置
"""

import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Config:
    """配置类"""
    # 小红书配置
    xhs_cookie: str
    
    # LLM配置
    llm_api_key: str
    llm_base_url: str
    
    # Notion配置
    notion_token: str
    original_database_id: str
    processed_database_id: str
    
    # 豆包Seedance配置
    doubao_api_key: str
    doubao_base_url: str
    
    # 视频生成配置
    video_output_dir: str
    default_scene_count: int
    video_resolution: str
    video_style: str
    
    # 搜索参数
    note_type: int
    sort: int
    total_number: int
    
    # 其他配置
    log_level: str
    request_timeout: int
    max_retries: int

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            env_file: 环境变量文件路径，如果为None则从系统环境变量读取
        """
        self.env_file = env_file
        self._load_env_file()
    
    def _load_env_file(self):
        """加载环境变量文件"""
        if self.env_file and os.path.exists(self.env_file):
            try:
                with open(self.env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                logger.info(f"成功加载环境变量文件: {self.env_file}")
            except Exception as e:
                logger.warning(f"加载环境变量文件失败: {e}")
    
    def get_config(self) -> Config:
        """
        获取配置对象
        
        Returns:
            配置对象
            
        Raises:
            ValueError: 当必需配置项缺失时
        """
        # 验证必需配置项
        required_configs = {
            'XHS_COOKIE': '小红书Cookie',
            'LLM_API_KEY': 'LLM API密钥',
            'NOTION_TOKEN': 'Notion Token',
            'ORIGINAL_DATABASE_ID': '原始数据库ID',
            'PROCESSED_DATABASE_ID': '处理后数据库ID',
            'DOUBAO_API_KEY': '豆包Seedance API密钥'
        }
        
        missing_configs = []
        for key, description in required_configs.items():
            if not os.getenv(key):
                missing_configs.append(f"{key} ({description})")
        
        if missing_configs:
            raise ValueError(f"缺少必需配置项: {', '.join(missing_configs)}")
        
        # 创建配置对象
        config = Config(
            # 小红书配置
            xhs_cookie=os.getenv('XHS_COOKIE'),
            
            # LLM配置
            llm_api_key=os.getenv('LLM_API_KEY'),
            llm_base_url=os.getenv('LLM_BASE_URL', 'https://api.deepseek.com'),
            
            # Notion配置
            notion_token=os.getenv('NOTION_TOKEN'),
            original_database_id=os.getenv('ORIGINAL_DATABASE_ID'),
            processed_database_id=os.getenv('PROCESSED_DATABASE_ID'),
            
            # 豆包Seedance配置
            doubao_api_key=os.getenv('DOUBAO_API_KEY'),
            doubao_base_url=os.getenv('DOUBAO_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3'),
            
            # 视频生成配置
            video_output_dir=os.getenv('VIDEO_OUTPUT_DIR', 'videos'),
            default_scene_count=int(os.getenv('DEFAULT_SCENE_COUNT', '3')),
            video_resolution=os.getenv('VIDEO_RESOLUTION', '720p'),
            video_style=os.getenv('VIDEO_STYLE', 'realistic'),
            
            # 搜索参数
            note_type=int(os.getenv('NOTE_TYPE', '2')),
            sort=int(os.getenv('SORT', '2')),
            total_number=int(os.getenv('TOTAL_NUMBER', '2')),
            
            # 其他配置
            log_level=os.getenv('LOG_LEVEL', 'INFO'),
            request_timeout=int(os.getenv('REQUEST_TIMEOUT', '30')),
            max_retries=int(os.getenv('MAX_RETRIES', '3'))
        )
        
        # 验证配置值
        self._validate_config(config)
        
        logger.info("配置加载成功")
        return config
    
    def _validate_config(self, config: Config):
        """
        验证配置值
        
        Args:
            config: 配置对象
            
        Raises:
            ValueError: 当配置值无效时
        """
        # 验证笔记类型
        if config.note_type not in [0, 1, 2]:
            raise ValueError("NOTE_TYPE必须是0(全部)、1(视频)或2(图文)")
        
        # 验证排序方式
        if config.sort not in [0, 1, 2]:
            raise ValueError("SORT必须是0(综合)、1(最新)或2(最热)")
        
        # 验证总数
        if config.total_number <= 0:
            raise ValueError("TOTAL_NUMBER必须大于0")
        
        # 验证日志级别
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        if config.log_level.upper() not in valid_log_levels:
            raise ValueError(f"LOG_LEVEL必须是以下之一: {', '.join(valid_log_levels)}")
        
        # 验证超时时间
        if config.request_timeout <= 0:
            raise ValueError("REQUEST_TIMEOUT必须大于0")
        
        # 验证重试次数
        if config.max_retries < 0:
            raise ValueError("MAX_RETRIES必须大于等于0")
    
    def get_config_dict(self) -> Dict[str, Any]:
        """
        获取配置字典
        
        Returns:
            配置字典
        """
        config = self.get_config()
        return {
            'xhs_cookie': config.xhs_cookie,
            'llm_api_key': config.llm_api_key,
            'llm_base_url': config.llm_base_url,
            'notion_token': config.notion_token,
            'original_database_id': config.original_database_id,
            'processed_database_id': config.processed_database_id,
            'doubao_api_key': config.doubao_api_key,
            'doubao_base_url': config.doubao_base_url,
            'video_output_dir': config.video_output_dir,
            'default_scene_count': config.default_scene_count,
            'video_resolution': config.video_resolution,
            'video_style': config.video_style,
            'note_type': config.note_type,
            'sort': config.sort,
            'total_number': config.total_number,
            'log_level': config.log_level,
            'request_timeout': config.request_timeout,
            'max_retries': config.max_retries
        }
    
    def print_config_summary(self):
        """打印配置摘要（隐藏敏感信息）"""
        config = self.get_config()
        
        print("=" * 50)
        print("配置摘要")
        print("=" * 50)
        print(f"小红书Cookie: {'已配置' if config.xhs_cookie else '未配置'}")
        print(f"LLM API密钥: {'已配置' if config.llm_api_key else '未配置'}")
        print(f"LLM基础URL: {config.llm_base_url}")
        print(f"Notion Token: {'已配置' if config.notion_token else '未配置'}")
        print(f"原始数据库ID: {config.original_database_id}")
        print(f"处理后数据库ID: {config.processed_database_id}")
        print(f"豆包Seedance API密钥: {'已配置' if config.doubao_api_key else '未配置'}")
        print(f"豆包Seedance基础URL: {config.doubao_base_url}")
        print(f"视频输出目录: {config.video_output_dir}")
        print(f"默认分镜头数量: {config.default_scene_count}")
        print(f"视频分辨率: {config.video_resolution}")
        print(f"视频风格: {config.video_style}")
        print(f"笔记类型: {config.note_type} ({'全部' if config.note_type == 0 else '视频' if config.note_type == 1 else '图文'})")
        print(f"排序方式: {config.sort} ({'综合' if config.sort == 0 else '最新' if config.sort == 1 else '最热'})")
        print(f"抓取数量: {config.total_number}")
        print(f"日志级别: {config.log_level}")
        print(f"请求超时: {config.request_timeout}秒")
        print(f"最大重试: {config.max_retries}次")
        print("=" * 50)

def load_config(env_file: Optional[str] = None) -> Config:
    """
    便捷函数：加载配置
    
    Args:
        env_file: 环境变量文件路径
        
    Returns:
        配置对象
    """
    manager = ConfigManager(env_file)
    return manager.get_config()

def load_config_dict(env_file: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷函数：加载配置字典
    
    Args:
        env_file: 环境变量文件路径
        
    Returns:
        配置字典
    """
    manager = ConfigManager(env_file)
    return manager.get_config_dict()

if __name__ == "__main__":
    # 测试配置加载
    try:
        manager = ConfigManager()
        manager.print_config_summary()
    except ValueError as e:
        print(f"配置错误: {e}")
    except Exception as e:
        print(f"加载配置时发生错误: {e}")
