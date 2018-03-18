#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年12月21日

@author: pacao
'''

import requests
import logging
import httplib as http_client
import json
import os,sys
import ssl

#ssl._create_default_https_context = ssl._create_unverified_context

http_client.HTTPConnection.debuglevel=1

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)-6s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)
 
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'en-US,en;q=0.9',
           'Connection':'keep-alive',
           'Host':'logintolabra.tre.noklab.net',
           'Upgrade-Insecure-Requests':1,
           #'Cookie':'DSPREAUTH=51bf551a%3AyUM7WjsJAQABAAAAlL%2BDjIBfga5JGedvpuQRX4ILCAy3cBDQNkUGfT%2F%2FTWquVnQb%2BDvUIGFYd10BJXp4wqersQ653TEivQoTOwcxZzD76SCGDIHEynNx5h%2FphgIgc%2Fc5u6oGIPb1O43d%2BwQKsNGpGm4HtgmgM1PMCnTy%2B1CJEsNA5weV245vk1DO7%2B67LBmay4y%2FjL20w%2FeAW1O9c4dIe2NPZkJp8I2jxKDDqpEgP0Ck7PjEXcQ2iuzJlCb0jSxC0vUIuWot5nbzWTFSJns87CQUOQuAyGelENHVXL4%2F%2BamvEJimt7bu%2Bh0XxczP8%2BUdn83uIBW01qqM5LJK4t1%2FBAjoFwzsTR%2BreAL8z%2BBqxYwcY7i%2FItXvEv8g9IBgYWx2pIyu73nHb8uV3NX25mNNltmJLnv%2Bu97QsmWrH0aDL2rM%2B0453Sw7tN7FwUWTd%2FqZDlrX4p64M8mXR6WY; DSID=f7afe1879b3379d2a3b8420cf8ff3a3f; DSFirstAccess=1513833417; DSLastAccess=1513833420',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.4 Safari/537.36'
               }

headers2 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'en-US,en;q=0.9',
           'Cache-Control':'max-age=0',
           'Connection':'keep-alive',
           'Content-Type':'application/x-www-form-urlencoded',
           'Host':'logintolabra.tre.noklab.net',
           'Upgrade-Insecure-Requests':1,
           'Origin':'https://logintolabra.tre.noklab.net',
           'Referer':'https://logintolabra.tre.noklab.net/dana-na/auth/url_5/welcome.cgi',
           'Cookie':'DSPREAUTH=51bf551a%3AyUM7WjsJAQABAAAAlL%2BDjIBfga5JGedvpuQRX4ILCAy3cBDQNkUGfT%2F%2FTWquVnQb%2BDvUIGFYd10BJXp4wqersQ653TEivQoTOwcxZzD76SCGDIHEynNx5h%2FphgIgc%2Fc5u6oGIPb1O43d%2BwQKsNGpGm4HtgmgM1PMCnTy%2B1CJEsNA5weV245vk1DO7%2B67LBmay4y%2FjL20w%2FeAW1O9c4dIe2NPZkJp8I2jxKDDqpEgP0Ck7PjEXcQ2iuzJlCb0jSxC0vUIuWot5nbzWTFSJns87CQUOQuAyGelENHVXL4%2F%2BamvEJimt7bu%2Bh0XxczP8%2BUdn83uIBW01qqM5LJK4t1%2FBAjoFwzsTR%2BreAL8z%2BBqxYwcY7i%2FItXvEv8g9IBgYWx2pIyu73nHb8uV3NX25mNNltmJLnv%2Bu97QsmWrH0aDL2rM%2B0453Sw7tN7FwUWTd%2FqZDlrX4p64M8mXR6WY; DSID=f7afe1879b3379d2a3b8420cf8ff3a3f; DSFirstAccess=1513833417; DSLastAccess=1513833420',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.4 Safari/537.36'
               }

headers3 = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'en-US,en;q=0.9',
           'Connection':'keep-alive',
           'Host':'logintolabra.tre.noklab.net',
           'Upgrade-Insecure-Requests':1,
           #'Cookie':'DSPREAUTH=51bf551a%3AyUM7WjsJAQABAAAAlL%2BDjIBfga5JGedvpuQRX4ILCAy3cBDQNkUGfT%2F%2FTWquVnQb%2BDvUIGFYd10BJXp4wqersQ653TEivQoTOwcxZzD76SCGDIHEynNx5h%2FphgIgc%2Fc5u6oGIPb1O43d%2BwQKsNGpGm4HtgmgM1PMCnTy%2B1CJEsNA5weV245vk1DO7%2B67LBmay4y%2FjL20w%2FeAW1O9c4dIe2NPZkJp8I2jxKDDqpEgP0Ck7PjEXcQ2iuzJlCb0jSxC0vUIuWot5nbzWTFSJns87CQUOQuAyGelENHVXL4%2F%2BamvEJimt7bu%2Bh0XxczP8%2BUdn83uIBW01qqM5LJK4t1%2FBAjoFwzsTR%2BreAL8z%2BBqxYwcY7i%2FItXvEv8g9IBgYWx2pIyu73nHb8uV3NX25mNNltmJLnv%2Bu97QsmWrH0aDL2rM%2B0453Sw7tN7FwUWTd%2FqZDlrX4p64M8mXR6WY; DSID=f7afe1879b3379d2a3b8420cf8ff3a3f; DSFirstAccess=1513833417; DSLastAccess=1513833420',
           'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.4 Safari/537.36'
               }


data = {
        'tz_offset':480,
        'username':'pacao@nsn-intra',
        'password':'Dongji90921',
        'realm':'NSN-AD',
        'btnSubmit':'Sign In',
        
        }

#proxies = {"http":"http://10.144.1.10:8080"}
session = requests.session()
welcome_url = 'https://logintolabra.tre.noklab.net/dana-na/auth/url_5/welcome.cgi'
login_url = 'https://logintolabra.tre.noklab.net/dana-na/auth/url_5/login.cgi'
#html = session.get(welcome_url,headers=headers,verify=False).text
html = session.post(login_url,headers=headers,data=data,verify=False).text
with open('login1.html','w') as f:
    f.write(html)


# import time
# time.sleep(5)
# 
# 
# html2 = session.get(login_url,headers=headers3,verify=False).text
# with open('login2.html','w') as f:
#     f.write(html2)


def login():
    
    pass
    
    
    