#!/usr/bin/env python
#encoding=utf-8
import socket  
import os
import time
class Communicate():
        #处理收到的数据或命令
        def deal_command(data):
            if '0x01' in data:
                #打开摄像头
               os.system("python open_camera.py")
            elif '0x04' in data:
                #自定义命令
               cus_command=data.split(':')[1]
               print(cus_command) 
               os.system(cus_command)
            else:
                #数据
               timer=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
               f=open('data/'+timer,"w")
               f.write(data)
               f.close()
                
        #连接Socket
        def connect_scoket(self):
            #主机地址    
            HOST_IP=''
            #端口
            HOST_PORT=7777
            #最大传输长度
            MAX_LENGTH=2000
            #最大连接数
            MAX_CONNECT=10
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #让套接字允许地址重用
            s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            addr = (HOST_IP, HOST_PORT)
            s.bind(addr)
            s.listen(MAX_CONNECT)
            while 1:  
            	time.sleep(1)
                conn, (HOST_IP, HOST_PORT) = s.accept()
                data=conn.recv(MAX_LENGTH) 
                if not data:  
                    break  
                else:  
                    print(data)
                    deal_command(data)
                    


