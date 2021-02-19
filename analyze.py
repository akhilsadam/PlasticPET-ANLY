import numpy as np
import pandas as pd
import os
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
import matplotlib.cm as cm
import matplotlib.markers as mk
from functools import lru_cache
from scipy import stats
from scipy.optimize import curve_fit
from tqdm import tqdm
import cv2
#------------------------------------------------------------------------------------
plotDIR = "plots/"
ML_PATH = "tools/ML/"
#------------------------------------------------------------------------------------
MaxEventLimit = True
MaxEvents = 400
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
DRES_Train = True #Train or Test?
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


