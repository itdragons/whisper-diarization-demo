"""
音频处理模块
负责音频加载、格式转换和分段处理
"""

from pathlib import Path

import torch
import torchaudio


class AudioProcessor:
    """音频处理器"""

    def __init__(self, sample_rate: int = 16000):
        """
        初始化音频处理器

        Args:
            sample_rate: 目标采样率,Whisper 使用 16kHz
        """
        self.sample_rate = sample_rate

    def load_audio(self, audio_path: str) -> tuple[torch.Tensor, int]:
        """
        加载音频文件

        Args:
            audio_path: 音频文件路径

        Returns:
            (waveform, sample_rate): 音频波形和采样率
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")

        # 加载音频
        waveform, sr = torchaudio.load(str(audio_path))

        # 转换为单声道
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        # 重采样到目标采样率
        if sr != self.sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.sample_rate)
            waveform = resampler(waveform)

        return waveform, self.sample_rate

    def extract_segment(
        self, waveform: torch.Tensor, start: float, end: float, sample_rate: int
    ) -> torch.Tensor:
        """
        提取音频片段

        Args:
            waveform: 完整音频波形
            start: 开始时间(秒)
            end: 结束时间(秒)
            sample_rate: 采样率

        Returns:
            音频片段
        """
        start_sample = int(start * sample_rate)
        end_sample = int(end * sample_rate)

        # 确保索引在有效范围内
        start_sample = max(0, start_sample)
        end_sample = min(waveform.shape[1], end_sample)

        return waveform[:, start_sample:end_sample]

    def get_duration(self, waveform: torch.Tensor, sample_rate: int) -> float:
        """
        获取音频时长

        Args:
            waveform: 音频波形
            sample_rate: 采样率

        Returns:
            时长(秒)
        """
        return waveform.shape[1] / sample_rate

    def save_segment(self, waveform: torch.Tensor, output_path: str, sample_rate: int):
        """
        保存音频片段

        Args:
            waveform: 音频波形
            output_path: 输出路径
            sample_rate: 采样率
        """
        torchaudio.save(output_path, waveform, sample_rate)
