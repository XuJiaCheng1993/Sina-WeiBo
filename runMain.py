#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/8 11:41
# @Author  : JiachengXu
# @Software: PyCharm
'''

import os
import datetime
from spider import spider, item
from amails import send_email
from configs import targets, months, path_message
import time


def rumMain(now):
    message_file_path = os.path.join(path_message, f'messeage_{now}.txt')

    for ii in targets:
        url = f'https://weibo.com/{ii}?is_all=1&stat_date={months}#feedtop'
        try:
            html = spider(url)
            messages = item(html)
        except:
            Warning(f'{ii} fetch failed!!!')
            messages='\n'

        with open(message_file_path, 'a+', encoding='utf-8') as file:
            file.writelines(messages)

    try:
        send_email(f'Weibo{now}', message_file_path)
    except:
        Warning(f'{message_file_path} failed to send e-mail!!!')


weibo_beg = 11 * 3600


flag = False
while True:
    date = datetime.datetime.now()
    current = date.second + 60 * date.minute + 3600 * date.hour

    if current < 100:
        flag = True

    if flag and current >= weibo_beg:
        rumMain(date.strftime('%Y%m%d'))
        flag = False
    else:
        time.sleep(1)


    print(current)