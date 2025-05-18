#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站视频监控和下载系统

这个模块用于监控指定UP主的最新视频，自动下载并在超过保存期限后删除。
"""

import os
import sys
import json
import time
import datetime
import requests
import logging
from pathlib import Path
import schedule
import shutil

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bilibili_monitor.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('bilibili_monitor')


class BilibiliMonitor:
    """B站视频监控类"""
    
    def __init__(self, config):
        """初始化
        
        Args:
            config: 配置信息字典
        """
        self.config = config
        self.up_list = config.get('bilibili', {}).get('up_list', [])
        self.save_days = config.get('bilibili', {}).get('save_days', 7)
        self.download_dir = Path(config.get('bilibili', {}).get('download_dir', 'downloads'))
        self.video_info_file = self.download_dir / 'video_info.json'
        
        # 确保下载目录存在
        os.makedirs(self.download_dir, exist_ok=True)
        
        # 加载已下载视频信息
        self.downloaded_videos = self._load_downloaded_videos()
        
    def _load_downloaded_videos(self):
        """加载已下载视频信息"""
        if not self.video_info_file.exists():
            return {}
            
        try:
            with open(self.video_info_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"加载视频信息文件失败: {e}")
            return {}
    
    def _save_downloaded_videos(self):
        """保存已下载视频信息"""
        try:
            with open(self.video_info_file, 'w', encoding='utf-8') as f:
                json.dump(self.downloaded_videos, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存视频信息文件失败: {e}")
    
    def get_up_latest_videos(self, up_mid):
        """获取UP主最新视频
        
        Args:
            up_mid: UP主的用户ID
            
        Returns:
            最新视频列表
        """
        try:
            # B站API获取UP主视频列表
            url = f"https://api.bilibili.com/x/space/arc/search?mid={up_mid}&ps=10&pn=1"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            data = response.json()
            
            if data['code'] != 0:
                logger.error(f"获取UP主视频列表失败: {data['message']}")
                return []
            
            videos = data['data']['list']['vlist']
            return videos
        except Exception as e:
            logger.error(f"获取UP主视频列表异常: {e}")
            return []
    
    def download_video(self, video):
        """下载视频
        
        Args:
            video: 视频信息
            
        Returns:
            是否下载成功
        """
        try:
            video_id = video['bvid']
            video_title = video['title']
            up_name = video['author']
            
            # 创建UP主目录
            up_dir = self.download_dir / up_name
            os.makedirs(up_dir, exist_ok=True)
            
            # 视频文件名
            video_filename = f"{video_title}_{video_id}.mp4"
            video_path = up_dir / video_filename
            
            # 如果已经下载过，跳过
            if video_id in self.downloaded_videos:
                logger.info(f"视频已下载过: {video_title}")
                return True
            
            # 这里使用you-get或其他工具下载视频
            # 实际使用时需要替换为真实的下载逻辑
            logger.info(f"开始下载视频: {video_title}")
            
            # 模拟下载过程
            # 实际项目中，可以使用subprocess调用you-get或其他下载工具
            # 例如: subprocess.run(['you-get', '-o', str(up_dir), f'https://www.bilibili.com/video/{video_id}'])
            time.sleep(2)  # 模拟下载时间
            
            # 记录下载信息
            download_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.downloaded_videos[video_id] = {
                'title': video_title,
                'up_name': up_name,
                'download_time': download_time,
                'path': str(video_path)
            }
            self._save_downloaded_videos()
            
            logger.info(f"视频下载完成: {video_title}")
            return True
        except Exception as e:
            logger.error(f"下载视频失败: {e}")
            return False
    
    def check_and_download_new_videos(self):
        """检查并下载新视频"""
        for up_mid in self.up_list:
            logger.info(f"检查UP主 {up_mid} 的最新视频")
            videos = self.get_up_latest_videos(up_mid)
            
            for video in videos:
                video_id = video['bvid']
                if video_id not in self.downloaded_videos:
                    logger.info(f"发现新视频: {video['title']}")
                    self.download_video(video)
    
    def clean_expired_videos(self):
        """清理过期视频"""
        now = datetime.datetime.now()
        expired_videos = []
        
        for video_id, info in list(self.downloaded_videos.items()):
            download_time = datetime.datetime.strptime(info['download_time'], '%Y-%m-%d %H:%M:%S')
            days_passed = (now - download_time).days
            
            if days_passed > self.save_days:
                logger.info(f"视频超过保存期限({self.save_days}天): {info['title']}")
                
                # 删除视频文件
                video_path = Path(info['path'])
                if video_path.exists():
                    try:
                        os.remove(video_path)
                        logger.info(f"已删除视频文件: {video_path}")
                    except Exception as e:
                        logger.error(f"删除视频文件失败: {e}")
                
                # 从记录中移除
                expired_videos.append(video_id)
        
        # 更新记录
        for video_id in expired_videos:
            del self.downloaded_videos[video_id]
        
        if expired_videos:
            self._save_downloaded_videos()
            logger.info(f"共清理 {len(expired_videos)} 个过期视频")
    
    def run_scheduler(self):
        """运行定时任务"""
        # 每小时检查新视频
        schedule.every(1).hours.do(self.check_and_download_new_videos)
        
        # 每天凌晨2点清理过期视频
        schedule.every().day.at("02:00").do(self.clean_expired_videos)
        
        logger.info("B站视频监控服务已启动")
        
        while True:
            schedule.run_pending()
            time.sleep(60)


def main():
    """主函数"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent
    
    # 加载配置
    config_path = project_root / 'config' / 'config.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        logger.error(f"加载配置文件失败: {e}")
        return
    
    # 启动监控
    monitor = BilibiliMonitor(config)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # 单次运行模式
        monitor.check_and_download_new_videos()
        monitor.clean_expired_videos()
    else:
        # 定时任务模式
        monitor.run_scheduler()


if __name__ == "__main__":
    main()