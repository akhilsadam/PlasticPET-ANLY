import pickle
import numpy as np
import pandas as pd
import math
import os
import io
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
from functools import lru_cache
from tqdm import tqdm
import multiprocessing
from numba import jit
import sys
@lru_cache(maxsize=2000)
def process_MLDRESinput(c):
	try:
		photonDatas = photonSiPMData(c)
		if(len(photonDatas)==0):
			# print(photonDatas)
			# print("[STATUS] length = 0 - an uninteracted event")
			return None
		else:
			# array filtering
			# print(photonDatas[4][0])
			photonArrayData = photonDatas[:,photonDatas[4]==ArrayNumber]
			photonDataL = np.transpose(photonArrayData[:,photonArrayData[2]>UZ])
			photonDataR = np.transpose(photonArrayData[:,photonArrayData[2]<=UZ])
			if((len(photonDataL)==0) or (len(photonDataR)==0)):
				# print("[STATUS] THIS ARRAY - length = 0 - event on another array")
				return None
			else:
				photonDataL = np.transpose(sorted(photonDataL, key=lambda photonDataL: photonDataL[3]))
				photonDataR = np.transpose(sorted(photonDataR, key=lambda photonDataR: photonDataR[3]))
				#if lengths differ
				#print(photonDataL.shape)
				minlen = min(photonDataL.shape[1],photonDataR.shape[1])
				if (minlen < Options.firstPhoton+Options.photoLen):
					print("[WARNING] minlen = {}, not totalLen(10)".format(minlen))
					return None
				if (photonDataL.ndim>1) and (photonDataR.ndim>1):
					photonDataL = photonDataL[:,Options.firstPhoton:Options.firstPhoton+Options.photoLen]
					photonDataR = photonDataR[:,Options.firstPhoton:Options.firstPhoton+Options.photoLen]
				else:
					print("[WARNING] ndim < 1")
					return None
					
				Ltimes = photonDataL[3] - ((photonDataL[2]-LZ)*n_EJ208/(1000*c_const*nanosec))
				Rtimes = photonDataR[3] + ((photonDataR[2])*n_EJ208/(1000*c_const*nanosec))
				fastestTime = min(Ltimes[0],Rtimes[0]) #min(min(Ltimes),min(Rtimes))
				#if lengths differ
				# print(fastestTime)
				minlen = min(len(Ltimes),len(Rtimes))
				if(minlen != Options.photoLen):
					print("[WARNING] minlen = {}, not Options.photoLen(5)".format(minlen))
					return None
				photonDataL[3] = Ltimes - fastestTime
				photonDataR[3] = Rtimes - fastestTime
				photonDataL[2]=LZ
				photonDataR[2]=0
				photonDataL = photonDataL[0:4]
				photonDataR = photonDataR[0:4]
				
				#BIN X,Y:
				photonDataL[0] = binx*np.floor(photonDataL[0]/binx)
				photonDataR[0] = binx*np.floor(photonDataR[0]/binx)
				photonDataL[1] = biny*np.floor(photonDataL[1]/biny)
				photonDataR[1] = biny*np.floor(photonDataR[1]/biny)
				#--

				ETZ = torch.zeros(4)
				ETZ[0:3] = torch.from_numpy(actEvtPosN[c])
				ETZ[3] = (time_I_N[c]-fastestTime)
	 
				if (dataNotWithinLimits(ETZ)): 
					# why is this so prevalent??
					# print("[ERROR] data not within limits")
					# print(ETZ)
					return None
				
				TZ = torch.zeros(4,2*Options.photoLen+1)
				TZ[:,0:2*Options.photoLen:2] = torch.from_numpy(photonDataL)
				#print(torch.from_numpy(photonDataL))
				TZ[:,1:2*Options.photoLen:2] = torch.from_numpy(photonDataR)

				# print(ETZ)
				TZ[:,2*Options.photoLen] = ETZ
				#print(TZ)
				TZ[3] = 1000*(TZ[3]*nanosec)*(c_const/n_EJ208) #UNIT CONVERSION from ns to mm
				#print(TZ)

		return TZ
	except Exception as e:
		print(e)
		return None

def MLDRESpreprocess(workers):
	print(ArrayNumber)
	try:
		if(Options.regenerateMLPickles):
			raise ValueError('[NotAnERROR] Regenerating ML Pickles')
		with open(ml_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
			inputTensor,expecTensor,eventIDS = pickle.load(f)
	except:
		with multiprocessing.Pool(workers) as pool:
			inptL = list(tqdm(pool.imap(process_MLDRESinput,range(nEvents)),total=nEvents))
			print(len(inptL))
			tList = [i for i in inptL if type(i)==torch.Tensor]
			print(len(tList))
			eventIDS = [i for i in range(nEvents) if type(inptL[i])==torch.Tensor]
			#print(tList)
			trainTensor = torch.stack(tList)
			inputTensor = trainTensor[:,:,0:2*Options.photoLen]
			expecTensor = trainTensor[:,:,2*Options.photoLen]
		with open(ml_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
			pickle.dump([inputTensor,expecTensor,eventIDS], f)
	return inputTensor,expecTensor
