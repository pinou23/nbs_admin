#-*-coding:utf-8-*-
'''
Created on 2017年9月27日

@author: pacao
'''

import time
import paramiko
import os
from logger import Mylog



class File_Oper(object):
    
    def __init__(self, ip, port, uname, pwd):
        self.__Log = Mylog().get_logger()
        self.ip = ip
        self.uname = uname
        self.pwd = pwd
        self.port = int(port)
        self._transport = None
        self._sftp = None
        self.chan = None
        self._connect()  # 建立连接

    def _connect(self):
        #设置ssh连接的远程主机地址和端口
        self._transport = paramiko.Transport(self.ip, self.port)
        #transport.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #设置登录名和密码
        self._transport.connect(username=self.uname, password=self.pwd)
        #连接成功后打开一个channel
        self.chan = self._transport.open_session()
        # 获取一个终端
        self.chan.get_pty()
        # 激活终端
        self.chan.invoke_shell()
        self.__Log.info('Connect to %s successfully'%self.ip)
        
    #下载文件
    def _download_file(self, remote_path, local_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp.get(remote_path, local_path)
            self.__Log.info('Download %s to %s successfully'%(remote_path, local_path))
        except Exception as err:
            raise Exception('Download file failed, reason:%s'%err)
            self.close()  
    #上传文件
    def _upload_file(self, local_path, remote_path):
        try:
            if self._sftp is None:
                self._sftp = paramiko.SFTPClient.from_transport(self._transport)
            self._sftp.put(local_path, remote_path)
        except Exception:
            new_folder = os.path.dirname(remote_path)
            print new_folder
            self._sftp.mkdir(new_folder)
            self.__Log.info('Create new path:%s successfully'%new_folder)
            self._sftp.put(local_path, remote_path)
            #raise Exception('uploadload file failed, reason:%s'%err)
            self.__Log.info('Upload %s to %s successfully'%(local_path, remote_path))
            self.close()  
                    
    def _ssh_command(self,command):
        timeout = 3600*2
        #p = re.compile(r'#')

        result = ''
        self.__Log.info("Execute command '%s'"%command)
        try:
            self.chan.send(command+'\n')
        except Exception as err:
            raise Exception("Send command '%s' fail,reason:%s"%(command,err))
        
        try:
            while True:
                time.sleep(2)
                ret = _timelimit(timeout,self.chan.recv, 65535)
    
                #print ret.decode('utf-8')
                result += ret
                if result[:-1].endswith('#') or result[:-1].endswith('$') or result[:-1].endswith('>'):
                    return result
        except TimeLimitExpired:
            raise Exception("Timeout %ds ,pls check the command:'%s'"%(timeout,command))    
    
    def _ssh_command_without_result(self,command):
        self.__Log.info("Execute command '%s'"%command)
        try:
            self.chan.send(command+'\n')
            print 'Execute command OK'
        except Exception as err:
            raise Exception("Send command '%s' fail,reason:%s"%(command,err))
        
    def _new_jfr_folder(self, remote_path):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)        
        folders = self._sftp.listdir(remote_path)
        jfr_path = remote_path+'/'+'jfr'
        #print jfr_path
        if 'jfr' not in folders:
            self._sftp.mkdir(jfr_path)
            self._sftp.chmod(jfr_path,0777)  #修改文件夹模式为可读可写权限
            print r"create new folder 'jfr' under '/opt'"
        else:
            self._sftp.chmod(jfr_path,0777)    
        #print folders

    def close(self):
        if self.chan:
            self.chan.close()
        if self._transport:
            self._transport.close()

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
        return it.result







# if __name__ == '__main__':
#     command = '/opt/imp/`rpm -qa | grep nokia | cut -d "-" -f 3`/bin/log-helper.sh cacheInfo'
#     b = 'su btsmed'
#     ip = '10.92.67.220'
#     r = execute_command_with_result(ip,command)
#     print r
    
    
    
#     log_path = r'/opt/jfr/imp-test-jfr.jfr'
#     local_path = r'D:\backlog\imp-test-jfr.jfr'
#     ip = '10.92.67.220'
#     start_jfr_log(ip)
#     time.sleep(10)
#     save_jfr_log(local_path)

#     test_dir = r'D:\backlog\test.txt'
#     logtest_path = r'/opt/jfr/cpf/test.txt'
#     
#     result = file_should_contain(r'D:\cpf\log_test\New folder\imp.log','.*mrbts-3492')
#     print 'done'
#     print result
    
#     for i in result:
#         print i

    
#     ip = '10.91.125.59'
#     username = 'toor4nsn'
#     password = 'oZPS0POrRieRtu'
#     command = 'su btsmed'
#     command1 = 'jcmd -l'
#     port = 22 
#     con = File_Oper(ip, port, username, password)
#     con.ssh_command(command)
#     result = con.ssh_command(command1).split('\n')
#     for i in result:
#         if 'standalone' in i:
#             id = re.findall(r'\d+',i)
#     
#     print id
#     result1 = con.ssh_command(r'jcmd %s JFR.start name=cy compress=true maxsize=300M'%id[0])
#     print result1
#     time.sleep(10)
#     result2 = con.ssh_command(r'jcmd %s JFR.dump name=cy filename=/opt/log/cpf/imp-test-jfr.jfr'%id[0])
#     print result2
#     con.download(r'/opt/log/cpf/imp-test-jfr.jfr',r'D:\backlog\imp-test-jfr.jfr')
#     
#     
#     con.close()     
    