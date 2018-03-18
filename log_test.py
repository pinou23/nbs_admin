#-*-coding:utf-8-*-
'''
Created on 2017年12月5日

@author: pacao
'''
from logger import Mylog
import logging
class Test(object):
    def __init__(self):
        
        _log = Mylog().get_logger("log_test")
        _log.info('msg')
        
        
if __name__ == '__main__':
    log = Mylog()
    log.config_log(logtag='log_test',
                   stream_loglevel="INFO",
                   file_loglevel="INFO",
                   file_name=r"D:\cpf\ReportServer.log",
                   file_mode='w',
                   filter_list=[],
                   max_filesize=1024*1024*30,
                   max_filenum=100
                   )
    t = Test()
    print 'done'