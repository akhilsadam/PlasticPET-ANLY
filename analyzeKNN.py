#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math
import os
import io

from torch.utils import data
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
from functools import lru_cache
from scipy import stats
from scipy import signal
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline
import tqdm
import multiprocessing
import cv2
import sys
import matplotlib.pyplot as plt
from tools.dimensions import *
from tools.geo import *
from tools.reconstruct import *
from tools.ML.ML import *
import random
import gc
ngpu = 1
#---------------------------------------------|
# OPTIONS
#--------------------------------------------/
from analyzeOptions import *
#---------------------------------------------
# Constructing ML stuff / Rendering ? - i.e. are we just doing single array studies?
try: ML_Construct
except: ML_Construct = True
# Turns on all of the following if this is a first run / or we have additonal data.
try: newData
except: newData = True
ML_rePickle = newData # do we need to make ML pickles (singles)?
recreateDatabase = newData # make the database again
try: defaultDatabase
except: defaultDatabase = False # use data from another run as training data
unsafe_vis = False # this
#--------------------------------------------- 
# rePickle single arrays
regenerateGlobalPickle(newData)
regenerateMLPickle(ML_rePickle) #turn this off if doing single array analysis
regenerateLocalPickle(newData)

rePickle = (newData or ML_rePickle)
# createDatabase
# if not Options.TACC:
#     recreateDatabase = False
# else:
#---------------------------------------------
#KNN
try: use_KNN # also needed for reconstruction
except: use_KNN = True 
reKNN = True
PCA = False
# visualization
vis = False
mem_intense_vis = False
# ML processing
ML_SPLIT_FRACTION = 0.75
Options.knn_neighbors = 4
# Reconstruction
try: remake_listmode
except: remake_listmode = True
# opt
try: database_test_plot
except: database_test_plot = False
if database_test_plot:
    recreateDatabase = True
    defaultDatabase = False
try: center_source
except: center_source = False
#------------------------------------------------
# Filepaths
# Options.ml_database_pkl = Options.datadir+'ML_DATABASE_PICKLE_P'+str(Options.photoLen)+'.pkl'
# Options.ml_default_database_pkl = Options.defaultdatadir +'ML_DATABASE_PICKLE_P'+str(Options.photoLen)+'.pkl'
# Options.ml_run_pkl = Options.datadir+'ML_RUN_PICKLE_P'+str(Options.photoLen)+'.pkl'
# Options.knn_pkl = Options.datadir+'ML_OUT_PICKLE_P'+str(Options.photoLen)+'.pkl'
#---------------------------------------------|
# from tools.ML import *
with open('tools/ML/ML.py') as f: exec(f.read())
with open(Options.ML_PATH+'ML_detRes.py') as f: exec(f.read())
model_path = str(Options.ML_PATH)+"Data/ML_DET_RES_KNN_"+str(Options.photoLen)+"_Photo.pt"
# with open('analyzeOptions.py') as f: exec(f.read())
Options.COMPLETEDETECTOR = True
Options.MaxEventLimit = True
Options.MaxEvents = 200
Options.ReflectionTest = False
Options.SiPM_Based_Reconstruction = False
Options.Process_Based_Breakdown = False
Options.STRIPHIST = False # already set by default, just in case
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
if not ML_Construct:
    Options.ArrayNumber = 0
    dataOpen = False
    Options.Process_Based_Breakdown = True
    Options.STRIPHIST = True
    Options.STRIP_OPT = ["process_breakdown","electron_processes","singles"]
    with open('analyzeSingleArray.py') as f: exec(f.read())
    Options.STRIP_OPT = ["process_breakdown","electron_processes"]
    with open('analyzeSingleArray.py') as f: exec(f.read())
    Options.Process_Based_Breakdown = False
    Options.MaxEventLimit = True
    Options.MaxEvents = 10000
    Options.STRIP_OPT = ["DOI"]
    with open('analyzeSingleArray.py') as f: exec(f.read())
else:
    #--------------------------------------------\
    if use_KNN:
        try: 
            if recreateDatabase:
                raise FileNotFoundError('[NotAnERROR] Regenerating KNN Database')
            if defaultDatabase:
                with open(Options.ml_default_database_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
                    dataTensorX,dataTensorY = pickle.load(f)
                with open(Options.ml_complete_run_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
                    dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT = pickle.load(f)
            else:
                with open(Options.ml_database_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
                    dataTensorX,dataTensorY = pickle.load(f)
                with open(Options.ml_run_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
                    dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT = pickle.load(f)
        except FileNotFoundError as VALERIN:
            print(VALERIN)
            print("[REGENERATION] KNN Database Pickling...")
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
            if not defaultDatabase:
                # Get Random 75% split... NEED TO SORT BY EVENT NOT OTHERWISE!!!

                length = len(np.unique(EventIDTensor.numpy()))
                print(length)
                splitList = [int(length*ML_SPLIT_FRACTION),length - int(length*ML_SPLIT_FRACTION)]
                listset = list(range(length))
                random.shuffle(listset)
                dataIndE,testIndE = torch.split(torch.tensor(listset),splitList)
                dataInd = np.isin(EventIDTensor.numpy(),EventIDTensor.numpy()[dataIndE])
                testInd = np.isin(EventIDTensor.numpy(),EventIDTensor.numpy()[testIndE])
                print(inputTensor.shape)
                print(dataInd)

                # length = len(ArrayIDTensor)
                # splitList = [int(length*ML_SPLIT_FRACTION),length - int(length*ML_SPLIT_FRACTION)]
                # listset = list(range(length))
                # random.shuffle(listset)
                # dataInd,testInd = torch.split(torch.tensor(listset),splitList)

                #---------------------------------------------
                dataTensorX = inputTensor[dataInd]
                dataTensorXT = inputTensor[testInd]
                dataTensorY = expectTensor[dataInd]
                dataTensorYT = expectTensor[testInd]
                arrayIndexTensorT = ArrayIDTensor[testInd]
                eventIndexTensorT = EventIDTensor[testInd]
                if database_test_plot:
                    arrayIndexTensorD = ArrayIDTensor[dataInd]
                    eventIndexTensorD = EventIDTensor[dataInd]
                #---------------------------------------------
                # Pickle Again...
                with open(Options.ml_database_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
                    pickle.dump([dataTensorX,dataTensorY], f)
                with open(Options.ml_run_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
                    pickle.dump([dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT], f)
                with open(Options.ml_database_test_pkl, 'wb') as f:
                    pickle.dump([arrayIndexTensorD,eventIndexTensorD],f)
            else:
                with open(Options.ml_default_database_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
                    dataTensorX,dataTensorY = pickle.load(f)
                dataTensorXT = inputTensor
                dataTensorYT = expectTensor
                arrayIndexTensorT = ArrayIDTensor
                eventIndexTensorT = EventIDTensor
                #---------------------------------------------
                with open(Options.ml_complete_run_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
                    pickle.dump([dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT], f)
    #------------------------------------------------------------------------------|
    # KNN
    #------------------------------------------------------------------------------/
    gc.collect()
    if use_KNN:
        #--------------------------------------------/
        gc.collect()
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
            gc.collect()    
            drnet = DRKNN()
            gc.collect()
            drnet.eval()
            drnet._initialize_weights()
            print(drnet)
            #--------------------------------------------
            # Run Options.KNN (note out is xyzt of gamma)
            drnet.setK(Options.knn_neighbors)
            gc.collect()
            out,outs = drnet(dataTensorX,dataTensorY,dataTensorXT)
            if database_test_plot:
                out = dataTensorY
                with open(Options.ml_database_test_pkl, 'rb') as f:
                    arrayIndexTensorT,eventIndexTensorT = pickle.load(f)

            with open(Options.knn_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
                pickle.dump([out,outs], f)
        if not database_test_plot:
            ml_detRes_vis(out,dataTensorYT,Options.knn_neighbors)
            ml_detRes_vis2(out,dataTensorYT,Options.knn_neighbors)
    #--------------------------------------------
    if mem_intense_vis:
        print("memory_intensive_vis")
        with open(Options.ML_PATH+"ML_KNN_Functions.py") as f: exec(f.read())
        kvisNP(10,dataTensorY,dataTensorYT,out,outs,Options.knn_neighbors)
    #--------------------------------------------
    #calculate gamma global reco position by event id
    try:
        if remake_listmode:
            raise FileNotFoundError('[NotAnERROR] Regenerating LISTMODE output')
        with open(Options.renderaddinfo_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
            Options.nRTotalEvents,Options.nREvents,Options.nREventLimit,Options.TOTALEVENTS,Options.SOURCE = pickle.load(f)
    except (FileNotFoundError,ValueError) as VALERIN:
        print(VALERIN)
        print("[REGENERATION] LISTMODE output")
        print("Number of Single Events From KNN: ",len(out))
        print("Approximate Number of Total Single Events: ",4*len(out))

        with open(Options.datadir + Options.electronpath,"r") as f:
        #     Options.TOTALEVENTS = len(f.readlines())
            if Options.MaxEventLimit:
                Options.TOTALEVENTS = min(Options.MaxEvents,len(f.readlines()))
            else:
                Options.TOTALEVENTS = len(f.readlines())

        try: Options.SOURCE
        except: 
            if center_source:
                Options.SOURCE = np.array([0,0,500])
            else:
                Options.SOURCE = np.array([np.nan,np.nan,np.nan])

        for i in range(5):
            print(out[i],arrayIndexTensorT[i],eventIndexTensorT[i])
        outGlobal = ArrayToGlobalMT(out,arrayIndexTensorT)
        outGlobal[:,3] = (outGlobal[:,3]*n_EJ208)/(1000*nanosec*c_const)
        indxs = []
        outPaired = []
        maxEVT = int(max(eventIndexTensorT).item())
        for i in range(maxEVT+1):
            idx = np.where(eventIndexTensorT==i)[0].astype(int)
            if len(idx) > 0:
                indxs.append(idx)
            if len(idx) > 1:
                outPaired.append(outGlobal[idx])
        indxs = np.array(indxs)
        print("Number of KNN Events that are atleast Singles: ",len(indxs))
        # print(len([i for i in range(len(indxs)) if len(indxs[i]) > 1]))
        print("Number of KNN Events that are atleast Coincidence: ",len(outPaired))
        # print(indxs)
        # print(outPaired[0][:,0:3].T)
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
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_zlabel("Z")
        if defaultDatabase:
            plt.savefig(Options.plotDIR+"renderLOR_OOC.jpg",dpi=600)
        else:
            plt.savefig(Options.plotDIR+"renderLOR.jpg",dpi=600)
        np.savetxt(Options.datadir+"pointdata.txt",lor)
        with open(Options.renderaddinfo_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
            pickle.dump([Options.nRTotalEvents,Options.nREvents,Options.nREventLimit,Options.TOTALEVENTS,Options.SOURCE], f)
    #_-----------------------------------
    # plot reconstructed 3d image
    from recvis.render import render
    SPATIALRESOLUTION,SENSITIVITY,SCATTERFRACTION = render(defaultDatabase,database_test_plot)
    SPATIALRESOLUTION_X,SPATIALRESOLUTION_Y,SPATIALRESOLUTION_Z= SPATIALRESOLUTION
