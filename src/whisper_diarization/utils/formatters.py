"""
输出格式化工具
提供时间格式化和多种输出格式支持
"""

import json
from pathlib import Path
from typing import Any


def format_time(seconds: float) -> str:
    """
    格式化时间为 HH:MM:SS.mmm 格式

    Args:
        seconds: 秒数

    Returns:
        格式化后的时间字符串

    Examples:
        >>> format_time(65.5)
        '00:01:05.500'
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def save_json(data: dict[str, Any], output_path: Path) -> None:
    """
    保存为 JSON 格式

    Args:
        data: 要保存的数据
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_text(data: dict[str, Any], output_path: Path) -> None:
    """
    保存为纯文本格式

    Args:
        data: 要保存的数据
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"音频文件: {data['audio_file']}\n")
        f.write(f"总时长: {format_time(data['duration'])}\n")
        f.write(f"说话人数: {data['speakers']}\n")
        f.write("=" * 60 + "\n\n")

        for segment in data["segments"]:
            f.write(f"[{segment['speaker']}] ")
            f.write(f"{format_time(segment['start'])} --> {format_time(segment['end'])}\n")
            f.write(f"{segment['text']}\n\n")


def save_srt(data: dict[str, Any], output_path: Path) -> None:
    """
    保存为 SRT 字幕格式

    Args:
        data: 要保存的数据
        output_path: 输出文件路径
    """
    with open(output_path, "w", encoding="utf-8") as f:
        for i, segment in enumerate(data["segments"], 1):
            # 序号
            f.write(f"{i}\n")

            # 时间轴 (SRT 格式: HH:MM:SS,mmm)
            start = format_time(segment["start"]).replace(".", ",")
            end = format_time(segment["end"]).replace(".", ",")
            f.write(f"{start} --> {end}\n")

            # 文本 (包含说话人标识)
            f.write(f"[{segment['speaker']}] {segment['text']}\n\n")
