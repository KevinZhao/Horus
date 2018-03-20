# -*- coding:utf-8 -*-
import os 
import sys
import drawbox
import ext_csv
import db2json

if __name__ == '__main__':
    if len(sys.argv)>1:
        argv= sys.argv[1]
        if argv=="-d":
            #画框
            print("Start Drawbox")
            drawbox.main()
            print("Completed")
            pass
        elif argv=="-c":
            #生成csv文件
            print("Start Export CSV,Please Wait...")
            ext_csv.createListCSV('data.csv')
            print("Completed")
            pass
        elif "-j" in argv:
            a=argv.split(':')
            #生成json
            if len(a)==1:
                db2json.jsonwithoutpic('','')
            elif len(a)==2:
                s=a[1]
                if len(s)==14:
                    db2json.jsonwithoutpic(a[1]+'0','')
                else:
                    print '输入格式不对,请按以下格式输入(-j:yyyyMMddHHmmss)'
            elif len(a)==3:
                s = a[1]
                e = a[2]
                if len(s) == 14 and len(e)==14:
                    db2json.jsonwithoutpic(a[1]+'0', a[2]+'0')
                else:
                    print '输入格式不对,请按以下格式输入(-j:yyyyMMddHHmmss:yyyyMMddHHmmss)'
            else:
                print '输入格式不对，请重新输入'
                pass
        elif "-p" in argv:
            #生成带图片二进制的json
            a = argv.split(':')
            if len(a)==1:
                db2json.jsonwithpic('','')
            elif len(a)==2:
                s=a[1]
                if len(s)==14:
                    db2json.jsonwithpic(a[1]+'0','')
                else:
                    print '输入格式不对,请按以下格式输入(-j:yyyyMMddHHmmss)'
            elif len(a)==3:
                s = a[1]
                e = a[2]
                if len(s) == 14 and len(e)==14:
                    db2json.jsonwithpic(a[1]+'0', a[2]+'0')
                else:
                    print '输入格式不对,请按以下格式输入(-j:yyyyMMddHHmmss:yyyyMMddHHmmss)'
            else:
                print '输入格式不对，请重新输入'
                pass
        else:
            pass
    else:
        pass
    

