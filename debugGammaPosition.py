import math

from iminuit.minuit import Minuit
from analyzeOptions import Options
import pickle
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from tools.dimensions import *
from scipy import stats

#// ASSUMING GAMMA FIRED FROM CENTER (central point source!)
centre = np.array([0,0,500])

with open(Options.datadir+'beamInteraction.pkl', 'rb') as f:  # Python 3: open(..., 'wb')
    print("[OPENING]")
    evtPhotoInteractG, evtComptonInteractG,evtInteractG = pickle.load(f)

#//---------\\ BeamData // position and direction of fired gamma
beamData = np.load(Options.datadir+"beamData.npy")
evtPos = beamData[:,0,:] # - first index is event #
evtDir = beamData[:,1,:]


error_R =[]
error_T =[]
error_Z =[]

bad_evt = 0
geo_failed_evt = 0
unnatural = 0
total_evt = int(len(beamData)/2)

for i in tqdm(range(total_evt)):

    directAX = evtDir[i] # R
    direct = np.array([directAX[0],directAX[1],0]) #Rxy
    el = evtInteractG[i] #evt interactions
    print(el)

    if len(el) > 0:

        mask = [el[:,5] == gammaID for gammaID in range(3)]

        trueInt = [gammaID for gammaID in range(3) if np.sum(el[mask[gammaID],3],axis=0)>0]

        n_Gamma = len(trueInt)

        if n_Gamma <= 0:
            geo_failed_evt+=1
        else :

            means = np.array([np.mean(el[mask[gammaID],0:3] - centre,axis=0) for gammaID in trueInt])
            # print(means)
            # print(direct)
            directed_Lxy = np.linalg.norm(direct)

            stdxyzs = np.array([np.std(el[mask[gammaID],0:3],axis=0) for gammaID in trueInt])

            eL = np.linalg.norm(stdxyzs,axis=1)
            er = np.abs(np.dot(stdxyzs,direct))
            ez = stdxyzs[:,2]

            error_Tv = np.sqrt(eL**2 - er**2 - ez**2)
            # print(error_Tv)
            # print(means)
            # print(eL)
            # print(er)
            # print(ez)
            # print(directed_L)


            if np.nan not in error_Tv:
                error_R.extend(er)        
                error_T.extend(error_Tv)
                error_Z.extend(ez)
            else:
                bad_evt +=1
                unnatural +=1
    else:
        bad_evt+=1
        unnatural+=1

print(np.mean(error_R),np.mean(error_T),np.mean(error_Z))
print("Bad Counting loss: ",bad_evt/total_evt)
print("Lost due to Geo: ",geo_failed_evt/total_evt)
print("[SUCCESS]:",unnatural==0)

guess = [[0,10],[0,10],[0,5]]
limit = [50,50,50]
displayBinsMM = np.array([0.5,0.5,5])#*0.25
axes = ["Radial Error (Depth/Width) ","Transverse Error (arc-length) ","Axial Error (Z) "]
# fig, axs = plt.subplots(3)
# for i in range(3):
# 	axs[i].hist(errorPosIN[:,i],bins=200)
# plt.savefig(Options.plotDIR+"test.png")
# plt.close()
errorPos = [error_R,error_T,error_Z]
fig, axs = plt.subplots(3)
for i in range(3):
    errorPosI = errorPos[i]
    # errorPosI = errorPosI[np.isfinite(errorPosI)]
    print("-------------------\n" ,i,"- axis events: ",len(errorPosI))

    xmin,xmax = 0,limit[i]
    axs[i].set_xlim(xmin/2,xmax/2)
    nbins = len(errorPosI)
    dbins = int(L[i]/displayBinsMM[i])#8*int(2*U[i]/10)
    axs[i].hist(errorPosI,bins = dbins, range = (xmin,xmax), density=False)	
    hist, bin_edges = np.histogram(errorPosI,bins=np.arange(xmin,xmax,L[i]/nbins))
    ###hist = hist*nbins/(len(errorPosI)*(xmax-xmin)) #- enable if density=true
    hist = (nbins/dbins)*len(errorPosI)*hist/np.sum(hist)
    # print(np.sum(hist)*(L[i]/nbins))
    # bins = bin_edges[0:(len(bin_edges)-1)] + 0.5*(L[i]/nbins)

    # lnspc = np.linspace(xmin,xmax,len(hist))
    # def pdf(x,m,s):
    #     ###return	(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2)) #- enable if density=true
    #     return	(nbins/dbins)*len(errorPosI)*(L[i]/nbins)*(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2))
    # def spdf(x,df,scale):
    #     return (len(errorPosI)*(L[i]/dbins))*stats.t.pdf(x,df,0,scale)
    # def fcn(m,s):
    #     return np.sum(np.power((hist-pdf(bins,m,s)),2))
    # def sfcn(df,scale):
    #     return np.sum(np.power((hist-spdf(bins,df,scale)),2))
    # fcn.errordef = Minuit.LEAST_SQUARES
    # sfcn.errordef = Minuit.LEAST_SQUARES

    # param = guess[i]
    # m=Minuit(fcn,param[0],param[1])
    # m.migrad()
    # param = m.values
    # pdf_g = pdf(lnspc,param[0],param[1])
    # axs[i].plot(lnspc, pdf_g, label = 'Norm')

    # axs[i].text(0.01, 0.99, "Total Events = %1.0f " %(total_evt),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
    # axs[i].text(0.01, 0.79, "Interacted Events = %1.0f " %(total_evt-geo_failed_evt),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
    # axs[i].text(0.01, 0.19, "Bin Size = %1.2f mm" %(displayBinsMM[i]),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)

    axs[i].text(0.99, 0.99, "Mean = %4.2f mm" %(np.mean(errorPosI)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
    axs[i].text(0.99, 0.79, "STD = %4.2f mm" %(np.std(errorPosI)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
    axs[i].text(0.99, 0.59, "FWHM = %4.2f mm" %(FWHM*np.std(errorPosI)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
    # axs[i].text(0.99, 0.39, "Error = +-%4.2f mm" %(0.5*FWHM*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
    # axs[i].text(0.99, 0.19, "RSQ = %1.2f" %(RSQ(hist,pdf_g)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)

    axs[i].set_title(axes[i])

    # print("MU  =", param[0])
    # print("STD =", param[1])
    # print("FWHM =", FWHM*param[1]," mm")
    # print("Error = +-", 0.5*FWHM*param[1]," mm")
plt.tight_layout()
plt.savefig(Options.plotDIR+'debug_Gamma_position.png')
plt.show()