# -*- coding: utf-8 -*-
"""
Crawling pictures by selenium and urllib
url: 虎扑 马刺 http://photo.hupu.com/nba/tag/%E9%A9%AC%E5%88%BA
Created on 2015-10-24
@author: Eastmount CSDN
适用于python3
"""

import time
import re
import os
import urllib.request
import shutil
import datetime
from selenium import webdriver
import selenium.webdriver.support.ui as ui

jxh_phantomjs_path = "/Users/JinXiaoHao/Desktop/JINXIAOHAO/Software/phantomjs-2.1.1-macosx/bin/phantomjs"
Picture_HP_path = "/Users/JinXiaoHao/Desktop/Picture_HP/"

# Open PhantomJS
driver = webdriver.PhantomJS(executable_path=jxh_phantomjs_path)
wait = ui.WebDriverWait(driver, 10)

# Download one Picture By urllib
def loadPicture(pic_url, pic_path):
    print(' *** loadPicture ***')
    pic_name = os.path.basename(pic_url)  # 删除路径获取图片名字
    pic_name = pic_name.replace('*', '')  # 去除'*' 防止错误 invalid mode ('wb') or filename
    urllib.request.urlretrieve(pic_url, pic_path + pic_name)

# 爬取具体的图片及下一张
def getScript(elem_url, path, nums):
    print(' *** getScript ***')
    try:
        count = 1
        t = elem_url.find(r'.html')
        n = int(nums)
        while (count <= n):
            html_url = elem_url[:t] + '-' + str(count) + '.html'
            print('htme_url', html_url)
            '''
            driver_pic.get(html_url)
            elem = driver_pic.find_element_by_xpath("//div[@class='pic_bg']/div/img")
            url = elem.get_attribute("src")
            '''
            # 采用正则表达式获取第3个<div></div> 再获取图片URL进行下载
            content = urllib.request.urlopen(html_url).read()
            content = str(content, encoding='gbk')
            start = content.find(r'<div class="flTab" style="width:100%;">')         # 图集标签，来源，查看原图
            end = content.find(r'<div class="comMark" style="">')   # 转帖到人人／微信／QQ ……
            content = content[start:end]
            div_pat = r'<div .*?>(.*?)<\/div>'                  # *匹配前面的子表达式零次或多次。例如，zo*能匹配“z”以及“zoo”。*等价于{0,}。?匹配前面的子表达式零次或一次。例如，“do(es)?”可以匹配“do”或“does”中的“do”。?等价于{0,1}。

            div_m = re.findall(div_pat, content, re.S | re.M)  #re.S ' . '并且包括换行符在内的任意字符（注意：' . '不包括换行符）| re.M 多行模式
            if len(div_m):
                link_list = re.findall(r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')", div_m[2])
                url = link_list[0]  # 仅仅一条url链接
                loadPicture('http:'+url, path)
                count = count + 1
            else:
                print('******************* div_m 为空')
                break

    except Exception as e:
        print('!!!!!!!!!!!!!!!!!!!!    getScript - Error:', e)

    finally:
        print('Download ' + str(count-1) + ' pictures\n')

# 爬取主页图片集的URL和主题
def getTitle(url):
    print(' *** getTitle ***')
    try:
        # 爬取URL和标题
        count = 0
        print('Function getTitle(key,url)')

        driver.get(url)
        wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='piclist3']"))
        print('Title: ' + driver.title + '\n')

        # 缩略图片url(此处无用) 图片数量 标题(文件名) 注意顺序
        elem_url = driver.find_elements_by_xpath("//a[@class='ku']/img")
        elem_num = driver.find_elements_by_xpath("//div[@class='piclist3']/table/tbody/tr/td/dl/dd[1]")
        elem_title = driver.find_elements_by_xpath("//div[@class='piclist3']/table/tbody/tr/td/dl/dt/a")
        print('elem_url', elem_url)

        for url in elem_url:
            print('\n === getTitle / url ===')
            pic_url = url.get_attribute("src")
            html_url = elem_title[count].get_attribute("href")

            # 在path路径下创建图片文件夹
            file_path = Picture_HP_path + elem_title[count].text + "/"
            # print('file_path', file_path)
            m = re.findall(r'(\w*[0-9]+)\w*', elem_num[count].text)  # 爬虫图片张数
            nums = re.findall(r"\d+\.?\d*", (str(m)))  # ['共5'] 获取数字['5']
            print('爬虫图片张数', m)

            count = count + 1
            while 1:
                if os.path.isfile(file_path):  # Delete file
                    os.remove(file_path)

                elif os.path.isdir(file_path):  # Delete dir
                    shutil.rmtree(file_path, True)
                else:
                    os.makedirs(file_path)  # create the file directory
                    getScript(html_url, file_path, nums[0])  # visit pages
                    break

    except Exception as e:
        print('!!!!!!!!!!!!!!!!!!!!    getTitle - Error:', e)

    finally:
        print('Find ' + str(count) + ' pages with key\n')

def main():
    # Create Folder
    basePathDirectory = Picture_HP_path
    if not os.path.exists(basePathDirectory):
        os.makedirs(basePathDirectory)

    # Input the Key for search
    key = input("Please input a key: ")
    print(key)

    # Set URL List  Sum:1-2 Pages
    print('Ready to start the Download!!!\n\n')

    starttime = datetime.datetime.now()
    num = 1
    while num <= int(key):
        url = 'http://photo.hupu.com/nba/tag/%E9%A9%AC%E5%88%BA?p='+str(num)+'&o=1'
        print('\n\n\n~~~~~~~~~~~~~~~第' + str(num) + '页', 'url:' + url)

        # Determine whether the title contains key
        getTitle(url)
        time.sleep(1)
        num = num + 1
    else:
        print('Download Over!!!')

    # get the runtime
    endtime = datetime.datetime.now()
    print('The Running time : ', (endtime - starttime).seconds)

main()