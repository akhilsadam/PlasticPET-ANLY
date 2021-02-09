epsil = 0.001
lr = 0.002
lrt = 0.002
L_time = 0.001 #ns

UL = [77.4,103.2,1000]

def ACTTimeReconstruct():

	photoLen = 5 # set parameter
	photonData = np.zeros(shape=(5,photoLen))
	recPosT = np.zeros(shape=(nEvents,4))
	for c in range(3,4):#nEvents
		photonDatas = np.transpose(photonSiPMData(c))
		photonData = np.transpose(sorted(photonDatas, key=lambda photonDatas: photonDatas[3]))[:,0:photoLen]

		fastestTime = min(photonData[3])
		#print(photonData)
		#photoLen = len(photonData[3])
		#for i in range(0,photoLen):

		#Bin Data into Strips
		# ct estimator for x,y,z position.
		point = [0,0,UZ,1]
		for u in range(50):
			for dr in range(0,3):
				point[dr] = point[dr] - lr*drGrad(dr,point, photoLen, photonData)
				if(point[2] <= UZ):
					dist = point[2]
				else:
					dist = LZ-point[2]
				point[3] = fastestTime - (dist)*n_EJ208/(1000*c_const*nanosec)
			#point[3] = point[3] - lrt*tGrad(point, photoLen, photonData)
			#print(err[:,5])
		#print(point)


		recPosT[c] = point
		
	return recPosT
def ACTZTimeReconstruct(photoLen):

	#photoLen = 5 # set parameter
	photonData = np.zeros(shape=(5,photoLen))
	ZrecPosT = np.zeros(shape=(nEvents,3))
	err_ZrecPosT = np.zeros(shape=(nEvents,2))
	for c in range(nEvents):
		photonDatas = photonSiPMData(c)
		if(len(photonDatas)==0):
			ZrecPosT[c] = np.nan
			err_ZrecPosT[c] = np.nan
			continue
		photonDataL = np.transpose(photonDatas[:,photonDatas[2]>UZ])
		photonDataR = np.transpose(photonDatas[:,photonDatas[2]<=UZ])
		if((len(photonDataL)==0) or (len(photonDataR)==0)):
			ZrecPosT[c] = np.nan
			err_ZrecPosT[c] = np.nan
			continue
		photonDataL = np.transpose(sorted(photonDataL, key=lambda photonDataL: photonDataL[3]))
		photonDataR = np.transpose(sorted(photonDataR, key=lambda photonDataR: photonDataR[3]))
		#if lengths differ
		minlen = min(len(photonDataL),len(photonDataR),photoLen)
		if (photonDataL.ndim>1) and (photonDataR.ndim>1):
			photonDataL = photonDataL[:,0:minlen]
			photonDataR = photonDataR[:,0:minlen]
		elif (photonDataL.ndim>1):
			photonDataL = photonDataL[:,0]
		else:
			photonDataR = photonDataR[:,0]
			
		fastestTime = min(min(photonDataL[3]),min(photonDataR[3]))
		slowestTime = max(max(photonDataL[3]),max(photonDataR[3]))
		readTime = slowestTime-fastestTime
		#print(photonDataL)
		#print(photonDataR)
		Ltimes = photonDataL[3] - ((photonDataL[2]-LZ)*n_EJ208/(1000*c_const*nanosec))
		Rtimes = photonDataR[3] + ((photonDataR[2])*n_EJ208/(1000*c_const*nanosec))
		#if lengths differ
		minlen = min(len(Ltimes),len(Rtimes),photoLen)
#		print(len(np.transpose(photonDataL)),len(np.transpose(photonDataR)))
		delTime = Ltimes[0:minlen]-Rtimes[0:minlen]
		#print(delTime)
		r_Z = np.average(0.5*(LZ - 1000*(c_const/n_EJ208)*(delTime*nanosec)))
		if(r_Z <= UZ):
			dist = r_Z
		else:
			dist = LZ-r_Z

		r_T = fastestTime - (dist)*n_EJ208/(1000*c_const*nanosec)
		ZrecPosT[c] = [r_Z,r_T,readTime]
		err_ZrecPosT[c] = [r_Z - actEvtPosN[c,2], r_T - time_I_N[c]]
		#print([r_Z,r_T,readTime])

	return np.transpose(ZrecPosT),np.transpose(err_ZrecPosT)

def ERR(point, photoLen, photonData):
	pt = np.zeros(shape = (3,photoLen))
	pt = np.transpose([point[0:3]]*photoLen)
	pt = photonData[0:3,] - pt		
	pt = np.power(pt,2)
	times = photonData[3]-[point[3]*photoLen]
	CT2 = np.power(times*nanosec*c_const/n_EJ208,2)
	return np.sum(np.abs(np.sum(pt,axis=0)-CT2))
def drGrad(dr,point, photoLen, photonData):
	e0 = ERR(point, photoLen, photonData)
	point1 = point
	point1[dr] = point1[dr] + epsil*UL[dr]
	e1 = ERR(point1, photoLen, photonData)
	return (e1-e0)/(epsil*UL[dr])
def tGrad(point, photoLen, photonData):
	e0 = ERR(point, photoLen, photonData)
	point1 = point 
	point1[3] = point1[3] + epsil*L_time
	e1 = ERR(point1, photoLen, photonData)
	return (e1-e0)/(epsil*L_time)
