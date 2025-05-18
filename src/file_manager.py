#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文件管理模块

这个模块负责视频文件的存储和清理操作。
"""

import os
import shutil
import logging
import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('file_manager.log', encoding='utf-8')
    ]
)
logger = logging.getLogger('file_manager')


class FileManager:
    """文件管理类"""
    
    def __init__(self, base_dir):
        """初始化
        
        Args:
            base_dir: 基础目录
        """
        self.base_dir = Path(base_dir)
        
        # 确保基础目录存在
        os.makedirs(self.base_dir, exist_ok=True)
    
    def create_directory(self, dir_name):
        """创建目录
        
        Args:
            dir_name: 目录名
            
        Returns:
            目录路径
        """
        dir_path = self.base_dir / dir_name
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"创建目录: {dir_path}")
        return dir_path
    
    def save_file(self, file_path, content, mode='wb'):
        """保存文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
            mode: 写入模式
            
        Returns:
            是否保存成功
        """
        try:
            # 确保父目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, mode) as f:
                f.write(content)
            
            logger.info(f"保存文件: {file_path}")
            return True
        except Exception as e:
            logger.error(f"保存文件失败: {e}")
            return False
    
    def delete_file(self, file_path):
        """删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否删除成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"删除文件: {file_path}")
                return True
            else:
                logger.warning(f"文件不存在，无法删除: {file_path}")
                return False
        except Exception as e:
            logger.error(f"删除文件失败: {e}")
            return False
    
    def get_file_info(self, file_path):
        """获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件信息字典
        """
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            create_time = datetime.datetime.fromtimestamp(stat.st_ctime)
            modify_time = datetime.datetime.fromtimestamp(stat.st_mtime)
            size = stat.st_size
            
            return {
                'path': file_path,
                'size': size,
                'create_time': create_time,
                'modify_time': modify_time,
                'size_human': self._format_size(size)
            }
        except Exception as e:
            logger.error(f"获取文件信息失败: {e}")
            return None
    
    def _format_size(self, size_bytes):
        """格式化文件大小
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            格式化后的大小字符串
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0 or unit == 'TB':
                break
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} {unit}"
    
    def list_files(self, directory=None, pattern=None):
        """列出目录中的文件
        
        Args:
            directory: 目录路径，默认为基础目录
            pattern: 文件名匹配模式
            
        Returns:
            文件路径列表
        """
        try:
            if directory is None:
                directory = self.base_dir
            else:
                directory = Path(directory)
            
            if not directory.exists():
                logger.warning(f"目录不存在: {directory}")
                return []
            
            if pattern:
                files = list(directory.glob(pattern))
            else:
                files = [f for f in directory.iterdir() if f.is_file()]
            
            return files
        except Exception as e:
            logger.error(f"列出文件失败: {e}")
            return []
    
    def clean_expired_files(self, directory, days, pattern=None):
        """清理过期文件
        
        Args:
            directory: 目录路径
            days: 过期天数
            pattern: 文件名匹配模式
            
        Returns:
            清理的文件数量
        """
        try:
            directory = Path(directory)
            if not directory.exists():
                logger.warning(f"目录不存在，无法清理: {directory}")
                return 0
            
            now = datetime.datetime.now()
            count = 0
            
            # 获取文件列表
            files = self.list_files(directory, pattern)
            
            for file_path in files:
                file_info = self.get_file_info(file_path)
                if not file_info:
                    continue
                
                # 计算文件创建时间距今的天数
                days_old = (now - file_info['create_time']).days
                
                if days_old > days:
                    if self.delete_file(file_path):
                        count += 1
            
            logger.info(f"共清理 {count} 个过期文件")
            return count
        except Exception as e:
            logger.error(f"清理过期文件失败: {e}")
            return 0


def main():
    """测试函数"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python file_manager.py <目录> <过期天数>")
        return
    
    directory = sys.argv[1]
    days = int(sys.argv[2])
    
    manager = FileManager(directory)
    count = manager.clean_expired_files(directory, days)
    
    print(f"共清理 {count} 个过期文件")


if __name__ == "__main__":
    main()