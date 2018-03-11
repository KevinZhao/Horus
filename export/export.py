# -*- coding:utf-8 -*-
import os 
import sys
import drawbox
import ext_csv

if __name__ == '__main__':
    if len(sys.argv)>1:
        argv= sys.argv[1]
        if argv=="-d":
            #画框
            print("Start Drawbox")
            drawbox.main()
            pass
        elif argv=="-c":
            #生成csv文件
            print("Start Export CSV,Please Wait...")
            ext_csv.createListCSV('data.csv')
            pass
        elif argv=="-j":
            #生成json
            pass
        elif argv=="-jp":
            #生成带图片二进制的json
            pass
        else:
            pass
    else:
        pass
    

