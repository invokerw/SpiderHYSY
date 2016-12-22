#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import sys
import re
import os

reload(sys)
sys.setdefaultencoding('gbk')

# 通过更换strs的不同请求搜索不同的书籍 可以找到对应网页的网址

strs = u'圣墟'  # 一定要有这个 u  没有u的话请求的编码会有错误

url = 'http://www.huanyue123.com/modules/article/search.php'

values = {'searchkey': strs}

data = urllib.urlencode(values)


try:
    request = urllib2.Request(url, data=data)
    response = urllib2.urlopen(request)
    content = response.read().decode('gbk')
    head = response.info()

    page = re.compile('<li>.*?<a.*?href="(.*?)">.*?</a>*?</li>', re.S)

    hrefList = re.findall(page, content)
    chapterQty = 0
    print "Begin->"
    for item in hrefList:
        chapterQty = chapterQty + 1
        print str(chapterQty) + item
        os.system('python GetNoteTxt.py ' + str(item))
        # print item

    # 如果 chapterQty = 0 那么说明了并没有你搜的这个小说
    print chapterQty
    print "End->"
    # f = file('hy.html', 'w')
    # f.write(content)
    # f.close()
    # print head
    # print content

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
