"""
Whisper Diarization Demo - 中文说话人分离和语音识别

一个完全离线的中文说话人分离和语音识别演示项目。
基于 pyannote.audio 和 OpenAI Whisper。
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from .audio_processor import AudioProcessor
from .speaker_diarization import SpeakerDiarization
from .speech_recognition import SpeechRecognition

__all__ = [
    "AudioProcessor",
    "SpeakerDiarization",
    "SpeechRecognition",
]
