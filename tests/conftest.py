"""测试配置和共享 fixtures"""

from pathlib import Path

import pytest


@pytest.fixture
def sample_audio_path():
    """返回测试音频文件路径"""
    return Path(__file__).parent.parent / "multi-speaker.wav"


@pytest.fixture
def output_dir(tmp_path):
    """返回临时输出目录"""
    output_path = tmp_path / "output"
    output_path.mkdir(exist_ok=True)
    return output_path
