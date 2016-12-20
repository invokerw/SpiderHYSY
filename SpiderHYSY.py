#!/usr/bin/python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import sys

reload(sys)
sys.setdefaultencoding('gbk')

url = 'http://www.huanyue123.com/modules/article/search.php'

# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

strs = u'圣墟'  # 一定要有这个 u  没有u的话请求的编码会有错误

values = {'searchkey': strs}

data = urllib.urlencode(values)


try:
    request = urllib2.Request(url, data=data)
    response = urllib2.urlopen(request)
    content = response.read().decode('gbk')
    head = response.info()
    f = file('hy.html', 'w')
    f.write(content)
    f.close()
    print head
    print content

except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason
