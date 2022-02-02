import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
from analyzeOptions import *
from tools.dimensions import *
from tools.geo import *
import pickle
import os
def render(OOCDataset=False,database_test_plot=False):
    p = np.loadtxt(Options.datadir+"pointdata.txt")
    try:
        with open(Options.renderaddinfo_pkl, 'rb') as f:  # Python 3: open(..., 'rb')
            print("OPENING")
            a,b,c,d,e = pickle.load(f)
    except:
        a,b,c = blenderOptions.maxVert,blenderOptions.maxVert,blenderOptions.maxVert
        d = 1
        e = np.array([0,0,0])
        print("FAILED TO OPEN PICKLE; Name : RenderAdditionalInformation")
    Options.nRTotalEvents,Options.nREvents,Options.nREventLimit,Options.TOTALEVENTS,Options.SOURCE = a,b,c,d,e

    det = np.array([
        np.array([
            ArrayToGlobalCoordinates(0, 0, 0, A),
            ArrayToGlobalCoordinates(0, 0, LZ, A),
        ]).T
        for A in range(nArray)
    ])

    dt = (p[3]-p[7]) # ns->ps (does not work with PETSYS - they give picoseconds)
    dx = tof_const*dt#mm
    center = np.array([(p[0,:]+p[4,:])/2, (p[1,:]+p[5,:])/2, (p[2,:]+p[6,:])/2])
    line = -np.array(((p[0,:]-p[4,:]), (p[1,:]-p[5,:]), (p[2,:]-p[6,:])))
    shift = dx*line/(np.linalg.norm(line,axis=0))
    point = center+shift

    delta = point - np.reshape(np.repeat(np.array([Options.SOURCE[0],0,Options.SOURCE[1]+UZ]),point.shape[1]),point.shape)
    print("Source-position:",Options.SOURCE)
    if np.nan not in Options.SOURCE:
        SPATIALRESOLUTION = np.std(delta,axis=1)*FWHM
    else:
        SPATIALRESOLUTION = np.array([-1,-1,-1])
    print("SR",SPATIALRESOLUTION)
    print("SR_noshift_STD",np.std(point,axis=1))
    print("P",p.T[0:5])
    print("T",dt)
    print("DX",dx)
    print("line",(line/np.linalg.norm(line,axis=0)).T)
    print("shift",shift.T)
    delta2 = center - np.reshape(np.repeat(np.array([Options.SOURCE[0],0,Options.SOURCE[1]+UZ]),point.shape[1]),point.shape)
    print("POINT_error",np.linalg.norm(delta,axis=0))
    print("Center_error",np.linalg.norm(delta2,axis=0))
    SENSITIVITY = Options.nREvents/Options.TOTALEVENTS #absolute
    SCATTERFRACTION = -1 #NOT YET IMPLEMENTED!!!!!!!

    np.savetxt(Options.datadir+"reco_pointdata.txt",point)

    xyz = point[:,0:Options.nREventLimit]

    with open(Options.render_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(xyz, f)

    xy = np.vstack([xyz[0],xyz[2],xyz[1]])
    z = gaussian_kde(xy)(xy)
    #ax1.scatter(b, data["CTR"], c=z, s=16, cmap = "nipy_spectral")

    # fig = plt.figure(figsize=(12,12))
    # ax = fig.add_subplot(111, projection='3d')
    lim = np.array([[-UZ,UZ],[-UZ,UZ],[0,LZ]])
    labels = ["Radial - X","Radial - Y","Z - Length"]

    fig = plt.figure(figsize = (28,12),constrained_layout=True)
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    ax = [ax1,ax2]
    for i in tqdm(range(2)):
        img = ax[i].scatter(xyz[i%3],xyz[(i+1)%3],xyz[(i+2)%3], c=z,s=2,alpha = 0.7,cmap="rainbow")
        ax[i].set_xlim(lim[i%3,0],lim[i%3,1])
        ax[i].set_ylim(lim[(i+1)%3,0],lim[(i+1)%3,1])
        ax[i].set_zlim(lim[(i+2)%3,0],lim[(i+2)%3,1])
        ax[i].set_xlabel(labels[i%3])
        ax[i].set_ylabel(labels[(i+1)%3])
        ax[i].set_zlabel(labels[(i+2)%3])
        ax[i].set_box_aspect((1,1,1))
        for A in range(nArray):
            detpoint = det[A]
            # print(detpoint)
            ax[i].plot(detpoint[i%3,:],detpoint[(i+1)%3,:],detpoint[(i+2)%3,:],c='b',linestyle='-.',alpha = 0.5)
    cax = plt.axes([0.4875, 0.1, 0.025, 0.8])
    cbar = plt.colorbar(img,cax=cax)
    cbar.set_alpha(1)
    cbar.draw_all()
    plt.figtext(0.45,0.96,'Total Single Events: '+str(Options.nRTotalEvents),fontsize = Options.fontsize)
    plt.figtext(0.45,0.94,'Total Coincidence Events: '+str(Options.nREvents),fontsize = Options.fontsize)
    plt.figtext(0.45,0.92,'Spatial Resolution: '+str(SPATIALRESOLUTION),fontsize = Options.fontsize)

    if OOCDataset:
        plt.figtext(0.45,0.90,'Absolute Sensitivity: '+str(SENSITIVITY),fontsize = Options.fontsize)
        #plt.figtext(0.45,0.88,'SCATTERFRACTION: '+str(SCATTERFRACTION),fontsize = Options.fontsize)
        plt.suptitle("Complete Reconstruction [mm] via KNN with Dataset")
        outstring = "renderI_OOC.png"
    else:
        plt.suptitle("Complete Reconstruction [mm] via KNN")
        outstring = "renderI.png"
        
    if database_test_plot:
        outstring = "database_test_render.png"

    fig.savefig(os.getcwd()+"/"+Options.plotDIR+outstring)
    plt.show()
    return SPATIALRESOLUTION,SENSITIVITY,SCATTERFRACTION