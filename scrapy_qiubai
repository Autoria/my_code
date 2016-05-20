# -*- coding: utf-8 -*-
import urllib2
import urllib
import re
import thread
import time

class spider:
    def __init__(self):
        self.page = 0
        self.pages = []
        self.enable = False

    def get_page(self, page):
        my_url = "http://m.qiushibaike.com/hot/page/" + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent':user_agent}
        req = urllib2.Request(my_url, headers = headers)
        response = urllib2.urlopen(req)
        page = response.read()
        unicodePage = page.decode("utf-8")

        myitems = re.findall(r'<div class="content">\n[\s\S]*?\n</div>',unicodePage)

        items = []
        for i in myitems:
            a = i.replace("\n","")
            a = a.replace(r'<div class="content">','')
            a = a.replace(r'</div>','')
            a = a.replace(r'<br/>','\n')
            a = a.replace(r'&quot;','"')
            items.append(a)
        return items

    def load_page(self):
        while self.enable:
            if len(self.pages) < 2:
                try:
                    my_page = self.get_page(str(self.page))
                    self.page += 1
                    self.pages.append(my_page)
                except Exception as e:
                    print 'except', e
                    print '无法链接糗事百科!\n'
            else:
                time.sleep(1)
    def show_page(self, now_page, page):
        for items in now_page:
            print u'第%d页' %page, items
            my_input = raw_input()
            if my_input == 'quit':
                self.enable = False
                break
    def start(self):
        self.enable = True
        page = self.page

        print '正在加载中请稍等......'

        thread.start_new_thread(self.load_page,())

        while self.enable:
            if self.pages:
                now_page = self.pages[0]
                del self.pages[0]
                self.show_page(now_page, page)
                page += 1


print u'按下回车显示内容'
raw_input(' ')
spider = spider()
spider.start()
