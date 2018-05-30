import urllib.request
import chardet
#1. 确定好要爬取的入口链接
url = "http://blog.csdn.net"
# 2.根据需求构建好链接提取的正则表达式 <a href="//download.csdn.net" title="下载" target="_blank">下载</a>
pattern1 = '<a href="(.*?).*?</a>'
#3.模拟成浏览器并爬取对应的网页
a = urllib.request.urlopen(url)
encode = chardet.detect(a.read())
print(encode['encoding'])
# headers = {'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# opener = urllib.request.build_opener()
# opener.addheaders = [headers]
# data = opener.open(url).read().decode('utf8')
# print(data)