#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
包含各种辅助函数和工具类
"""

import re
import time
import random
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
import hashlib
import base64

logger = logging.getLogger(__name__)

class TextProcessor:
    """文本处理工具类"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        清理文本内容
        
        Args:
            text: 原始文本
            
        Returns:
            清理后的文本
        """
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text.strip())
        
        # 移除特殊字符
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()（）【】""''""''，。！？；：]', '', text)
        
        return text
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 2000) -> str:
        """
        截断文本到指定长度
        
        Args:
            text: 原始文本
            max_length: 最大长度
            
        Returns:
            截断后的文本
        """
        if not text or len(text) <= max_length:
            return text
        
        # 在合适的位置截断（避免截断单词）
        truncated = text[:max_length-3]
        last_space = truncated.rfind(' ')
        if last_space > max_length * 0.8:  # 如果最后一个空格位置合理
            truncated = truncated[:last_space]
        
        return truncated + "..."
    
    @staticmethod
    def extract_hashtags(text: str) -> List[str]:
        """
        提取文本中的标签
        
        Args:
            text: 文本内容
            
        Returns:
            标签列表
        """
        if not text:
            return []
        
        # 匹配 #标签 格式
        hashtags = re.findall(r'#([^\s#]+)', text)
        return [tag.strip() for tag in hashtags if tag.strip()]
    
    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        提取文本中的URL
        
        Args:
            text: 文本内容
            
        Returns:
            URL列表
        """
        if not text:
            return []
        
        # URL正则表达式
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        return list(set(urls))  # 去重

class URLProcessor:
    """URL处理工具类"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """
        验证URL是否有效
        
        Args:
            url: URL字符串
            
        Returns:
            是否有效
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def extract_domain(url: str) -> Optional[str]:
        """
        提取URL的域名
        
        Args:
            url: URL字符串
            
        Returns:
            域名
        """
        try:
            result = urlparse(url)
            return result.netloc
        except Exception:
            return None
    
    @staticmethod
    def clean_url(url: str) -> str:
        """
        清理URL
        
        Args:
            url: 原始URL
            
        Returns:
            清理后的URL
        """
        if not url:
            return ""
        
        # 移除多余的参数和锚点
        url = url.split('#')[0]
        
        # 确保协议
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url

class RateLimiter:
    """速率限制器"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        初始化速率限制器
        
        Args:
            max_requests: 时间窗口内最大请求数
            time_window: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def wait_if_needed(self):
        """如果需要，等待直到可以发送请求"""
        now = time.time()
        
        # 清理过期的请求记录
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        # 如果请求数达到限制，等待
        if len(self.requests) >= self.max_requests:
            sleep_time = self.time_window - (now - self.requests[0]) + 1
            if sleep_time > 0:
                logger.info(f"速率限制：等待 {sleep_time:.1f} 秒")
                await asyncio.sleep(sleep_time)
                # 重新清理请求记录
                now = time.time()
                self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        # 记录当前请求
        self.requests.append(now)

class RetryHandler:
    """重试处理器"""
    
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, backoff_factor: float = 2.0):
        """
        初始化重试处理器
        
        Args:
            max_retries: 最大重试次数
            base_delay: 基础延迟时间（秒）
            backoff_factor: 退避因子
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.backoff_factor = backoff_factor
    
    async def execute_with_retry(self, func, *args, **kwargs):
        """
        执行函数并处理重试
        
        Args:
            func: 要执行的函数
            *args: 函数参数
            **kwargs: 函数关键字参数
            
        Returns:
            函数执行结果
            
        Raises:
            Exception: 重试次数用尽后的异常
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    delay = self.base_delay * (self.backoff_factor ** attempt)
                    # 添加随机抖动
                    jitter = random.uniform(0.1, 0.3) * delay
                    total_delay = delay + jitter
                    
                    logger.warning(f"执行失败，{total_delay:.1f}秒后重试 (尝试 {attempt + 1}/{self.max_retries + 1}): {e}")
                    await asyncio.sleep(total_delay)
                else:
                    logger.error(f"重试次数用尽，执行失败: {e}")
        
        raise last_exception

class DataValidator:
    """数据验证器"""
    
    @staticmethod
    def validate_note_data(note_data: Dict[str, Any]) -> bool:
        """
        验证笔记数据
        
        Args:
            note_data: 笔记数据字典
            
        Returns:
            是否有效
        """
        required_fields = ['note_id', 'note_display_title', 'note_url', 'auther_nick_name']
        
        for field in required_fields:
            if field not in note_data or not note_data[field]:
                logger.warning(f"笔记数据缺少必需字段: {field}")
                return False
        
        return True
    
    @staticmethod
    def validate_content_data(content_data: Dict[str, Any]) -> bool:
        """
        验证内容数据
        
        Args:
            content_data: 内容数据字典
            
        Returns:
            是否有效
        """
        required_fields = ['title', 'desc']
        
        for field in required_fields:
            if field not in content_data or not content_data[field]:
                logger.warning(f"内容数据缺少必需字段: {field}")
                return False
        
        return True

class SecurityUtils:
    """安全工具类"""
    
    @staticmethod
    def mask_sensitive_data(data: str, mask_char: str = '*', visible_chars: int = 4) -> str:
        """
        遮蔽敏感数据
        
        Args:
            data: 敏感数据
            mask_char: 遮蔽字符
            visible_chars: 可见字符数
            
        Returns:
            遮蔽后的数据
        """
        if not data or len(data) <= visible_chars:
            return mask_char * len(data) if data else ""
        
        visible_start = data[:visible_chars//2]
        visible_end = data[-(visible_chars//2):] if visible_chars > 1 else ""
        masked_middle = mask_char * (len(data) - len(visible_start) - len(visible_end))
        
        return visible_start + masked_middle + visible_end
    
    @staticmethod
    def generate_request_id() -> str:
        """
        生成请求ID
        
        Returns:
            请求ID
        """
        timestamp = str(int(time.time() * 1000))
        random_str = str(random.randint(1000, 9999))
        return f"req_{timestamp}_{random_str}"
    
    @staticmethod
    def hash_data(data: str) -> str:
        """
        对数据进行哈希
        
        Args:
            data: 原始数据
            
        Returns:
            哈希值
        """
        return hashlib.md5(data.encode('utf-8')).hexdigest()

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.start_time = None
        self.checkpoints = {}
    
    def start(self):
        """开始监控"""
        self.start_time = time.time()
        self.checkpoints = {}
    
    def checkpoint(self, name: str):
        """添加检查点"""
        if self.start_time is None:
            self.start_time = time.time()
        
        current_time = time.time()
        self.checkpoints[name] = current_time - self.start_time
        logger.info(f"检查点 '{name}': {self.checkpoints[name]:.2f}秒")
    
    def get_summary(self) -> Dict[str, float]:
        """获取性能摘要"""
        if not self.checkpoints:
            return {}
        
        summary = {}
        prev_time = 0
        
        for name, time_elapsed in self.checkpoints.items():
            summary[f"{name}_duration"] = time_elapsed - prev_time
            prev_time = time_elapsed
        
        summary["total_duration"] = max(self.checkpoints.values()) if self.checkpoints else 0
        return summary

# 导入asyncio用于异步操作
import asyncio
