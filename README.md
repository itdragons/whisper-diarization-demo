# Whisper Diarization Demo

[![CI](https://github.com/yourusername/whisper-diarization-demo/workflows/CI/badge.svg)](https://github.com/yourusername/whisper-diarization-demo/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

> 基于 **pyannote.audio** 和 **OpenAI Whisper** 的中文说话人分离和语音识别演示项目

**✨ 支持完全离线运行!**

## 功能特性

- ✅ **说话人分离**: 自动识别音频中的不同说话人
- ✅ **语音识别**: 高精度中文语音转文字
- ✅ **时间对齐**: 精确标记每个说话人的说话时间段
- ✅ **多种输出格式**: 支持 JSON、纯文本、SRT 字幕格式
- ✅ **完全离线**: 下载模型后可完全离线运行,无需网络连接
- ✅ **工程化**: 完整的测试、代码检查、CI/CD 支持

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/whisper-diarization-demo.git
cd whisper-diarization-demo
```

### 2. 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -e .
```

### 3. 下载模型(一次性操作)

**首次使用需要下载模型到本地**:

```bash
# 配置 Hugging Face Token(仅用于下载模型)
cp .env.example .env
# 编辑 .env 文件,填入您的 HF_TOKEN

# 下载模型
python scripts/download_models.py
```

> [!IMPORTANT]
> **Hugging Face Token 获取步骤**:
> 1. 访问 https://huggingface.co/settings/tokens 创建 token
> 2. 访问 https://huggingface.co/pyannote/speaker-diarization-3.1 接受模型协议
> 3. 访问 https://huggingface.co/pyannote/segmentation-3.0 接受模型协议

### 4. 离线使用

模型下载完成后,即可**完全离线**使用:

```bash
# 使用命令行工具
whisper-diarization --audio multi-speaker.wav --offline

# 或使用 Python 模块
python -m whisper_diarization --audio multi-speaker.wav --offline
```

## 使用方法

### 基本用法

```bash
# 离线模式处理音频
whisper-diarization --audio audio.wav --offline

# 指定输出文件
whisper-diarization --audio audio.wav --offline --output result.json

# 选择不同的输出格式
whisper-diarization --audio audio.wav --offline --format text
whisper-diarization --audio audio.wav --offline --format srt
```

### 选择 Whisper 模型

```bash
# 使用 large 模型获得更高准确度(速度较慢)
whisper-diarization --audio audio.wav --offline --whisper-model large

# 使用 small 模型获得更快速度(准确度较低)
whisper-diarization --audio audio.wav --offline --whisper-model small
```

### 在线模式

如果您不想下载模型,也可以使用在线模式(需要网络连接):

```bash
# 需要在 .env 中配置 HF_TOKEN
whisper-diarization --audio audio.wav
```

## 输出示例

### JSON 格式

```json
{
  "audio_file": "multi-speaker.wav",
  "duration": 120.5,
  "speakers": 2,
  "segments": [
    {
      "speaker": "SPEAKER_00",
      "start": 0.0,
      "end": 5.2,
      "text": "大家好,今天我们来讨论一下这个项目。"
    },
    {
      "speaker": "SPEAKER_01",
      "start": 5.5,
      "end": 10.8,
      "text": "好的,我认为我们应该先从需求分析开始。"
    }
  ]
}
```

### 文本格式

```
音频文件: multi-speaker.wav
总时长: 00:02:00.500
说话人数: 2
============================================================

[SPEAKER_00] 00:00:00.000 --> 00:00:05.200
大家好,今天我们来讨论一下这个项目。

[SPEAKER_01] 00:00:05.500 --> 00:00:10.800
好的,我认为我们应该先从需求分析开始。
```

## 技术栈

- **pyannote.audio 3.1+**: 说话人分离(支持离线)
- **OpenAI Whisper**: 语音识别(完全离线)
- **PyTorch 2.1**: 深度学习框架
- **torchaudio**: 音频处理

## 项目结构

```
whisper-diarization-demo/
├── src/
│   └── whisper_diarization/    # 核心包
│       ├── __init__.py
│       ├── __main__.py         # CLI 入口
│       ├── config.py           # 配置文件
│       ├── audio_processor.py  # 音频处理模块
│       ├── speaker_diarization.py  # 说话人分离模块
│       ├── speech_recognition.py   # 语音识别模块
│       └── utils/              # 工具模块
│           ├── formatters.py   # 输出格式化
│           └── logger.py       # 日志工具
├── scripts/
│   └── download_models.py      # 模型下载脚本
├── tests/                      # 测试代码
│   ├── conftest.py
│   ├── test_formatters.py
│   └── test_config.py
├── models/                     # 本地模型缓存
├── output/                     # 输出目录
├── pyproject.toml             # 项目配置
├── LICENSE                    # MIT 许可证
├── CHANGELOG.md              # 变更日志
└── README.md                 # 项目文档
```

## 技术栈

- **pyannote.audio 3.1+**: 说话人分离(支持离线)
- **OpenAI Whisper**: 语音识别(完全离线)
- **PyTorch 2.1**: 深度学习框架
- **torchaudio**: 音频处理
- **ruff**: 代码检查和格式化
- **pytest**: 测试框架
- **mypy**: 类型检查

## 性能优化

- **GPU 加速**: 如果有 NVIDIA GPU,程序会自动使用 CUDA 加速
- **模型选择**: 
  - `tiny/base`: 快速但准确度较低
  - `small`: 平衡速度和准确度
  - `medium`: 推荐用于中文(默认)
  - `large`: 最高准确度但速度最慢

## 开发指南

### 安装开发依赖

```bash
# 安装所有依赖(包括开发工具)
uv sync --all-extras
```

### 代码检查和格式化

```bash
# 检查代码风格
uv run ruff check .

# 自动修复代码问题
uv run ruff check --fix .

# 格式化代码
uv run ruff format .

# 类型检查
uv run mypy src/
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 生成覆盖率报告
uv run pytest --cov=src/whisper_diarization --cov-report=html

# 查看覆盖率报告
open htmlcov/index.html
```

### 安装 pre-commit hooks

```bash
# 安装 git hooks
uv run pre-commit install

# 手动运行 pre-commit
uv run pre-commit run --all-files
```

## 贡献指南

欢迎贡献! 请遵循以下步骤:

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

在提交 PR 前请确保:
- 所有测试通过
- 代码风格符合 ruff 规范
- 添加了必要的测试用例

## 常见问题

### 1. 如何实现完全离线?

1. 首次使用时运行 `python scripts/download_models.py` 下载模型(需要临时联网)
2. 下载完成后,使用 `--offline` 参数即可完全离线运行
3. Whisper 模型会自动缓存到 `~/.cache/whisper/`,无需额外配置

### 2. 模型下载失败怎么办?

确保:
- Hugging Face token 有效且已复制正确
- 已接受 pyannote/speaker-diarization-3.1 和 pyannote/segmentation-3.0 模型协议
- 网络连接正常

### 3. 内存不足

- 使用较小的 Whisper 模型(如 `small` 或 `base`)
- 处理较短的音频文件
- 关闭其他占用内存的程序

### 4. 识别准确度不高

- 使用更大的 Whisper 模型(如 `large`)
- 确保音频质量良好
- 检查音频语言是否为中文

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

使用的开源模型:
- pyannote.audio: MIT License
- OpenAI Whisper: MIT License

## 致谢

- [pyannote.audio](https://github.com/pyannote/pyannote-audio) - 说话人分离
- [OpenAI Whisper](https://github.com/openai/whisper) - 语音识别

