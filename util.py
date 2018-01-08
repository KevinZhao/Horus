# -*- coding:utf-8 -*-
import os 
import shutil
import time
import logging
import json
import signal
#日志log类
def log(log_str):

    fd = open('/tmp/Horus.log', 'w')
    
    while True:
        fd.write(log_str + '\n')
        fd.flush()
        time.sleep(1)
    fd.close()

#文件夹下的所有文件移动到指定文件夹
def folder_move_all(folder_path,newpath):
	if os.path.exists(folder_path):
		dirs=os.listdir(folder_path)
		for i in range(0,len(dirs)):
			print(dirs[i])
			oldfilepath = os.path.join(folder_path,dirs[i])
			newfilepath=os.path.join(newpath,dirs[i])
			shutil.move(oldfilepath,newfilepath)

def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError:
            log('ValueError: is not json data')
            return False
        return True

def alter(files,key,value):
    new_str = ""
    with open(files, "r") as f:
        for line in f:
            if key in line:
                first_part=line.split('=')[0]
                line=''
                line+=first_part+"="+value
            new_str += line
    with open(files,"w") as f:
        if new_str != '':
            f.write(new_str)

def kill(pid):
        try:
            a = os.kill(pid, signal.SIGKILL)
        except OSError, e:
            log('OSError: no such pid')






