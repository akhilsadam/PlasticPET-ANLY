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
import cv2
import sys
import matplotlib.pyplot as plt
from tools.dimensions import *
from tools.geo import *
from tools.reconstruct import *
from tools.ML import *
#---------------------------------------------|
# OPTIONS
#--------------------------------------------/
from analyzeOptions import *
# rePickle single arrays
rePickle = False
if(rePickle):
    regenerateGlobalPickle(False)
    regenerateMLPickle(True)
    regenerateLocalPickle(False)

# createDatabase
createDatabase = False
#KNN
use_KNN = True # also needed for reconstruction
reKNN = False
PCA = False
# visualization
vis = False
# ML processing
ML_SPLIT_FRACTION = 0.75
Options.knn_neighbors = 4
# Reconstruction
remake_listmode = False
# Filepaths
# Options.ml_database_pkl = Options.datadir+'ML_DATABASE_PICKLE_P'+str(Options.photoLen)+'.pkl'
# Options.ml_run_pkl = Options.datadir+'ML_RUN_PICKLE_P'+str(Options.photoLen)+'.pkl'
# Options.knn_pkl = Options.datadir+'ML_OUT_PICKLE_P'+str(Options.photoLen)+'.pkl'
#---------------------------------------------|
# from tools.ML import *
with open('tools/ML/ML.py') as f: exec(f.read())
with open(Options.ML_PATH+'ML_detRes.py') as f: exec(f.read())
model_path = str(Options.ML_PATH)+"Data/ML_DET_RES_KNN_"+str(Options.photoLen)+"_Photo.pt"
# with open('analyzeOptions.py') as f: exec(f.read())
Options.COMPLETEDETECTOR = True
Options.MaxEventLimit = False
Options.ReflectionTest = False
Options.SiPM_Based_Reconstruction = False
Options.Process_Based_Breakdown = False
#---------------------------------------------|
# dataOpen = True
# with open('tools/data.py') as f: exec(f.read())
#--------------------------------------------/
# Pickling Individual Arrays:
#--------------------------------------------|
if rePickle:
    # Options.regenerateLocalPickles = True
    for ArrayNumber in tqdm(range(nArray)):
        print(ArrayNumber)
        Options.ArrayNumber = ArrayNumber
        with open('analyzeSingleArray.py') as f: exec(f.read())
#--------------------------------------------\
if createDatabase:
    # Read In Data
    inputTensorL = []
    expectTensorL = []
    ArrayIDTensorL = []
    EventIDTensorL = []
    for ArrayNumber in (range(nArray)):
        ml_pkl = Options.datadir+'ML_DATA_PICKLE_AR'+str(ArrayNumber)+'_P'+str(Options.photoLen)+'.pkl'
        with open(ml_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            inptTensor,expTensor,eventIDs = pickle.load(f)
            inputTensorL.append(inptTensor)
            expectTensorL.append(expTensor)
            ArrayIDTensorL.append(torch.Tensor([ArrayNumber]*(len(inptTensor))))
            EventIDTensorL.append(torch.Tensor(eventIDs))
    inputTensor = torch.cat(inputTensorL, dim=0)
    expectTensor = torch.cat(expectTensorL, dim=0)
    ArrayIDTensor = torch.cat(ArrayIDTensorL, dim=0)
    EventIDTensor = torch.cat(EventIDTensorL, dim=0)
    # print(inputTensor.shape)
    # print(expectTensor.shape)
    # print(ArrayIDTensor)
    #--------------------------------------------\
    if PCA:
        PATH_OPT=PATH_OPT+"PCA"
        pcaSTD = False
        pcaMAHA = False
        with open(Options.ML_PATH+'ML_PCA.py') as f: exec(f.read())
    #--------------------------------------------\
    # Get Random 75% split...
    length = len(ArrayIDTensor)
    splitList = [int(length*ML_SPLIT_FRACTION),length - int(length*ML_SPLIT_FRACTION)]
    listset = list(range(length))
    random.shuffle(listset)
    dataInd,testInd = torch.split(torch.tensor(listset),splitList)
    #---------------------------------------------
    dataTensorX = inputTensor[dataInd]
    dataTensorXT = inputTensor[testInd]
    dataTensorY = expectTensor[dataInd]
    dataTensorYT = expectTensor[testInd]
    arrayIndexTensorT = ArrayIDTensor[testInd]
    eventIndexTensorT = EventIDTensor[testInd]
    #---------------------------------------------
    # Pickle Again...
    with open(Options.ml_database_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([dataTensorX,dataTensorY], f)
    with open(Options.ml_run_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT], f)
#------------------------------------------------------------------------------|
# Load Pickles
#------------------------------------------------------------------------------/
if use_KNN:
    try: dataTensorXT
    except: 
        with open(Options.ml_database_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            dataTensorX,dataTensorY = pickle.load(f)
        with open(Options.ml_run_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT = pickle.load(f)
    Options.nEvents = len(dataTensorY)+len(dataTensorYT)
    print("nEvents:", Options.nEvents)
    #--------------------------------------------/
    try:
        if(reKNN):
            raise FileNotFoundError('[NotAnERROR] Regenerating KNN output')
        with open(Options.knn_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            print("[OPENING]")
            out,outs = pickle.load(f)
    except FileNotFoundError as VALERIN:
        print(VALERIN)
        print("[REGENERATION] KNN Pickling...")
        #Model Definition:
        try: KNNOPENED
        except: KNNOPENED = False
        if not (KNNOPENED):
            with open(Options.ML_PATH+'ML_Model_detRes_KNN.py') as f: exec(f.read()) # helper file # model definition
            KNNOPENED = True
        drnet = DRKNN()
        drnet.eval()
        drnet._initialize_weights()
        print(drnet)
        #--------------------------------------------
        # Run Options.KNN (note out is xyzt of gamma)
        drnet.setK(Options.knn_neighbors)
        out,outs = drnet(dataTensorX,dataTensorY,dataTensorXT)
        with open(Options.knn_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([out,outs], f)

    ml_detRes_vis(out,dataTensorYT,Options.knn_neighbors)
    ml_detRes_vis2(out,dataTensorYT,Options.knn_neighbors)
#--------------------------------------------
if vis:
    with open(Options.ML_PATH+"ML_KNN_Functions.py") as f: exec(f.read())
    kvisNP(10,dataTensorY,dataTensorYT,out,outs,Options.knn_neighbors)
#--------------------------------------------
#calculate gamma global reco position by event id
try:
    if remake_listmode:
        raise FileNotFoundError('[NotAnERROR] Regenerating LISTMODE output')
    with open(Options.renderaddinfo_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
        Options.nRTotalEvents,Options.nREvents,Options.nREventLimit = pickle.load(f)
except FileNotFoundError as VALERIN:
    print(VALERIN)
    print("[REGENERATION] LISTMODE output")
    for i in range(5):
        print(out[i],arrayIndexTensorT[i],eventIndexTensorT[i])
    outGlobal = ArrayToGlobalMT(out,arrayIndexTensorT)
    outGlobal[:,3] = (outGlobal[:,3]*n_EJ208)/(1000*nanosec*c_const)
    indxs = []
    outPaired = []
    for i in range(Options.nEvents):
        idx = np.where(eventIndexTensorT==i)[0].astype(int)
        if len(idx) > 0:
            indxs.append(idx)
        if len(idx) > 1:
            outPaired.append(outGlobal[idx])
    indxs = np.array(indxs)
    print(len(indxs))
    # print(len([i for i in range(len(indxs)) if len(indxs[i]) > 1]))
    print(len(outPaired))
    print(indxs)
    print(outPaired[0][:,0:3].T)
    #----------------------------------------------
    Options.nRTotalEvents = len(indxs)
    Options.nREvents = len(outPaired)
    Options.nREventLimit = Options.nREvents
    lor = np.zeros(shape=(8,Options.nREvents))

    fig = plt.figure(figsize=(8,8))
    ax = plt.axes(projection='3d')
    for i in range(Options.nREvents):
        event = outPaired[i]
        A = event[:,0:4].T
        lor[0:4,i] = event[0,0:4]
        lor[4:8,i] = event[1,0:4]
        ax.plot3D(A[0,:],A[1,:],A[2,:])
    plt.savefig(Options.plotDIR+"renderLOR.jpg",dpi=600)
    np.savetxt(Options.datadir+"pointdata.txt",lor)
    with open(Options.renderaddinfo_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([Options.nRTotalEvents,Options.nREvents,Options.nREventLimit], f)
#_-----------------------------------
# plot reconstructed 3d image
from recvis.render import render
render()
