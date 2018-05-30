# 今日头条为例来尝试用ajax
import json
import requests
import re
from urllib.parse import urlencode
import pymongo
from bs4 import BeautifulSoup
import os
from requests.exceptions import ConnectionError
from hashlib import md5
from json.decoder import JSONDecodeError
# from config import *
from multiprocessing import Pool



MONGO_URL = 'localhost'
MONGO_DB = 'toutiao'
MONGO_TABLE = 'toutiao'
KEYWORD = '街拍'
GROUP_START = 1
GROUP_END = 10

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
}
# MongoDB
client = pymongo.MongoClient(MONGO_URL,connect =False)
db = client[MONGO_DB]
# 抓取图集列表索引，获取每个图集response内容
def get_page_index(offset,keyword):
        data = {
            'offset':offset,
            'format':'json',
            'keyword':keyword,
            'autoload':'true',
            'count':20,
            'cur_tap':3,
            'from':'gallery'
        }
        params = urlencode(data)
        base = 'http://www.toutiao.com/search_content/'
        url = base + '?' + params
        try:
            response = requests.get(url,headers = headers)
            if response.status_code ==200:
                return response.text
            return None    
        except ConnectionError as e:
            print('索引链接错误')
            return None


#对获取到的每个图集信息进行解析，得到图集URL
def parse_page_index(text): 
    try:
        data = json.loads(text)
        if data and 'data' in data.keys():
            print(data)
            for item in data.get('data'):
                #存储到生成器中
                yield item.get('article_url')
    except JSONDecodeError as e:
        print('解析出错')
   
       
# 从parse_page_index()中获取 URL，对URL页面进行读取 
def get_page_detail(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            return response.text
        return None    
    except ConnectionError as e:
        print('详情页面错误')
        return None    

# 从get_page_detail（）读取到的内容中提取图集URL的title和图片
def parse_page_detail(html, url):  
    soup = BeautifulSoup(html,'lxml') 
    result = soup.select('title') 
    title = result[0].get_text()  
    print(title)

    #图片,形式为url，所以后面要下载

    images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)',re.S)
    result = re.search(images_pattern, html)
    if result:
        # 解析，得到正常的字符串
        data = json.loads(result.group(1).replace('\\',''))
        if data and 'sub_images' in data.keys():
            # 提取
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:download_image(image)
            return{
            'title':title,
            'url':url,
            'images':images
            }
 

 # 下载图片
def download_image(url):
    print('开始下载.......')
    try:
        response = requests.get(url,headers = headers)
        if response.status_code ==200:
            save_image(response.content)
            return response.content
        return None    
    except ConnectionError as e:
        print('下载图片错误')
        return None    


# 保存图片：保存位置，保存对象，保存格

def save_image(content):
    #文件夹 名字  后缀
    # md5(content) 去重，获取随机的文件名
    file_path = '{0}\{1}.{2}'.format(os.path.join(os.getcwd(),'图片'),md5(content).hexdigest(),'jpg')
    print(file_path)
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
# 保存到MongoDB
def  save_to_mongodb(result):
    if db[MONGO_TABLE].insert(result):
        print('sucessful saved.....',result)
        return True
    return False
 


def main(offset):

    html = get_page_index(offset,KEYWORD) 
    for url in parse_page_index(html):
        html = get_page_detail(url)
        result = parse_page_detail(html,url)
        print(result) 
        if result:save_to_mongodb(result)



# 
if __name__ == '__main__':
    main(20)
    # pool = Pool()
    # groups = ([x * 20 for x in range(GROUP_START,GROUP_END+1)])
    # pool.map(main,groups)
    # pool.close()
    # pool.join()

# 下载多个图集，可以设置多线程    