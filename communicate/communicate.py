#!/usr/bin/env python
#encoding=utf-8
import socket
import os
import time
import datetime
import camera
import sys
import struct
import json
from sqlalchemy import text
from sqlalchemy import create_engine
import select
import os

class Communicate():
    
    pid=1
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
            util.log('no such log file')

    def createCamereDaemon(self):
        pid = os.fork()
        if pid > 0:
            return pid
        # 开启摄像头
        camera.Camera().opencamera()

    

    
    #处理收到的数据或命令
    def deal_command(self,socket,data):
        sys.path.append("..")
        import config
        import util
        if '0x01' in data:
            #摄像头操作
            global pid
            pid = Communicate().createCamereDaemon()

        elif '0x02' in data:
            #自定义命令
            cus_command=data.split(':')[1]
            if cus_command != '':
                os.system(cus_command)

        elif '0x03' in data:
            util.kill(pid)
            util.folder_move_all(config.FILE_PATH,config.PIC_PATH)

        elif '0x04' in data:
            Communicate().sendFile(socket,config.LOG_PATH)

        elif '0x05' in data:
            key=data.split(':')[1]
            value=data.split(':')[2]
            if key != '' and value != '':
                util.alter("/home/nvidia/Horus/config.py", key, value)

        elif 'test' in data:
            pass

        else:
            if util.is_json(data):
                with open('/home/nvidia/Horus/mysql/sql.cnf') as json_data:
                    cnf = json.load(json_data)
                    db = create_engine(cnf['db'])
                    s=json.loads(data)
                    insert_data="insert into tb_mobile_sensor(timestamp,accx,accy,accz,gpsLongitude,gpsLatitude,gpsAltitude,gpsSpeed,gpsBearing,light,deviceID,frequency) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%(s["time"],s["accx"],s["accy"],s["accz"],s["longitude"],s["latitude"],s["altitude"],s["speed"],s["bearing"],s["lightx"],s["deviceID"],s["frequency"])
                    db.execute(insert_data)


    #连接Socket
    def connect_scoket(self):
        sys.path.append("..")
        import config
        #主机地址
        HOST_IP=config.HOST_IP
        #端口
        HOST_PORT=config.HOST_PORT
        #最大传输长度
        MAX_LENGTH=config.MAX_LENGTH
        #最大连接数
        MAX_CONNECT=config.MAX_CONNECT
        #客户端超时
        TIME_OUT=config.TIME_OUT
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
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
                    print address
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
        

                    


