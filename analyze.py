import numpy as np
import pandas as pd
import math
import os
import io
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
import matplotlib
matplotlib.use('AGG')
##matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.markers as mk
import matplotlib.ticker as mticker
from functools import lru_cache
from scipy import stats
from scipy.optimize import curve_fit
from tqdm import tqdm
import multiprocessing
import cv2
import sys

#------------------------------------------------------------------------------------
PYTHONIOENCODING="UTF-8"  #sys.setdefaultencoding("ISO-8859-1")
#----------------------------------------------------------------------------------
plotDIR = "plots/"
ML_PATH = "tools/ML/"
#------------------------------------------------------------------------------------
cpus = multiprocessing.cpu_count()
print("CPU Count:",cpus)
if(cpus>16):
	num_cores = 48 #48
	MaxEventLimit = True
else:
	num_cores = cpus
	MaxEventLimit = True
#------------------------------------------------------------------------------------
#MaxEventLimit = True #manual override
MaxEvents = 12000#int(input("Number of Events:"))
#--------------------------
#Defining Flags:
STRIPHIST = False
#subdefines - needs striphist True and SiPM_Based_Reconstruction False
Creation = False
Detection = False
PD = False
#---------------
Strip_Based_Reconstruction = False #otherwise uses only endcount data
SiPMTime_Based_Reconstruction = False
SiPM_Based_Reconstruction = False #a binning method, massages data to use only binned SiPM counts #unrealistic!
#---------------
#SiPM Timing: (number of photons to count in SiPM timing) (needs SiPMTime_Based_Reconstruction)
photoLen = 5
SiPMtimeRES = False
SiPMtimeVSatt = False
SiPMtimePOSRES = False #multilateration style x,y,z positioning for visualization?.
ML_DRES = True #(turn off SiPMTime_Based_Reconstruction)
DRES_Train = True #Train or Test/VIS?
#---CNN
warmstart=True # warmstart the CNN
#---KNN
KNN = True #using KNN OR CNN ? 
MLOPT = ["PCA","STD"] #options "PCA" "STD" (note STD requires PCA)
KVIS = "RUN" #options "RUNONE" "RUN" "OPTNUM" "ERR" "VIS" "False" #nearest neighbor output visualization?
knn_neighbors = 4 #set value
#---------------
POSRES = False
RES_ADD = False #additional resolution plots
SIGRES = False #needs Strip_Based_Reconstruction
SUBSTRIP = False #needs SiPM_Based_Reconstruction False
SUBSTRIP_RECONSTRUCT = False #needs SiPM_Based_Reconstruction False
#---------------
TIMERES = False
#------------------------------------------------------------------------------------
with open('tools/dimensions.py') as f: exec(f.read()) # helper file
with open('tools/data.py') as f: exec(f.read()) # helper file
with open('tools/geo.py') as f: exec(f.read()) # helper file (geo in mm)
with open('tools/reconstruct.py') as f: exec(f.read()) # helper file
with open('tools/vis.py') as f: exec(f.read()) # helper file
#------------------------------------------------------------------------------------
# Data Arrays:
#		left, strip, right
#		evtPos, evtDir
#		evtPhotoInteract, evtComptonInteract, evtInteract
#		recPos, errorPosN, actEvtPosN, (recSignal,zTensor if Strip_Based_Reconstruction)
#		time_I_N, time_I_Rec,
#		def photonSiPMData(evt)
#---\
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
	with open('tools/positionRes_Time.py') as f: exec(f.read())
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
	with open('tools/timeGammaRes.py') as f: exec(f.read()) # helper fil
#------------------------------------------------------------------------------------
#event for special analysis
#vis(eventID = 606)
#visTime(eventID = 169)


