import urllib.request
import re

sum = 1
def write_content(file):
    with open('xw.doc', 'a', encoding='utf8') as f:
        f.write(file)

def domain_urls(url):
    patt = '<div class="txt-box">\s<h3>\s<a target="_blank" href="(.+?)"'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
        'Connection': 'keep-alive',
        'Referer': 'http://weixin.sogou.com/weixin?type=2&query=中国'.encode('utf-8'),
        'Host': 'weixin.sogou.com',
        'Server':'nginx',
        'Set-Cookie':'black_passportid=1; domain=.sogou.com; path=/; expires=Thu, 01-Dec-1994 16:00:00 GMT',
    }
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req).read().decode('utf8')
    # print(response)
    content = re.compile(patt).findall(response)
    for i in range(len(content)):
        content[i] = content[i].replace('amp;','')
    return content

def child_content():

    father_content = domain_urls(url)
    patt1 = r'<h2 class="rich_media_title" id="activity-name">([\s\S]*?)\s+?</h2>'
    patt2 = r'<div class="rich_media_content " id="js_content">\s*?([\s\S]*?)</div>'
    patt3 = '>([\S]*?)<'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
        'Connection': 'keep-alive',
        'Host': 'mp.weixin.qq.com',
        'Referer':'http://weixin.sogou.com/weixin?query=%E4%B8%AD%E5%9B%BD&_sug_type_=&sut=1606&lkt=1%2C1524299756554%2C1524299756554&s_from=input&_sug_=y&type=2&sst0=1524299756658&page=2&ie=utf8&w=01019900&dr=1',
    }
    for i in range(len(father_content)):#len(father_content)
        global sum
        req = urllib.request.Request(father_content[i], headers=header)
        response = urllib.request.urlopen(req)
        cld_content = response.read().decode('utf8')
        # print(cld_content)
        cld_title = re.compile(patt1).findall(cld_content)
        cld_contents = re.compile(patt2).findall(cld_content)
        cld_contents = re.compile(patt3).findall(str(cld_contents))
        print('标题：'+cld_title[0].strip())
        write_content('标题：'+cld_title[0].strip()+'\n'+'内容('+str(sum)+')：')
        print('内容('+str(sum)+')：', end='')
        for content1 in cld_contents:
            if content1 != '':
                content1 = content1.replace('&nbsp;', ' ')
                if content1.__len__() < 10:
                    print(content1.strip(), end='')
                    write_content(content1.strip())
                else:
                    print(content1.strip())
                    write_content(content1.strip())
        sum += 1
        print('\n')
        write_content('\n\n\n')


for a in range(1, 11):
    url = 'http://weixin.sogou.com/weixin?query=%E4%B8%AD%E5%9B%BD&_sug_type_=&sut=1606&lkt=1%2C1524299756554%2C1524299756554&s_from=input&_sug_=y&type=2&sst0=1524299756658&page='+str(a)+'&ie=utf8&w=01019900&dr=1'
    child_content()