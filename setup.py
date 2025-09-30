#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安装和设置脚本
用于快速设置工作流环境
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 错误: 需要Python 3.8或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def install_requirements():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def create_env_file():
    """创建环境变量文件"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if env_file.exists():
        print("✅ .env文件已存在")
        return True
    
    if env_example.exists():
        try:
            shutil.copy(env_example, env_file)
            print("✅ 已创建.env文件，请编辑其中的配置")
            return True
        except Exception as e:
            print(f"❌ 创建.env文件失败: {e}")
            return False
    else:
        print("❌ 找不到env.example文件")
        return False

def check_config():
    """检查配置"""
    print("🔧 检查配置...")
    
    # 检查.env文件
    if not Path(".env").exists():
        print("❌ .env文件不存在，请先运行安装脚本")
        return False
    
    # 尝试加载配置
    try:
        from config import ConfigManager
        config_manager = ConfigManager('.env')
        config = config_manager.get_config()
        print("✅ 配置检查通过")
        return True
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        print("请检查.env文件中的配置项")
        return False

def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    try:
        result = subprocess.run([sys.executable, "test_workflow.py"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ 测试通过")
            return True
        else:
            print("❌ 测试失败")
            print("错误输出:", result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print("❌ 测试超时")
        return False
    except Exception as e:
        print(f"❌ 运行测试时发生错误: {e}")
        return False

def main():
    """主函数"""
    print("🚀 小红书笔记搜索与内容处理工作流 - 安装脚本")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 安装依赖包
    if not install_requirements():
        return False
    
    # 创建环境变量文件
    if not create_env_file():
        return False
    
    print("\n" + "=" * 60)
    print("📋 安装完成！接下来的步骤:")
    print("=" * 60)
    print("1. 编辑 .env 文件，填入你的配置信息:")
    print("   - XHS_COOKIE: 小红书Cookie")
    print("   - LLM_API_KEY: DeepSeek API密钥")
    print("   - NOTION_TOKEN: Notion集成Token")
    print("   - ORIGINAL_DATABASE_ID: 原始数据库ID")
    print("   - PROCESSED_DATABASE_ID: 处理后数据库ID")
    print()
    print("2. 运行测试验证配置:")
    print("   python test_workflow.py")
    print()
    print("3. 运行主程序:")
    print("   python main.py")
    print()
    print("📖 详细说明请查看 README.md 文件")
    
    # 询问是否运行测试
    try:
        response = input("\n是否现在运行测试? (y/n): ").strip().lower()
        if response in ['y', 'yes', '是']:
            if check_config():
                run_tests()
    except KeyboardInterrupt:
        print("\n👋 安装完成，再见！")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎉 安装脚本执行完成！")
        else:
            print("\n💥 安装过程中遇到问题，请检查错误信息")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 安装被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 安装过程中发生未预期的错误: {e}")
        sys.exit(1)
