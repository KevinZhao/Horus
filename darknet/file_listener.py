#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import datetime
import pyinotify
import sys
import darknet
class MyEventHandler(pyinotify.ProcessEvent):
    
    def process_IN_CLOSE_WRITE(self, event):

        r = darknet.detect(event.pathname)
        print(r)


def startListener():
    # watch manager
    wm = pyinotify.WatchManager()
    sys.path.append("..")
    import config
    wm.add_watch(config.FILE_PATH, pyinotify.ALL_EVENTS, rec=True)
    # event handler
    eh = MyEventHandler()
 
    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()
 

