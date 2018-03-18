#-*- coding:utf-8-*-
'''
Created on 2017年12月4日

@author: pacao
'''
import logging
import os


class Mylog(object):
    LOGGINGLEVELS = {"NOTSET" : logging.NOTSET,
                 "DEBUG" : logging.DEBUG, 
                 "INFO" : logging.INFO, 
                 "WARN" : logging.WARN, 
                 "ERROR" : logging.ERROR, 
                 "FATAL" : logging.FATAL,
                 "CRITICAL" : logging.CRITICAL}
    def __init__(self):
        self.streamformat = '%(asctime)s %(name)s/%(module)s(%(lineno)d)/%(levelname)s(%(process)d): %(message)s'
        self.fileformat = '%(asctime)s %(name)s/%(module)s(%(lineno)d)/%(levelname)s(%(process)d): %(message)s'
        self.logtag = None
        self.stream_loglevel = None
        self.file_loglevel = None
        self.file_mode = None
        self.filter_list =[] 
        self.max_filenum = None
        self.max_filesize = None
    def config_log(self,
                   logtag='log',
                   stream_loglevel=None,
                   file_loglevel=None,
                   file_name=None,
                   file_mode='w',
                   filter_list=[],
                   max_filesize=1024*1024*30,
                   max_filenum=100
                   ):
        self.logtag = logtag
        self.stream_loglevel = self.check_loglevel(stream_loglevel)
        self.file_loglevel = self.check_loglevel(file_loglevel)
        self.file_name = file_name
        if file_name is not None:
            self.create_log(file_name)
        self.file_mode = file_mode
        self.max_filesize = max_filesize
        self.max_filenum = max_filenum
        self.logger = logging.getLogger(logtag)
        self.logger.setLevel(logging.DEBUG)
        
        for filter in filter_list:
            filter_tag = logging.Filter(filter)
            self.logger.addFilter(filter_tag)
        
        if self.stream_loglevel:
            self._config_stream_handler()
            
        if self.file_loglevel:
            self._config_file_handler()
        
    def check_loglevel(self,loglevel):
        if loglevel == None:
            return loglevel
        level = loglevel.upper()
        if level in self.LOGGINGLEVELS:
            tlevel = self.LOGGINGLEVELS[level]
            return tlevel
        else:
            raise Exception("The level '%s' is not valid,please check it!"%level)
        
    def create_log(self,file_fullpath_name):
        if os.path.isfile(file_fullpath_name):
            print "log file '%s' has existed"%file_fullpath_name
        try:
            parent_path = os.path.dirname(file_fullpath_name)
            if not os.path.exists(parent_path):
                os.makedirs(parent_path)
            with open (file_fullpath_name,'w') as a:
                pass
        except Exception as error:
            raise Exception('create log file failed, Error:%s'%error)
        print "INFO - Create File %s OK" % file_fullpath_name
    
    def _config_stream_handler(self):
        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(self.stream_loglevel)
        streamhandler_formatter = logging.Formatter(self.streamformat)
        streamhandler.setFormatter(streamhandler_formatter)
        self.logger.addHandler(streamhandler)
    
    def _config_file_handler(self):
        from logging.handlers import RotatingFileHandler
        
        filehandler = RotatingFileHandler(filename=self.file_name,
                                          mode=self.file_mode,
                                          maxBytes=self.max_filesize,
                                          backupCount=self.max_filenum)
        filehandler.setLevel(self.file_loglevel)
        filehandler_format = logging.Formatter(self.fileformat)
        filehandler.setFormatter(filehandler_format)
        self.logger.addHandler(filehandler)
        
    def get_logger(self, logtag=""):
        return logging.getLogger(logtag)
    
            
if __name__ == '__main__':
    a = Mylog()
    a.config_log(stream_loglevel='DEBUG')                   