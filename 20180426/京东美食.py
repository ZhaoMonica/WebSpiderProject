from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
from hashlib import md5
import re
import urllib.request
import time
import urllib.error
from urllib.parse import urlencode
browser = webdriver.Chrome()
try:
    browser.get('https://www.jd.com/?cu=true&utm_source=baidu-search&utm_medium=cpc&utm_campaign=t_262767352_baidusearch&utm_term=44710086808_0_3dbf64dcb02e4435ad64ff102fe558bf')
    browser.implicitly_wait(10)
    input = browser.find_element_by_xpath('//*[@id="key"]')
    input.send_keys('京东美食')
    input.send_keys(Keys.ENTER)

    time.sleep(10)
    
    listurl = []
    url = browser.current_url
    data = urllib.request.urlopen(url).read().decode('utf-8')
    #<img width="220" height="220" class="err-product" data-img="1" src="//img12.360buyimg.com/n7/jfs/t18520/319/809865010/164143/4ffa63f5/5aa8c270Nc6629a08.jpg">
    listurlpat = '<img width="220" height="220".*?src="//(.*?)".*?/>'
    # 获取所有文章的链接并添加到列表listurl中
    listurl.append(re.compile(listurlpat,re.S).findall(data))
    # for list1 in listurl:
    #     print(list1)
    # 将图片保存为链接
    # with open('href.txt','w') as f:
    #     for list1 in listurl:

    #         for list2 in list1:
    #             # print(list2)
    #             f.write(list2)
    #             f.write('\n')
    #     f.close()
    # print(listurl)
    # 将图片保存在本地

    x = 0
    for addr in listurl:
        file_path = '{0}\{1}.{2}'.format(os.path.join(os.getcwd(),'京东美食'),md5(addr).hexdigest(),'jpg')
        print(file_path)
        if not os.path.exists(file_path):
            with open(file_path,'wb') as f:
                f.write(content)
                f.close()
        x += 1
    time.sleep(1)
    # 将图片保存为本地图片
    
finally:
    browser.close()