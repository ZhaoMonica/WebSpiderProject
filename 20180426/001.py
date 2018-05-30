from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
browser = webdriver.Chrome()
try:
    
    browser.get('http://my.cnki.net/elibregister/CheckCode.aspx')
    cookies = browser.get_cookies()
    for cook in cookies:
        for name in cook:
            value = name['ImageV']
    
   print(value)
finally:
    browser.close()