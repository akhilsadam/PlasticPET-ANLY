epsil = 0.001
lr = 0.002
lrt = 0.002
L_time = 0.001 #ns

UL = [77.4,103.2,1000]

#from joblib import Parallel,delayed
import multiprocessing
from itertools import repeat
from functools import partial
from analyzeOptions import *
Options.num_cores = multiprocessing.cpu_count()

def ACTTimeReconstruct():

	#Options.photoLen = 5 # set parameter
	photonData = np.zeros(shape=(5,Options.photoLen))
	recPosT = np.zeros(shape=(nEvents,4))
	for c in range(3,4):#nEvents
		photonDatas = np.transpose(photonSiPMData(c))
		photonData = np.transpose(sorted(photonDatas, key=lambda photonDatas: photonDatas[3]))[:,0:Options.photoLen]

		fastestTime = min(photonData[3])
		#print(photonData)
		#Options.photoLen = len(photonData[3])
		#for i in range(0,Options.photoLen):

		#Bin Data into Strips
		# ct estimator for x,y,z position.
		point = [0,0,UZ,1]
		for _ in range(50):
			for dr in range(3):
				point[dr] = point[dr] - lr*drGrad(dr,point, photonData)
				dist = point[2] if (point[2] <= UZ) else LZ-point[2]
				point[3] = fastestTime - (dist)*n_EJ208/(1000*c_const*nanosec)
					#point[3] = point[3] - lrt*tGrad(point, photonData)
					#print(err[:,5])
		#print(point)


		recPosT[c] = point

	return recPosT

@lru_cache(maxsize=2000)
def process_ACTZT(c):
	photonDatas = photonSiPMData(c)
	# print(photonDatas)
	if (len(photonDatas)==0):
		r_Z,r_T,readTime = np.nan,np.nan,np.nan
	else:
		# array filtering
		photonArrayData = photonDatas[:,(photonDatas[4]).astype(int)==Options.ArrayNumber]
		#print(photonArrayData)
		photonDataL = np.transpose(photonArrayData[:,photonArrayData[2]>UZ])
		photonDataR = np.transpose(photonArrayData[:,photonArrayData[2]<=UZ])
		#print(photonDataL.shape)
		if ((len(photonDataL)==0) or (len(photonDataR)==0)):
			r_Z,r_T,readTime = np.nan,np.nan,np.nan
		else:
			photonDataL = np.transpose(sorted(photonDataL, key=lambda photonDataL: photonDataL[3]))
			photonDataR = np.transpose(sorted(photonDataR, key=lambda photonDataR: photonDataR[3]))
			#if lengths differ
			minlen = min(photonDataL.shape[1],photonDataR.shape[1],Options.firstPhoton+Options.photoLen)
			# print(photonDataL.shape)
			# print(Options.photoLen)
			# print(minlen)
			if (photonDataL.ndim>1) and (photonDataR.ndim>1):
				photonDataL = photonDataL[:,Options.firstPhoton:minlen]
				photonDataR = photonDataR[:,Options.firstPhoton:minlen]
			elif (photonDataL.ndim>1):
				photonDataL = photonDataL[:,Options.firstPhoton]
			else:
				photonDataR = photonDataR[:,Options.firstPhoton]

			# print(photonDataL)
			# print(photonDataR)
			Ltimes = photonDataL[3] - ((photonDataL[2]-LZ)*n_EJ208/(1000*c_const*nanosec))
			Rtimes = photonDataR[3] + ((photonDataR[2])*n_EJ208/(1000*c_const*nanosec))

			#if lengths differ
			minlen = min(len(Ltimes),len(Rtimes),Options.photoLen)

			if (minlen==0):
				return np.nan,np.nan,np.nan,np.nan,np.nan

			fastestTime =min(Ltimes[0],Rtimes[0])#min(min(Ltimes),min(Rtimes))
			slowestTime =max(Ltimes[minlen-1],Rtimes[minlen-1])#max(max(Ltimes),max(Rtimes))
			readTime = slowestTime-fastestTime
			#print(minlen)
			#print(len(np.transpose(photonDataL)),len(np.transpose(photonDataR)))
			delTime = Ltimes[0:minlen]-Rtimes[0:minlen]
			#print(delTime)
			r_Z = np.average(0.5*(LZ - 1000*(c_const/n_EJ208)*(delTime*nanosec)))
			dist = r_Z if (r_Z <= UZ) else LZ-r_Z
			r_T = fastestTime - (dist)*n_EJ208/(1000*c_const*nanosec)
	#pbar.update(1)
	# print(r_Z,r_T,readTime,r_Z - actEvtPosN[c,2], r_T - time_I_N[c])
	return r_Z,r_T,readTime,r_Z - actEvtPosN[c,2], r_T - time_I_N[c]
#pbar = tqdm(total=nEvents)
def ACTZTimeProcess():
	#results = np.zeros(shape=(nEvents,5))
	#for c in range(nEvents):
	#		results[c] = process_ACTZT(c,Options.photoLen)
	#results = Parallel(n_jobs=Options.num_cores)(delayed(process_ACTZT)(c) for c in range(nEvents)
	#inpt = list(zip(range(nEvents), repeat(Options.photoLen)))
	#print(inpt)
	with multiprocessing.Pool(Options.num_cores-1) as pool:
		results = list(tqdm(pool.imap(process_ACTZT,range(nEvents)),total=nEvents)) #zip(range(nEvents), repeat(Options.photoLen))
	return np.transpose(results)

def ACTZTimeReconstruct():

	#Options.photoLen = 5 # set parameter
	ZrecPosT = np.zeros(shape=(nEvents,3))
	err_ZrecPosT = np.zeros(shape=(nEvents,2))
	results = ACTZTimeProcess()
	ZrecPosT=results[0:3]
	err_ZrecPosT=results[3:5]
	#return np.transpose(ZrecPosT),np.transpose(err_ZrecPosT)
	return ZrecPosT,err_ZrecPosT
def ERR(point,photonData):
	pt = np.zeros(shape = (3,Options.photoLen))
	pt = np.transpose([point[0:3]]*Options.photoLen)
	pt = photonData[0:3,] - pt		
	pt = np.power(pt,2)
	times = photonData[3]-[point[3]*Options.photoLen]
	CT2 = np.power(times*nanosec*c_const/n_EJ208,2)
	return np.sum(np.abs(np.sum(pt,axis=0)-CT2))
def drGrad(dr,point, photonData):
	e0 = ERR(point, photonData)
	point1 = point
	point1[dr] = point1[dr] + epsil*UL[dr]
	e1 = ERR(point1,photonData)
	return (e1-e0)/(epsil*UL[dr])
def tGrad(point, photonData):
	e0 = ERR(point, photonData)
	point1 = point 
	point1[3] = point1[3] + epsil*L_time
	e1 = ERR(point1, photonData)
	return (e1-e0)/(epsil*L_time)
