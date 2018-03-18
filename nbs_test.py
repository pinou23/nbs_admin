#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2017年11月30日

@author: pacao
'''


import requests
import logging
import httplib as http_client
import json
import os,sys


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

headers = None
session = None
base_url = None
timeout=120

def init_nbs_host(host,port=12345):
    """This keyword use to init NBS_admin.
    | Input Parameters | Man. | Description |
    | host | Yes | host ip |
    | port | No | host port,default value is 12345 |
    Example
    | init_nbs_host | 10.9.224.173 | 12345 |
    
    """
    global headers
    global base_url
    global session
    port = int(port)
    headers = {'Content-Type':'application/json;charset=UTF-8',
               'Host':'%s:%s'%(host,port),
               'Origin':'http://%s:%s'%(host,port),
               'Referer':'http://%s:%s/index.html'%(host,port),
               'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3047.4 Safari/537.36'
               }
    
    base_url = r'http://%s:%s'%(host,port)
    logging.info('base_url is %s'%base_url)
    #proxies = {"http":"http://10.144.1.10:8080"}
    session = requests.session()

def config_nbs(nhost,shost,nport=8080,sport=8102,tport=49392):
    """This keyword use to config BTS in NBS_admin.
    | Input Parameters | Man. | Description |
    | nhost | Yes | BTSMED North Host |
    | shost | Yes | BTSMED South Host |
    | nport | No | North Port,default is 8080 |
    | sport | No | South Port,default is 8102 |
    | tport | No | Trace Port,default is 49392 |
    Example
    | config_nbs | 10.92.67.220 | 10.92.66.229 | 8080 | 8102 | 49392 |
    
    """
    url = base_url+'/api/imp'
    source_data = {
      'nhost':nhost,
      'shost':shost,
      'nport':int(nport),
      'sport':int(sport),
      'tport':int(tport)
      }
    data=json.dumps(source_data)    

    r = session.post(url,headers=headers,data=data,timeout=timeout)
    #status = session.post(url,headers=headers,data=data).status_code
    status = r.status_code
    if status ==200:
        logging.info('Config nbs successfully')  
    else:
        raise Exception("Config nbs failed,please check the link:%s,reply_status:%d"%(url,status))

    result = eval(r.content)
    for i in source_data:
        if source_data[i] == result[i]:
            continue
        else:
            raise Exception("%s:%s != %s,config nbs fail!"%(i,source_data[i],result[i]))
  
    
def add_bts(size):
    """This keyword use to add BTS in NBS_admin.
    | Input Parameters | Man. | Description |
    | size | Yes | BTS number |
    Example
    | add_bts | 100 |
    
    """
    
    size = int(size)
    url = base_url+'/api/bts'
    logging.info('Add_bts_link is %s'%url)
    data=json.dumps({
      'size':size,
      })

    status = session.post(url,headers=headers,data=data).status_code
    if status ==200:
        logging.info('Add %s bts successfully'%size)
    else:
        raise Exception("Add bts failed,please check the link:%s,reply_status:%d"%(url,status))



def delete_bts(bts_id):
    """This keyword use to delete BTS in NBS_admin.
    | Input Parameters | Man. | Description |
    | bts_id | Yes | BTS id |
    Example
    | delete_bts | 1 |
    | delete_bts | all |
    
    """
    
    if bts_id == 'all':
        url = base_url+'/api/bts/all'
    else:
        url = base_url+'/api/bts/mrbts-%s'%bts_id
    logging.info('delete_bts_link is %s'%url)

    status = session.delete(url,headers=headers,timeout=timeout).status_code
    if status ==200:
        logging.info('Delete mrbts-%s successfully'%bts_id)
    else:
        raise Exception("Delete bts failed,please check the link:%s,reply_status:%d"%(url,status))

    
def notify_alarm(bts_id,ratio,per_bts,alarm_num):
    """This keyword use to trigger fault to BTS in NBS_admin.
    | Input Parameters | Man. | Description |
    | bts_id | Yes | BTS ID Range |
    | ratio | Yes | Events Ratio |
    | per_bts | Yes | Events per BTS |
    | alarm_num | Yes | Alarm Number |
    
    Example
    | notify_alarm | all | 100 | 10 | 7100 |
    
    """
    
    url = base_url+'/api/operation/notify_alarm'
    logging.info('notify_alarm_link is %s'%url)
    data=json.dumps({
      'amount':bts_id,
      'ratio':int(ratio),
      'loop':int(per_bts),
      'alarm':[alarm_num]
      })

    status = session.post(url,headers=headers,data=data,timeout=2*60*60).status_code
    if status ==200:
        logging.info('Notify alarm%s successfully'%alarm_num)
    else:
        raise Exception("Notify alarm%s failed,please check the link:%s,reply_status:%d"%(alarm_num,url,status)) 
  

def cancel_alarm(bts_id):
    """This keyword use to cancel fault to BTS in NBS_admin.
    | Input Parameters | Man. | Description |
    | bts_id | Yes | BTS ID Range |
    
    Example
    | cancel_alarm | all |
    
    """
    url = base_url+'/api/operation/cancel_alarm'
    logging.info('notify_alarm_link is %s'%url)
    data=json.dumps({
      'amount':bts_id,
      })

    status = session.post(url,headers=headers,data=data,timeout=timeout).status_code
    if status ==200:
        logging.info('Cancel alarm for %s successfully'%bts_id)
    else:
        raise Exception("Cancel alarm for %s failed,please check the link:%s,reply_status:%d"%(bts_id,url,status)) 

def pm_upload(bts_id_range,per_bts,interval,cell_number):
    """This keyword use to upload pm filein NBS_admin.
    | Input Parameters | Man. | Description |
    | bts_id_range | Yes | BTS ID Range |
    | per_bts | Yes | Events per BTS |
    | interval | Yes | Interval T(min) |
    | cell_number | Yes | Cell Number |
    Example
    | pm_upload | all | 10 | 15 | 1 |
    
    """
    url = base_url+'/api/operation/pm_upload'
    logging.info('pm_upload_link is %s'%url)
    data=json.dumps({
      'amount':bts_id_range,
      'loop':int(per_bts),
      'interval':int(interval)*60,
      'cell':int(cell_number)
      })
    #print data
    logging.info('post data:%s'%data)
    status = session.post(url,headers=headers,data=data,timeout=2.5*60*60).status_code
    if status ==200:
        logging.info('PM upload successfully')
    else:
        raise Exception("PM upload failed,please check the link:%s,reply_status:%d"%(url,status)) 
def cancel_pm_upload():
    """This keyword use to cancel pm uoload in NBS_admin.
    Example
    | cancel_pm_upload |
    
    """
    url = base_url+'/api/operation/stop'
    logging.info('cancel_pm_upload_link is %s'%url)
    status = session.post(url,headers=headers,timeout=timeout).status_code
    if status ==200:
        logging.info('Cancel PM upload successfully')
    else:
        raise Exception("Cancel PM upload failed,please check the link:%s,reply_status:%d"%(url,status))
        

if __name__ == '__main__':
    init_nbs_host('10.9.224.174',12345)
    config_nbs('10.92.67.220','10.92.66.229')
    #pm_upload('all',2,1,1)
    #add_bts(100)
    #delete_bts('all')
