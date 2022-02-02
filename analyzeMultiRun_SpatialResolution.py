#!/usr/bin/env python3
from pickle import TRUE
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
from analyzeOptions import *
#
#
# For general run metrics; will create plots based upon the variables used in the filenames!
# At present only supports exactly two axes!
#-------------------------------------------------------
from tools.finite import *
#-------------------------------------------------------
#photoLen=5
filenames=join(["database_radial"],["0"])#join(["spatialR_V2_"],["0"])#"0","1","2","3","4","5",,"7"["brain"] 
#filenames=join(["datacollectionruns/noroughend_"],["12vk_12ej","12vk_2ej","2vk_2ej"])
GeneralPlots = True
render_only = True
remake_dataframe =  True
database_test_plot = True
title="spatialR_V2"
xvars = ["xshift","zshift"]
yvars = ["SPATIALRESOLUTION_X","SPATIALRESOLUTION_Y","SPATIALRESOLUTION_Z","SENSITIVITY","SCATTERFRACTION"]
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

    try: 
        if remake_dataframe:
            raise FileNotFoundError('[NotAnERROR] Regenerating DATAFRAME')
        df=pd.read_csv(multidatadir+"data.csv")
    except:
        df = pd.DataFrame()
        keyargs = '-D'
        for i in tqdm(range(NRuns)):
            Options.plotDIR=plotdirs[i]
            Options.datadir=datadirs[i]

            infoFile = open(Options.plotDIR+"info.txt")
            line = pd.Series(infoFile.readline().rstrip('\n').split(' '))
            args = line[line.str.contains('|'.join([keyargs]))].tolist()
            args = [arg.replace(keyargs,"",1) for arg in args]

            row = {}
            for arg in args:
                if '=' in arg:
                    var,val=arg.split('=')
                else:
                    var = arg
                    val = 1
                row[var]=float(val)
                if var not in xvars:
                    xvars.append(var)

            x_src = row.get(xvars[0], 0)
            if x_src == 0:
                row[xvars[0]] = x_src
            z_src = row.get(xvars[1], 0)
            if z_src == 0:
                row[xvars[1]] = z_src
            Options.SOURCE = np.array([x_src,0,z_src])

            regenNames()
            with open('analyzeComplete.py') as f: exec(f.read()) # helper file

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
    cmap="winter"
    dpi=600
    for yvar in yvars:
        fig,ax = plt.subplots(figsize=(5,5),tight_layout=True)
        plot = ax.scatter(df['xshift'],df['zshift'],c=df[yvar],cmap=cmap)
        ax.set_xlabel('xshift [mm]')
        ax.set_ylabel('zshift [mm]')
        #ax.set_aspect(1)
        ax.set_title(title+":"+yvar)
        plt.colorbar(plot)
        plt.savefig(multiplotdir+yvar+".jpg",dpi=dpi)
        plt.close()
else:
    for i in tqdm(range(NRuns)):
        Options.plotDIR=plotdirs[i]
        try: os.makedirs(Options.plotDIR)
        except: pass
        Options.datadir=datadirs[i]
        with open('analyzeComplete.py') as f: exec(f.read()) # helper file
