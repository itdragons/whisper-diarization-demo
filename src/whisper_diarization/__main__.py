"""
命令行接口主入口
整合说话人分离和语音识别功能
"""

import os
import warnings

# 禁用 NNPACK 以避免警告
os.environ["OMP_NUM_THREADS"] = "1"

# 过滤第三方库的弃用警告
warnings.filterwarnings(
    "ignore", category=UserWarning, module="pyannote.audio.pipelines.speaker_verification"
)
warnings.filterwarnings(
    "ignore", category=UserWarning, module="pyannote.audio.tasks.segmentation.mixins"
)
warnings.filterwarnings("ignore", category=UserWarning, module="torch._utils")
warnings.filterwarnings("ignore", category=UserWarning, message=".*FP16 is not supported on CPU.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*TypedStorage is deprecated.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*torchaudio.*")
warnings.filterwarnings("ignore", category=UserWarning, message=".*speechbrain.*")
warnings.filterwarnings("ignore", message=".*NNPACK.*")

import argparse
from datetime import datetime
from pathlib import Path

from . import config
from .audio_processor import AudioProcessor
from .speaker_diarization import SpeakerDiarization
from .speech_recognition import SpeechRecognition
from .utils.formatters import format_time, save_json, save_srt, save_text
from .utils.logger import setup_logger


def main() -> None:
    """主函数 - 命令行入口"""
    logger = setup_logger()

    parser = argparse.ArgumentParser(
        description="中文说话人分离和语音识别工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 离线模式处理音频
  python -m whisper_diarization --audio audio.wav --offline
  
  # 指定输出格式
  python -m whisper_diarization --audio audio.wav --offline --format srt
  
  # 使用更大的 Whisper 模型
  python -m whisper_diarization --audio audio.wav --offline --whisper-model large
        """,
    )

    parser.add_argument("--audio", required=True, help="输入音频文件路径")
    parser.add_argument("--output", default=None, help="输出文件路径,默认保存到 output 目录")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="使用离线模式(需要先运行 scripts/download_models.py 下载模型)",
    )
    parser.add_argument(
        "--hf-token",
        default=None,
        help="Hugging Face token (在线模式需要,也可以在 .env 文件中设置)",
    )
    parser.add_argument(
        "--whisper-model",
        default=config.WHISPER_MODEL,
        choices=["tiny", "base", "small", "medium", "large"],
        help=f"Whisper 模型大小 (默认: {config.WHISPER_MODEL})",
    )
    parser.add_argument(
        "--format", default="json", choices=["json", "text", "srt"], help="输出格式 (默认: json)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="日志级别 (默认: INFO)",
    )

    args = parser.parse_args()

    # 更新日志级别
    logger.setLevel(args.log_level)

    # 验证音频文件
    audio_path = Path(args.audio)
    if not audio_path.exists():
        logger.error(f"音频文件不存在: {audio_path}")
        return

    logger.info("=" * 60)
    logger.info("中文说话人分离和语音识别")
    logger.info("=" * 60)
    logger.info(f"音频文件: {audio_path}")
    logger.info(f"运行模式: {'离线模式' if args.offline else '在线模式'}")
    logger.info(f"Whisper 模型: {args.whisper_model}")
    logger.info(f"设备: {config.DEVICE}")
    logger.info("=" * 60)

    try:
        # 1. 加载音频
        logger.info("[1/4] 加载音频文件...")
        processor = AudioProcessor()
        waveform, sample_rate = processor.load_audio(str(audio_path))
        duration = processor.get_duration(waveform, sample_rate)
        logger.info(f"音频时长: {format_time(duration)}")

        # 2. 说话人分离
        logger.info("[2/4] 执行说话人分离...")
        diarizer = SpeakerDiarization(hf_token=args.hf_token, offline=args.offline)
        segments = diarizer.diarize(str(audio_path))

        # 显示统计信息
        stats = diarizer.get_speaker_statistics(segments)
        logger.info("说话人统计:")
        for speaker, info in stats.items():
            logger.info(
                f"  {speaker}: {info['segment_count']} 个片段, "
                f"总时长 {format_time(info['total_duration'])}"
            )

        # 3. 语音识别
        logger.info("[3/4] 执行语音识别...")
        recognizer = SpeechRecognition(model_name=args.whisper_model)
        results = recognizer.transcribe_segments(waveform, segments, sample_rate)

        # 4. 保存结果
        logger.info("[4/4] 保存结果...")

        # 准备输出数据
        output_data = {
            "audio_file": str(audio_path.absolute()),
            "duration": duration,
            "speakers": len(stats),
            "segments": results,
            "statistics": stats,
            "timestamp": datetime.now().isoformat(),
        }

        # 确定输出路径
        if args.output:
            output_path = Path(args.output)
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = config.OUTPUT_DIR / f"result_{timestamp}.{args.format}"

        # 根据格式保存
        if args.format == "json":
            save_json(output_data, output_path)
        elif args.format == "text":
            save_text(output_data, output_path)
        elif args.format == "srt":
            save_srt(output_data, output_path)

        logger.info(f"结果已保存到: {output_path}")
        logger.info("处理完成!")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"处理过程中发生错误: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
