#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站视频下载模块

这个模块负责实际的视频下载功能，使用you-get作为下载工具。
"""

import os
import sys
import json
import time
import logging
import subprocess
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bilibili_downloader.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('bilibili_downloader')


class BilibiliDownloader:
    """B站视频下载器"""
    
    def __init__(self, download_dir):
        """初始化
        
        Args:
            download_dir: 下载目录
        """
        self.download_dir = Path(download_dir)
        
        # 确保下载目录存在
        os.makedirs(self.download_dir, exist_ok=True)
    
    def check_you_get(self):
        """检查you-get是否已安装"""
        try:
            result = subprocess.run(['you-get', '--version'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
            if result.returncode == 0:
                logger.info(f"you-get版本: {result.stdout.strip()}")
                return True
            else:
                logger.error("you-get未安装或无法运行")
                return False
        except Exception as e:
            logger.error(f"检查you-get失败: {e}")
            return False
    
    def install_you_get(self):
        """安装you-get"""
        try:
            logger.info("正在安装you-get...")
            result = subprocess.run(['pip', 'install', 'you-get'], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   text=True)
            if result.returncode == 0:
                logger.info("you-get安装成功")
                return True
            else:
                logger.error(f"you-get安装失败: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"安装you-get异常: {e}")
            return False
    
    def download_video(self, video_id, up_name):
        """下载视频
        
        Args:
            video_id: 视频ID (BV号)
            up_name: UP主名称
            
        Returns:
            下载结果信息字典
        """
        try:
            # 检查you-get是否已安装
            if not self.check_you_get():
                if not self.install_you_get():
                    return {
                        'success': False,
                        'message': 'you-get未安装且安装失败'
                    }
            
            # 创建UP主目录
            up_dir = self.download_dir / up_name
            os.makedirs(up_dir, exist_ok=True)
            
            # 构建视频URL
            video_url = f"https://www.bilibili.com/video/{video_id}"
            
            logger.info(f"开始下载视频: {video_url}")
            
            # 使用you-get下载视频
            result = subprocess.run(
                ['you-get', '-o', str(up_dir), video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"视频下载成功: {video_id}")
                
                # 查找下载的文件
                downloaded_files = list(up_dir.glob(f"*{video_id}*"))
                if downloaded_files:
                    file_path = downloaded_files[0]
                    return {
                        'success': True,
                        'message': '下载成功',
                        'file_path': str(file_path)
                    }
                else:
                    return {
                        'success': True,
                        'message': '下载成功，但无法找到下载的文件',
                        'file_path': None
                    }
            else:
                logger.error(f"视频下载失败: {result.stderr}")
                return {
                    'success': False,
                    'message': f'下载失败: {result.stderr}'
                }
                
        except Exception as e:
            logger.error(f"下载视频异常: {e}")
            return {
                'success': False,
                'message': f'下载异常: {str(e)}'
            }
    
    def get_video_info(self, video_id):
        """获取视频信息
        
        Args:
            video_id: 视频ID (BV号)
            
        Returns:
            视频信息字典
        """
        try:
            # 构建视频URL
            video_url = f"https://www.bilibili.com/video/{video_id}"
            
            # 使用you-get获取视频信息
            result = subprocess.run(
                ['you-get', '-i', video_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                info_text = result.stdout
                
                # 解析视频信息
                title = None
                for line in info_text.split('\n'):
                    if 'Title:' in line:
                        title = line.split('Title:')[1].strip()
                        break
                
                return {
                    'success': True,
                    'title': title,
                    'info': info_text
                }
            else:
                logger.error(f"获取视频信息失败: {result.stderr}")
                return {
                    'success': False,
                    'message': f'获取视频信息失败: {result.stderr}'
                }
        except Exception as e:
            logger.error(f"获取视频信息异常: {e}")
            return {
                'success': False,
                'message': f'获取视频信息异常: {str(e)}'
            }


def main():
    """测试函数"""
    if len(sys.argv) < 2:
        print("用法: python bilibili_downloader.py <BV号> [UP主名称]")
        return
    
    video_id = sys.argv[1]
    up_name = sys.argv[2] if len(sys.argv) > 2 else "测试UP主"
    
    downloader = BilibiliDownloader("../downloads")
    
    # 获取视频信息
    info_result = downloader.get_video_info(video_id)
    if info_result['success']:
        print(f"视频标题: {info_result.get('title')}")
    
    # 下载视频
    result = downloader.download_video(video_id, up_name)
    print(result)


if __name__ == "__main__":
    main()