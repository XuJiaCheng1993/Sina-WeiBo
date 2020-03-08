#!/usr/bin/env python
# encoding: utf-8
'''
# @Time    : 2020/3/7 15:40
# @Author  : JiachengXu
# @Software: PyCharm
'''
import os
import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from configs import username, password, path_cookie
from dateutil.parser import parse

def __address_date(struct_time):
    ''' 时间转换格式'''
    y, m, d = struct_time.tm_year, struct_time.tm_mon, struct_time.tm_mday
    h, M, s = struct_time.tm_hour, struct_time.tm_min, struct_time.tm_sec
    return f'{y}-{m}-{d} {h}:{M}:{s}'

def __is_update_cookie():
    ''' 判断cookie是否需要更新'''
    ## 如果cookie文件不存，则直接返回
    file_name = os.path.join(path_cookie, 'cookie.txt')
    if not os.path.exists(file_name):
        return False

    ## 获取cookie文件的更新日期
    atime = __address_date(time.localtime(os.path.getatime(file_name)))

    ## 获取当前时间
    current = __address_date(time.localtime(time.time()))

    ## 如果两者差超过一天，则需要更新cookie
    if (parse(current) - parse(atime)).seconds >= 3600 * 24:
        return True
    else:
        return False

def __load_cookie():
    ''' 读取cookie'''
    try:
        with open(os.path.join(path_cookie, 'cookie.txt') , 'rb') as file:
            cookies = pickle.load(file)
    except:
        cookies = None
    return cookies


def __dump_cookie(cookies):
    ''' 保存cookie'''
    for ii in cookies:
        if 'expiry' in ii:
            ii.update({'expiry':int(ii['expiry'])})

    with open(os.path.join(path_cookie, 'cookie.txt'), 'wb') as file:
        pickle.dump(cookies, file)


def __laungh_driver():
    ''' 启动chrome'''
    driver = webdriver.Chrome('./chromedriver', )
    driver.maximize_window()#将浏览器最大化显示
    driver.get("https://weibo.com/")  # 打开微博登录页面
    time.sleep(10)  # 因为加载页面需要时间，所以这里延时10s来确保页面已加载完毕
    return driver

def get_and_set_cookie():
    ''' 启动浏览器，获取并保存cookie'''
    ## 启动chrome
    driver = __laungh_driver()

    ## 获取cookie
    driver.find_element_by_name("username").send_keys(username)  ##输入用户名
    driver.find_element_by_name("password").send_keys(password)  ##输入密码
    driver.find_element_by_xpath("//a[@node-type='submitBtn']").click()  ##点击登录按钮


    ## 保存cookie
    time.sleep(2) ## 等待加载
    cookies = driver.get_cookies()  ##获取cookies
    __dump_cookie(cookies)
    return driver


def set_cookie(cookies):
    ''' 启动浏览器并设置cookie'''
    driver = __laungh_driver()

    ## 删除并重新设置cookie
    driver.delete_all_cookies()
    for ii in cookies:
        driver.add_cookie(ii)
    return driver


def spider(url):
    '''Sina WeiBo爬虫 '''
    ## 获取cookie
    if __is_update_cookie():
        driver = get_and_set_cookie()
    else:
        cookie = __load_cookie()
        driver = set_cookie(cookie)

    ## 跳转到指定页面
    driver.get(url)
    time.sleep(1)

    ## 将页面加载到最底端
    for i in range(30):
        try:
            try:
                web_element = driver.find_elements_by_class_name('W_pages')[0]
            except:
                web_element = driver.find_elements_by_xpath('//*[@id="Pl_Official_MyProfileFeed__21"]/div/div[27]/a')[0]
            flag = True
        except:
            web_element = driver.find_elements_by_class_name('company')[0]
            flag = False


        ActionChains(driver).move_to_element(web_element).perform()
        if flag:
            break
        time.sleep(0.5)

    ## 打开所有“展开全文”
    window_handle = driver.current_window_handle
    web_element = driver.find_elements_by_class_name('WB_text_opt')
    for ii in web_element:
        ActionChains(driver).click(ii).perform()
        ## 如果有误点击时，切换回原网址
        if len(driver.window_handles) > 1:
            driver.switch_to.window(window_handle)
        time.sleep(0.5)

    return driver.page_source


def item(html):
    ''' 提款需要信息'''
    ## 解析html
    soup = BeautifulSoup(html, 'lxml')
    ## 解析微博
    messeags = ''
    weibos = soup.select('.WB_cardwrap.WB_feed_type.S_bg2.WB_feed_like ') # 获取整条微博
    for wb in weibos:
        yb, zb = ['', ] * 4, ['', ] * 3

        # 微博、被转微博(如果有)的作者
        authors = wb.select('.WB_info')
        yb[0] = authors[0].text.replace('\n', '').replace(' ', '')
        if len(authors) > 1:
            zb[0] = authors[1].text.replace('\n', '').replace('@', '').replace(' ', '')

        # 微博、被转微博(如果有)的时间、设备
        froms = wb.select('.WB_from a')
        yb[1] = froms[0].attrs['title']
        if len(froms) > 2:
            zb[1] = froms[2].attrs['title']

        ## 微博链接
        yb[-1] = froms[0]['href']

        # ## 主体微博的点赞、转发、评论数
        # pos = wb.select('.pos')

        # 微博、被转微博（如果有）的内容
        contents = wb.select('.WB_text')
        node_type = [ff.attrs['node-type'] for ff in contents]

        if 'feed_list_content_full' in node_type:
            index = node_type.index('feed_list_content_full')
        else:
            index = node_type.index('feed_list_content')

        yb[2] = contents[index].text.replace('\n', '').replace(' ', '').replace('\u200b', '').replace('\xa0', '')
        if len(authors) > 1:
            if 'feed_list_reason_full' in node_type:
                index = node_type.index('feed_list_reason_full')
            else:
                index = node_type.index('feed_list_reason')
            zb[2] = contents[index].text.replace('\n', '').replace(' ', '').replace('\u200b', '').replace('\xa0', '')

        #整合所有内容
        messeags += '|+|'.join(yb + zb) + '\n'

    return messeags


