# -*- coding: utf-8 -*-
'''
Created on 2017年12月21日

@author: pacao
'''
from selenium import webdriver
import selenium.common.exceptions
import time
from time import sleep
from tqdm import tqdm
import getpass
from selenium.webdriver.support.ui import WebDriverWait

profile_dir = r'D:\userdata\pacao\Application Data\Mozilla\Firefox\Profiles\bcpwycus.default'

class Auth(object):
    def __init__(self,username,password,link,alias):
        self.username = username
        self.password = password
        self.link = link
        profile = webdriver.FirefoxProfile(profile_dir)
        self.browser = webdriver.Firefox(profile)
        self.alias = alias
    def login(self):
        try:
            self.browser.get(self.link)
            self.parent = self.browser.current_window_handle
            self.browser.implicitly_wait(15)
            self.browser.find_element_by_xpath(".//*[@id='username']").send_keys(self.username)
            self.browser.find_element_by_xpath(".//*[@id='password']").send_keys(self.password)
            self.browser.find_element_by_xpath(".//*[@id='btnSubmit_6']").click()
            self.browser.find_element_by_xpath(".//*[@id='liveclock2']")
            
            time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            print '%s %s Login OK!'%(time_stamp,self.alias)
        except Exception as e:
            raise Exception('Login failed,Error:',e)
            
    def extend(self):
        try:
            print 'en?'
            self.browser.find_element_by_xpath(".//*[@id='liveclock2']").click()
            handles = self.browser.window_handles
            #print handles
            child = handles[-1]
            self.browser.switch_to_window(child)
            self.browser.implicitly_wait(10)
            self.browser.find_element_by_xpath(".//*[@id='username']").send_keys(username)
            self.browser.find_element_by_xpath(".//*[@id='password']").send_keys(password)
            self.browser.find_element_by_xpath(".//*[@id='btnSubmit_6']").click()
            self.browser.switch_to_window(self.parent)
            time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print '%s %s Extend time OK!'%(time_stamp,self.alias)
        except Exception as e:
            raise Exception('Error:',e)
    
    def check_connection(self):
        flag = True
        try:
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print 'start time:',start_time
            
            self.browser.find_element_by_xpath(".//*[@id='liveclock2']")
            
        except selenium.common.exceptions.NoSuchElementException:
            flag = False
            print flag
        
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print 'end time:',end_time
        return flag
    
    def relogin_if_lost(self):
        result = self.check_connection()
        if not result:
            time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print '%s connection lost at:%s, will relogin'%(self.alias,time_stamp)
            try:
                self.browser.find_element_by_xpath(".//*[@id='signindiv']").click()
            except selenium.common.exceptions.NoSuchElementException:
                pass
            
            self.browser.find_element_by_xpath(".//*[@id='username']").send_keys(username)
            self.browser.find_element_by_xpath(".//*[@id='password']").send_keys(password)
            self.browser.find_element_by_xpath(".//*[@id='btnSubmit_6']").click()
            
    def close(self):
        self.browser.quit()

class TimeLimitExpired(Exception): pass

def _timelimit(timeout, func, args, kwargs={}):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """
    import threading
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None

        def run(self):
            self.result = func(args, **kwargs)

        def _stop(self):
            if self.isAlive():
                self._Thread__stop()

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it._stop()
        raise TimeLimitExpired()
    else:
        it._stop()
        return it.result    

if __name__ == '__main__':
    tampere_link = 'https://logintolabra.tre.noklab.net/dana-na/auth/welcome.cgi'
    hangzhou_link = 'https://10.68.148.38/dana-na/auth/url_default/welcome.cgi'
    short_name = raw_input("Please input your name:")
    username = short_name+'@nsn-intra'
    password = getpass.getpass("Please input your password:")

    
    tampere = Auth(username,password,tampere_link,'Tampere')
    hangzhou = Auth(username,password,hangzhou_link,'Laboratory')
    try:
        tampere.login()
        hangzhou.login()
        while True:
            print '***********************wait to extend time***********************'
            for i in tqdm(range(10*3600),desc='Extend time remaining:'):
                sleep(1)
                tampere.relogin_if_lost()
                hangzhou.relogin_if_lost()
                
            tampere.extend()
            hangzhou.extend()
      
    except Exception as e:
        tampere.close()
        hangzhou.close()
        raise Exception(e)
        

