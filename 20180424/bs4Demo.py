html_doc='''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HTML文档</title>
</head>
<body>
    <h1>我的第一个标题<h1>
    <!--这是一个注释 -->
    <p class = 'title'>我的第一个段落。</p>
</body>
</html> <!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>HTML文档</title>
</head>
<body>
    <h1>我的第一个标题<h1>
    <!--这是一个注释 -->
    <p>我的第一个段落。</p>
</body>
</html> 



'''

from bs4 import BeautifulSoup


soup = BeautifulSoup(html_doc,'lxml')
print(soup.prettify())

print(soup.h1)
print(soup.findAll('h1'))
# 可以有层级关系
print(soup.body.h1)
# 提取内容
print(soup.h1.string)
# 提取注释

#标签名
print(soup.h1.name)
# 提取属性？
print(soup.p.attr)