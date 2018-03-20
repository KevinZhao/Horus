# -*- coding:utf-8 -*- 
from ctypes import *
import math
import random
from sqlalchemy import create_engine
from sqlalchemy import text
import json
import sys
# import lstm
sys.path.append("..")
import util

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]


with open('/home/nvidia/Horus/config.cnf') as f:
    cnf = json.load(f)
lib = CDLL(str(cnf['darknet_path'])+'libdarknet.so', RTLD_GLOBAL)

lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

make_boxes = lib.make_boxes
make_boxes.argtypes = [c_void_p]
make_boxes.restype = POINTER(BOX)

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

num_boxes = lib.num_boxes
num_boxes.argtypes = [c_void_p]
num_boxes.restype = c_int

make_probs = lib.make_probs
make_probs.argtypes = [c_void_p]
make_probs.restype = POINTER(POINTER(c_float))

detect = lib.network_predict
detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

free_image = lib.free_image
free_image.argtypes = [IMAGE]

draw_box = lib.draw_box
draw_label = lib.draw_label
get_label = lib.get_label
save_image = lib.save_image
draw_box_width=lib.draw_box_width


letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

network_detect = lib.network_detect
network_detect.argtypes = [c_void_p, IMAGE, c_float, c_float, c_float, POINTER(BOX), POINTER(POINTER(c_float))]

with open('/home/nvidia/Horus/config.cnf') as f:
    cnf = json.load(f)
net = load_net(str(cnf['darknet_path'])+'cfg/'+str(cnf['cfg'])+'.cfg', str(cnf['darknet_path'])+'weight/'+str(cnf['weight'])+'.weights', 0)
# net = load_net(str(cnf['darknet_path'])+'cfg/yolo9000.cfg', str(cnf['darknet_path'])+'weight/yolo.weights', 0)

#初始化LSTM
# lstm_bl=lstm.BasicLSTM()

# c=config.TIME_FREQUENCY
# if c == 0:
#     c = 200
# elif c == None:
#     c = 200
# timeF = c/1000.0

#是否是所要的分类数据
def isPass(name):
    if name=='car' or name=='motorcycle' or name=='bus' or name=='truck' or name=='stop sign' or name=='traffic light' or name=='person' or name=='bicycle' or name=='clock':
        return True
    else:
        return False

#处理tb_object数据
def dealData(name,probability,img_id,p_x,p_y,p_w,p_h):

    with open('/home/nvidia/Horus/config.cnf') as json_data:
        cnf = json.load(json_data)                
        db = create_engine(cnf['db'])
    
        if not name.strip():
            pass
        else: 
            resultProxy=db.execute(text('select * from tb_classify where classify = :classify'), {'classify':name})
            result = resultProxy.fetchall()
            if not result:
                db.execute(text('insert into tb_classify(classify) values( :classify)'), {'classify':name})

            resultProxy_id=db.execute(text('select id from tb_classify where classify = :classify'), {'classify':name})
            id_result = resultProxy_id.fetchall()

            type_id=id_result[0][0]
            insert_obj="insert into tb_object(type_id,probability,img_id,p_x,p_y,p_w,p_h) values (%s,%s,%s,%s,%s,%s,%s)"%(type_id,probability,img_id,p_x,p_y,p_w,p_h)
            db.execute(insert_obj)

            # draw_box_width(im,int(p_x-p_w/2.),int(p_y-p_h/2.),int(p_x+p_w/2.),int(p_y+p_h/2.),3,255,0,0)
            # save_image(im,cnf['detect_path']+'/'+img_id)

#处理统计数据
def dealDtatistics(img_id,car,motorcycle,bus,truck,stop_sign,traffic_light,person,bicycle,clock):
    with open('/home/nvidia/Horus/config.cnf') as json_data:
            cnf = json.load(json_data)                
            db = create_engine(cnf['db'])

            insert="insert into tb_object_statistics(img_id,car,motorcycle,bus,truck,stop_sign,traffic_light,person,bicycle,clock) values (%s,%d,%d,%d,%d,%d,%d,%d,%d,%d)"%(img_id,car,motorcycle,bus,truck,stop_sign,traffic_light,person,bicycle,clock)
            db.execute(insert)
            # #LSTM判断危险级别
            # pred_list=[[bicycle,bus,car,clock,person,stop_sign,traffic_light,truck,0]]
            # result=lstm_bl.prediction(pred_list)
            # print("lstm----：%d",result)
            # sqlInsert='insert into tb_camera(timestamp,img_id,frequency,result) values(%s,%s,%s,%d)'%(img_id,img_id,timeF,result)
            # db.execute(sqlInsert)






def detect(image, hier_thresh=.5, nms=.45):
    with open('/home/nvidia/Horus/config.cnf') as f:
        cnf = json.load(f)
    meta = load_meta(str(cnf['darknet_path'])+'cfg/'+str(cnf['model'])+'.data')
    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    im = load_image(image, 0, 0)
    network_detect(net, im, float(cnf['probability']), hier_thresh, nms, boxes, probs)
    res = []
    img_id=util.OnlyNumber(image)
    
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x-boxes[j].w/2., boxes[j].y-boxes[j].h/2., boxes[j].w, boxes[j].h)))
                if isPass(meta.names[i]):
                    dealData(meta.names[i],probs[j][i],img_id,boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)

    res = sorted(res, key=lambda x: -x[1])
    if len(res)>0:
        car=0
        motorcycle=0
        bus=0
        truck=0
        stop_sign=0
        traffic_light=0
        person=0
        bicycle=0
        clock=0
        for m in range(len(res)):
            name=res[m][0]
            if name=='car':
                car += 1
            elif name=='motorcycle':
                motorcycle += 1
            elif name=='bus':
                bus += 1
            elif name=='truck':
                truck += 1
            elif name=='stop sign':
                stop_sign += 1
            elif name=='traffic light':
                traffic_light += 1
            elif name=='person':
                person += 1
            elif name=='bicycle':
                bicycle += 1
            elif name=='clock':
                clock +=1
        dealDtatistics(img_id,car,motorcycle,bus,truck,stop_sign,traffic_light,person,bicycle,clock)


    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res


    

