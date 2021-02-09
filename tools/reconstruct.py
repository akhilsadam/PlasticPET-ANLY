import math
from iminuit import Minuit
from itertools import chain
with open('tools/finite.py') as f: exec(f.read()) # helper file
FWHMC = 2*pow(2*math.log(2),0.5)
#------------------------------------------------------------------------------------
def SiPM_Downsample(inarray):
	return np.transpose(np.transpose(inarray,(0,2,1)).reshape(nEvents,nx,ny//Sy,Sy).sum(3),(0,2,1))
def flatten(listOfLists):
    "Flatten one level of nesting"
    return (chain.from_iterable(listOfLists))
def reconstruct():
	recPos = np.zeros(shape = (nEvents,3))
	for c in range(nEvents):
		X = np.sum(stripPos[:,:,0]*strip[c])/np.sum(strip[c])
		Y = np.sum(stripPos[:,:,1]*strip[c])/np.sum(strip[c])
		if((np.sum(left[c])/np.sum(right[c]))!=0):
			Z = (att_len/16)*math.log(np.sum(left[c])/np.sum(right[c])) + UZ;
		#elif(((np.sum(left[c])/np.sum(right[c]))==0) and (np.sum(right[c]))!=0)):
		#	Z = 0
		#elif(((np.sum(right[c])/np.sum(left[c]))==0) and (np.sum(left[c]))!=0)):
		#	Z = LZ
		#elif((np.sum(left[c])==0) and (np.sum(right[c])==0)):
		#	Z = UZ/2
		else: Z = np.nan
		recPos[c,:] = [X,Y,Z]
	return recPos
def ACTreconstruct():
	recPos = np.zeros(shape = (nEvents,3))
	recSignal = np.zeros(shape = (nEvents,ny,nx))
	sigMatrix = np.zeros(shape = (ny,nx))
	zTensor = np.zeros(shape = (nEvents,ny,nx))
	zMatrix = np.zeros(shape = (ny,nx))
	for c in range(nEvents):
		if((np.sum(left[c])!=0) and (np.sum(right[c])!=0)):
			zMatrix = (att_len/16)*np.log(left[c]/right[c]) + UZ;
			zTensor[c,:,:] = zMatrix

			sigMatrix = 0.5*((right[c]*np.exp(zMatrix/att_len))+(left[c]*np.exp((LZ-zMatrix)/att_len)))
			sigMatrix[~np.isfinite(sigMatrix)] = 0
			recSignal[c] = sigMatrix
			X = np.sum(stripPos[:,:,0]*sigMatrix)/np.sum(sigMatrix)
			Y = np.sum(stripPos[:,:,1]*sigMatrix)/np.sum(sigMatrix)

		else:
			zMatrix[:,:] = np.nan
			X,Y = np.nan,np.nan
			recSignal[c,:,:] = np.nan
			zTensor[c,:,:] = np.nan
		#---Z only
		if((np.sum(left[c])/np.sum(right[c]))!=0):
			Z = (att_len/16)*math.log(np.sum(left[c])/np.sum(right[c])) + UZ;
		else:
			Z = np.nan
			
			
		recPos[c,:] = [X,Y,Z]
		
	return recPos,recSignal,zTensor
def TOF_GammaInteractRec(recPos):
	dist = np.power((UX-recPos[:,0]),2) + np.power((recPos[:,1]-evtPos[:,1]),2) + np.power((recPos[:,2]-evtPos[:,2]),2)
	dist = np.power(dist,0.5)
	time_I = ((UX-recPos[:,0])/1000)/(c_const/n_EJ208)
	time_I = time_I/nanosec
	return time_I
def RSQ(data, model):
	return 1-np.var(data-model)/np.var(data)
#------------------------------------------------------------------------------------
if Strip_Based_Reconstruction:
	recPos = reconstruct()
else:
	recPos,recSignal,zTensor = ACTreconstruct()
time_I_Rec = TOF_GammaInteractRec(recPos)
#------------------------------------------------------------------------------------
#reconstruction errors:
#------------------------------------------------------------------------------------
evtIC = evtInteract
#get photo only indices
#for evt in range(nEvents):
#	allx = np.transpose(evtIC[evt])[0]
#	allxIC = np.transpose(evtComptonInteract[evt])[0]
#	print(evtIC[evt])
#	evtIC[evt] = [(np.where(allx[i] in allxIC,evtIC[evt][i],np.nan)).tolist() for i in range(len(allx))]
	#print(evtIC[evt])
	#break
#
errorPosN = np.zeros(shape=(nEvents,3))
errorPos = np.zeros(shape=(3),dtype = list)
actEvtPosN = np.zeros(shape=(nEvents,3))
actEvt = np.zeros(shape=(3),dtype = list)
time_I_N = np.zeros(shape=(nEvents))
uninteractedEvents = 0
for evt in range(nEvents):
	if(len(evtIC[evt])>0):
		for i in range(3):
			#actEvt[i] = np.average(np.transpose(evtInteract[evt])[i])
			actEvt[i] = np.dot(np.transpose(evtIC[evt])[i],np.transpose(evtIC[evt])[3])/np.sum(np.transpose(evtIC[evt])[3])
		errorPosN[evt] = recPos[evt]-actEvt#evtInteract[evt][0][0:3]
		actEvtPosN[evt] = actEvt
		time_I_N[evt] = np.dot(np.transpose(evtIC[evt])[4],np.transpose(evtIC[evt])[3])/np.sum(np.transpose(evtIC[evt])[3])
	else:
		uninteractedEvents = uninteractedEvents + 1
		errorPosN[evt] = [np.nan,np.nan,np.nan]
		actEvtPosN[evt] = [np.nan,np.nan,np.nan]
		time_I_N[evt] = np.nan
#------------------------------------------------------------------------------------
if(SiPMTime_Based_Reconstruction):
	with open('tools/reconstruct_SIPMTime.py') as f: exec(f.read()) # helper file
	#recPosT = ACTTimeReconstruct() #need to complete implementation - at present only useful for vis2
	ZrecPosT,err_ZrecPosT = ACTZTimeReconstruct(photoLen)
