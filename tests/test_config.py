"""测试配置模块"""

from whisper_diarization import config


def test_config_values():
    """测试配置值"""
    assert hasattr(config, "WHISPER_MODEL")
    assert hasattr(config, "WHISPER_LANGUAGE")
    assert hasattr(config, "DEVICE")
    assert hasattr(config, "OUTPUT_DIR")

    # 验证默认值
    assert config.WHISPER_LANGUAGE == "zh"
    assert config.DEVICE in ["cuda", "cpu"]
