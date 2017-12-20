# -*- coding:utf-8 -*- 
from img_proc. import *
from obj_detect. import *
import os
import sys

def createCommunicate():
	import communicate.communicate as commu
	communicate=commu.Communicate();
	communicate.connect_scoket();

#守护进程
def createDaemon():
	try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print (sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror))
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
        print (sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        sys.exit(1)
    #创建通讯模块
    createCommunicate()

if __name__ == "__main__":
	createDaemon()
	