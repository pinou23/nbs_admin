#-*-coding:utf-8-*-
'''
Created on 2017年12月7日

@author: pacao
'''
from collect_log import *
import logger
from nbs_test import *
from netact_db import *


import os,re,datetime

from constant import *


def _check_msg_in_file(source_file_path, target_msgs):
    #lines = filec.read_file(source_file_path, 'r', 'list')
    contain_lines = []

    if not isinstance(target_msgs, list):
        target_msgs = [target_msgs]

    unfound_msgs = [msg for msg in target_msgs]
    with open(source_file_path, "r") as file_obj:
        for line in file_obj:
            for keyword in target_msgs:
                search_result = re.search(keyword, line)
                if search_result:
                    #print("Find '%s' in line <%s>" % (keyword, line))
                    contain_lines.append(line)
                    try:
                        unfound_msgs.remove(keyword)
                    except ValueError:
                        pass
    return unfound_msgs, target_msgs, contain_lines

def _modify_tnsnames(db_host,file_path=tnsnames_path):
    """This keyword use to modify tnsnames to corresponding value before connecting to database.
    | Input Parameters | Man. | Description |
    | db_host | Yes | NetAct_db host |
    | file_path | No | tnsnames.ora file path |
    Example
    | modify_tnsnames | 10.92.66.42 |
    
    """
    rc = re.compile(".*HOST = (.*).netact.nsn-rdnet.net.*")
    host_name = None
    with open(file_path,'r+') as f:
        for line in f:
            print line
            result = rc.match(line)
            if result:
                host_name =  result.groups()[0]
        if not host_name:
            raise Exception('Get db_host_name fail!')        
        
    with open(file_path,'r+') as f:
        content = f.read()
        content = content.replace(host_name,NetAct_DB_SUITE[db_host])
        f.seek(0)  
        f.truncate(0)
        f.write(content)

#**********************Keyword for writing TA script********************************

def file_should_contain(source_file_path, target_msgs):
    """This keyword checks whether file contains specified messages.
    | Input Parameters | Man. | Description |
    | source_file_path | Yes | Source file directory |
    | target_msgs | Yes | type as list or string |

    | Return value | lines contain given messages |

    Example
    | File Should Contain | C:\\test.txt | PBCH |  |
    | ${check_list} | create list | PBCH | Onair |
    | File Should Contain | C:\\test.txt | ${check_list} |  |
    """

    unfound_msgs, target_msgs, contain_lines = _check_msg_in_file(
        source_file_path, target_msgs)

    if len(unfound_msgs) != 0:  # some messages was not found
        raise Exception(
            "Not find '%s' in '%s'" %
            (unfound_msgs, source_file_path))

    return contain_lines

def ssh_to_remote_host(host_ip,port=PORT,uname=USERNAME,pwd=PASSWORD):
    """This keyword use ssh to connect remote host.
    | Input Parameters | Man. | Description |
    | host_ip | Yes | host ip |
    | port | Yes | host port,default: 22 |
    | uname | Yes | host username |
    | pwd | Yes | host password |
        
    | Return value | ${instance} |
    Example
    | ${instance} |  execute_command_to_remote_host| 10.92.67.220 | 22 | root | arthur |
    
    """
    inst = File_Oper(host_ip, port, uname, pwd)
    return inst

def execute_command_to_remote_host(inst,command):
    """This keyword use to send command to remote host.
    | Input Parameters | Man. | Description |
    | inst | Yes | connection object from 'ssh_to_remote_host' |
    | command | Yes | the command send to remote host|
    
    | Return value | ${result} |
    Example
    | ${result} | execute_command_to_remote_host | ${instance} | su btsmed |
    
    """
    result = inst._ssh_command(command)
    return result

def execute_command_to_remote_host_without_result(inst,command):
    """This keyword use to send command to remote host.
    | Input Parameters | Man. | Description |
    | inst | Yes | connection object from 'ssh_to_remote_host' |
    | command | Yes | the command send to remote host|
    
    Example
    | execute_command_to_remote_host_without_result | ${instance} | su btsmed |
    
    """
    inst._ssh_command_without_result(command)


def close_ssh_connection(inst):
    """This keyword use to close ssh_connection.
    | Input Parameters | Man. | Description |
    | inst | Yes | connection object from 'ssh_to_remote_host' |
    Example
    | close_ssh_connection | ${inst} |
    
    """
    inst.close()
        
def sftp_download(host_ip,remote_path, local_path,uname=USERNAME,pwd=PASSWORD):
    """This keyword use to download files from host to local.
    | Input Parameters | Man. | Description |
    | host_ip | Yes | host ip address |
    | remote_path | Yes | host file dir |
    | local_path | Yes | local file |
    | uname | No | username,default as 'toor4nsn' |
    | pwd | Yes | password,default as 'oZPS0POrRieRtu' |
    Example
    | Sftp_Download | 10.91.125.59 | //opt//jfr//cpf//test.txt | D:\\backlog\\test.txt |
    """
    instance = File_Oper(host_ip, PORT, uname, pwd)
    instance._download_file(remote_path, local_path)
    instance.close()

def sftp_upload(host_ip,local_path, remote_path,uname=USERNAME,pwd=PASSWORD):
    """This keyword use to upload files from host to local.
    | Input Parameters | Man. | Description |
    | host_ip | Yes | host ip address |
    | local_path | Yes | local file |
    | remote_path | Yes | host file dir |
    | uname | No | username,default as 'toor4nsn' |
    | pwd | Yes | password,default as 'oZPS0POrRieRtu' |

    Example
    | Sftp_Download | 10.91.125.59 | D:\\backlog\\test.txt | //opt//jfr//cpf//test.txt |
    """
    instance = File_Oper(host_ip, PORT, uname, pwd)
    instance._upload_file(local_path, remote_path)
    instance.close()
        

process_id = None
ssh_instance = None

def start_jfr_log(host_ip):
    """This keyword starts catching of JFR log.
    | Input Parameters | Man. | Description |
    | host_ip | Yes | IP used for generating JFR log |
    Example
    | Start_JFR_Log | 10.91.125.59 |
    """
    global process_id
    global ssh_instance

    command1 = 'su btsmed'
    command2 = 'jcmd -l'
    remote_path = r'/opt'
    
    #ssh连接到ip
    ssh_instance = File_Oper(host_ip, PORT, USERNAME, PASSWORD)
    print 'SSH connect to %s successfully'%host_ip
    try:
        ssh_instance._new_jfr_folder(remote_path)  #如果文件夹没有，则在/opt下新建jfr文件夹
        ssh_instance._ssh_command(command1)
        result = ssh_instance._ssh_command(command2).split('\n')
        for i in result:
            #print i
            if 'standalone' in i:
                process_id = re.findall(r'\d+',i)[0]
        if process_id:
            print 'The process id is %s'%process_id
            #开启JFR进程
            result = ssh_instance._ssh_command(r'jcmd %s JFR.start name=cpf compress=true maxsize=300M'%process_id)
        else:
            raise Exception('The process id is not found, pls check the command!')
    except Exception as err:
        raise Exception("start jfr log fail,err:%s"%err)
        ssh_instance.close()

def save_jfr_log(local_path):
    """This keyword save JFR log to local path.
    | Input Parameters | Man. | Description |
    | local_path | Yes | local_path |
    Example
    | Save_JFR_Log | local_path='D:\\backlog\\imp-test-jfr.jfr' |
    
    """
    try:
        time_flag = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        log_path = r'/opt/jfr/imp-test-jfr_%s.jfr'%time_flag
        
        #将缓存中的数据存储到文件里
        ssh_instance._ssh_command(r'jcmd %s JFR.dump name=cpf filename=%s'%(process_id,log_path))
        
        starttime = datetime.datetime.now()
        file_size = ssh_instance._sftp.stat(log_path).st_size
        print '%s Start to save JFR log, file size is about %sM'%(starttime,file_size/(1024*1024))
        
        #下载jfr文件到本地 
        ssh_instance._download_file(log_path, local_path)
        
        endtime = datetime.datetime.now()
        print '%s JRF log has saved to %s'%(endtime,local_path)
        
        #结束进程并删除远程PC上的文件
        ssh_instance._ssh_command('jcmd %s JFR.stop name=cpf discard=true'%(process_id))
        ssh_instance._sftp.remove(log_path)
    except Exception as err:
        raise Exception("save jfr log fail,err:%s"%err)
        ssh_instance.close()

def compare_logs_num_and_get_lost_logs(log_content,num_total,check_point):
    """This keyword will compare log numbers and return lost numbers if the log_content's number is not match with num_total.
    | Input Parameters | Man. | Description |
    | log_content | Yes | local_path |
    | num_total | Yes | log numbers |
    | check_point | Yes | check_point |
    
    | Return value | return compare result and lost numbers | eg.(False, [3, 31])
    Example
    | compare_logs_num_and_get_lost_logs | ${log_content} | 32 | "mrbts-%d transaction" |
    
    """
    match = True if len(log_content)==num_total else False
    lost=[]
    for num in range(num_total):
        num = num+1
        flag = False
        for i in log_content:
            if check_point%num in i:
                flag = True
                break
        if not flag:
            lost.append(num)
            
    return (match,lost)

def connect_to_NetAct_db(host,uname=DB_UNAME,pwd=DB_PWD,port=1521):    
    """This keyword use to connect NetAct database,make sure you has accessed to Tampere Laboratory Login Service before using this keyword.
    | Input Parameters | Man. | Description |
    | host | Yes | NetAct database host |
    | uname | No | NetAct database usename,default as 'omc' |
    | pwd | No | NetAct database password,default as 'omc' |
    | host | No | NetAct database port,default is 1521 |
    
    | Return value | db_conn |
    Example
    | connect_to_NetAct_db | 10.91.125.20 |
    
    """
    _modify_tnsnames(host)
    db_conn = NetAct_db(NetAct_DB_SUITE[host],uname,pwd,port)
    return db_conn

def send_command_to_NetAct_db(db_conn,sql_statement):    
    """This keyword use to send SQL statement.
    | Input Parameters | Man. | Description |
    | db_conn | Yes  | connection object from 'connect_to_NetAct_db' |
    | sql_statement | Yes | sql query statement |
    
    | Return value | result |
    Example
    | send_command_to_NetAct_db | ${db_conn} | "select count(0) from fx_alarm where alarm_number= 7100" |
    
    """
    cursor = db_conn.execute_command(sql_statement)
    result = cursor.fetchall()
    return result

def close_NetAct_db_connection(db_conn):    
    """This keyword use to close NetAct_db_connection after using the database.
    | Input Parameters | Man. | Description |
    | db_conn | Yes | connection object from 'connect_to_NetAct_db' |
    Example
    | close_NetAct_db_connection | ${db_conn} |
    
    """
    db_conn.close_connection()

def generate_cm_upload_command(num_start,num_end):
    """This keyword use to generate cm upload command.
    | Input Parameters | Man. | Description |
    | num_start | Yes | first BTS id |
    | num_end | Yes | last BTS id |
    
    | Return value | ${com} | #cm upload command
    Example
    | ${com} | generate_cm_upload_command | 1 | 3 |
    return "racclimx.sh -DN PLMN-PLMN/MRBTS-1,PLMN-PLMN/MRBTS-2,PLMN-PLMN/MRBTS-3 -op Upload -v"
    """
    command = []
    base_info = "PLMN-PLMN/MRBTS-"
    for i in range(int(num_start),int(num_end)+1):
        info = base_info+str(i)
        #print info
        command.append(info)
    com = ",".join(command)
    com = "racclimx.sh -DN "+com+" -op Upload -v"
    return com


if __name__ == '__main__':
    
    
#     c = generate_cm_upload_command(1,20)
#     print type(c)
#     print c
#     path = r'C:\product\12.1.0\client_1\tnsnames.ora'
#     _modify_tnsnames('10.92.66.42',path)
    
    
    ip = '10.92.67.172'
    username = 'toor4nsn'
    password = 'oZPS0POrRieRtu'
    command = 'nohup nbscli start-admin 12345 8001 &'
#     command1 = 'jcmd -l'
    port = 22 
    con = ssh_to_remote_host(ip, port, username, password)
    execute_command_to_remote_host_without_result(con,command)
#     print 'r:',r
#     r1 = execute_command_to_remote_host(con,'su - oracle')
#     print 'r1:',r1
#     r2 = execute_command_to_remote_host(con,'sqlplus /nolog')
#     print 'r2:',r2
#     r3 = execute_command_to_remote_host(con,'connect /as sysdba')
#     print 'r3:',r3
#     execute_command_to_remote_host(con,'TRUNCATE table FM.FM_EVENTS;')
#     execute_command_to_remote_host(con,'TRUNCATE table FM.FX_EVENTS;')
#     execute_command_to_remote_host(con,'TRUNCATE table FM.FM_ALARM_STATES;')
#     execute_command_to_remote_host(con,'TRUNCATE table AC.AC_CORRELATION;')
#     execute_command_to_remote_host(con,'TRUNCATE table AC.AC_HISTORY;')
#     r4 = execute_command_to_remote_host(con,'TRUNCATE table FM.FX_ALARM;')
#     print 'r4:',r4
        
#     init_nbs_host('10.91.125.30',12345)
#     config_nbs('10.91.125.59','10.91.63.218')
#     #add_bts(1)
#     notify_alarm('all',100,10,7100)
# 
#     
#     db_host = 'sprintlab317vm4'
#     db_uname = 'omc'
#     db_pwd = 'omc'
#     sql = "select count(0) from fx_alarm where alarm_number= 7200"
#     con = connect_to_NetAct_db(db_host, db_uname, db_pwd)
#     r = send_command_to_NetAct_db(con,sql)
#     print r
#     close_NetAct_db_connection(con)
    
    
#     command = '/opt/imp/`rpm -qa | grep nokia | cut -d "-" -f 3`/bin/log-helper.sh cacheInfo'
#     b = 'su btsmed'
#     ip = '10.92.67.220'
#     r = execute_command_to_remote_host(command,ip)
#     print r