import urllib.request
import re
# 封装成函数getcontent(url,page)

def getcontent(url,page):
    # 模拟成浏览器
    headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]

    #将opener安装成全局
    urllib.request.install_opener(opener)
    data = urllib.request.urlopen(url).read().decode('utf8')


    # 构建对应用户提取的正则表达式
    userpat = '<div class="author clearfix">.*?<h2>(.*?)</h2>.*?</div>'


    # 构建段子内容提取的正则表达式
    contentpat = '<div class="content">.*?<span>(.*?)</span>.*?</div>'
    # 寻找出所有的用户
    user_list = re.compile(userpat,re.S).findall(data)

    # 寻找出所有的内容
    content_list = re.compile(contentpat,re.S).findall(data)

    x = 1
    # 通过for循环遍历段子内容并将内容分别赋给对应的变量
    for  content in content_list:
        content= content.replace('\n', '')

        # 用字符串作为变量名，先将对应字符串赋给一个变量
        name = 'content' + str(x)
        #通过exec()函数实现用字符串作为变量名并赋值
        exec(name+'=content')
        x += 1
    y = 1
    #通过for循环遍历用户，并输出该用户对应的内容
    for user in user_list:
        user = user.replace("\n", "")
        name = "content"+str(y)
        print("第"+str(page)+"页用户"+str(y)+"是："+user)
        print("内容是：")
        exec("print("+name+")")
        print("\n")
        y += 1
#分别获取各页的段子，通过for循环可以获取多页
for i in range(3,4):
    url = "https://www.qiushibaike.com/8hr/page/"+str(i)
    getcontent(url,i)