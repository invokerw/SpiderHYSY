#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import time
import urllib
import urllib2
import sys
import re

reload(sys)
sys.setdefaultencoding('gbk')

# 经测试,开线程确实快了很多。


class myThread (threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, strUrls):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.strUrls = strUrls

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        self.ThreadDownLoad(self.threadID, self.strUrls)
        print "thread %d exit" % self.threadID

    def ThreadDownLoad(self, threadID, strUrls):
        for url in strUrls:
            DownLoadTextFromUrl(url)


def DownLoadTextFromUrl(url):

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

        # print tit
        # print arti

        f = file("./0/" + tit + ".txt", 'w')
        f.write(tit)
        f.write("\n\n")
        f.write(arti)
        f.close()

    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


strs = u'圣墟'  # 一定要有这个 u  没有u的话请求的编码会有错误

url = 'http://www.huanyue123.com/modules/article/search.php'

values = {'searchkey': strs}

data = urllib.urlencode(values)

strUrls = []
print "Start:%s" % (time.ctime(time.time()))
try:
    request = urllib2.Request(url, data=data)
    response = urllib2.urlopen(request)
    content = response.read().decode('gbk')
    head = response.info()

    page = re.compile('<li>.*?<a.*?href="(.*?)">.*?</a>*?</li>', re.S)

    hrefList = re.findall(page, content)
    chapterQty = 0

    for item in hrefList:
        chapterQty = chapterQty + 1
        strUrls.append(item)
        # print str(chapterQty) + ":" + item
    print "Get All Urls,Check Qty Of url:"
    print chapterQty == len(strUrls)


except urllib2.URLError, e:
    if hasattr(e, "code"):
        print e.code
    if hasattr(e, "reason"):
        print e.reason

# 分为四个线程的话 总共有 Len(strUrls)个数 分为5个线程并发

urlNum = len(strUrls)
threadNum = 5

strUrl1 = strUrls[0:urlNum / threadNum]
strUrl2 = strUrls[urlNum / threadNum:2 * urlNum / threadNum]
strUrl3 = strUrls[2 * urlNum / threadNum:3 * urlNum / threadNum]
strUrl4 = strUrls[3 * urlNum / threadNum:4 * urlNum / threadNum]
strUrl5 = strUrls[4 * urlNum / threadNum:urlNum]


# 创建新线程
thread1 = myThread(1, strUrl1)
thread2 = myThread(2, strUrl2)
thread3 = myThread(3, strUrl3)
thread4 = myThread(4, strUrl4)
thread5 = myThread(5, strUrl5)


# 添加线程到线程列表
threads = []
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)
threads.append(thread5)


# 开始线程
print "Start Threads,Download Note..."
for t in threads:
    t.start()
t.join()

print "End:%s" % (time.ctime(time.time()))
