"""
语音识别模块
使用 OpenAI Whisper 进行中文语音识别
"""

from . import config
import torch
import whisper


class SpeechRecognition:
    """语音识别器"""

    def __init__(self, model_name: str = None):
        """
        初始化语音识别器

        Args:
            model_name: Whisper 模型名称 (tiny, base, small, medium, large)
        """
        self.model_name = model_name or config.WHISPER_MODEL

        print(f"正在加载 Whisper 模型: {self.model_name}")
        print(f"使用设备: {config.DEVICE}")

        # 加载模型
        self.model = whisper.load_model(self.model_name, device=config.DEVICE)

        print("Whisper 模型加载完成!")

    def transcribe(self, audio_input, language: str = None, initial_prompt: str = None) -> str:
        """
        转录音频为文字

        Args:
            audio_input: 音频输入,可以是:
                - 文件路径 (str)
                - numpy array
                - torch.Tensor
            language: 语言代码,默认为中文 "zh"
            initial_prompt: 初始提示,用于引导模型输出简体中文

        Returns:
            识别的文本
        """
        language = language or config.WHISPER_LANGUAGE

        # 如果是 torch.Tensor,转换为 numpy array
        if isinstance(audio_input, torch.Tensor):
            audio_input = audio_input.squeeze().cpu().numpy()

        # 设置中文简体提示
        if initial_prompt is None and language == "zh":
            initial_prompt = "以下是普通话的句子。"  # 引导输出简体中文

        # 执行转录
        result = self.model.transcribe(
            audio_input, language=language, initial_prompt=initial_prompt, verbose=False
        )

        return result["text"].strip()

    def transcribe_segments(self, waveform: torch.Tensor, segments: list, sample_rate: int) -> list:
        """
        对多个音频片段进行转录

        Args:
            waveform: 完整音频波形
            segments: 片段列表,每个片段包含 start 和 end 时间
            sample_rate: 采样率

        Returns:
            带有转录文本的片段列表
        """
        from .audio_processor import AudioProcessor

        processor = AudioProcessor(sample_rate=sample_rate)
        results = []

        total = len(segments)
        for i, segment in enumerate(segments, 1):
            print(f"正在转录片段 {i}/{total} ({segment['speaker']})")

            # 提取音频片段
            audio_segment = processor.extract_segment(
                waveform, segment["start"], segment["end"], sample_rate
            )

            # 转录
            text = self.transcribe(audio_segment)

            # 添加转录结果
            result = segment.copy()
            result["text"] = text
            results.append(result)

            print(f"  [{segment['start']:.2f}s - {segment['end']:.2f}s] {text}")

        return results
