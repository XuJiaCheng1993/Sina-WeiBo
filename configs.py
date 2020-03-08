#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/7 11:53
# @Author  : JiachengXu
# @Software: PyCharm
'''

import os
import configparser

config_file_path = '../SinaWeiBoCache'

## 读取配置文件
cf = configparser.ConfigParser()
cf.read(os.path.join(config_file_path, 'config.ini'))

## 信息的保存位置
path_cookie = os.path.join(config_file_path, cf.get('Path', 'cookie'))
path_message = os.path.join(config_file_path, cf.get('Path', 'message'))

## 微博账号的用户名和密码
username = cf.get('Acc', 'username')
password = cf.get('Acc', 'password')

## 爬取对象的url/月份
targets = cf.get('Objects', 'target').split('&&')
months = cf.get('Objects', 'months')

## 邮箱的授权码、发送、接收
email_code = cf.get('Email', 'password')
email_host = cf.get('Email', 'host')
delivery = cf.get('Email', 'delivery')
receipt = cf.get('Email', 'receipt')

