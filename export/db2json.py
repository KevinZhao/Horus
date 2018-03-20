#!/usr/bin/python
# -*- coding: utf-8 -*-
#10s存储一次
import json
from sqlalchemy import create_engine
import base64
from datetime import datetime
import os



# 降序  desc  升序  asc

def TableToJson(type,path,starttime,endtime):
    try:
        with open('/home/nvidia/Horus/config.cnf') as json_data:
            cnf = json.load(json_data)
            db = create_engine(cnf['db'])


        sql = "SELECT * FROM tb_envsensor order by time asc"

        envdata = db.execute(sql).fetchall()

        sql_cam = "SELECT * FROM tb_mobile_sensor order by timestamp asc"

        mobdata = db.execute(sql_cam).fetchall()
        if not starttime.strip() and not endtime.strip():
            sql_img = "SELECT * FROM tb_camera order by timestamp asc"
        elif starttime.strip() and not endtime.strip():
            sql_img = "SELECT * FROM tb_camera where %s<timestamp  order by timestamp asc" % (starttime)
        elif starttime.strip() and endtime.strip():
            sql_img = "SELECT * FROM tb_camera where %s<timestamp and timestamp <%s order by timestamp asc" % (starttime, endtime)
        imgdata = db.execute(sql_img).fetchall()
        sql_obj = "SELECT * FROM tb_object order by img_id asc"

        objdata = db.execute(sql_obj).fetchall()

        sql_obd = "SELECT * FROM tb_obd order by timestamp asc"
        obddata = db.execute(sql_obd).fetchall()

        sql_simulation = "SELECT * FROM tb_simulation order by time asc"
        simulationdata = db.execute(sql_simulation).fetchall()

        sql_statistics = "SELECT * FROM tb_object_statistics order by img_id asc"
        statisticsdata = db.execute(sql_statistics).fetchall()

        k1 = ''

        e_timestamp=''
        e_temperature=0
        e_humidity=0
        e_light=0
        e_uvIndex=0
        e_pressure=0
        e_noise=0
        e_discomfortIndex=0
        e_heatStrokerRisk=0
        e_accX=0
        e_accY=0
        e_accZ=0

        m_timestamp=''
        m_accx=0
        m_accy=0
        m_accz=0
        m_gpsLongitude=0
        m_gpsLatitude=0
        m_gpsAltitude=0
        m_gpsSpeed=0
        m_gpsBearing=0
        m_light=0

        o_timestamp = ''
        o_longitude = 0
        o_latitude = 0
        o_altitude = 0
        o_speed = 0

        s_timestamp = ''
        s_injure_count = 0
        s_injure_count_2 = 0
        s_death_count = 0
        s_damage_cost = 0
        s_damage_count = 0
        s_scrap = 0
        s_accident_count = 0
        s_period = 0

        t_car = 0
        t_motorcycle = 0
        t_bus = 0
        t_truck = 0
        t_stop_sign = 0
        t_traffic_light = 0
        t_person = 0
        t_bicycle = 0
        t_clock = 0

        if len(imgdata)>0:
            cday = datetime.strptime(imgdata[0][1][:14], '%Y%m%d%H%M%S')
            for f in range(0,len(imgdata)):
                print str(f + 1) + '/' + str(len(imgdata))
                k = imgdata[f][1][:12]
                cd = datetime.strptime(imgdata[f][1][:14], '%Y%m%d%H%M%S')
                if k in k1 and (cd - cday).seconds < 10:
                    continue
                else:
                    k1 = k
                    cday = cd
                    total = []
                    for f in imgdata:
                        k = f[1][:12]
                        cd = datetime.strptime(f[1][:14], '%Y%m%d%H%M%S')
                        if k in k1 and (cd - cday).seconds < 10:
                            imgname='/home/nvidia/images/archive/' + str(f[2]) + '.jpg'
                            if os.path.exists(imgname):
                                result = {}
                                result['t_img_id'] = f[1]
                                result['t_label'] = f[4]
                                if type == 1:
                                    IMAGE_NAME = '/home/nvidia/images/archive/' + str(f[2]) + '.jpg'
                                    with open(IMAGE_NAME, 'rb') as jpg_file:
                                        byte_content = jpg_file.read()
                                    base64_bytes = base64.b64encode(byte_content)
                                    result['t_image'] = base64_bytes
                                if len(envdata) > 0:
                                    for s in envdata:
                                        if s[1][:14] <= f[1][:14]:
                                            if s[1][:14] in f[1][:14]:
                                                if type == 1:
                                                    result['e_timestamp'] = s[1]
                                                result['e_temperature'] = s[9]
                                                result['e_humidity'] = s[10]
                                                result['e_light'] = s[11]
                                                result['e_uvIndex'] = s[12]
                                                result['e_pressure'] = s[13]
                                                result['e_noise'] = s[14]
                                                result['e_discomfortIndex'] = s[15]
                                                result['e_heatStrokerRisk'] = s[16]
                                                result['e_accX'] = s[17]
                                                result['e_accY'] = s[18]
                                                result['e_accZ'] = s[19]
                                                break
                                            else:
                                                if type == 1:
                                                    result['e_timestamp'] = s[1]
                                                result['e_temperature'] = s[9]
                                                result['e_humidity'] = s[10]
                                                result['e_light'] = s[11]
                                                result['e_uvIndex'] = s[12]
                                                result['e_pressure'] = s[13]
                                                result['e_noise'] = s[14]
                                                result['e_discomfortIndex'] = s[15]
                                                result['e_heatStrokerRisk'] = s[16]
                                                result['e_accX'] = s[17]
                                                result['e_accY'] = s[18]
                                                result['e_accZ'] = s[19]
                                                if type == 1:
                                                    e_timestamp = s[1]
                                                e_temperature = s[9]
                                                e_humidity = s[10]
                                                e_light = s[11]
                                                e_uvIndex = s[12]
                                                e_pressure = s[13]
                                                e_noise = s[14]
                                                e_discomfortIndex = s[15]
                                                e_heatStrokerRisk = s[16]
                                                e_accX = s[17]
                                                e_accY = s[18]
                                                e_accZ = s[19]
                                        else:
                                            if type == 1:
                                                result['e_timestamp'] = e_timestamp
                                            result['e_temperature'] = e_temperature
                                            result['e_humidity'] = e_humidity
                                            result['e_light'] = e_light
                                            result['e_uvIndex'] = e_uvIndex
                                            result['e_pressure'] = e_pressure
                                            result['e_noise'] = e_noise
                                            result['e_discomfortIndex'] = e_discomfortIndex
                                            result['e_heatStrokerRisk'] = e_heatStrokerRisk
                                            result['e_accX'] = e_accX
                                            result['e_accY'] = e_accY
                                            result['e_accZ'] = e_accZ
                                            break
                                else:
                                    if type == 1:
                                        result['e_timestamp'] = ''
                                    result['e_temperature'] = ''
                                    result['e_humidity'] = ''
                                    result['e_light'] = ''
                                    result['e_uvIndex'] = ''
                                    result['e_pressure'] = ''
                                    result['e_noise'] = ''
                                    result['e_discomfortIndex'] = ''
                                    result['e_heatStrokerRisk'] = ''
                                    result['e_accX'] = ''
                                    result['e_accY'] = ''
                                    result['e_accZ'] = ''

                                if len(mobdata) > 0:
                                    for s in mobdata:
                                        if s[1][:14] <= f[1][:14]:
                                            if s[1][:14] in f[1][:14]:
                                                if type == 1:
                                                    result['m_timestamp'] = s[1]
                                                result['m_accx'] = s[2]
                                                result['m_accy'] = s[3]
                                                result['m_accz'] = s[4]
                                                result['m_gpsLongitude'] = s[5]
                                                result['m_gpsLatitude'] = s[6]
                                                result['m_gpsAltitude'] = s[7]
                                                result['m_gpsSpeed'] = s[8]
                                                result['m_gpsBearing'] = s[9]
                                                result['m_light'] = s[10]
                                                break
                                            else:
                                                if type == 1:
                                                    result['m_timestamp'] = s[1]
                                                result['m_accx'] = s[2]
                                                result['m_accy'] = s[3]
                                                result['m_accz'] = s[4]
                                                result['m_gpsLongitude'] = s[5]
                                                result['m_gpsLatitude'] = s[6]
                                                result['m_gpsAltitude'] = s[7]
                                                result['m_gpsSpeed'] = s[8]
                                                result['m_gpsBearing'] = s[9]
                                                result['m_light'] = s[10]
                                                if type == 1:
                                                    m_timestamp = s[1]
                                                m_accx = s[2]
                                                m_accy = s[3]
                                                m_accz = s[4]
                                                m_gpsLongitude = s[5]
                                                m_gpsLatitude = s[6]
                                                m_gpsAltitude = s[7]
                                                m_gpsSpeed = s[8]
                                                m_gpsBearing = s[9]
                                                m_light = s[10]
                                        else:
                                            if type == 1:
                                                result['m_timestamp'] = m_timestamp
                                            result['m_accx'] = m_accx
                                            result['m_accy'] = m_accy
                                            result['m_accz'] = m_accz
                                            result['m_gpsLongitude'] = m_gpsLongitude
                                            result['m_gpsLatitude'] = m_gpsLatitude
                                            result['m_gpsAltitude'] = m_gpsAltitude
                                            result['m_gpsSpeed'] = m_gpsSpeed
                                            result['m_gpsBearing'] = m_gpsBearing
                                            result['m_light'] = m_light
                                else:
                                    if type == 1:
                                        result['m_timestamp'] = ''
                                    result['m_accx'] = ''
                                    result['m_accy'] = ''
                                    result['m_accz'] = ''
                                    result['m_gpsLongitude'] = ''
                                    result['m_gpsLatitude'] = ''
                                    result['m_gpsAltitude'] = ''
                                    result['m_gpsSpeed'] = ''
                                    result['m_gpsBearing'] = ''
                                    result['m_light'] = ''

                                if len(obddata) > 0:
                                    for o in obddata:
                                        if o[1][:14] <= f[1][:14]:
                                            if o[1][:14] in f[1][:14]:
                                                if type == 1:
                                                    result['o_timestamp'] = o[1]
                                                result['o_longitude'] = o[2]
                                                result['o_latitude'] = o[3]
                                                result['o_altitude'] = o[4]
                                                result['o_speed'] = o[5]
                                                break
                                            else:
                                                if type == 1:
                                                    result['o_timestamp'] = o[1]
                                                result['o_longitude'] = o[2]
                                                result['o_latitude'] = o[3]
                                                result['o_altitude'] = o[4]
                                                result['o_speed'] = o[5]
                                                if type == 1:
                                                    o_timestamp = o[1]
                                                o_longitude = o[2]
                                                o_latitude = o[3]
                                                o_altitude = o[4]
                                                o_speed = o[5]
                                        else:
                                            if type == 1:
                                                result['o_timestamp'] = o_timestamp
                                            result['o_longitude'] = o_longitude
                                            result['o_latitude'] = o_latitude
                                            result['o_altitude'] = o_altitude
                                            result['o_speed'] = o_speed
                                            break
                                else:
                                    if type == 1:
                                        result['o_timestamp'] = ''
                                    result['o_longitude'] = ''
                                    result['o_latitude'] = ''
                                    result['o_altitude'] = ''
                                    result['o_speed'] = ''

                                if len(simulationdata) > 0:
                                    for s in simulationdata:
                                        if s[1][:14] <= f[1][:14]:
                                            if s[1][:14] in f[1][:14]:
                                                if type == 1:
                                                    result['s_timestamp'] = s[1]
                                                result['s_injure_count'] = s[2]
                                                result['s_injure_count_2'] = s[3]
                                                result['s_death_count'] = s[4]
                                                result['s_damage_cost'] = s[5]
                                                result['s_damage_count'] = s[6]
                                                result['s_scrap'] = s[7]
                                                result['s_accident_count'] = s[8]
                                                result['s_period'] = s[9]
                                                break
                                            else:
                                                if type == 1:
                                                    result['s_timestamp'] = s[1]
                                                result['s_injure_count'] = s[2]
                                                result['s_injure_count_2'] = s[3]
                                                result['s_death_count'] = s[4]
                                                result['s_damage_cost'] = s[5]
                                                result['s_damage_count'] = s[6]
                                                result['s_scrap'] = s[7]
                                                result['s_accident_count'] = s[8]
                                                result['s_period'] = s[9]
                                                if type == 1:
                                                    s_timestamp = s[1]
                                                s_injure_count = s[2]
                                                s_injure_count_2 = s[3]
                                                s_death_count = s[4]
                                                s_damage_cost = s[5]
                                                s_damage_count = s[6]
                                                s_scrap = s[7]
                                                s_accident_count = s[8]
                                                s_period = s[9]
                                        else:
                                            if type == 1:
                                                result['s_timestamp'] = s_timestamp
                                            result['s_injure_count'] = s_injure_count
                                            result['s_injure_count_2'] = s_injure_count_2
                                            result['s_death_count'] = s_death_count
                                            result['s_damage_cost'] = s_damage_cost
                                            result['s_damage_count'] = s_damage_count
                                            result['s_scrap'] = s_scrap
                                            result['s_accident_count'] = s_accident_count
                                            result['s_period'] = s_period
                                            break
                                else:
                                    if type == 1:
                                        result['s_timestamp'] = ''
                                    result['s_injure_count'] = ''
                                    result['s_injure_count_2'] = ''
                                    result['s_death_count'] = ''
                                    result['s_damage_cost'] = ''
                                    result['s_damage_count'] = ''
                                    result['s_scrap'] = ''
                                    result['s_accident_count'] = ''
                                    result['s_period'] = ''

                                if len(statisticsdata) > 0:
                                    for s in statisticsdata:
                                        if s[1][:14] <= f[1][:14]:
                                            if s[1][:] in f[1][:]:
                                                result['t_car'] = s[2]
                                                result['t_motorcycle'] = s[3]
                                                result['t_bus'] = s[4]
                                                result['t_truck'] = s[5]
                                                result['t_stop_sign'] = s[6]
                                                result['t_traffic_light'] = s[7]
                                                result['t_person'] = s[8]
                                                result['t_bicycle'] = s[9]
                                                result['t_clock'] = s[10]
                                                break
                                            else:
                                                result['t_car'] = s[2]
                                                result['t_motorcycle'] = s[3]
                                                result['t_bus'] = s[4]
                                                result['t_truck'] = s[5]
                                                result['t_stop_sign'] = s[6]
                                                result['t_traffic_light'] = s[7]
                                                result['t_person'] = s[8]
                                                result['t_bicycle'] = s[9]
                                                result['t_clock'] = s[10]
                                                t_car = s[2]
                                                t_motorcycle = s[3]
                                                t_bus = s[4]
                                                t_truck = s[5]
                                                t_stop_sign = s[6]
                                                t_traffic_light = s[7]
                                                t_person = s[8]
                                                t_bicycle = s[9]
                                                t_clock = s[10]
                                        else:
                                            result['t_car'] = t_car
                                            result['t_motorcycle'] = t_motorcycle
                                            result['t_bus'] = t_bus
                                            result['t_truck'] = t_truck
                                            result['t_stop_sign'] = t_stop_sign
                                            result['t_traffic_light'] = t_traffic_light
                                            result['t_person'] = t_person
                                            result['t_bicycle'] = t_bicycle
                                            result['t_clock'] = t_clock
                                            break
                                else:
                                    result['t_car'] = ''
                                    result['t_motorcycle'] = ''
                                    result['t_bus'] = ''
                                    result['t_truck'] = ''
                                    result['t_stop_sign'] = ''
                                    result['t_traffic_light'] = ''
                                    result['t_person'] = ''
                                    result['t_bicycle'] = ''
                                    result['t_clock'] = ''

                                if type == 1:
                                    object = []
                                    if len(objdata) > 0:
                                        for o in objdata:
                                            if o[1][:] in f[1][:]:
                                                oresult = {}
                                                oresult['t_img_id'] = o[1]
                                                oresult['t_type_id'] = o[2]
                                                oresult['t_p_x'] = o[3]
                                                oresult['t_p_y'] = o[4]
                                                oresult['t_p_w'] = o[5]
                                                oresult['t_p_h'] = o[6]
                                                oresult['t_probability'] = o[7]
                                                object.append(oresult)
                                        if len(object) == 0:
                                            oresult = {}
                                            oresult['t_img_id'] = ''
                                            oresult['t_type_id'] = ''
                                            oresult['t_p_x'] = ''
                                            oresult['t_p_y'] = ''
                                            oresult['t_p_w'] = ''
                                            oresult['t_p_h'] = ''
                                            oresult['t_probability'] = ''
                                            object.append(oresult)
                                    else:
                                        oresult = {}
                                        oresult['t_img_id'] = ''
                                        oresult['t_type_id'] = ''
                                        oresult['t_p_x'] = ''
                                        oresult['t_p_y'] = ''
                                        oresult['t_p_w'] = ''
                                        oresult['t_p_h'] = ''
                                        oresult['t_probability'] = ''
                                        object.append(oresult)

                                    result['object'] = object
                                total.append(result)
                    if len(total)>0:
                        jsondatar = json.dumps(total, ensure_ascii=False, sort_keys=True)
                        name = path + cday.strftime('%Y%m%d%H%M%S') + '.json'
                        f = open(name, 'w+')
                        f.write(jsondatar)
                        f.close()
                    



    except Exception as e:
        print e


def jsonwithpic(starttime,endtime):
    route = r'/home/nvidia/Horus/export/jsondata/'
    TableToJson(1,route,starttime,endtime)


def jsonwithoutpic(starttime,endtime):
    routev2=r'/home/nvidia/Horus/export/jsondatav2/'
    TableToJson(2, routev2,starttime,endtime)

