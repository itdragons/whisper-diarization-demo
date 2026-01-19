"""测试格式化工具"""

from whisper_diarization.utils.formatters import format_time, save_json, save_srt, save_text


def test_format_time():
    """测试时间格式化"""
    assert format_time(0) == "00:00:00.000"
    assert format_time(65.5) == "00:01:05.500"
    assert format_time(3661.123) == "01:01:01.123"


def test_save_json(output_dir):
    """测试 JSON 格式保存"""
    test_data = {
        "audio_file": "/test/audio.wav",
        "duration": 120.5,
        "speakers": 2,
        "segments": [{"speaker": "SPEAKER_00", "start": 0.0, "end": 5.0, "text": "测试文本"}],
    }

    output_path = output_dir / "test.json"
    save_json(test_data, output_path)

    assert output_path.exists()

    # 验证能正确读取
    import json

    with open(output_path) as f:
        loaded_data = json.load(f)
    assert loaded_data == test_data


def test_save_text(output_dir):
    """测试文本格式保存"""
    test_data = {
        "audio_file": "/test/audio.wav",
        "duration": 120.5,
        "speakers": 2,
        "segments": [{"speaker": "SPEAKER_00", "start": 0.0, "end": 5.0, "text": "测试文本"}],
    }

    output_path = output_dir / "test.txt"
    save_text(test_data, output_path)

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert "音频文件" in content
    assert "SPEAKER_00" in content
    assert "测试文本" in content


def test_save_srt(output_dir):
    """测试 SRT 格式保存"""
    test_data = {
        "audio_file": "/test/audio.wav",
        "duration": 120.5,
        "speakers": 2,
        "segments": [
            {"speaker": "SPEAKER_00", "start": 0.0, "end": 5.0, "text": "测试文本"},
            {"speaker": "SPEAKER_01", "start": 5.5, "end": 10.0, "text": "第二段文本"},
        ],
    }

    output_path = output_dir / "test.srt"
    save_srt(test_data, output_path)

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")

    # 验证 SRT 格式
    assert "1\n" in content
    assert "2\n" in content
    assert "00:00:00,000 --> 00:00:05,000" in content
    assert "[SPEAKER_00]" in content
    assert "测试文本" in content
