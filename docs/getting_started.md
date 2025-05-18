# 开始使用

本文档将指导您如何开始使用B站视频监控系统。

## 功能介绍

B站视频监控系统可以帮助您：

1. 监控指定UP主的最新视频发布
2. 自动下载新发布的视频
3. 设置保存期限，自动删除过期视频（默认为7天）

## 环境要求

- Python 3.6+
- pip（Python包管理器）
- 网络连接（用于访问B站API和下载视频）

## 安装步骤

1. 克隆或下载项目到本地

2. 安装依赖包
   ```bash
   cd my-project
   pip install -r requirements.txt
   ```

3. 配置项目
   - 修改 `config/config.json` 文件中的 `bilibili` 部分：
     - `up_list`: 设置要监控的UP主ID列表
     - `save_days`: 视频保存天数（默认7天）
     - `download_dir`: 视频下载目录
     - `check_interval`: 检查新视频的时间间隔（小时）

## 运行项目

### 定时任务模式（推荐）

```bash
python src/main.py
```

这将启动定时任务，按照配置的时间间隔自动检查新视频并下载，同时定期清理过期视频。

### 单次运行模式

```bash
python src/main.py --once
```

这将执行一次检查和清理操作，然后退出程序。

### 其他运行选项

- 仅检查新视频：`python src/main.py --check`
- 仅清理过期视频：`python src/main.py --clean`

## 项目结构说明

- `src/`: 源代码目录
  - `main.py`: 主程序入口
  - `bilibili_monitor.py`: B站视频监控模块
  - `bilibili_downloader.py`: 视频下载模块
  - `file_manager.py`: 文件管理模块
- `config/`: 配置文件目录
  - `config.json`: 主配置文件
- `docs/`: 文档目录
- `tests/`: 测试目录
- `downloads/`: 视频下载目录（默认）

## 常见问题

### Q: 如何添加更多UP主？
A: 在 `config/config.json` 文件中的 `bilibili.up_list` 数组中添加UP主ID。

### Q: 如何修改视频保存时间？
A: 在 `config/config.json` 文件中修改 `bilibili.save_days` 值，单位为天。

### Q: 如何查找UP主ID？
A: 访问UP主的B站个人空间页面，URL中的数字部分就是UP主ID。例如：https://space.bilibili.com/12345678 中的 12345678 就是UP主ID。

### Q: 下载的视频保存在哪里？
A: 默认保存在项目根目录下的 `downloads` 文件夹中，按UP主名称分类存储。您可以在配置文件中修改 `bilibili.download_dir` 来更改保存位置。