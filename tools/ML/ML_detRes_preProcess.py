@lru_cache(maxsize=2000)
def process_MLDRESinput(c):
	photonDatas = photonSiPMData(c)
	if(len(photonDatas)==0):
		return None
	else:
		photonDataL = np.transpose(photonDatas[:,photonDatas[2]>UZ])
		photonDataR = np.transpose(photonDatas[:,photonDatas[2]<=UZ])
		if((len(photonDataL)==0) or (len(photonDataR)==0)):
			return None
		else:
			photonDataL = np.transpose(sorted(photonDataL, key=lambda photonDataL: photonDataL[3]))
			photonDataR = np.transpose(sorted(photonDataR, key=lambda photonDataR: photonDataR[3]))
			#if lengths differ
			minlen = min(len(photonDataL),len(photonDataR))
			if (minlen < photoLen):
				return None
			if (photonDataL.ndim>1) and (photonDataR.ndim>1):
				photonDataL = photonDataL[:,0:photoLen]
				photonDataR = photonDataR[:,0:photoLen]
			else:
				return None
				
			Ltimes = photonDataL[3] - ((photonDataL[2]-LZ)*n_EJ208/(1000*c_const*nanosec))
			Rtimes = photonDataR[3] + ((photonDataR[2])*n_EJ208/(1000*c_const*nanosec))
			fastestTime = min(min(Ltimes),min(Rtimes))
			#if lengths differ
			minlen = min(len(Ltimes),len(Rtimes))
			if(minlen != photoLen):
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

			TZ = torch.zeros(4,2*photoLen+1)
			TZ[:,0:2*photoLen:2] = torch.from_numpy(photonDataL)
			TZ[:,1:2*photoLen:2] = torch.from_numpy(photonDataR)
			ETZ = torch.zeros(4)
			ETZ[0:3] = torch.from_numpy(actEvtPosN[c])
			ETZ[3] = (time_I_N[c]-fastestTime)
			#print(ETZ)
			TZ[:,2*photoLen] = ETZ
			#print(TZ)
			TZ[3] = 1000*(TZ[3]*nanosec)*(c_const/n_EJ208) #UNIT CONVERSION from ns to mm
			#print(TZ)

	return TZ
from tqdm import tqdm
def MLDRESpreprocess(photoLen):
	with multiprocessing.Pool(workers) as pool:
		inptL = list(tqdm(pool.imap_unordered(process_MLDRESinput,range(nEvents)),total=nEvents))
		tList = [i for i in inptL if type(i)==torch.Tensor]
		#print(tList)
		trainTensor = torch.stack(tList)
		inputTensor = trainTensor[:,:,0:2*photoLen]
		expecTensor = trainTensor[:,:,2*photoLen]
	return inputTensor,expecTensor
