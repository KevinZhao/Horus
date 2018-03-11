#!/usr/bin/env python
#encoding=utf-8
import socket
import os
import time
import datetime
import sys
import struct
import json
import subprocess
from sqlalchemy import text
from sqlalchemy import create_engine
import select
import os
sys.path.append("..")
from envsensor import envsensor_observer as env
import multiprocessing 
import psutil
import threading

envid=1



class Communicate():

    #发送文件数据
    def sendFile(self,socket,filepath):
        if os.path.isfile(filepath):
            filesize = struct.calcsize('128sl')#定义打包规则
            #定义文件头信息，包含文件名和文件大小
            fhead = struct.pack('128sl',os.path.basename(filepath),os.stat(filepath).st_size)
            socket.send(fhead)
            fo = open(filepath,'rb')
            while True:
                filedata = fo.read(1024)
                if not filedata:
                    break
                socket.send(filedata)
            fo.close()
        else:
            sys.path.append("..")
            import util
            util.Logprint(4,'no such log file')

    def dbquery(self,socket):
        with open("/home/nvidia/Horus/config.cnf", 'r') as f:
            cnf = json.load(f)
            db = create_engine(cnf['db'])
            sql_query = 'select * from tb_object_statistics'
            count = db.execute(sql_query).fetchall()
            socket.sendall(str(len(count))+"eof")



    def createnvDaemon(self):
        envid = os.fork()
        if envid > 0:
            return envid
        env.evsensor()
    
    #处理收到的数据或命令
    def deal_command(self,socket,data):
        sys.path.append("..")
        import util
        if '0x01' in data:
            util.Logprint(2,data)
            #打开摄像头
            with open('/home/nvidia/Horus/config.cnf') as f:
                cnf = json.load(f)
                fq=1000/int(cnf['time_frequency'])
                wb=int(cnf['whitebalance'])
                ae=int(cnf['autoexposure'])
                size=int(cnf['imagesize'])
            cmd='/home/nvidia/Horus/nvgstcapture-1.0 --setWB='+str(wb)+' --setFQ='+str(fq)+' --setAE='+str(ae)+' --image-res='+str(size)
            subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            util.Logprint(2,"open the camera:"+cmd)
    
            
        elif '0x02' in data:
            #自定义命令
            util.Logprint(2,data)
            cus_command=data.split(':')[1]
            if cus_command != '':
                os.system(cus_command)

        elif '0x03' in data:
            util.Logprint(2,data)
            #关闭摄像头
            pids = psutil.pids()
            for pid in pids:
                p = psutil.Process(pid)
                if "nvgstcapture-1.0" in p.name():
                    util.Logprint(1,data)
                    util.kill(pid)
#            with open('/home/nvidia/Horus/config.cnf') as f:
#                cnf = json.load(f)
#            util.folder_move_all(cnf['cap_path'],cnf['arc_path'])


        elif '0x04' in data:
            #发送日志
            # Communicate().sendFile(socket,config.LOG_PATH)
            pass

        elif '0x05' in data:
            import util#更新config的level值
            util.Logprint(2,data)
            #设置config
            key=data.split(':')[1]
            value=data.split(':')[2]
            #修改K-V
            with open('/home/nvidia/Horus/config.cnf') as f:
                cnf = json.load(f)
                cnf[key]=value
                jsonstr=json.dumps(cnf,ensure_ascii=False,sort_keys=True)
                util.replace('/home/nvidia/Horus/config.cnf',jsonstr)
        elif '0x06' in data:
            util.Logprint(2,data)
            #打开环境传感器
            global envid
            envid = Communicate().createnvDaemon()

        elif '0x07' in data:
            util.Logprint(2,data)
            #关闭环境传感器
            util.kill(envid)
        elif '0x08' in data:
            util.Logprint(2,data)
            obddata=data[5:]
            if util.is_json(obddata):
                with open('/home/nvidia/Horus/config.cnf') as json_data:
                    cnf = json.load(json_data)
                    db = create_engine(cnf['db'])
                    s = json.loads(obddata)
                    insert_data = "insert into tb_obd(timestamp,longitude,latitude,altitude,speed) values (%s,%s,%s,%s,%s)" % (s["timestamp"],  s["longitude"], s["latitude"], s["altitude"],s["speed"])
                    db.execute(insert_data)
        elif '0x09' in data:
            util.Logprint(2,data)
            #关闭摄像头
            pids = psutil.pids()
            for pid in pids:
                
                p = psutil.Process(pid)
                if "python" in p.name():
                    ss=p.cmdline()
                    if len(ss)>0:
                        if ss[1]=="Horus.py":
                            util.kill(pid)
                    util.Logprint(1,data)
            #杀死运行程序
                if "Horus" in p.name():
                    util.kill(pid)
                            
#
        elif 'test' in data:
            util.Logprint(1,data)
            #心跳测试和数据库表的条目查询
            Communicate().dbquery(socket)
            pass

        else:
            util.Logprint(1,data)
            #手机端json数据
            if util.is_json(data):
                with open('/home/nvidia/Horus/config.cnf') as json_data:
                    cnf = json.load(json_data)
                    db = create_engine(cnf['db'])
                    s=json.loads(data)
                    insert_data="insert into tb_mobile_sensor(timestamp,accx,accy,accz,gpsLongitude,gpsLatitude,gpsAltitude,gpsSpeed,gpsBearing,light,deviceID,frequency) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%(s["time"],s["accx"],s["accy"],s["accz"],s["longitude"],s["latitude"],s["altitude"],s["speed"],s["bearing"],s["lightx"],s["deviceID"],s["frequency"])
                    db.execute(insert_data)


    #连接Socket
    def connect_scoket(self):
        with open('/home/nvidia/Horus/config.cnf') as f:
            cnf = json.load(f)
        #主机地址
        HOST_IP=cnf['host_ip']
        #端口
        HOST_PORT=cnf['host_port']
        #最大传输长度
        MAX_LENGTH=cnf['max_length']
        #最大连接数
        MAX_CONNECT=cnf['max_connect']
        #客户端超时
        TIME_OUT=cnf['time_out']
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #阻塞模式
        # sock.setblocking(1)
        #非阻塞模式
        # sock.setblocking(0)
        epoll = select.epoll()
        #获取创建好的sock的文件描述符
        fd = sock.fileno()
        sock.bind((HOST_IP,HOST_PORT))
        sock_dict = {}
        sock_dict[fd] = sock
        #对该sock进行注册
        epoll.register(fd,select.EPOLLIN)
        sock.listen(MAX_CONNECT)
        while True:
            events = epoll.poll(1)
            for fileno,event in events:
                #获取到的文件描述符和sock的相同就说明是一个新的连接
                if fileno == fd:
                    (client,address) = sock.accept()
                    #util.Logprint(3,address)
                    print(address)
                    client.setblocking(0)
                    #将新的连接进行注册，用来接收消息
                    epoll.register(client.fileno(),select.EPOLLIN)
                    sock_dict[client.fileno()] = client
                elif event & select.EPOLLIN:
                    data = sock_dict[fileno].recv(MAX_LENGTH)
                    if len(data) == 0:
                        epoll.unregister(fileno)
                    else:
                        Communicate().deal_command(client,data)

                    


