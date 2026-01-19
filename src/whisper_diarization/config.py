"""
配置文件
包含模型配置、路径配置等
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Hugging Face Token (用于 pyannote.audio)
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Whisper 模型配置
WHISPER_MODEL = "medium"  # 可选: tiny, base, small, medium, large
WHISPER_LANGUAGE = "zh"  # 中文

# pyannote.audio 模型配置
DIARIZATION_MODEL = "pyannote/speaker-diarization-3.1"

# 输出配置
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# 设备配置 (自动检测 GPU)
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# 日志配置
LOG_LEVEL = "INFO"
