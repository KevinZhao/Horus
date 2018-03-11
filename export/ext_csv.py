# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import json
import csv
import numpy
import random

from collections import OrderedDict
monitorItems = OrderedDict()
#添加列名
column=['t_img_id','e_accX','e_accY','e_accZ','e_discomfortIndex','e_heatStrokerRisk','e_humidity','e_light','e_noise','e_pressure','e_temperature','e_uvIndex','m_accx','m_accy','m_accz','m_gpsAltitude','m_gpsLatitude','m_gpsLongitude','m_gpsSpeed','m_gpsBearing','m_light','o_altitude','o_latitude','o_longitude','o_speed','s_accident_count','s_damage_cost','s_damage_count','s_death_count','s_injure_count','s_injure_count_2','s_period','s_scrap','t_bicycle','t_bus','t_car','t_clock','t_person','t_stop_sign','t_traffic_light','t_truck','children','man','woman','oldman','benchmark','label']
#四舍五入取整
def IntegerNum(num):
    return int(round(num))

#小孩的主观分
def ChildrenSimulation(num):
    count = 0
    if num == 1:
        for x in xrange(1,11):
            count = count + 1
    elif num == 2:
        for x in xrange(1,11):
            count = count + random.randint(1,2)
    elif num == 3:
        for x in xrange(1,11):
            count = count + random.randint(2,3)
    elif num == 4:
        for x in xrange(1,11):
            count = count + random.randint(2,4)
    elif num == 5:
        for x in xrange(1,11):
            count = count + random.randint(2,5)

    return count/10.0

#男人的主观分
def ManSimulation(num):
    count = 0
    if num == 1:
        for x in xrange(1,11):
            count = count + random.randint(1,2)
    elif num == 2:
        for x in xrange(1,11):
            count = count + random.randint(1,3)
    elif num == 3:
        for x in xrange(1,11):
            count = count + random.randint(2,4)
    elif num == 4:
        for x in xrange(1,11):
            count = count + random.randint(3,4)
    elif num == 5:
        for x in xrange(1,11):
            count = count + random.randint(3,5)

    return count/10.0

# 女人的主观分
def WomenSimulation(num):
    count = 0
    if num == 1:
        for x in xrange(1, 11):
            count = count + random.randint(1, 2)
    elif num == 2:
        for x in xrange(1, 11):
            count = count + random.randint(2, 3)
    elif num == 3:
        for x in xrange(1, 11):
            count = count + random.randint(3, 4)
    elif num == 4:
        for x in xrange(1, 11):
            count = count + random.randint(3, 5)
    elif num == 5:
        for x in xrange(1, 11):
            count = count + random.randint(4, 5)

    return count / 10.0
#老人的主观分
def OldManSimulation(num):
    count = 0
    if num == 1:
        for x in xrange(1,11):
            count = count + random.randint(1,3)
    elif num == 2:
        for x in xrange(1,11):
            count = count + random.randint(2,4)
    elif num == 3:
        for x in xrange(1,11):
            count = count + random.randint(3,5)
    elif num == 4:
        for x in xrange(1,11):
            count = count + random.randint(4,5)
    elif num == 5:
        for x in xrange(1,11):
            count = count + 5

    return count/10.0


#四类人主观平均分
def AvragePoint(num):
    count = 0;
    count = count + ManSimulation(num)
    count = count + WomenSimulation(num)
    count = count + OldManSimulation(num)
    count = count + ChildrenSimulation(num)
    return count/4.0


    
#处理一条json数据，存入列表中
def single_json(jsonstr):
    f = open(jsonstr)
    array = json.load(f)
    single_list=[]
    for index in range(len(array)):
        json_str = array[index]
        dictionary={}

        dictionary['t_img_id']=json_str['t_img_id'].encode('utf-8')

        dictionary['e_accX']=json_str['e_accX']
        dictionary['e_accY']=json_str['e_accY']
        dictionary['e_accZ']=json_str['e_accZ']
        dictionary['e_discomfortIndex']=json_str['e_discomfortIndex']
        dictionary['e_heatStrokerRisk']=json_str['e_heatStrokerRisk']
        dictionary['e_humidity']=json_str['e_humidity']
        dictionary['e_light']=json_str['e_light']
        dictionary['e_noise']=json_str['e_noise']
        dictionary['e_pressure']=json_str['e_pressure']
        dictionary['e_temperature']=json_str['e_temperature']
        dictionary['e_uvIndex']=json_str['e_uvIndex']

        dictionary['m_accx']=json_str['m_accx']
        dictionary['m_accy']=json_str['m_accy']
        dictionary['m_accz']=json_str['m_accz']
        dictionary['m_gpsAltitude']=json_str['m_gpsAltitude']
        dictionary['m_gpsLatitude']=json_str['m_gpsLatitude']
        dictionary['m_gpsLongitude']=json_str['m_gpsLongitude']
        dictionary['m_gpsSpeed']=json_str['m_gpsSpeed']
        dictionary['m_gpsBearing']=json_str['m_gpsBearing']
        dictionary['m_light']=json_str['m_light']

        dictionary['o_altitude']=json_str['o_altitude']
        dictionary['o_latitude']=json_str['o_latitude']
        dictionary['o_longitude']=json_str['o_longitude']
        dictionary['o_speed']=json_str['o_speed']

        dictionary['s_accident_count']=json_str['s_accident_count']
        dictionary['s_damage_cost']=json_str['s_damage_cost']
        dictionary['s_damage_count']=json_str['s_damage_count']
        dictionary['s_death_count']=json_str['s_death_count']
        dictionary['s_injure_count']=json_str['s_injure_count']
        dictionary['s_injure_count_2']=json_str['s_injure_count_2']
        dictionary['s_period']=json_str['s_period']
        dictionary['s_scrap']=json_str['s_scrap']

        dictionary['t_bicycle']=json_str['t_bicycle']
        dictionary['t_bus']=json_str['t_bus']
        dictionary['t_car']=json_str['t_car']
        dictionary['t_clock']=json_str['t_clock']
        #dictionary['t_motorcycle']=json_str['t_motorcycle']
        dictionary['t_person']=json_str['t_person']
        dictionary['t_stop_sign']=json_str['t_stop_sign']
        dictionary['t_traffic_light']=json_str['t_traffic_light']
        dictionary['t_truck']=json_str['t_truck']

        p=int(json_str['t_bicycle'])+int(json_str['t_person'])
        b=int(json_str['t_bus'])+int(json_str['t_car'])+int(json_str['t_truck'])
        t=int(json_str['t_clock'])+int(json_str['t_traffic_light'])+int(json_str['t_stop_sign'])
        score=benchmark(p,b,t)
        dictionary['benchmark']=score

        dictionary['children']=IntegerNum(ChildrenSimulation(score)) 
        dictionary['man']=IntegerNum(ManSimulation(score))
        dictionary['woman']=IntegerNum(WomenSimulation(score))
        dictionary['oldman']=IntegerNum(OldManSimulation(score))

        la=(AvragePoint(score)+score)/2.0
        dictionary['label']=IntegerNum(la) 

        for key in column:
            if dictionary.get(key) is not None:
                monitorItems[key] = dictionary.get(key)
        tupledata=tuple(monitorItems.values())
        single_list.append(list(tupledata))
    return single_list

def benchmark(p,b,t):
    
    if p>=6 or b>=6 or t>=2:
        return 5
    elif p==5 or b==5 or t==1:
        return 4
    elif p==4 or b==4:
        return 3
    elif p==3 or b==3:
        return 2
    else:
        return 1
  
def dealAllData():
    allList=[]
    allList.append(column)

    jsondir='/home/nvidia/Horus/export/jsondatav2'
    jsonlist = os.listdir(jsondir)
    for i in range(0,len(jsonlist)):
        path = os.path.join(jsondir,jsonlist[i])
        allList.extend(single_json(path))
    return allList


def createListCSV(fileName):
    with open(fileName, "wb") as csvFile:
        csvWriter = csv.writer(csvFile)
        dataList=dealAllData();
        if len(dataList)>0:
            for data in dataList:
                csvWriter.writerow(data)
        csvFile.close
