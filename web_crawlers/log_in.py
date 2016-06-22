# -*- coding: utf-8 -*-
#see also: http://www.cnblogs.com/autoria/p/5526762.html
import urllib2
import cookielib
import urllib
cookie = cookielib.CookieJar()
#cookie = cookielib.MozillaCookieJar()
#cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
for item in cookie:
    item.name = 'JSESSIONID'
    item.value = 'XFca9XUKVdIUyRz1xKSPvSK1kL0OzhWKHQkW6ae0MMyYwqV3rOja!1269920556'
    cookie.set_cookie_if_ok(item)
for i in cookie:
    print i.name
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)
req = urllib2.Request(
    'http://202.118.31.197/ACTIONQUERYSTUDENTSCHEDULEBYSELF.APPPROCESS'
    )
response = opener.open(req)
#print response.read()
