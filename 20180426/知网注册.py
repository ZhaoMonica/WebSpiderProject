from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
browser = webdriver.Chrome()
try:
    browser.get('http://my.cnki.net/elibregister/commonRegister.aspx')
    browser.implicitly_wait(10)
    input = browser.find_element_by_id('username')
    input.send_keys('Monica_li')
    input.send_keys(Keys.ENTER)
    time.sleep(1)
    input = browser.find_element_by_id('txtPassword')
    input.send_keys('moni1995')
    input.send_keys(Keys.ENTER)
    time.sleep(1)
    input = browser.find_element_by_id('txtEmail')
    input.send_keys('2874379769@qq.com')
    input.send_keys(Keys.ENTER)
    time.sleep(1)
    input = browser.find_element_by_xpath('//*[@id="txtOldCheckCode"]')
  
    # browser.get('http://my.cnki.net/elibregister/CheckCode.aspx')
    cookies = browser.get_cookies()
    print(cookies)
    value = cookies[2]['value']
    print(value)

    input.send_keys(value)
    input.send_keys(Keys.ENTER)   
    time.sleep(1)
    # input = browser.find_element_by_xpath('//*[@id="txtOldCheckCode"]')
    # input.send_keys(text)
    # input.send_keys(Keys.ENTER)
    # time.sleep(5)
    input = browser.find_element_by_xpath('//*[@id="ButtonRegister"]')
    input.click()
    time.sleep(10)
finally:
    browser.close()