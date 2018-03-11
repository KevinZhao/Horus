# -*- coding:utf-8 -*-
import os 
import shutil
import time
import logging
import json
import signal
import threading
import string 
# import cv2
# import numpy
# import config


with open('/home/nvidia/Horus/config.cnf') as f:
    cnf = json.load(f)
level=int(cnf['level'])

def log(log_str):

    fd = open('/tmp/Horus.log', 'w')
    
    while True:
        fd.write(log_str + '\n')
        fd.flush()
        time.sleep(1)
    fd.close()


#log日志打印
#0：不打印
#1：debug
#2：info
#3：warnning
#4：error
#5：fatal
#level代表可打印的级别

def Logprint(debug,log):
    if level==0:
        pass
    elif level==1:
        if debug==1:
            print("debug:",log)
        elif debug==2:
            print("info:",log)
        elif debug==3:
            print("warnning:",log)
        elif debug==4:
            print("error:",log)
        elif debug==5:
            print("fatal:",log)

    elif level==2:
        if debug==2:
            print("info:",log)
        elif debug==3:
            print("warnning:",log)
        elif debug==4:
            print("error:",log)
        elif debug==5:
            print("fatal:",log)

    elif level==3:
        if debug==3:
            print("warnning:",log)
        elif debug==4:
            print("error:",log)
        elif debug==5:
            print("fatal:",log)

    elif level==4:
        if debug==4:
            print("error:",log)
        elif debug==5:
            print("fatal:",log)

    elif level==5:
        if debug==5:
            print("fatal:",log)




#文件夹下的所有文件移动到指定文件夹
def folder_move_all(folder_path,newpath):
	if os.path.exists(folder_path):
		dirs=os.listdir(folder_path)
		for i in range(0,len(dirs)):
			oldfilepath = os.path.join(folder_path,dirs[i])
			newfilepath=os.path.join(newpath,dirs[i])
			shutil.move(oldfilepath,newfilepath)

#移动单张图片
def move_single_image(old_folder_path,new_folder_path,imagename):
    oldfilepath = os.path.join(old_folder_path,imagename)
    newfilepath=os.path.join(new_folder_path,imagename)
    shutil.move(oldfilepath,newfilepath)

#将文件复制到指定目录
def copy_file(oldfilepath,newfilepath):
    if os.path.exists(oldfilepath):
        shutil.copyfile(oldfilepath,newfilepath)
            

def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError:
            Logprint(4,'ValueError: is not json data')
            return False
        return True


#删除文件并替换
def replace(filename,jsonstr):
    if os.path.exists(filename):
        os.remove(filename)
    f = open(filename, 'w+')
    f.write(jsonstr)
    f.close()


#新字符串替换就字符串
def alter(file,old_str,new_str):
        
        file_data = ""
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                if old_str in line:
                    line = line.replace(old_str,new_str)
                file_data += line
        with open(file,"w",encoding="utf-8") as f:
            f.write(file_data)

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

#字符串中只保留数字和_
def OnlyNumber(text):
    fomart = '0123456789'
    for c in text:
        if not c in fomart:
            text=text.replace(c,'')
    return text
    
# #图像旋转180度
# def rotate(imgpath,imagename):
#     image=cv2.imread(imgpath)
#     # 获取图片尺寸并计算图片中心点
#     (h, w) = image.shape[:2]
#     center = (w/2, h/2)
#     # 将图像旋转180度
#     M = cv2.getRotationMatrix2D(center, 180, 1.0)
#     rotated = cv2.warpAffine(image, M, (w, h))
#     # image_path=config.FILE_PATH+'/'+imagename+'.jpg'
#     # print(image_path)
#     # cv2.imwrite(image_path,rotated)
#     # cv2.waitKey(0)









