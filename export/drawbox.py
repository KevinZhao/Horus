# -*- coding:utf-8 -*-
import os
import sys
# import MySQLdb
from sqlalchemy import create_engine
from sqlalchemy import text
import json
from ctypes import *
sys.path.append("..")
import config
import util


class IMAGE(Structure):
	_fields_ = [("w", c_int),
				("h", c_int),
				("c", c_int),
				("data", POINTER(c_float))]

lib = CDLL(str(config.DARKNET_PATH)+'libdarknet.so', RTLD_GLOBAL)

free_image = lib.free_image


load_image=lib.load_image
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE
load_image_color = lib.load_image_color

draw_box_width=lib.draw_box_width


save_image = lib.save_image


ARC_PATH="/home/nvidia/images/archive/"
DETECT_PATH="/home/nvidia/images/detect/"

def drawbox(im,img_id,x,y,w,h,paintwidth):
	draw_box_width(im,int(x-w/2.),int(y-h/2.),int(x+w/2.),int(y+h/2.),int(paintwidth),3,255,0,0)
	save_image(im,config.DETECT_PATH+'/'+img_id)
	free_image(im)

def queryDataByImgId(img_id):

	with open('/home/nvidia/Horus/config.cnf') as json_data:
		cnf = json.load(json_data)                
		db = create_engine(cnf['db'])

		result=db.execute(text('select * from tb_object where img_id = :img_id'), {'img_id':img_id})
		data = result.fetchall()

		if len(data)>0:
			img=ARC_PATH+str(img_id)+'.jpg'

			if os.path.exists(img):
				imgs=DETECT_PATH+str(img_id)+".jpg"
				util.copy_file(img,imgs)

				for s in data:
					if len(s[1])>0:
						if os.path.exists(imgs):
							im = load_image(imgs, 0, 0)
							drawbox(im,img_id,round(float((s[3]))),round(float((s[4]))),round(float((s[5]))),round(float((s[6]))),3)
					
			


def main():
	if os.path.exists(ARC_PATH):
		dirs=os.listdir(ARC_PATH)
		for i in range(0,len(dirs)):
			img_id=dirs[i].split('.')[0]
			queryDataByImgId(img_id)
			print(str(i+1)+"/"+str(len(dirs)))









