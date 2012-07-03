#!/usr/bin/python
# -*- coding: UTF-8 -*-
# this is a test program of get sina weibo api 
# I just take the public time api as the example
# if u want to use other apis,u need to change the api url of fucntion get_api_content() 
# and u must take care of the parameter of api
# u can see the detail infomation here --- http://open.weibo.com/wiki/API%E6%96%87%E6%A1%A3_V2
# notice: if u want to do something by the weibo data from api, u should add some action (eg. save in database) in functin get_api_content() 

from SinaWeiboAPICrawler import *

username = 'XXXXXXXX' # your uesrname in weibo
pwd = 'XXXXXXXXX' # your password in weibo
login(username,pwd)# u can login in sina weibo by this function

appkey = ['XXXXXXXXX','XXXXXXXXX','XXXXXXXXX','XXXXXXXXX','XXXXXXXXX','XXXXXXXXX','XXXXXXXXX'] # here is the appkey of your app in weibo(detail u can see http://open.weibo.com/apps)
#the parameter of api (here is the public time)
crawl_time = 1 # 
count = 50 # each page return 50 results 
ap_index = 0 # the index of appkey list
while crawl_time < 1000:
    try:
	result = get_api_content(appkey[ap_index],count)
	if result == 0:# means data are crawled over,the program must stop
	    break
	else: # go on crawling the data 
	    crawl_time += 1
    except Exception,e: # when u use the api to get weibo data,u will always meet the problem of appkey forbidden(just because of the fucking api limit)
        # when u meet the exception,u often meet the http forbiden,namely the api limit
	# here is a litte trick,the more correct way is considering more exception situations
        print e 
	print "change the appkey"
	if ap_index < 6:# because the length of appkey list is 7
	    ap_index += 1
	else:
	    ap_index = 0
	print "now the appkey is %s" %(appkey[ap_index])
