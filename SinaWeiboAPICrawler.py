#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# the program is completely free
# anyone can use and modify it 
# the program is aiming at helping data miner to crawl Sina Weibo data by the API
# I will make a demo for it
# u can learn how to use it there

import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import mechanize
import os
import time

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)
postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'wsse',
    'sp': '',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print 'Get severtime error!'
        return None

def get_pwd(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login(username,pwd):#login function

    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
    try:
        servertime, nonce = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req  = urllib2.Request(
        url = url,
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        login_url = p.search(text).group(1)
        #print login_url
        urllib2.urlopen(login_url)
        print "µÇÂ¼³É¹¦!"
    except:
        print 'Login error!'

def get_api_content(appkey,count):#here we can get the api of public time of sina weibo
    url = 'https://api.weibo.com/2/statuses/public_timeline.json?source=%s&count=%d' %(appkey,count)#the api url
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.107 Safari/535.1')
    content = urllib2.urlopen(req).read() 
    data = json.loads(content)#replace the json data by python dict
    weibos = data['statuses'] # return a weibo list
    if len(weibos) == 0 :
        return 0 # this means u get nothing in this time of visiting api
    else:	
        for weibo in weibos: #get information from each weibo in weibo list
            uid = weibo['user']['id']
	    mid =weibo['id']
            content = weibo['text']
            timestamp = weibo['created_at']
	    ##################################
	    #here u can do something,using or saving the weibo data.
	    #e.g. save the data into local mysql 
	    ##################################
        time.sleep(5) #control the velocity of visiting sina api(because of the limit of api) 
    return 1 # this means u've got something already

