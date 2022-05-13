import numpy as np
from tqdm import tqdm
from matplotlib import projections, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde
from analyzeOptions import *
from tools.dimensions import *
from tools.geo import *
import pickle
import os
from sklearn.neighbors import LocalOutlierFactor
import jpcm


def outlierfilter(data):
    clf = LocalOutlierFactor(n_neighbors=40,contamination=0.05) #expect 5% outliers
    decision = clf.fit_predict(data)
    inliers = (decision == 1)
    print("OUTLIERS: ",np.count_nonzero(decision == -1))
    return data[inliers]

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
    shift = line/(np.linalg.norm(line,axis=0))
    # point = center+dx*shift

    cdelta = center - np.reshape(np.repeat(np.array([Options.SOURCE[0],0,Options.SOURCE[1]+UZ]),center.shape[1]),center.shape)
    #EXPECTED:
    if np.nan not in Options.SOURCE:
        dtexp = [(1/tof_const)*np.dot(cdelta[:,i],shift[:,i]) for i in range(cdelta.shape[1])]
        print("DT",dt[0:20])
        print("exp",dtexp[0:20])
        r = dtexp[0:20]/dt[0:20]
        print("ratio",r)
        print("ratiostats",np.mean(r),np.std(r))
    # Filter bad points
    # point = outlierfilter(point.T).T
    #

    point = center+dx*shift

    delta = point - np.reshape(np.repeat(np.array([Options.SOURCE[0],0,Options.SOURCE[1]+UZ]),point.shape[1]),point.shape)
    print("Source-position:",Options.SOURCE)
    if np.nan not in Options.SOURCE:
        SPATIALRESOLUTION = np.std(delta,axis=1)*FWHM
    else:
        SPATIALRESOLUTION = np.array([-1,-1,-1])
    print("SR",SPATIALRESOLUTION)
    print("SR_noshift_STD",np.std(point,axis=1))
    # print("P", p.T[:5])
    # print("T",dt)
    # print("DX",dx)
    # print("line",(line/np.linalg.norm(line,axis=0)).T)
    # print("shift",shift.T)
    # delta2 = center[:,:point.shape[1]] - np.reshape(np.repeat(np.array([Options.SOURCE[0],0,Options.SOURCE[1]+UZ]),point.shape[1]),point.shape)
    # print("POINT_error",np.linalg.norm(delta,axis=0))
    # print("Center_error",np.linalg.norm(delta2,axis=0))
    # print("Center_error",delta2)
    # print("Centers",center)
    SENSITIVITY = point.shape[1] / Options.TOTALEVENTS #Options.nREvents/Options.TOTALEVENTS #absolute
    SCATTERFRACTION = -1 #NOT YET IMPLEMENTED!!!!!!!

    np.savetxt(Options.datadir+"reco_pointdata.txt",point)

    xyz = point[:,0:Options.nREventLimit]
    for i in range(3):
        fig, ax = plt.subplots()
        ax.plot(xyz[i,:])
        plt.savefig(Options.plotDIR + "i_"+str(i)+".png")

    with open(Options.render_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(xyz, f)

    xy = np.vstack([xyz[0],xyz[2],xyz[1]])
    try: z = gaussian_kde(xy)(xy)
    except:
        z = 0.5+np.zeros(len(xyz[0]))
    #ax1.scatter(b, data["CTR"], c=z, s=16, cmap = "nipy_spectral")

    # fig = plt.figure(figsize=(12,12))
    # ax = fig.add_subplot(111, projection='3d')
    lim = np.array([[-UZ,UZ],[-UZ,UZ],[0,LZ]])
    labels = ["Radial - X","Radial - Y","Z - Length"]
    insetS = lambda i : [0.3 + 0.5*i, 0.10, 0.30, 0.30]
    spacer = 15
    Ilim = np.array([[-spacer+Options.SOURCE[0],spacer+Options.SOURCE[0]],[-spacer,spacer],[-spacer+UZ+Options.SOURCE[1],spacer+UZ+Options.SOURCE[1]]])
    cmap = jpcm.get("fuyu")
    panecolor = jpcm.maps.murasaki

    fig = plt.figure(figsize = (26,12),constrained_layout=True)
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    ax = [ax1,ax2]
    # ax = plt.subplots(2,1,projection='3d')
    for i in tqdm(range(2)):
        img = ax[i].scatter(xyz[i%3],xyz[(i+1)%3],xyz[(i+2)%3], c=z,s=2,alpha = 0.4,cmap=cmap)
        # img = ax[i].scatter(xyz[i%3],xyz[(i+1)%3],xyz[(i+2)%3],s=2,alpha = 0.7)
        ax[i].set_xlim(lim[i%3,0],lim[i%3,1])
        ax[i].set_ylim(lim[(i+1)%3,0],lim[(i+1)%3,1])
        ax[i].set_zlim(lim[(i+2)%3,0],lim[(i+2)%3,1])
        ax[i].set_xlabel(labels[i%3])
        ax[i].set_ylabel(labels[(i+1)%3])
        ax[i].set_zlabel(labels[(i+2)%3])
        ax[i].set_box_aspect((1,1,1))
        ax[i].xaxis.pane.fill = False
        ax[i].yaxis.pane.fill = False
        ax[i].zaxis.pane.fill = False
        if np.nan not in Options.SOURCE:
            inset = fig.add_axes(insetS(i), anchor='NW', projection='3d')
            inset.set_facecolor(jpcm.maps.transparent)
            # fig.patch.set_facecolor(jpcm.maps.transparent)
            inset.scatter(xyz[i%3],xyz[(i+1)%3],xyz[(i+2)%3], c=z,s=2,alpha = 0.8,cmap=cmap)
            inset.set_xlim(Ilim[i%3,0],Ilim[i%3,1])
            inset.set_ylim(Ilim[(i+1)%3,0],Ilim[(i+1)%3,1])
            inset.set_zlim(Ilim[(i+2)%3,0],Ilim[(i+2)%3,1])
            inset.set_xlabel(labels[i%3])
            inset.set_ylabel(labels[(i+1)%3])
            inset.set_zlabel(labels[(i+2)%3])
            inset.w_xaxis.set_pane_color(panecolor)
            inset.w_yaxis.set_pane_color(panecolor)
            inset.w_zaxis.set_pane_color(panecolor)
            inset.xaxis.pane.set_edgecolor(jpcm.maps.transparent)
            inset.yaxis.pane.set_edgecolor(jpcm.maps.transparent)
            inset.zaxis.pane.set_edgecolor(jpcm.maps.transparent)
            inset.grid(False)
            inset.set_box_aspect((1,1,1))
        for A in range(nArray):
            detpoint = det[A]
            # print(detpoint)
            ax[i].plot(detpoint[i%3,:],detpoint[(i+1)%3,:],detpoint[(i+2)%3,:],c=tuple(jpcm.maps.rurikon),linestyle='-.',alpha = 0.5)
    cax = plt.axes([0.4875, 0.05, 0.0125, 0.8])
    cbar = plt.colorbar(img,cax=cax)
    cbar.set_alpha(1)
    cbar.draw_all()
    plt.figtext(0.45,0.96,'Total Single Events: '+str(Options.nRTotalEvents),fontsize = Options.fontsize)
    plt.figtext(0.45,0.94,'Total Coincidence Events: '+str(point.shape[1])+' events + '+str(Options.nREvents - point.shape[1])+' outliers',fontsize = Options.fontsize)
    plt.figtext(0.45,0.92,'Spatial Resolution: '+str(SPATIALRESOLUTION),fontsize = Options.fontsize)

    if OOCDataset or database_test_plot:
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