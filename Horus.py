# -*- coding:utf-8 -*- 
import os
import sys
import time
import threading
from communicate import communicate as commu 
from darknet import file_listener
from Queue import Queue
import util
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
                util.log(e.errno)
                util.log(e.strerror)
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
                    print ("Daemon PID %d" % pid)
                    sys.exit(0)
        except OSError, e:
                util.log(e.errno)
                util.log(e.strerror)
                sys.exit(1)
        
        #开启通讯模块
        createCommunicate()



if __name__ == "__main__":
    file_thread=myFileThread()
    file_thread.start()
    createDaemon()

