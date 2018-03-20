#!/usr/bin/env python
#encoding=utf-8
import sys
import cv2
import time
import json

global number
global shijian


def opencamera():
        number=0
        shijian=''
        #打开摄像头
        cap = cv2.VideoCapture(1)
        with open("/home/nvidia/Horus/config.cnf", 'r') as f:
            cnf = json.load(f)
            imagesize=int(cnf['imagesize'])
            if imagesize==2:
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);  
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480); 
            else :
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280);  
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);

            global timeF
    
            c=int(cnf['time_frequency'])
            if c == 0:
                c = 200
            elif c == None:
                c = 200
            timeF = c/1000.0
            while True:
                ret, frame = cap.read()
                # while True:
                    if shijian==time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())):
                        number+=1
                    else:
                        number=0
                        shijian=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

                    img_id=shijian+str(number);
                    imgname=cnf['cap_path']+'/'+shijian+str(number)+'.jpg'
                    cv2.imwrite(imgname,frame)
                    time.sleep(timeF)

if __name__ == '__main__':
    opencamera()

