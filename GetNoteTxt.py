#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib2
import sys
import re

reload(sys)
sys.setdefaultencoding('gbk')

# 输入IP地址转换为文章文件保存至当前目录下  后面可能需要改一下输入保存地址

url = 'http://www.huanyue123.com/book/0/11/10551.html'  # 文章的地址

try:
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    content = response.read().decode('gbk')
    # head = response.info()
    title = re.compile('<div.*?class="h1title.*?>.*?<h1.*?>(.*?)</h1>' +
                       '.*?</div>', re.S)
    article = re.compile('<div.*?id="htmlContent".*?>(.*?)</div>', re.S)

    # 将<br />替换为\t
    replaceBr = re.compile('<br.*?\n.*?<br.*?>')
    replaceSpace = re.compile('&nbsp;')

    replaceBrIndex = re.compile(u'章节目录 ')

    tit = ''   # 文章名字
    arti = ''  # 文章内容

    itemsTit = re.findall(title, content)
    for item in itemsTit:
        tit = item

    itemsArticle = re.findall(article, content)
    for item in itemsArticle:
        arti = item

    # 去掉章节目录
    tit = re.sub(replaceBrIndex, "", tit)

    # 把空格键替换， 把<br / >换成回车
    arti = re.sub(replaceBr, "\n", arti)
    arti = re.sub(replaceSpace, " ", arti)

    print tit
    print arti

    f = file(tit + ".txt", 'w')
    f.write(tit)
    f.write("\n\n")
    f.write(arti)
    f.close()
    # print head
    # print content

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
