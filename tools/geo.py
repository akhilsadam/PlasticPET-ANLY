#------------------------------------------------------------------------------------
#Geometry Setup
#------------------------------------------------------------------------------------
#set up stripPos
from itsdangerous import exc
import numpy as np
from numba import jit
from tools.dimensions import *
import multiprocessing
from tqdm import tqdm
import torch
from analyzeOptions import Options
@jit(nopython=True, parallel=True)
def stripPosGenerate():
	stripPos = np.zeros(shape=(ny,nx,nz))
	for j in range(ny):
		numSiPM = int(j/4)
		VKOffset = (2*numSiPM + 1)*VKT
		y = UY - ((j+0.5)*stripWy + VKOffset)
		for i in range(nx):
			VKOffset = (2*i + 1)*VKT
			x = (i+0.5)*stripWx + VKOffset - UX
			stripPos[j,i,0] = x
			stripPos[j,i,1] = y
			stripPos[j,i,2] = UZ
	return stripPos
# Bin->Array->Global coordinates
def ArrayToGlobalCoordinates(x,y,z,A):
	angle = A*theta
	cosine = math.cos(angle)
	sine = math.sin(angle)
	x_global = (Radius+x)*cosine - y*sine
	y_global = (Radius+x)*sine + y*cosine
	return np.array([x_global,y_global,z])

def BinToGlobalCoordinates(x,y,z,A):
	[x_A,y_A,z_A] = stripPos[y,x]
	if(z==0):z_global = 0
	elif(z==2):z_global = LZ
	else: z_global = z_A
	return ArrayToGlobalCoordinates(x_A,y_A,z_global,A)

def GlobalToArrayCoordinates(x,y,z,A):
	angle = A*theta
	translatedPosition = np.array([np.array(x) - Radius*math.cos(angle),np.array(y) - Radius*math.sin(angle),np.array(z)])
	# print(translatedPosition[0])
	xy = np.sqrt(np.power(translatedPosition[0],2)+np.power(translatedPosition[1],2))
	angle2 = -angle + np.arctan2(translatedPosition[1],translatedPosition[0])
	return np.array([xy*np.cos(angle2),xy*np.sin(angle2),z])

def GlobalToArray(pos,A):
	return GlobalToArrayCoordinates(pos[0],pos[1],pos[2],A)

def GlobalToArrayM(pos,A):
	try: pos[0:3] = GlobalToArrayCoordinates(pos[0],pos[1],pos[2],A)[:3]
	except: print(pos)
	return pos

def ArrayToGlobalM(*params):
	pos = list(params)
	# expect input x,y,z,t,A
	pos[0:3] = ArrayToGlobalCoordinates(pos[0],pos[1],pos[2],pos[4])[:3]
	return pos

# @jit(nopython=True, parallel=True)
def ArrayToGlobalMT(pos,A):
	if(Options.device=="cpu"):
		A_np = A.detach().numpy()
		pos_np = pos.detach().numpy()
	else:
		A_np = A.detach().cpu().numpy()
		pos_np = pos.detach().cpu().numpy()

	dataP = np.zeros(shape = (pos_np.shape[0],pos_np.shape[1]+1))
	dataP[:,0:pos_np.shape[1]] = pos_np
	dataP[:,pos_np.shape[1]] = A_np

	with multiprocessing.Pool(Options.workers) as pool:
		outG = np.array(list(pool.starmap(ArrayToGlobalM,dataP)))
	return outG
# @jit(nopython=True)
# def ArrayToBinCoordinates(x,y,z,A):
# 	  TO BE IMPLEMENTED

#-----------------------------------------
stripPos = stripPosGenerate()
