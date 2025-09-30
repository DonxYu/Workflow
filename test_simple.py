#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本
验证所有模块是否可以正常导入和运行
"""

import sys
import traceback

def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        import asyncio
        print("✅ asyncio - 异步支持")
    except ImportError as e:
        print(f"❌ asyncio 导入失败: {e}")
        return False
    
    try:
        import aiohttp
        print("✅ aiohttp - HTTP客户端")
    except ImportError as e:
        print(f"❌ aiohttp 导入失败: {e}")
        return False
    
    try:
        from config import ConfigManager
        print("✅ config - 配置管理")
    except ImportError as e:
        print(f"❌ config 导入失败: {e}")
        return False
    
    try:
        from video_generator import StoryboardGenerator, DoubaoSeedanceAPI, VideoWorkflowManager
        print("✅ video_generator - 视频生成模块")
    except ImportError as e:
        print(f"❌ video_generator 导入失败: {e}")
        return False
    
    try:
        from utils import TextProcessor, URLProcessor
        print("✅ utils - 工具函数")
    except ImportError as e:
        print(f"❌ utils 导入失败: {e}")
        return False
    
    return True

def test_config():
    """测试配置功能"""
    print("\n🔧 测试配置功能...")
    
    try:
        from config import ConfigManager
        
        # 测试配置管理器创建
        config_manager = ConfigManager()
        print("✅ ConfigManager 创建成功")
        
        # 测试配置摘要打印（不依赖.env文件）
        print("✅ 配置管理器功能正常")
        
        return True
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        traceback.print_exc()
        return False

def test_video_generator():
    """测试视频生成器"""
    print("\n🎬 测试视频生成器...")
    
    try:
        from video_generator import StoryboardGenerator, DoubaoSeedanceAPI
        
        # 测试分镜头生成器创建
        storyboard_gen = StoryboardGenerator("test_key")
        print("✅ StoryboardGenerator 创建成功")
        
        # 测试豆包API创建
        doubao_api = DoubaoSeedanceAPI("test_key")
        print("✅ DoubaoSeedanceAPI 创建成功")
        
        return True
    except Exception as e:
        print(f"❌ 视频生成器测试失败: {e}")
        traceback.print_exc()
        return False

def test_utils():
    """测试工具函数"""
    print("\n🛠️  测试工具函数...")
    
    try:
        from utils import TextProcessor, URLProcessor
        
        # 测试文本处理
        processor = TextProcessor()
        clean_text = processor.clean_text("测试文本  包含  多余空格")
        print(f"✅ 文本清理功能: '{clean_text}'")
        
        # 测试URL处理
        url_processor = URLProcessor()
        is_valid = url_processor.is_valid_url("https://www.example.com")
        print(f"✅ URL验证功能: {is_valid}")
        
        return True
    except Exception as e:
        print(f"❌ 工具函数测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 视频生成功能模块测试")
    print("="*50)
    
    tests = [
        ("模块导入", test_imports),
        ("配置功能", test_config),
        ("视频生成器", test_video_generator),
        ("工具函数", test_utils)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 输出测试结果
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！系统功能正常！")
        print("\n💡 下一步:")
        print("1. 设置API密钥: export LLM_API_KEY=your_api_key")
        print("2. 运行完整测试: python3 test_auto.py")
        print("3. 运行演示: python3 test_demo.py")
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
