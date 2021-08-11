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
#---------------------------------------------|
# OPTIONS
#--------------------------------------------/
from analyzeOptions import *
# rePickle single arrays
rePickle = False
# createDatabase
createDatabase = True
PCA = False
# visualization
vis = True
# ML processing
ML_SPLIT_FRACTION = 0.75
knn_neighbors = 4
# Filepaths
ml_database_pkl = datadir+'ML_DATABASE_PICKLE_P'+str(photoLen)+'.pkl'
ml_run_pkl = datadir+'ML_RUN_PICKLE_P'+str(photoLen)+'.pkl'
#---------------------------------------------|
# from tools.ML import *
with open('tools/ML/ML.py') as f: exec(f.read())
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read())
model_path = str(ML_PATH)+"Data/ML_DET_RES_KNN_"+str(photoLen)+"_Photo.pt"
# with open('analyzeOptions.py') as f: exec(f.read())
COMPLETEDETECTOR = True
datadir = "../data/current/"
MaxEventLimit = False
ReflectionTest = False
SiPM_Based_Reconstruction = False
Process_Based_Breakdown = False
#---------------------------------------------|
# dataOpen = True
# with open('tools/data.py') as f: exec(f.read())
#--------------------------------------------/
# Pickling Individual Arrays:
#--------------------------------------------|
if rePickle:
    KVIS = "PICKLE"
    regenerateMLPickles = True
    regeneratePickles = True
    for ArrayNumber in tqdm(range(nArray)):
        print(ArrayNumber)
        with open('analyzeSingleArray.py') as f: exec(f.read())
#--------------------------------------------\
if createDatabase:
    # Read In Data
    inputTensorL = []
    expectTensorL = []
    ArrayIDTensorL = []
    EventIDTensorL = []
    for ArrayNumber in (range(nArray)):
        ml_pkl = datadir+'ML_DATA_PICKLE_AR'+str(ArrayNumber)+'_P'+str(photoLen)+'.pkl'
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
        with open(ML_PATH+'ML_PCA.py') as f: exec(f.read())
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
    with open(ml_database_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([dataTensorX,dataTensorY], f)
    with open(ml_run_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump([dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT], f)
#------------------------------------------------------------------------------|
# Load Pickles
#------------------------------------------------------------------------------/
try: dataTensorXT
except: 
    with open(ml_database_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
        dataTensorX,dataTensorY = pickle.load(f)
    with open(ml_run_pkl, 'rb') as f:  # Python 3: open(..., 'wb')
        dataTensorXT,dataTensorYT,arrayIndexTensorT,eventIndexTensorT = pickle.load(f)
#--------------------------------------------/
#Model Definition:
try: KNNOPENED
except: KNNOPENED = False
if(KNNOPENED):
	pass
else:
	with open(ML_PATH+'ML_Model_detRes_KNN.py') as f: exec(f.read()) # helper file # model definition
	KNNOPENED = True
drnet = DRKNN()
drnet.eval()
drnet._initialize_weights()
print(drnet)
#--------------------------------------------
# Run KNN (note out is xyzt of gamma)
drnet.setK(knn_neighbors)
out,outs = drnet(dataTensorX,dataTensorY,dataTensorXT)
ml_detRes_vis(out,dataTensorYT,knn_neighbors)
ml_detRes_vis2(out,dataTensorYT,knn_neighbors)
#--------------------------------------------
if vis == True :
    with open(ML_PATH+"ML_KNN_Functions.py") as f: exec(f.read())
    kvisNP(10,dataTensorY,dataTensorYT,out,outs,knn_neighbors)
#--------------------------------------------
sorted, indices = torch.sort()
