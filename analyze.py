import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
import matplotlib.cm as cm
from scipy import stats
from scipy.optimize import curve_fit
import cv2
#------------------------------------------------------------------------------------
#Defining Flags:
STRIPHIST = False
#subdefines - needs striphist True and SiPM_Based_Reconstruction False
Creation = False
Detection = False
PD = False
#---------------
Strip_Based_Reconstruction = False #otherwise uses only endcount data
SiPM_Based_Reconstruction = False #massages data to use only averaged SiPM counts #unrealistic!
#---------------
POSRES = False
RES_ADD = True
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
#		time_I_N, time_I_Rec
#---\
#------------------------------------------ 
#Strip Histogram Plots
if STRIPHIST:
	with open('tools/stripHistograms.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Position Resolution Plots
if POSRES:
	with open('tools/positionRes.py') as f: exec(f.read()) # helper file
if RES_ADD:
	with open('tools/resAdditional.py') as f: exec(f.read()) # helper file
if SIGRES:
	#with open('tools/signalRes.py') as f: exec(f.read()) # helper file
	with open('tools/signalResAlongStrip.py') as f: exec(f.read()) # helper file
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



