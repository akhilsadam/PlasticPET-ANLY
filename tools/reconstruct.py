import math
import numpy as np
import pickle
from iminuit import Minuit
from itertools import chain
from tools.dimensions import *
from tools.geo import *
from tools.finite import *
from analyzeOptions import *
FWHMC = 2*pow(2*math.log(2),0.5)
#------------------------------------------------------------------------------------
def SiPM_Downsample(inarray):
	return np.transpose(np.transpose(inarray,(0,2,1)).reshape(Options.nEvents,nx,ny//Sy,Sy).sum(3),(0,2,1))
def flatten(listOfLists):
    "Flatten one level of nesting"
    return (chain.from_iterable(listOfLists))
def reconstruct(left,right,strip):
	recPos = np.zeros(shape = (Options.nEvents,3))
	for c in range(Options.nEvents):
		X = np.sum(stripPos[:,:,0]*strip[c])/np.sum(strip[c])
		Y = np.sum(stripPos[:,:,1]*strip[c])/np.sum(strip[c])
		if((np.sum(left[c])/np.sum(right[c]))!=0):
			Z = (att_len/16)*math.log(np.sum(left[c])/np.sum(right[c])) + UZ
		#elif(((np.sum(left[c])/np.sum(right[c]))==0) and (np.sum(right[c]))!=0)):
		#	Z = 0
		#elif(((np.sum(right[c])/np.sum(left[c]))==0) and (np.sum(left[c]))!=0)):
		#	Z = LZ
		#elif((np.sum(left[c])==0) and (np.sum(right[c])==0)):
		#	Z = UZ/2
		else: Z = np.nan
		recPos[c,:] = [X,Y,Z]
	return recPos
def ACTreconstruct(left,right):
	recPos = np.zeros(shape = (Options.nEvents,3))
	recSignal = np.zeros(shape = (Options.nEvents,ny,nx))
	sigMatrix = np.zeros(shape = (ny,nx))
	zTensor = np.zeros(shape = (Options.nEvents,ny,nx))
	zMatrix = np.zeros(shape = (ny,nx))
	for c in range(Options.nEvents):
		if((np.sum(left[c])!=0) and (np.sum(right[c])!=0)):
			zMatrix = (att_len/16)*np.log(left[c]/right[c]) + UZ
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
			Z = (att_len/16)*math.log(np.sum(left[c])/np.sum(right[c])) + UZ
		else:
			Z = np.nan
			
			
		recPos[c,:] = [X,Y,Z]
		
	return recPos,recSignal,zTensor
def ACTreconstruct_time(left,right,rec_Z):
	# needs SiPM_Time_reconstruction first!
	recPos = np.zeros(shape = (Options.nEvents,3))
	# sigMatrix = np.zeros(shape = (ny,nx))
	# uip = 0
	# uipx=0
	for c in range(Options.nEvents):
		sigMatrix = left[c]+right[c]
		# if np.sum(sigMatrix) == 0:
		# 	uip+=1
		X = np.sum(stripPos[:,:,0]*sigMatrix)/np.sum(sigMatrix)
		# if np.isfinite(X):
		# 	uipx+=1
		Y = np.sum(stripPos[:,:,1]*sigMatrix)/np.sum(sigMatrix)
		Z = rec_Z[c]
		recPos[c,:] = X,Y,Z		
	# print("Number of failed left+right:",uip)
	# print("Number of failed X:",uipx)
	return recPos
# redo position calculation with better numbers!
# r_z ZrecPosT[0]
# r_t ZrecPosT[1]
def recalculate_errorPos(recPos,actEvtPosN):
	erp = recPos - actEvtPosN
	return erp[~np.isnan(erp).any(axis=1)]
	
def TOF_GammaInteractRec(recPos,evtPos):
	dist = np.power((UX-recPos[:,0]),2) + np.power((recPos[:,1]-evtPos[:,1]),2) + np.power((recPos[:,2]-evtPos[:,2]),2)
	dist = np.power(dist,0.5)
	time_I = ((UX-recPos[:,0])/1000)/(c_const/n_EJ208)
	time_I = time_I/nanosec
	return time_I
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#reconstruction errors:
#------------------------------------------------------------------------------------
#print(evtIC)
#get photo only indices
#for evt in range(Options.nEvents):
#	allx = np.transpose(evtIC[evt])[0]
#	allxIC = np.transpose(evtComptonInteract[evt])[0]
#	print(evtIC[evt])
#	evtIC[evt] = [(np.where(allx[i] in allxIC,evtIC[evt][i],np.nan)).tolist() for i in range(len(allx))]
	#print(evtIC[evt])
	#break
#
def gammaInteractPosition(evtInteract):
	evtIC = evtInteract
	# errorPosN = np.zeros(shape=(Options.nEvents,3))
	# errorPos = np.zeros(shape=(3),dtype = list)
	actEvtPosN = np.zeros(shape=(Options.nEvents,3))
	actEvtG = np.zeros(shape=(3,3),dtype = list)
	#actEvt = np.zeros(shape=(3),dtype = list)
	time_I_N = np.zeros(shape=(Options.nEvents))
	time_I_G = np.zeros(shape=(3))
	photonCut = 10
	uninteractedEvents = 0
	for evt in range(Options.nEvents):
		if (len(evtIC[evt])>0):
			allIC = np.asarray(evtIC[evt])
			for gam in range(3):
				# print(allIC)
				ICVT = allIC[(allIC[:,5]).astype(int)==gam,:]
				# print(ICVT)
				for i in range(3):
					#actEvt[i] = np.average(np.transpose(evtInteract[evt])[i])
					totPhot = np.sum(np.transpose(ICVT)[3])
					if (totPhot>photonCut):
						act = np.dot(np.transpose(ICVT)[i],np.transpose(ICVT)[3])/np.sum(np.transpose(ICVT)[3])
						actEvtG[gam,i] = act if withinLimitXYZ(act,i) else np.nan
					else:
						actEvtG[gam,i] = np.nan
				time_I_G[gam] = np.dot(np.transpose(ICVT)[4],np.transpose(ICVT)[3])/np.sum(np.transpose(ICVT)[3])
			try:
				indv = np.nanargmin(np.sum(np.power(actEvtG[:,0:2],2),axis=1))
			except:
				uninteractedEvents += 1
				# errorPosN[evt] = [np.nan,np.nan,np.nan]
				actEvtPosN[evt] = [np.nan,np.nan,np.nan]
				time_I_N[evt] = np.nan
			else:
				# errorPosN[evt] = recPos[evt]-actEvtG[indv] #evtInteract[evt][0][0:3]
				actEvtPosN[evt] = actEvtG[indv]
				time_I_N[evt] = time_I_G[indv]
				# print(actEvtG)
				# print(actEvtG[indv])
					# if(np.any(actEvtG[indv]==np.nan)):
					# 	print("[ERROR] EVT INTERACT IO FAIL")
		else:
			uninteractedEvents += 1
			# errorPosN[evt] = [np.nan,np.nan,np.nan]
			actEvtPosN[evt] = [np.nan,np.nan,np.nan]
			time_I_N[evt] = np.nan
			# print("[STATUS] Uninteracted Event")
	return uninteractedEvents,actEvtPosN,time_I_N
#------------------------------------------------------------------------------------


