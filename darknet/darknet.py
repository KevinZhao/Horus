# -*- coding:utf-8 -*- 
from ctypes import *
import math
import random
from sqlalchemy import create_engine
from sqlalchemy import text
import json
import sys
sys.path.append("..")
import config

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

    

lib = CDLL(str(config.DARKNET_PATH)+'libdarknet.so', RTLD_GLOBAL)

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


net = load_net(str(config.DARKNET_PATH)+'cfg/'+str(config.WEIGHT)+'.cfg', str(config.DARKNET_PATH)+'weight/'+str(config.WEIGHT)+'.weights', 0)

#字符串中只保留数字
def OnlyNumber(image):
    fomart = '0123456789'
    for c in image:
        if not c in fomart:
            image=image.replace(c,'')
    return image

def dealData(name,probability,img_id,p_x,p_y,p_w,p_h):

    with open('/home/nvidia/Horus/mysql/sql.cnf') as json_data:
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

def detect(image, hier_thresh=.5, nms=.45):
    meta = load_meta(str(config.DARKNET_PATH)+'cfg/'+str(config.MODEL)+'.data')
    boxes = make_boxes(net)
    probs = make_probs(net)
    num = num_boxes(net)
    im = load_image(image, 0, 0)
    network_detect(net, im, config.PROBABILITY, hier_thresh, nms, boxes, probs)
    res = []
    img_id=OnlyNumber(image)
    for j in range(num):
        for i in range(meta.classes):
            if probs[j][i] > 0:
                res.append((meta.names[i], probs[j][i], (boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)))
                dealData(meta.names[i],probs[j][i],img_id,boxes[j].x, boxes[j].y, boxes[j].w, boxes[j].h)
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_ptrs(cast(probs, POINTER(c_void_p)), num)
    return res

    

