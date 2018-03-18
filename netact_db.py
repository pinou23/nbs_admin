# -*- coding: UTF-8 -*-
'''
Created on 2017年8月29日

@author: pacao
'''
import cx_Oracle
import os
from logger import Mylog
from constant import *
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class NetAct_db(object):
    def __init__(self,host,uname,pwd,port):
        self.__Log = Mylog().get_logger()
        self.host = host
        self.port = int(port)
        self.uname = uname
        self.pwd = pwd
        self.conn = None
        self.cursor = None
        self.oracledbConnect()

    def oracledbConnect(self):
        try:    
            #self.conn = cx_Oracle.connect("omc/omc@sprintlab317vm4.netact.nsn-rdnet.net:1521/oss")
            self.conn = cx_Oracle.connect("%s/%s@%s.netact.nsn-rdnet.net:%d/oss"%(self.uname,self.pwd,self.host,self.port))     
            self.cursor = self.conn.cursor()  
            self.__Log.info('Connect to NetAct_db:%s successfully'%self.host)
        except Exception as err:
            raise Exception('connect to netact_db failed,error:%s'%err)
    
    def execute_command(self,command):
        try:
            self.cursor.execute(command)
            self.__Log.info('Execute SQL:%s successfully'%command)
            return self.cursor  

        except Exception as error:
            self.close_connection()
            raise Exception('Execute SQL statement [%s] failed, exception [%s]' % (command, error))
            
    
    def close_connection(self):
        self.cursor.close()
        #self.conn.commit()  Only read data    
        self.conn.close()
        self.__Log.info('Disconnect NetAct_db successfully')   

    
if __name__ == '__main__':
    NetAct_db('cpf','omc','omc')


