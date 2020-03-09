#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/9 19:45
# @Author  : JiachengXu
# @Software: PyCharm
'''

import logging

def set_logger(file_path):
	''' 配置日志'''
	logger = logging.getLogger(__name__)
	logger.setLevel(level = logging.INFO)
	handler = logging.FileHandler(file_path)
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger



