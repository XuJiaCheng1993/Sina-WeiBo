#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/8 11:41
# @Author  : JiachengXu
# @Software: PyCharm
'''

import os
import datetime
import time
from spider import spider
from amails import send_email
from configs import targets, months, path_message, logger


def rumMain(now):
    ''' 主程序'''
    t_bg = time.perf_counter()
    logger.info('[WeiBo System] start to run...')
    message_file_path = os.path.join(path_message, f'messeage_{now}.txt')

    spider(urls= [f'https://weibo.com/{ii}?is_all=1&stat_date={months}#feedtop' for ii in targets],
           message_file_path = message_file_path )

    try:
        send_email(f'Weibo{now}', message_file_path)
        logger.info('[Email] send e-mail successfully...')
    except:
        logger.warning(f'[Email] failed to send {message_file_path}!!!')
    t_ed = time.perf_counter()
    logger.info(f'[WeiBo System] end to run, escape {t_ed - t_bg:.2f} secs...')


weibo_beg = 11 * 3600

flag = True
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


    print(date)
