#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/8 12:41
# @Author  : JiachengXu
# @Software: PyCharm
'''

import smtplib
from  email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configs import email_code, delivery, receipt, email_host

def __loan_message_binary(filepath):
    with open(filepath, 'rb') as file:
        txtfile = file.readlines()
    return  b''.join(txtfile)


def send_email(subject, path):

    ## 配置参数
    message = MIMEMultipart('related')       # 不发送内容
    message['From'] = delivery               # 发件邮箱
    message['To'] = receipt                  # 收件邮箱
    message['Subject'] = subject             # 标题

    ## 以附件的形式发送信息
    binary_text = __loan_message_binary(path)
    attechment = MIMEText(binary_text, 'base64', 'utf-8')
    attechment['Content-Disposition'] = f'attachment;filename="{subject}.txt"'  # 设置附件名
    message.attach(attechment)


    # 登录邮箱
    client = smtplib.SMTP_SSL()
    client.connect(email_host, '465')
    client.login(delivery, email_code)

    ## 发送邮件
    client.sendmail(from_addr=delivery, to_addrs=receipt.split(','), msg=message.as_string())
    client.close()


