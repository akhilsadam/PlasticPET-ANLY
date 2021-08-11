#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math
import os
import io
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
from functools import lru_cache
from scipy import stats
from scipy import signal
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline
from tqdm import tqdm
import multiprocessing
from numba import jit
import cv2
import sys

#------------------------------------------------------------------------------------
PYTHONIOENCODING="UTF-8"  #sys.setdefaultencoding("ISO-8859-1")
#------------------------------------------------------------------------------------
from analyzeOptions import *
try: datadir
except NameError: datadir = "../data/current/"
Options.datadir = datadir
try: plotDIR
except NameError: plotDIR = "../plot/current/"
Options.plotDIR = plotDIR
reflectplotDIR = plotDIR + "reflect/"
ML_PATH = "tools/ML/"
#--------------------------
firstPhoton = 0
try: photoLen
except NameError: photoLen = 5
else: pass
try: ArrayNumber
except NameError: ArrayNumber = 0
else: pass
#----------------------------
print("SINGLEArray Number:",ArrayNumber)
#----------------------------
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.markers as mk
import matplotlib.ticker as mticker
#------------------------------------------------------------------------------------ Geometry / DATA SETUP ------------->^/v<--- ---------- ------ ------>------/  - - - - - |
from tools.geo import *
from tools.reconstruct import *
#------------------------------------------------------------------------------------
try: regeneratePickles
except: regeneratePickles = False
else: pass
try: regenerateMLPickles
except: regenerateMLPickles = False
else: pass
try: dataOpen
except: dataOpen = False
else: pass
if(not dataOpen):
	with open('tools/data.py') as f: exec(f.read()) # helper file

# with open('tools/reconstruct.py') as f: exec(f.read()) # helper file
pickles = ['beamInteraction.pkl','gammaInteractPosition.pkl']
ml_pkl = datadir+'ML_DATA_PICKLE_AR'+str(ArrayNumber)+'_P'+str(photoLen)+'.pkl'

if Options.Strip_Based_Reconstruction:
	recPos = reconstruct(left,right,strip,nEvents)
else:
	recPos,recSignal,zTensor = ACTreconstruct(left,right,nEvents)
time_I_Rec = TOF_GammaInteractRec(recPos,evtPos)

try:
	if(regeneratePickles):
		raise ValueError('[NotAnERROR] Regenerating Pickles')
	with open(datadir+pickles[0], 'rb') as f:  # Python 3: open(..., 'wb')
		evtPhotoInteract, evtComptonInteract,evtInteract,photonmask,comptonmap,photomap,n_Compt,n_Photo,evtType,evtType2 = pickle.load(f)
	with open(datadir+pickles[1],'rb') as f:  # Python 3: open(..., 'rb')
   		uninteractedEvents,errorPosN,actEvtPosN,time_I_N = pickle.load(f)
except:
	evtPhotoInteract, evtComptonInteract,evtInteract,photonmask,comptonmap,photomap,n_Compt,n_Photo,evtType,evtType2 = beamInteraction()
	uninteractedEvents,errorPosN,actEvtPosN,time_I_N = gammaInteractPosition(evtInteract, nEvents, recPos)
	with open(datadir+pickles[0], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([evtPhotoInteract, evtComptonInteract,evtInteract,photonmask,comptonmap,photomap,n_Compt,n_Photo,evtType,evtType2], f)
	with open(datadir+pickles[1], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([uninteractedEvents,errorPosN,actEvtPosN,time_I_N], f)

if(Options.SiPMTime_Based_Reconstruction):
	with open('tools/reconstruct_SIPMTime.py') as f: exec(f.read()) # helper file
	ZrecPosT,err_ZrecPosT = ACTZTimeReconstruct(photoLen)
	if(Options.SiPMtimePOSRES):
		recPosT = ACTTimeReconstruct() #need to complete implementation - at present only useful for vis2

with open('tools/vis.py') as f: exec(f.read()) # helper file
#------------------------------------------------------------------------------------
# Data Arrays:
#		left, strip, right, volumeCounts
#		evtPos, evtDir
#		evtPhotoInteract, evtComptonInteract, evtInteract
#		recPos, errorPosN, actEvtPosN, (recSignal,zTensor if Options.Strip_Based_Reconstruction)
#		time_I_N, time_I_Rec,
#		def photonSiPMData(evt)
#---\
try: MODE
except NameError: MODE="MANUAL"
else: pass
if MODE=="MANUAL":
	pass
else:
	print("\n[STATUS] IN AUTOMATIC MODE\n")
#------------------------------------------ 
#Strip Histogram Plots
if Options.STRIPHIST:
	with open('tools/stripHistograms.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Position Resolution Plots
if Options.POSRES:
	# with open('tools/positionRes.py') as f: exec(f.read()) # helper file
	from tools.positionRes import xyzResolution
	xyzResolution(nEvents,errorPosN)
if Options.SiPMtimeRES:
	with open('tools/sipmTimeRes.py') as f: exec(f.read()) # helper file
if Options.SiPMtimeVSatt:
	with open('tools/sipmTimeVsAtt.py') as f: exec(f.read())
if Options.SiPMtimePOSRES:
	# with open('tools/positionRes_Time.py') as f: exec(f.read()) #implementation not complete 
	from tools.positionRes_Time import recalculate_errorPos
	from tools.positionRes import xyzResolution
	errorPosN_time = recalculate_errorPos(left,right,nEvents,ZrecPosT,actEvtPosN)
	xyzResolution(nEvents,errorPosN_time,uninteractedEvents)
if Options.RES_ADD:
	with open('tools/resAdditional.py') as f: exec(f.read()) # helper file
if Options.SIGRES:
	#with open('tools/signalRes.py') as f: exec(f.read()) # helper file
	with open('tools/signalResAlongStrip.py') as f: exec(f.read()) # helper file
#------------------------------------------
#ML - Detector Unit Gamma Interaction Time Resolution
if Options.ML_DRES:
	if(Options.KNN):
		with open(ML_PATH+'ML_detRes_KNN.py') as f: exec(f.read()) # Options.KNN instead?
	else:
		if Options.DRES_Train:
			with open(ML_PATH+'ML_detResTRAIN.py') as f: exec(f.read()) # helper file
			
		else:
			with open(ML_PATH+'ML_detResTEST.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Sub-strip interaction location plots
if Options.SUBSTRIP:
	with open('tools/subStripPlots.py') as f: exec(f.read()) # helper file
if Options.SUBSTRIP_RECONSTRUCT:
	with open('tools/subStripRecPlots.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Time Resolution Plots
if Options.TIMERES:
	with open('tools/timeGammaRes.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
# Reflection Tests
if("DISABLE-VK" in Options.ReflectOPT):
    Options.Ropt=Options.Ropt+"_DISABLE_VK"
if Options.ReflectionTest:
	with open('tools/reflectionT.py') as f: exec(f.read()) # helper fil
#------------------------------------------------------------------------------------
#event for special analysis
#vis(eventID = 606)
#visTime(eventID = 169)


