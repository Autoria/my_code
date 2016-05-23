# -*- coding: utf-8 -*-
import string
import urllib2
import re
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&amp;","\""),("&nbsp;"," "),("&quot;","\"")]

    def replace_char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n    ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:
            x = x.replace(t[0], t[1])
        return x

class baidu_spider:
    def __init__(self, url):
        self.my_url = url + '?see_lz=1'
        self.datas = []
        self.my_tool = HTML_Tool()
        print u'已经启动百度贴吧爬虫'

    def baidu_tieba(self):
        my_page = urllib2.urlopen(self.my_url).read().decode("utf-8")

        end_page = self.page_counter(my_page)

        title = self.find_title(my_page)
        print u'汶航名称： ' + title

        self.save_data(self.my_url, title, end_page)

    def page_counter(self, my_page):

        my_match = re.search(r'<span class="red">(.*?)</span>',my_page,re.S)
        if my_match:
            end_page = int(my_match.group(1))
            print u'发现 共有 %d' %end_page
        else:
            end_page = 0
            print u'无法计算'
        return end_page

    def find_title(self, my_page):
        my_match = re.search(r'<title>(.*?)</title>',my_page, re.S)
        title = '暂无标题'
        if my_match:
            title = my_match.group(1)
        else:
            print u'爬虫报告： 无法加载文章标题'
        #maps = string.maketrans('\\/:*?"><|','')
        title = title.replace('\\','').replace('/','').replace(':','').replace('*','').replace('?','').replace('"','').replace('>','').replace('<','').replace('|','')
        return title

    def save_data(self, url, title, end_page):
        self.get_data(url, end_page)

        f = open(title+'.txt','w+')
        #for line in self.datas:
        #    f.writelines(line)
        #for line in self.datas:
        #    print line
        f.writelines(self.datas)
        f.close()

    def get_data(self, url, end_page):
        url = url + '&pn='
        for i in range(1, end_page+1):
            print 'downloading %d' %i
            my_page = urllib2.urlopen(url+str(i)).read().decode("utf-8")
            self.deal_data(my_page)
    def deal_data(self,my_page):
        myItems = re.findall('id="post_content.*?>(.*?)</div>',my_page,re.S)
        for item in myItems:
            data = self.my_tool.replace_char(item.replace("\n","").encode('utf-8'))
            self.datas.append(data+'\n')
mySpider = baidu_spider('http://tieba.baidu.com/p/3558790905')
mySpider.baidu_tieba()
