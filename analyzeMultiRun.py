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
#
#
# For general run metrics; will create plots based upon the variables used in the filenames!
# At present only supports exactly two axes!
#-------------------------------------------------------
from tools.finite import *
#-------------------------------------------------------
#photoLen=5
filenames=join(["BounceTime1_"],["0","1","2","3"])
#filenames=join(["datacollectionruns/noroughend_"],["12vk_12ej","12vk_2ej","2vk_2ej"])
GeneralPlots = False
title="SigmaAlphaStudies"
yvars = ["ENERGYRESOLUTION","PHOTOPEAK_SHARPNESS","PHOTOPEAK_FWHM","PHOTOPEAK_COUNT","PHOTOPEAK_PROPORTION"]
#-------------------------------------------------------
datadirs=tuplejoin(["../data/"],filenames,["/"])
plotdirs=tuplejoin(["../plot/"],filenames,["/"])
multidatadir = "../data/"+title+"/"
multiplotdir = "../plot/"+title+"/"
#-------------------------------------------------------
NRuns = len(datadirs)
if GeneralPlots:
    try: os.makedirs(multidatadir)
    except: pass
    try: os.makedirs(multiplotdir)
    except: pass

    nfeat = len(yvars)

    MODE="AUTOMATIC"

    df = pd.DataFrame()
    xvars = []

    try: df=pd.read_csv(multidatadir+"data.csv")
    except:
        for i in tqdm(range(NRuns)):
            plotDIR=plotdirs[i]
            datadir=datadirs[i]

            infoFile = open(plotDIR+"info.txt")
            line = pd.Series(infoFile.readline().rstrip('\n').split(' '))
            keyargs = '-D'
            args = line[line.str.contains('|'.join([keyargs]))].tolist()
            args = [arg.replace(keyargs,"",1) for arg in args]

            row=dict()
            for arg in args:
                var,val=arg.split('=')
                row[var]=float(val)
                if var not in xvars:
                    xvars.append(var)

            with open('analyze.py') as f: exec(f.read()) # helper file

            for yvar in yvars:
                try: row[yvar]=eval(yvar)
                except: row[yvar] = np.nan

            df=df.append(pd.DataFrame(data=row,index=[i]),ignore_index=False)
        df.to_csv(multidatadir+"data.csv",header=True)
        #print(df)
    else:
        xvars = [name for name in df.columns if (name not in yvars) and ("Unnamed" not in name)]
        print(xvars)
    #--------------------------------------------------------------------
    cmap="nipy_spectral"
    dpi=600
    for yvar in yvars:
        fig,ax = plt.subplots(figsize=(5,5),tight_layout=True)
        plot = ax.scatter(df[xvars[0]],df[xvars[1]],c=df[yvar],cmap=cmap)
        ax.set_xlabel(xvars[0])
        ax.set_ylabel(xvars[1])
        ax.set_aspect(1)
        ax.set_title(title+":"+yvar)
        plt.colorbar(plot)
        plt.savefig(multiplotdir+yvar+".jpg",dpi=dpi)
        plt.close()
else:
    for i in tqdm(range(NRuns)):
        plotDIR=plotdirs[i]
        try: os.makedirs(plotDIR)
        except: pass
        datadir=datadirs[i]
        with open('analyzeSingleArray.py') as f: exec(f.read()) # helper file
