#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import time
from sqlalchemy import create_engine
import sys

class Camera():
    def opencamera(self):
        #打开摄像头
        cap=cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720,format=(string)I420, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
        #关闭摄像头 cap.release()
        global timeF
        number=1
        sys.path.append("..")
        import config
        c=config.TIME_FREQUENCY
        if c == 0:
            c = 200
        elif c == None:
            c = 200
        timeF = c/1000.0
        while True:
            ret, frame = cap.read()
            while True:
                shijian=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                img_id=shijian+str(number);
                imgname=config.FILE_PATH+'/'+shijian+str(number)+'.png'
                cv2.imwrite(imgname,frame)
                conn = create_engine('mysql://root:nvidia@localhost:3306/miner?charset=utf8')
                sqlInsert='insert into tb_camera(timestamp,img_id,frequency) values(%s,%s,%s)'%(shijian,img_id,timeF)
                conn.execute(sqlInsert)
                number+=1
                time.sleep(timeF)


