"""
说话人分离模块
使用 pyannote.audio 进行说话人分离
支持离线模式:可从本地加载模型或在线下载
"""

from pathlib import Path

from . import config
import torch
from pyannote.audio import Pipeline


class SpeakerDiarization:
    """说话人分离器"""

    def __init__(self, hf_token: str = None, offline: bool = False, local_model_path: str = None):
        """
        初始化说话人分离器

        Args:
            hf_token: Hugging Face token (在线模式需要)
            offline: 是否使用离线模式
            local_model_path: 本地模型路径(离线模式使用)
        """
        self.offline = offline

        # 确定模型目录
        if local_model_path:
            models_dir = Path(local_model_path).parent.absolute()
        else:
            models_dir = Path("models").absolute()

        # 离线模式:从项目目录加载
        if offline:
            # 检查模型目录是否存在
            if not models_dir.exists():
                raise FileNotFoundError(
                    f"离线模式下找不到模型目录: {models_dir}\n"
                    "请先运行以下命令下载模型:\n"
                    "  python download_models.py\n"
                    "或者不使用 --offline 参数以在线下载模型"
                )

            print("✓ 使用离线模式")
            print(f"模型目录: {models_dir}")
            print(f"使用设备: {config.DEVICE}")

            # 设置环境变量指向项目模型目录
            import os

            os.environ["PYANNOTE_CACHE"] = str(models_dir)
            os.environ["HF_HOME"] = str(models_dir / "huggingface")

            try:
                # 从项目目录加载(不需要 token)
                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-3.1",
                    use_auth_token=False,  # 离线模式不需要 token
                )
            except Exception as e:
                print(f"❌ 从项目目录加载模型失败: {e}")
                print()
                print("解决方案:")
                print("1. 重新下载模型: python download_models.py")
                print("2. 或使用在线模式(需要 HF_TOKEN)")
                raise

        # 在线模式:从 Hugging Face 下载
        else:
            self.hf_token = hf_token or config.HF_TOKEN

            if not self.hf_token:
                raise ValueError(
                    "在线模式需要 Hugging Face token!\n\n"
                    "方案 1 - 使用离线模式(推荐):\n"
                    "  1. 先运行: python download_models.py (需要临时联网)\n"
                    "  2. 然后使用 --offline 参数运行程序\n\n"
                    "方案 2 - 使用在线模式:\n"
                    "  1. 访问 https://huggingface.co/settings/tokens 创建 token\n"
                    "  2. 访问 https://huggingface.co/pyannote/speaker-diarization-3.1 接受协议\n"
                    "  3. 在 .env 文件中设置 HF_TOKEN=your_token"
                )

            print(f"正在加载说话人分离模型: {config.DIARIZATION_MODEL}")
            print(f"使用设备: {config.DEVICE}")

            # 加载预训练模型
            self.pipeline = Pipeline.from_pretrained(
                config.DIARIZATION_MODEL, use_auth_token=self.hf_token
            )

        # 将模型移到指定设备
        if config.DEVICE == "cuda":
            self.pipeline = self.pipeline.to(torch.device("cuda"))

        print("✓ 说话人分离模型加载完成!")

    def diarize(self, audio_path: str) -> list[dict]:
        """
        执行说话人分离

        Args:
            audio_path: 音频文件路径

        Returns:
            说话人片段列表,每个片段包含:
            - speaker: 说话人标识
            - start: 开始时间(秒)
            - end: 结束时间(秒)
        """
        print(f"开始说话人分离: {audio_path}")

        # 执行分离
        diarization = self.pipeline(audio_path)

        # 转换结果为列表格式
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({"speaker": speaker, "start": turn.start, "end": turn.end})

        # 按时间排序
        segments.sort(key=lambda x: x["start"])

        # 统计说话人数量
        speakers = {seg["speaker"] for seg in segments}
        print(f"✓ 检测到 {len(speakers)} 个说话人,共 {len(segments)} 个片段")

        return segments

    def get_speaker_statistics(self, segments: list[dict]) -> dict:
        """
        获取说话人统计信息

        Args:
            segments: 说话人片段列表

        Returns:
            统计信息字典
        """
        stats = {}

        for segment in segments:
            speaker = segment["speaker"]
            duration = segment["end"] - segment["start"]

            if speaker not in stats:
                stats[speaker] = {"total_duration": 0.0, "segment_count": 0}

            stats[speaker]["total_duration"] += duration
            stats[speaker]["segment_count"] += 1

        return stats
