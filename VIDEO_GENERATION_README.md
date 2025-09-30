# 视频生成功能使用指南

## 功能概述

本功能在小红书仿写工作流的基础上，新增了视频生成能力：

1. **分镜头生成**：基于小红书仿写内容，使用LLM生成多个8秒左右的分镜头脚本
2. **视频制作**：调用豆包Seedance模型，为每个分镜头生成对应的视频文件

## 新增配置项

在 `.env` 文件中需要添加以下配置：

```bash
# 豆包Seedance视频生成配置
DOUBAO_API_KEY=your_doubao_seedance_api_key_here
DOUBAO_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

# 视频生成配置
VIDEO_OUTPUT_DIR=videos
DEFAULT_SCENE_COUNT=3
VIDEO_RESOLUTION=720p
VIDEO_STYLE=realistic
```

## 配置说明

### 必需配置

- `DOUBAO_API_KEY`: 豆包Seedance API密钥
  - 获取方法：访问豆包开放平台申请API Key

### 可选配置

- `DOUBAO_BASE_URL`: 豆包Seedance API基础URL（默认值已设置）
- `VIDEO_OUTPUT_DIR`: 视频输出目录（默认：videos）
- `DEFAULT_SCENE_COUNT`: 默认分镜头数量（默认：3）
- `VIDEO_RESOLUTION`: 视频分辨率（默认：720p，可选：720p, 1080p）
- `VIDEO_STYLE`: 视频风格（默认：realistic，可选：realistic, animated, artistic）

## 使用方法

### 1. 完整工作流（包含视频生成）

运行主程序，视频生成会自动集成到小红书仿写工作流中：

```bash
python main.py
```

### 2. 独立测试视频生成功能

```bash
python test_video_generation.py
```

测试脚本提供两种模式：
- 完整视频生成测试（包含分镜头生成和视频生成）
- 仅分镜头生成测试

## 工作流程

1. **小红书内容搜索和仿写**（原有功能）
2. **分镜头脚本生成**（新增）
   - 基于仿写内容，使用LLM生成3个8秒分镜头
   - 每个分镜头包含：标题、描述、视觉元素、文本覆盖、背景音乐、转场效果
3. **视频生成**（新增）
   - 调用豆包Seedance API为每个分镜头生成视频
   - 视频保存到指定目录
4. **结果存储**（原有功能，新增视频信息）

## 输出结果

### 分镜头脚本示例

```json
{
  "scenes": [
    {
      "scene_id": "scene_1",
      "scene_title": "开场引入",
      "scene_description": "详细描述这个分镜头的视觉内容、动作、场景设置等",
      "duration": 8,
      "visual_elements": ["元素1", "元素2", "元素3"],
      "text_overlay": "屏幕上显示的主要文字内容",
      "background_music": "背景音乐风格描述",
      "transition_effect": "转场效果描述"
    }
  ]
}
```

### 视频生成结果

```json
{
  "success": true,
  "message": "成功生成 3 个视频，失败 0 个",
  "total_scenes": 3,
  "successful_videos": 3,
  "failed_videos": 0,
  "scenes": [...],
  "video_results": [
    {
      "scene_id": "scene_1",
      "status": "success",
      "video_url": "https://example.com/video1.mp4",
      "video_path": "videos/scene_1_20241201_143022.mp4",
      "generation_time": 45.2
    }
  ]
}
```

## 文件结构

```
Workflow/
├── main.py                    # 主程序（已集成视频生成）
├── video_generator.py         # 视频生成模块
├── test_video_generation.py   # 视频生成测试脚本
├── config.py                  # 配置管理（已更新）
├── env.example               # 环境变量示例（已更新）
├── videos/                   # 视频输出目录（自动创建）
│   ├── scene_1_20241201_143022.mp4
│   ├── scene_2_20241201_143025.mp4
│   └── scene_3_20241201_143028.mp4
└── ...
```

## 注意事项

1. **API密钥**：确保豆包Seedance API密钥有效且有足够的配额
2. **网络连接**：视频生成需要稳定的网络连接
3. **存储空间**：确保有足够的磁盘空间存储生成的视频文件
4. **处理时间**：视频生成需要较长时间，请耐心等待
5. **错误处理**：如果某个分镜头视频生成失败，不会影响其他分镜头的生成

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查API密钥是否正确
   - 确认API配额是否充足
   - 检查网络连接

2. **分镜头生成失败**
   - 检查LLM API配置
   - 确认输入内容格式正确

3. **视频下载失败**
   - 检查输出目录权限
   - 确认磁盘空间充足

### 日志查看

程序运行时会输出详细的日志信息，包括：
- 分镜头生成进度
- 视频生成状态
- 错误信息和调试信息

## 扩展功能

可以根据需要扩展以下功能：

1. **视频后处理**：添加字幕、水印、特效等
2. **视频合并**：将多个分镜头合并为完整视频
3. **多风格支持**：支持更多视频风格和分辨率
4. **批量处理**：支持批量处理多个内容
5. **视频预览**：生成视频缩略图或预览

## 技术支持

如有问题，请检查：
1. 配置文件是否正确
2. API密钥是否有效
3. 网络连接是否正常
4. 日志文件中的错误信息
