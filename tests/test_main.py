#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
主程序测试文件

这个文件包含了对主程序功能的测试用例。
"""

import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到系统路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import load_config


class TestMain(unittest.TestCase):
    """测试主程序功能"""
    
    def setUp(self):
        """测试前准备"""
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / 'config' / 'config.json'
    
    def test_load_config(self):
        """测试配置加载功能"""
        config = load_config(self.config_path)
        self.assertIsInstance(config, dict)
        self.assertIn('app_name', config)
        self.assertEqual(config['app_name'], '我的新项目')


if __name__ == '__main__':
    unittest.main()