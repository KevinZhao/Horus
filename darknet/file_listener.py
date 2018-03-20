#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import pyinotify
import sys
import darknet
import json
from sqlalchemy import create_engine
from sqlalchemy import text
sys.path.append("..")
import util
from PIL import Image

with open('/home/nvidia/Horus/config.cnf') as f:
    cnf = json.load(f)
c=int(cnf['time_frequency'])
if c == 0:
    c = 200
elif c == None:
    c = 200
timeF = c/1000.0

cur_time='2018'


class MyEventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CLOSE_WRITE(self, event):
         
        with open('/home/nvidia/Horus/config.cnf') as json_data:
                    cnf = json.load(json_data)                
                    db = create_engine(cnf['db'])

                    imagename = util.OnlyNumber(event.pathname)
                    sqlInsert='insert into tb_camera(timestamp,img_id,frequency) values(%s,%s,%s)'%(imagename,imagename,timeF)
                    db.execute(sqlInsert)

                    if len(imagename)>14:
                        currenttime=imagename[:14]
                        global cur_time
                        if cmp(currenttime,cur_time) == 0:
                            pass
                        else:
                            cur_time=currenttime
                            insert_simulation='insert into tb_simulation(time,injure_count,injure_count_2,death_count,damage_cost,damage_count,scrap,accident_count,period) values(%s,%d,%d,%d,%d,%d,%d,%d,%d)'%(cur_time,3,5,4,10000,6,8,15,19)
                            db.execute(insert_simulation)

                    r = darknet.detect(event.pathname)
                    util.Logprint(1,imagename+":"+str(r))
                    util.move_single_image(cnf['cap_path'],cnf['arc_path'],imagename+".jpg")

                    



def startListener():
    util.Logprint(1,'开启文件夹监听')
    # watch manager
    wm = pyinotify.WatchManager()
    sys.path.append("..")
    with open('/home/nvidia/Horus/config.cnf') as f:
        cnf = json.load(f)
    wm.add_watch(cnf['cap_path'], pyinotify.ALL_EVENTS, rec=True)
    # event handler
    eh = MyEventHandler()
 
    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()


 

