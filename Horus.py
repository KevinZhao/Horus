# -*- coding:utf-8 -*- 
import os
import sys
import time
import threading
from communicate import communicate as commu 
from darknet import file_listener
from Queue import Queue
import util
import socket
import json

#开启通讯模块
def createCommunicate():
        commu.Communicate().connect_scoket();
        while True:
                time.sleep(1)


class myFileThread (threading.Thread):   
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):                   
        file_listener.startListener()

#守护进程
def createDaemon():
        try:
                pid = os.fork()
                if pid > 0:
                    # exit first parent
                    sys.exit(0)
        except OSError as e:
                util.Logprint(5,e.errno+e.strerror)
                # util.log(e.errno)
                # util.log(e.strerror)
                sys.exit(1)
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent, print eventual PID before
                    sys.exit(0)
        except OSError, e:
                # util.log(e.errno)
                # util.log(e.strerror)
                util.Logprint(5,e.errno+e.strerror)
                sys.exit(1)
        
        #开启通讯模块
        createCommunicate()


#自动获取当前IP地址
def Get_local_ip():

    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

def main():

    while True:
        ip=Get_local_ip()
        if ip and ip!="127.0.0.1":
            #修改IP地址
            with open('/home/nvidia/Horus/config.cnf') as f:
                cnf = json.load(f)
                cnf['host_ip']=ip
                jsonstr=json.dumps(cnf,ensure_ascii=False,sort_keys=True)
                util.replace('/home/nvidia/Horus/config.cnf',jsonstr)

            file_thread=myFileThread()
            file_thread.start()
            createDaemon()
            
            break;

        else:
            continue;





if __name__ == "__main__":
    main()
