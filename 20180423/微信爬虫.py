# 通过搜狗爬取微信文章
# 我们希望搜索与某个关键词相关的微信公众平台文章，并将这些文章的标题与内容爬取到本地。


# 第一步：检索对应关键词得到相关的文章检索结果，并在该页面中将文章的链接提取出来；
# 第二步：在文章链接提取出来之后，根据这些链接地址采集文章中的具体标题的内容。
import re
import urllib.request
import time
import urllib.error
from urllib.parse import urlencode

# 定义一个use_proxy的函数，实现使用代理服务器爬取网页，
# 第一个形参为代理服务器地址，第二个形参为要爬取网页的地址
def use_proxy(proxy_addr,url):
    
    # 设置代理
    try:
        proxy_handler = urllib.request.ProxyHandler({
            'http':proxy_addr
            })
        #将opener安装成全局
        opener = urllib.request.build_opener(proxy_handler,urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        # response = opener.open(url)
        # data = response.read().decode('utf-8')
        data = urllib.request.urlopen(url).read().decode('utf-8')
        #通过代理服务器爬取文章列表页数据,构造爬取文章列表页的正则表达式
        # listurl=[]

        # listurlpat = '<div class="txt-box">.*?href="(http://.*?)".*?</div>'
        # listurl.append(re.compile(listurlpat,re.S).findall(data))
        # print(listurl)
        return data
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        #若为URLError异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print("exception:"+str(e))
        #若为Exception异常，延时1秒执行
        time.sleep(1)

#获取文章列表并采集各页文章网址,获取所有文章链接
def getlisturl(key,pagestart,pageend):
    try:
        # 循环爬取各页的文章链接
        listurl = []
        base_url = 'http://weixin.sogou.com/weixin?'
        for page in range(pagestart,pageend+1):
            data ={
            'query':key,
            'type':2,
            'page':page
            }
            #转换为get请求参数
            queries = urlencode(data)
            
            url = base_url+queries
            # 用代理服务器爬，解决IP被封杀问题
            data = urllib.request.urlopen(url).read().decode('utf-8')
            # 获取文章链接的正则表达式
            listurlpat = '<div class="txt-box">.*?href="(http://.*?)".*?</div>'
            # 获取所有文章的链接并添加到列表listurl中
            listurl.append(re.compile(listurlpat,re.S).findall(data))
        print(listurl)
        # 便于调试
        print("共获取到" + str(len(listurl))+'页') 
        return listurl
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        # 若为URLError 异常，延时10秒执行
        time.sleep(10)
    except Exception as e:
        print('exception:'+str(e)) 
        # 若为Exception异常，延时1秒执行
        time.sleep(1)

# 通过文章链接获取对应内容

def getcontent(listurl):
    i = 0
    # 设置本地文件中的开始html编码
    # html1='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # <html xmlns="http://www.w3.org/1999/xhtml">
    # <head>
    # <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    # <title>微信文章页面</title>
    # </head>
    # <body>'''
    fh = open('weixinarticle.html','wb')
    # fh.write(html1.encode('utf-8'))
    # fh.close()
    # 再次以追加写入的方式打开文件，已写入对应文章内容
    fh = open('weixinarticle.html','ab')
    # 此时listurl 为二维列表，形如listurl[][]，第一维存储的信息跟第几页相关，第二维存的跟该页第几个文章链接相关
    for i in range(0, len(listurl)):
        for j in range(0, len(listurl[i])):
            try:
                url = listurl[i][j]
                # 处理成真是URL，读者亦可以观察对应网址的关系自行分析，采集网址比真是网址多了一串amp
                url = url.replace('amp','')
                # 使用代理去爬取对应网址的内容
                proxy_addr = '60.177.230.194:18118'
                data = use_proxy(proxy_addr, url)
                # 文章标题正则表达式
                titlepat = '<title>(.*?)</title>'
                # 文章内容正则表达式
                contentpat = 'id="js_content">(.*?)id="js_sg_bar"'
                # 通过对应正则表达式找到内容并赋给列表title
                title = re.compile(titlepat).findall(data)
                # 通过对应正则表达式找到内容并赋给列表content
                content = re.compile(contentpat,re.S).findall(data)
                # 初始化标题和内容
                thistitle = "此次没有获取到"
                thiscontent = '此次没有获取到'
                # 如果标题列表不为空，说明找到了标题，取列表第零个元素，即此次标题赋给变量thistitle
                if(title!=[]):
                    thistitle=title[0]
                if(content!=[]):
                    thiscontent = content[0]

                # 将标题与内容汇总并赋给变量dataall
                dataall = "<p>标题为："+thistitle + "</p><p>内容为:"+ thiscontent+"</p><br>" 
                # 将该篇文章的标题与内容的总信息写入对应文件
                fh.write(dataall.encode('utf-8'))
                print("第"+str(i)+ "个网页第" + str(j) +'次处理') # 便于调试
            except urllib.error.URLError as e:
                if hasattr(e,"code"):
                    print(e.code)
                if hasattr(e, "reason"):
                    print(e.reason)
                # 若为URLError  异常，延时10秒执行
                time.sleep(10)

            except Exception as e:
                print("exception"+str(e))
                # 若为Exception异常，延时1秒执行
                time.sleep(1) 
    fh.close()
    # 设置并写入本地文件的html后面结束部分代码
    html2 = '''</body>
    </html>
    '''      
    fh = open('weixinarticle.html','ab')
    fh.write(html2.encode('utf-8'))
    fh.close()



   
# key = "python"
# pagestart = 1
# pageend = 2
# url = getlisturl(key, pagestart,pageend)
# # print(url)
# proxy_addr = '60.177.230.194:18118'
# data1 = use_proxy(proxy_addr,url)
# print(data1)

#设置关键词
key="python"

#起始页
pagestart=1
#抓取到哪页
pageend=2

listurl=getlisturl(key,pagestart,pageend)
getcontent(listurl)