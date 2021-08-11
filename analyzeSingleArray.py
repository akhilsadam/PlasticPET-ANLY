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
try: datadir
except NameError: datadir = "../data/current/"
else: pass
try: plotDIR
except NameError: plotDIR = "../plot/current/"
else: pass
reflectplotDIR = plotDIR + "reflect/"
ML_PATH = "tools/ML/"
#------------------------------------------------------------------------------------ CPU/GPU/TPU SETUP ------------->/v<--- ---------- ------- ------>------/  - - - - - |
cpus = multiprocessing.cpu_count()
print("CPU Count:",cpus)
if(cpus>16):
	num_cores = 48 #48
	MaxEventLimit = False
	import matplotlib
	matplotlib.use('AGG')
else:
	num_cores = cpus
	MaxEventLimit = False
	import matplotlib
	#matplotlib.use('AGG')
#----------------------------
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.markers as mk
import matplotlib.ticker as mticker
#------------------------------------------------------------------------------------ Event / Main SETUP ------------->^/<--- ---------- ------- ------>------/  - - - - - |
MaxEventLimit = False #manual override
MaxEvents = 500 #int(input("Number of Events:"))
#--------------------------
COMPLETEDETECTOR = True
#--------------------------
firstPhoton = 0
try: photoLen
except NameError: photoLen = 5
else: pass
try: ArrayNumber
except NameError: ArrayNumber = 0
else: pass
print("SINGLEArray Number:",ArrayNumber)
# ------------------------------------------ RECONSTRUCTION SETUP ---->/=<--- ---------- ------- ------>------/  - - - - - |----------------------_|
# - \---------------------------------
Process_Based_Breakdown = False
Strip_Based_Reconstruction = False #otherwise uses only endcount data
SiPMTime_Based_Reconstruction = True
SiPM_Based_Reconstruction = False #a binning method, massages data to use only binned SiPM counts #unrealistic!
ML_DRES = False #(turn off SiPMTime_Based_Reconstruction)

#--------------- --------- --------- -------- ML SETUP ------\\-->^/v<--- ---------- ------- ------>------/  - - - - - |
DRES_Train = True #Train or Test/VIS?
#---CNN
warmstart=True # warmstart the CNN
#---KNN
KNN = True #using KNN OR CNN ? 
MLOPT = [] #options "PCA" "STD" "MAHA" "DISABLE-ZT" (note MAHA,STD requires PCA)
#options "RUNONE" "RUN" "OPTNUM" "ERR" "VIS" "False" "PICKLE" #nearest neighbor output visualization?
try: KVIS
except: KVIS = "PICKLE"

knn_neighbors = 4 #set value

#--------------- --------- --------- -------- TESTS ------------->^/v<--- ---------- ------- ------>------/  - - - - - |
# Reflection Tests \---------------------------------
ReflectionTest = False
ReflectOPT = [] #options "DISABLE-VK"
boundaryinteract = True
Ropt = ""
# SIPM TIMING Tests \---------------------------------
# (number of photons to count in SiPM timing) (needs SiPMTime_Based_Reconstruction)
SiPMtimeRES = True
SiPMtimeVSatt = False
SiPMtimePOSRES = True #multilateration style x,y,z positioning for visualization?.

#--------------- --------- --------- -------- ADDITIONAL RESOLUTION PLOTS/HISTOGRAMS ------------->/=<--- ---------- ------- ------>------/  - - - - - |
# Production/Detection Histograms \---------------------------------
STRIPHIST = False
#subdefines - needs striphist, Process_Based_Breakdown True and SiPM_Based_Reconstruction False
STRIP_OPT = ["process_breakdown","electron_processes"] #options "process_breakdown" "photocompton_breakdown" "electron_processes" "subfigures" (#2 requires #1) (#3 - default is gamma_processes) (#4 ~requires #3)
Creation = True
Detection = True
PD = False
#------------------------------------------------------------------_|
POSRES = False
RES_ADD = False #additional resolution plots
SIGRES = False #needs Strip_Based_Reconstruction
SUBSTRIP = False #needs SiPM_Based_Reconstruction False
SUBSTRIP_RECONSTRUCT = False #needs SiPM_Based_Reconstruction False
#---------------
TIMERES = False
#------------------------------------------------------------------_|
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

if Strip_Based_Reconstruction:
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

if(SiPMTime_Based_Reconstruction):
	with open('tools/reconstruct_SIPMTime.py') as f: exec(f.read()) # helper file
	ZrecPosT,err_ZrecPosT = ACTZTimeReconstruct(photoLen)
	if(SiPMtimePOSRES):
		recPosT = ACTTimeReconstruct() #need to complete implementation - at present only useful for vis2

with open('tools/vis.py') as f: exec(f.read()) # helper file
#------------------------------------------------------------------------------------
# Data Arrays:
#		left, strip, right, volumeCounts
#		evtPos, evtDir
#		evtPhotoInteract, evtComptonInteract, evtInteract
#		recPos, errorPosN, actEvtPosN, (recSignal,zTensor if Strip_Based_Reconstruction)
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
if STRIPHIST:
	with open('tools/stripHistograms.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Position Resolution Plots
if POSRES:
	with open('tools/positionRes.py') as f: exec(f.read()) # helper file
if SiPMtimeRES:
	with open('tools/sipmTimeRes.py') as f: exec(f.read()) # helper file
if SiPMtimeVSatt:
	with open('tools/sipmTimeVsAtt.py') as f: exec(f.read())
if SiPMtimePOSRES:
	with open('tools/positionRes_Time.py') as f: exec(f.read()) #implementation not complete 
if RES_ADD:
	with open('tools/resAdditional.py') as f: exec(f.read()) # helper file
if SIGRES:
	#with open('tools/signalRes.py') as f: exec(f.read()) # helper file
	with open('tools/signalResAlongStrip.py') as f: exec(f.read()) # helper file
#------------------------------------------
#ML - Detector Unit Gamma Interaction Time Resolution
if ML_DRES:
	if(KNN):
		with open(ML_PATH+'ML_detRes_KNN.py') as f: exec(f.read()) # KNN instead?
	else:
		if DRES_Train:
			with open(ML_PATH+'ML_detResTRAIN.py') as f: exec(f.read()) # helper file
			
		else:
			with open(ML_PATH+'ML_detResTEST.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Sub-strip interaction location plots
if SUBSTRIP:
	with open('tools/subStripPlots.py') as f: exec(f.read()) # helper file
if SUBSTRIP_RECONSTRUCT:
	with open('tools/subStripRecPlots.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Time Resolution Plots
if TIMERES:
	with open('tools/timeGammaRes.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
# Reflection Tests
if("DISABLE-VK" in ReflectOPT):
    Ropt=Ropt+"_DISABLE_VK"
if ReflectionTest:
	with open('tools/reflectionT.py') as f: exec(f.read()) # helper fil
#------------------------------------------------------------------------------------
#event for special analysis
#vis(eventID = 606)
#visTime(eventID = 169)


