from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
browser = webdriver.Chrome()
try:
    browser.get('http://my.cnki.net/elibregister/commonRegister.aspx')
    cookies = {}
    items = browser.get_cookies()    
    for item in items:
        print(item)
        cookies[item['name']] = item['value']
        print(item['name'])
        print(item['value'])
    code = cookies['ImageV']
    print(code)
    time.sleep(10)
finally:
    browser.close()