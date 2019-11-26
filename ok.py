#!usr/bin/env python  
#coding=utf-8  

import wave  
import soundfile as sf
#define stream chunk   
chunk = 1024
 
#read data 
def loadwaves():
	datas=[]
	for i in range(1,9):
		filename='waves/tmp' + str(i) + '.wav'	
		print(filename)
		data, fs = sf.read(filename)
		datas.append(data)
	return datas