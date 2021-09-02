#!/usr/bin/env python3
from utils.simpleimport import *
#------------------------------------------------------------------------------------
PYTHONIOENCODING="UTF-8"  #sys.setdefaultencoding("ISO-8859-1")
#------------------------------------------------------------------------------------
from analyzeOptions import *
reflectplotDIR = Options.plotDIR + "reflect/"
ML_PATH = "tools/ML/"
#--------------------------
try: Options.ArrayNumber
except: Options.ArrayNumber = 0
#----------------------------
print("Single Array Number:",Options.ArrayNumber)
#----------------------------
from utils.mplimport import *
#------------------------------------------------------------------------------------ Geometry / DATA SETUP ------------->^/v<--- ---------- ------ ------>------/  - - - - - |
from tools.reconstruct import *
#------------------------------------------------------------------------------------
try: Options.regenerateLocalPickles
except: Options.regenerateLocalPickles = False
try: Options.regenerateGlobalPickles
except: Options.regenerateGlobalPickles = False
try: Options.regenerateMLPickles
except: Options.regenerateMLPickles = False
try: dataOpen
except: dataOpen = False
if(not dataOpen):
	with open('tools/data.py') as f: exec(f.read()) # helper file

# with open('tools/reconstruct.py') as f: exec(f.read()) # helper file
pickles = ['beamInteraction.pkl','localBeam_AR'+str(Options.ArrayNumber)+'.pkl','gammaInteractPosition_AR'+str(Options.ArrayNumber)+'.pkl','reco_0_AR'+str(Options.ArrayNumber)+'.pkl']
sauerkraut = ['reco_0_opt_AR'+str(Options.ArrayNumber)+'.pkl'] # optional pickles
ml_pkl = Options.datadir+'ML_DATA_PICKLE_AR'+str(Options.ArrayNumber)+'_P'+str(Options.photoLen)+'.pkl'

sauerkrautOPT = (not Options.SiPMTime_Based_Reconstruction) and (not Options.Strip_Based_Reconstruction)
# print("Options.regenerateGlobalPickles",Options.regenerateGlobalPickles)
print(pickles)
try:
	if(Options.regenerateGlobalPickles):
		raise FileNotFoundError('[NotAnERROR] Regenerating Global Pickles')
	with open(Options.datadir+pickles[0], 'rb') as f:  # Python 3: open(..., 'wb')
		print("[OPENING]")
		evtPhotoInteractG, evtComptonInteractG,evtInteractG = pickle.load(f)
except FileNotFoundError as VALERIN:
	print(VALERIN)
	print("[REGENERATION] Global Pickling...")
	evtPhotoInteractG, evtComptonInteractG,evtInteractG = beamInteraction()
	with open(Options.datadir+pickles[0], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([evtPhotoInteractG, evtComptonInteractG,evtInteractG], f)


try:
	if(Options.regenerateLocalPickles):
		raise FileNotFoundError('[NotAnERROR] Regenerating Local Pickles')
	if(Options.STRIPHIST):
		left,strip,right = photonNPYLoad() # other semi-necessary loads
	with open(Options.datadir+pickles[1], 'rb') as f:  # Python 3: open(..., 'wb')
		print("[OPENING]")
		evtPhotoInteract, evtComptonInteract,evtInteract,evtType,evtType2 = pickle.load(f)
	with open(Options.datadir+pickles[2],'rb') as f:  # Python 3: open(..., 'rb')
		print("[OPENING]")
		uninteractedEvents,errorPosN,actEvtPosN,time_I_N = pickle.load(f)
	with open(Options.datadir+pickles[3],'rb') as f: 
		print("[OPENING]")
		recPos,ZrecPosT,err_ZrecPosT,errorPosN = pickle.load(f)
	with open(ml_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
		inptTensor,expTensor,eventIDs = pickle.load(f)
	if sauerkrautOPT:
		with open(Options.datadir+sauerkraut[0], 'rb') as f:  # Python 3: open(..., 'wb')
			recSignal,zTensor,time_I_Rec = pickle.load(f)
except FileNotFoundError as VALERIN:
	print(VALERIN)
	print("[REGENERATION] Local Pickling...")
	evtPhotoInteract, evtComptonInteract,evtInteract,evtType,evtType2 = localizeBeam(evtPhotoInteractG,evtComptonInteractG,evtInteractG)
	uninteractedEvents,actEvtPosN,time_I_N = gammaInteractPosition(evtInteract)
	left,strip,right = photonNPYLoad()

	if Options.SiPMTime_Based_Reconstruction:
		print("[STATUS] SIPM TIME RECONSTRUCT")
		with open('tools/reconstruct_SIPMTime.py') as f: exec(f.read()) # helper file
		ZrecPosT,err_ZrecPosT = ACTZTimeReconstruct()
		recPos = ACTreconstruct_time(left,right,ZrecPosT[0,:]) # this was an issue in the recent past...
	elif Options.Strip_Based_Reconstruction:
		recPos = reconstruct(left,right,strip)
	else:
		recPos,recSignal,zTensor = ACTreconstruct(left,right)
		time_I_Rec = TOF_GammaInteractRec(recPos,evtPos)

	errorPosN = recalculate_errorPos(recPos,actEvtPosN)

	with open(Options.datadir+pickles[1], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([evtPhotoInteract, evtComptonInteract,evtInteract,evtType,evtType2], f)
	with open(Options.datadir+pickles[2], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([uninteractedEvents,errorPosN,actEvtPosN,time_I_N], f)
	with open(Options.datadir+pickles[3], 'wb') as f:  # Python 3: open(..., 'wb')
		pickle.dump([recPos,ZrecPosT,err_ZrecPosT,errorPosN], f)
	if sauerkrautOPT:
		with open(Options.datadir+sauerkraut[0], 'wb') as f:  # Python 3: open(..., 'wb')
			pickle.dump([recSignal,zTensor,time_I_Rec], f)

	# 	print("[WARNING] SIPM TIME POSRES - NOT IMPLEMENTED YET")
	# 	recPosT = ACTTimeReconstruct() #need to complete implementation - at present only useful for vis2

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
if MODE != "MANUAL":
	print("\n[STATUS] IN AUTOMATIC MODE\n")
#------------------------------------------ 
#Strip Histogram Plots
if Options.STRIPHIST:
	with open('tools/energyResolution/stripHistograms.py') as f: exec(f.read()) # helper file
#------------------------------------------ 
#Position Resolution Plots
if Options.POSRES:
	# with open('tools/positionRes.py') as f: exec(f.read()) # helper file
	from tools.positionRes import xyzResolution
	xyzResolution(errorPosN,uninteractedEvents)
if Options.SiPMtimeRES:
	with open('tools/sipmTimeRes.py') as f: exec(f.read()) # helper file
if Options.SiPMtimeVSatt:
	with open('tools/sipmTimeVsAtt.py') as f: exec(f.read())
if Options.SiPMtimePOSRES:
	# with open('tools/positionRes_Time.py') as f: exec(f.read()) #implementation not complete 
	from tools.positionRes import xyzResolution
	xyzResolution(errorPosN,uninteractedEvents)
if Options.RES_ADD:
	with open('tools/resAdditional.py') as f: exec(f.read()) # helper file
if Options.SIGRES:
	#with open('tools/signalRes.py') as f: exec(f.read()) # helper file
	with open('tools/signalResAlongStrip.py') as f: exec(f.read()) # helper file
if Options.ML_DRES:
	if Options.KNN:
		with open(ML_PATH+'ML_detRes_KNN.py') as f: exec(f.read()) # Options.KNN instead?
	elif Options.DRES_Train:
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


