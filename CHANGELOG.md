# Changelog

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added
- 初始项目工程化改造
- 采用标准 `src/` 布局
- 添加完整的 `pyproject.toml` 配置
- 集成 ruff、pytest、mypy 等开发工具
- 添加 pre-commit hooks
- 创建测试框架和基础测试用例
- 添加 LICENSE 文件

### Changed
- 项目名称从 `whisper` 改为 `whisper-diarization-demo`
- 重构代码结构，将核心逻辑移至 `src/whisper_diarization/`
- 使用日志系统替换 print 语句
- 改进 CLI 设计和帮助信息

## [0.1.0] - 2026-01-19

### Added
- 基于 pyannote.audio 和 OpenAI Whisper 的说话人分离和语音识别功能
- 支持完全离线运行
- 多种输出格式（JSON、文本、SRT）
- 中文语音识别优化
