#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主程序入口文件

这个文件是项目的主要入口点，用于启动B站视频监控系统。
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path

# 导入B站视频监控模块
from bilibili_monitor import BilibiliMonitor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bilibili_monitor_main.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('main')


def load_config(config_path):
    """加载配置文件
    
    Args:
        config_path: 配置文件路径
        
    Returns:
        配置信息字典
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return {}


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='B站视频监控系统')
    parser.add_argument('--once', action='store_true', help='单次运行模式，不启动定时任务')
    parser.add_argument('--check', action='store_true', help='仅检查新视频')
    parser.add_argument('--clean', action='store_true', help='仅清理过期视频')
    args = parser.parse_args()
    
    logger.info("欢迎使用B站视频监控系统!")
    
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # 加载配置
    config_path = project_root / 'config' / 'config.json'
    config = load_config(config_path)
    
    if not config:
        logger.error("配置加载失败，程序退出")
        return
    
    # 检查必要的配置项
    if 'bilibili' not in config or not config['bilibili'].get('up_list'):
        logger.error("配置文件中缺少B站UP主列表，请在config.json中配置bilibili.up_list")
        return
    
    logger.info(f"已加载配置，监控UP主数量: {len(config['bilibili'].get('up_list', []))}")
    
    # 创建监控实例
    monitor = BilibiliMonitor(config)
    
    # 根据命令行参数执行不同操作
    if args.check:
        # 仅检查新视频
        logger.info("执行检查新视频任务")
        monitor.check_and_download_new_videos()
    elif args.clean:
        # 仅清理过期视频
        logger.info("执行清理过期视频任务")
        monitor.clean_expired_videos()
    elif args.once:
        # 单次运行模式
        logger.info("单次运行模式")
        monitor.check_and_download_new_videos()
        monitor.clean_expired_videos()
    else:
        # 定时任务模式
        logger.info("启动定时任务模式")
        monitor.run_scheduler()


if __name__ == "__main__":
    main()