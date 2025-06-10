# B站视频监控系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## 项目简介

本项目是一个B站视频监控和下载系统，可以帮助用户监控指定UP主的最新视频，自动下载并在超过保存期限后删除。

### 主要功能

- 监控指定UP主的最新视频发布
- 自动下载新发布的视频
- 设置保存期限，自动删除过期视频（默认为7天）
- 支持定时任务和单次运行模式

## 技术架构

本项目使用Python开发，主要包含以下模块：

- **监控模块**：负责检查UP主是否有新视频发布
- **下载模块**：负责下载视频文件
- **文件管理模块**：负责视频文件的存储和清理

## 目录结构

```
my-project/
├── README.md        # 项目说明文档
├── src/             # 源代码目录
│   ├── main.py              # 主程序入口
│   ├── bilibili_monitor.py  # B站视频监控模块
│   ├── bilibili_downloader.py # 视频下载模块
│   └── file_manager.py      # 文件管理模块
├── config/          # 配置文件目录
│   └── config.json          # 配置文件
├── docs/            # 文档目录
│   └── getting_started.md   # 使用指南
├── tests/           # 测试目录
└── downloads/       # 视频下载目录（默认）
```

## 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/allshota/bilibili-monitor.git
cd bilibili-monitor

# 安装依赖
pip install -r requirements.txt
```

### 配置

编辑 `config/config.json` 文件，设置要监控的UP主ID列表：

```json
{
  "bilibili": {
    "up_list": [
      "12345678",  // UP主ID
      "87654321"   // 另一个UP主ID
    ],
    "save_days": 7,  // 视频保存天数
    "download_dir": "../downloads",  // 下载目录
    "check_interval": 1  // 检查间隔（小时）
  }
}
```

### 运行

```bash
# 定时任务模式（推荐）
python src/main.py

# 单次运行模式
python src/main.py --once

# 仅检查新视频
python src/main.py --check

# 仅清理过期视频
python src/main.py --clean
```

## 详细文档

更多详细信息，请参阅 [使用指南](docs/getting_started.md)。

## 贡献

欢迎贡献代码、报告问题或提出新功能建议！请查看[贡献指南](CONTRIBUTING.md)了解更多信息。

## 注意事项

- 本项目仅用于个人学习和研究
- 请遵守B站用户协议，不要滥用下载功能
- 下载的视频版权归原作者所有，请勿用于商业用途

## 许可证

[MIT License](LICENSE)
