#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import tensorflow as tf
import json

#定义常量
rnn_unit=10       #hidden layer units
input_size=8
output_size=1
time_step=1
lr=0.0006         #学习率

#——————————————————导入数据——————————————————————
f=open('/home/nvidia/Horus/darknet/data.csv') 
df=pd.read_csv(f)     #读入数据
data=df.iloc[:,33:42].values  #取物体识别部分数据

df.dropna(inplace=True)


#——————————————————定义神经网络变量——————————————————
#输入层、输出层权重、偏置

weights={
		'in':tf.Variable(tf.random_normal([input_size,rnn_unit])),
		'out':tf.Variable(tf.random_normal([rnn_unit,1]))
		}
biases={
		'in':tf.Variable(tf.constant(0.1,shape=[rnn_unit,])),
		'out':tf.Variable(tf.constant(0.1,shape=[1,]))
		}

#——————————————————定义神经网络变量——————————————————
def lstm(X):     
	batch_size=tf.shape(X)[0]
	time_step=tf.shape(X)[1]
	w_in=weights['in']
	b_in=biases['in']  
	inputs=tf.reshape(X,[-1,input_size])  #需要将tensor转成2维进行计算，计算后的结果作为隐藏层的输入
	input_rnn=tf.matmul(inputs,w_in)+b_in
	input_rnn=tf.reshape(input_rnn,[-1,time_step,rnn_unit])  #将tensor转成3维，作为lstm cell的输入
	cell=tf.nn.rnn_cell.BasicLSTMCell(rnn_unit)
	init_state=cell.zero_state(batch_size,dtype=tf.float32)
	output_rnn,final_states=tf.nn.dynamic_rnn(cell, input_rnn,initial_state=init_state, dtype=tf.float32)  #output_rnn是记录lstm每个输出节点的结果，final_states是最后一个cell的结果
	output=tf.reshape(output_rnn,[-1,rnn_unit]) #作为输出层的输入
	
	w_out=weights['out']
	b_out=biases['out']
	pred=tf.matmul(output,w_out)+b_out
	return pred,final_states

X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
pred,_=lstm(X)     
#损失函数
loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
train_op=tf.train.AdamOptimizer(lr).minimize(loss)
saver=tf.train.Saver(tf.global_variables())

def dealJson(data_train):
	num = len(data_train[0])
	a = np.array(data_train)
	list_mean = []
	list_std = []
	for i in range(num):
		b = a[:,i]
		mean = np.mean(b,axis=0)
		std = np.std(b, axis=0)
		list_mean.append(mean)
		list_std.append(std)

	json_mean = json.dumps( list_mean, ensure_ascii=False, encoding='UTF-8')
	str_mean = r'/home/nvidia/Horus/mysqltest/lstm_mean.json'
	f = open(str_mean, 'w+')
	f.write(json_mean)
	f.close()

	json_std = json.dumps( list_std, ensure_ascii=False, encoding='UTF-8')
	str_std = r'/home/nvidia/Horus/mysqltest/lstm_std.json'
	f = open(str_std, 'w+')
	f.write(json_std)
	f.close()

#获取测试集
def get_pred_data(data_pred):
	for i in range(len(data_pred[0])-1):
		if data_pred[0][i]==0:
			data_pred[0][i]=0.00001

	data_test=np.array(data_pred)

	#导入json数据
	json_mean_dir = '/home/nvidia/Horus/mysqltest/lstm_mean.json'
	f = open(json_mean_dir, "rb")
	mean = np.array(json.load(f))

	json_std_dir = '/home/nvidia/Horus/mysqltest/lstm_std.json'
	ft = open(json_std_dir, "rb")
	std = np.array(json.load(ft))
	
	normalized_test_data = (data_test-mean)/std  #标准化
	size=(len(normalized_test_data)+time_step-1)//time_step  #有size个sample 

	test_x,test_y=[],[]  
	for i in range(size-1):
		x=normalized_test_data[i*time_step:(i+1)*time_step,:input_size]
		y=normalized_test_data[i*time_step:(i+1)*time_step,input_size]
		test_x.append(x.tolist())
		test_y.extend(y)
		test_x.append((normalized_test_data[(i)*time_step:,:input_size]).tolist())
		test_y.extend((normalized_test_data[(i)*time_step:,input_size]).tolist())
	if size==1:
		test_x.append((normalized_test_data[(0)*time_step:,:input_size]).tolist())
		test_y.extend((normalized_test_data[(0)*time_step:,input_size]).tolist())
	return mean,std,test_x,test_y



	#获取训练集
def get_train_data(batch_size=60,time_step=1,train_begin=0,train_end=4000):
	batch_index=[]
	data_train=data[train_begin:train_end] #(0,4000)
	dealJson(data_train)
	normalized_train_data=(data_train - np.mean(data_train,axis=0))/np.std(data_train, axis=0)  #标准化

	train_x,train_y=[],[]   #训练集 

	for i in range(len(normalized_train_data)-time_step):
		if i % batch_size == 0:
			batch_index.append(i)
		x=normalized_train_data[i:i+time_step,:input_size]
		y=normalized_train_data[i:i+time_step,1,np.newaxis]

		train_x.append(x.tolist())
		train_y.append(y.tolist())

	batch_index.append((len(normalized_train_data)-time_step))
	return batch_index,train_x,train_y

class BasicLSTM():
	# def __init__(self):
		# X=tf.placeholder(tf.float32, shape=[None,time_step,input_size])
		# Y=tf.placeholder(tf.float32, shape=[None,time_step,output_size])
		# pred,_=lstm(X)     
		# #损失函数
		# loss=tf.reduce_mean(tf.square(tf.reshape(pred,[-1])-tf.reshape(Y, [-1])))
		# train_op=tf.train.AdamOptimizer(lr).minimize(loss)
		# saver=tf.train.Saver(tf.global_variables())
		# module_file = tf.train.latest_checkpoint('ckpt/')

	#——————————————————训练模型——————————————————
	def train_lstm(self,batch_size=80,train_begin=0,train_end=4000):
	
		batch_index,train_x,train_y=get_train_data(batch_size,time_step,train_begin,train_end)

		module_file = tf.train.latest_checkpoint('/home/nvidia/Horus/darknet/ckpt/')

		with tf.Session() as sess:
			# sess.run(tf.global_variables_initializer())
			saver.restore(sess, module_file)
	        #重复训练10000次
			for i in range(100):
				for step in range(len(batch_index)-1):
					_,loss_=sess.run([train_op,loss],feed_dict={X:train_x[batch_index[step]:batch_index[step+1]],Y:train_y[batch_index[step]:batch_index[step+1]]})
				print(i,loss_)
				if i % 10==0:
					#print(i)
					print("save—model:",saver.save(sess,'./ckpt/model.ckpt'))

	def prediction(self,data_pred):
		mean,std,pred_x,pred_y=get_pred_data(data_pred)
		module_file = tf.train.latest_checkpoint('/home/nvidia/Horus/darknet/ckpt/')
		with tf.Session() as sess:
			#参数恢复
			print(tf.Graph())
			saver.restore(sess, module_file)
			pred_predict=[]
			for step in range(len(pred_x)-1):
				prob=sess.run(pred,feed_dict={X:[pred_x[step]]})
				predict=prob.reshape((-1))
				pred_predict.extend(predict)
			if len(pred_x)==1:
				prob=sess.run(pred,feed_dict={X:[pred_x[0]]})
				predict=prob.reshape((-1))
				pred_predict.extend(predict)
			pred_y=np.array(pred_y)*std[input_size]+mean[input_size]
			pred_predict=np.array(pred_predict)*std[input_size]+mean[input_size]
			acc=np.average(np.abs(pred_predict-pred_y[:len(pred_predict)])/pred_y[:len(pred_predict)])  #偏差
			return pred_predict[0]
			
