#!/usr/bin/env python3
"""
模型下载脚本
一次性下载所需的模型到本地,之后可完全离线使用
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def download_pyannote_models():
    """下载 pyannote.audio 模型到本地"""
    print("=" * 60)
    print("下载 pyannote.audio 说话人分离模型")
    print("=" * 60)
    print()
    
    # 检查 HF_TOKEN
    load_dotenv()
    
    hf_token = os.getenv("HF_TOKEN", "")
    
    if not hf_token:
        print("❌ 错误: 需要 Hugging Face token!")
        print()
        print("请按以下步骤操作:")
        print("1. 访问 https://huggingface.co/settings/tokens 创建 token")
        print("2. 访问 https://huggingface.co/pyannote/speaker-diarization-3.1 接受模型协议")
        print("3. 访问 https://huggingface.co/pyannote/segmentation-3.0 接受模型协议")
        print("4. 创建 .env 文件并设置 HF_TOKEN=your_token")
        print()
        return False
    
    print(f"✓ 找到 Hugging Face token")
    print()
    
    # 创建模型目录
    models_dir = Path("models").absolute()
    models_dir.mkdir(exist_ok=True)
    
    # 设置环境变量,让 pyannote 和 huggingface 使用项目目录
    # 必须在导入 pyannote 之前设置
    os.environ["PYANNOTE_CACHE"] = str(models_dir)
    os.environ["HF_HOME"] = str(models_dir / "huggingface")
    
    print("开始下载模型...")
    print(f"模型将保存到: {models_dir}")
    print("提示: 这是一次性操作,下载后可完全离线使用")
    print()
    
    try:
        from pyannote.audio import Pipeline
        
        # 下载说话人分离模型
        print("[1/2] 下载说话人分离模型...")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )
        
        print(f"✓ 模型已下载到: {models_dir}")
        print()
        
        print("✓ 所有模型下载完成!")
        print()
        print("=" * 60)
        print("现在您可以完全离线使用说话人分离功能!")
        print("=" * 60)
        print()
        print("使用方法:")
        print("  python main.py --audio /path/to/audio.wav --offline")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print()
        print("请检查:")
        print("1. 网络连接是否正常")
        print("2. Hugging Face token 是否有效")
        print("3. 是否已接受模型使用协议")
        return False


def download_whisper_models():
    """下载 Whisper 模型"""
    print("=" * 60)
    print("下载 Whisper 语音识别模型")
    print("=" * 60)
    print()
    
    try:
        import whisper
        
        # 下载 medium 模型
        print("下载 Whisper medium 模型 (约 1.5GB)...")
        print("提示: 模型会自动缓存到 ~/.cache/whisper/")
        print()
        
        model = whisper.load_model("medium")
        
        print("✓ Whisper 模型下载完成!")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def main():
    print()
    print("🚀 模型下载工具")
    print()
    print("此工具将下载所需的模型到本地,之后可完全离线使用。")
    print()
    
    # 下载 Whisper 模型
    # if not download_whisper_models():
    #     sys.exit(1)
    
    # print()
    
    # 下载 pyannote 模型
    if not download_pyannote_models():
        sys.exit(1)
    
    print()
    print("🎉 所有模型下载完成!")
    print()


if __name__ == "__main__":
    main()
