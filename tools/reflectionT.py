#reflectplotDIR

#---------------------------
#visReflect(0) #index from 0 - check?
#reflectData: x,y,z,t,alive/dead,ID, incident, reflection angles
eventID = 2
(nPhotons,reflectData) = photonReflectData(eventID)

print(nPhotons)
L = (reflectData.shape)[0]
print(L)
# Get all events
#--------------------------------------
# NEED TO OPTIMIZE !!!!!!!!
#with multiprocessing.Pool(processes=8) as pool:
#		lise = list(tqdm(pool.map(photonReflectData,range(2,nPhotoEvents)),total=nPhotoEvents-1))
#~~~~~~ need the following to use multiple events (TURN THIS BACK ON WHEN DONE TESTING - NEEDED FOR VIS)
reflectDataC = reflectData
#for u in range(2,nPhotoEvents):
#    (nPhot,reflectData) = photonReflectData(u)
#    reflectDataC = np.append(reflectDataC,reflectData,axis=1)
#--------------------------------------
# get RP and KP
# RP are the indices of boundary reflection events
# KP are the indices of boundary death events
# DP are the detected indices
#
rpC = (reflectDataC[4,:].astype(int) == 1)
kpC = (reflectDataC[4,:].astype(int) == 0)
#
reflectState = reflectData[4,:].astype(int)
rp = (reflectState == 1)
kp = (reflectState == 0)
dp = (reflectState == 4)
#-------------
reflect = np.count_nonzero(rp) # total # of reflections at a boundary
killed = np.count_nonzero(kp) # total # of kills at a boundary
other = np.count_nonzero(reflectState == 2) # other ought to be 0 (which it has been so far)
detect = np.count_nonzero(dp) # detections
print("killed+detect:"+str(killed+detect)+".\n")
tot = reflect+killed # total # of interactions (do not count detections)
print("ASSERT-EQUALS (no other events): "+str(other==0)+" .\n")
#-------------
##
# DIFFERENT VISUALIZATIONS: SELECT AS PREFERRED
#-----------------------------------------------------------------------------------
#visReflectBD(eventID,reflectData,kp,"Photon Boundary Absorption Interactions"+Ropt,"BoundaryKilled"+Ropt+".png",reflectplotDIR,L)
#visReflectBD(eventID,reflectData,rp,"Photon Boundary Reflection/Refraction Interactions"+Ropt,"BoundaryReflect"+Ropt+".png",reflectplotDIR,L)
#visReflectBRD(eventID,reflectData,"Photon Boundary Interactions"+Ropt,"BoundaryStatistics"+Ropt+".png",reflectplotDIR)
visReflectAAK(rpC,kpC,reflectDataC,"Photon Boundary Angle-Alive/Killed Histogram"+Ropt,"AliveKilledHistogram"+Ropt+".png",reflectplotDIR,L)
visReflectAA(rpC,reflectDataC,"Photon Boundary Incidence/Reflection Angle"+Ropt,"AliveAngles"+Ropt+".png",reflectplotDIR,L)
#-----------------------------------------------------------------------------------
#------------
pr = reflect/(reflect+killed) #pr is probability of reflection/refraction at a boundary interaction
#-------------
#print(reflectData[:,rp][:,0])
#-------------
reflects = reflectData[:,rp][5,:] # IDS of reflection events
kills = reflectData[:,kp][5,:]    # IDS of kill events
detects = reflectData[:,dp][5,:]  # IDS of detected events
#_------------
incident = abs(reflectData[:,rp][6,:]*180/(np.pi)) # incident angles
critical = (180/np.pi)*math.asin(1/n_EJ208)
print(critical)
TIRreflect = incident>critical
#print(incident)
#print(TIRreflect)
nonTIRids=np.unique(reflects[~TIRreflect]) # IDS of non-TIR reflections
incidentTIR = incident[TIRreflect]
incidentNonTIR = incident[~TIRreflect]
#print(nonTIRids)
#-------------
# Detected LR Photon counts
lvals = np.sum(left,axis=(1,2))
rvals = np.sum(right,axis=(1,2))
print("ASSERT-EQUALS (created Photon Counts match up): "+str(nPhotons==int(np.sum(strip[2])))+" .\n")
print(lvals)
print(rvals)
meanL = np.mean(lvals)
meanR = np.mean(rvals)
cL = lvals[eventID]
cR = rvals[eventID]
errL = 2*np.std(lvals)
errR = 2*np.std(rvals)
#-------------
dataout = np.zeros((nPhotons,2))
reflectCounts = np.zeros(nPhotons) # number of reflections by pid
AbsorptionType = np.zeros(nPhotons)    # Absorbed how (0 - bound.abs., 1 - vol.abs.,2 - det.) by pid?
#-------------

boundaryinteract = True
if(boundaryinteract):

    def countFunction(i):
        ct = np.count_nonzero(reflects == i)
        at = 0
        tir = 1
        if (i not in kills):
            if (i in detects):
                at = 2
            else:
                at = 1
        if (i in nonTIRids):
            tir = 0
        return np.array([ct,at,tir])

    with multiprocessing.Pool(processes=8) as pool:
	    dataout = np.array(list(tqdm(pool.map(countFunction,range(nPhotons)),total=nPhotons)))
    print(dataout.shape)
    reflectCounts = dataout[:,0]
    AbsorptionType = dataout[:,1]
    TIR = dataout[:,2]
    #for i in range(nPhotons):
    #    reflectCounts[i] = np.count_nonzero(reflects == i)
    #    if (i not in kills):
    #        if (i in detects):
    #            AbsorptionType[i] = 2
    #        else:
    #            AbsorptionType[i] = 1
    #---------------------------
    #print(reflectCounts[0:50])
    #--------------------------
    #--Counts
    #print(AbsorptionType)
    DetAbsorbCounts = reflectCounts[(AbsorptionType == 2)]
    DetAbsorbCountsTIR = reflectCounts[np.logical_and((TIR == 1),(AbsorptionType == 2))]
    DetAbsorbCountsNonTIR = reflectCounts[np.logical_and((TIR == 0),(AbsorptionType == 2))]
    VolAbsorbCounts = reflectCounts[(AbsorptionType == 1)] # note AbsorptionType contains straight shots, volumetric absorption, and detections!
    AbsorbCounts = reflectCounts[(AbsorptionType == 0)]
    #-------------------------
    directDetec = np.count_nonzero(DetAbsorbCounts==1)
    detec = len(DetAbsorbCounts)
    detecTIR = len(DetAbsorbCountsTIR)
    detecNonTIR = len(DetAbsorbCountsNonTIR)
    print("ASSERT-EQUALS (no double counting of detections): "+str(detec==detect)+" .\n")
    print("detec: "+str(detec)+" .\n")
    print("detect: "+str(detect)+" .\n")
    noniter = len(VolAbsorbCounts)
    print("vol.abs: "+str(noniter)+" .\n")
    #--Ranges
    binwidth=10
    rangeH = max(reflectCounts) # - min(reflectCounts)
    #print(VolAbsorbCounts)
    volabsorbdidnotreflect = False
    if(noniter!=0):
        VolAbsorbCounts_range = max(VolAbsorbCounts) - min(VolAbsorbCounts)
        if(VolAbsorbCounts_range==0):
            VolAbsorbCounts_range=binwidth
            volabsorbdidnotreflect = True
    else:
        VolAbsorbCounts_range = binwidth
        volabsorbdidnotreflect = True
    #
    if(detec!=0):
        DetAbsorbCounts_range = max(DetAbsorbCounts) - min(DetAbsorbCounts)
        if(DetAbsorbCounts_range==0):
            DetAbsorbCounts_range=binwidth
    else:
        DetAbsorbCounts_range = binwidth
    if(detecTIR!=0):
        DetAbsorbCountsTIR_range = max(DetAbsorbCountsTIR) - min(DetAbsorbCountsTIR)
        if(DetAbsorbCountsTIR_range==0):
            DetAbsorbCountsTIR_range=binwidth
    else:
        DetAbsorbCountsTIR_range = binwidth
    if(detecNonTIR!=0):
        DetAbsorbCountsNonTIR_range = max(DetAbsorbCountsNonTIR) - min(DetAbsorbCountsNonTIR)
        if(DetAbsorbCountsNonTIR_range==0):
            DetAbsorbCountsNonTIR_range=binwidth
    else:
        DetAbsorbCountsNonTIR_range = binwidth
    #
    if(len(AbsorbCounts)!=0):
        AbsorbCounts_range = max(AbsorbCounts) - min(AbsorbCounts)
        if(AbsorbCounts_range==0):
            AbsorbCounts_range=binwidth
    else:
        AbsorbCounts_range = binwidth
    #-------------------------
    # figure & text
    fig,ax = plt.subplots(1)
    xt = 0.15
    ax.set_xlim(-10,310)
    #-------------------------
    # histograms
    ax.hist(AbsorbCounts, bins=int(AbsorbCounts_range/binwidth), color ='gray',alpha=0.5)
    ax.hist(DetAbsorbCounts, bins=int(DetAbsorbCounts_range/binwidth), color ='cyan',alpha=0.5)
    ax.hist(DetAbsorbCountsTIR, bins=int(DetAbsorbCountsTIR_range/binwidth), color ='blue',alpha=0.25)
    ax.hist(DetAbsorbCountsNonTIR, bins=int(DetAbsorbCountsNonTIR_range/binwidth), color ='green',alpha=0.25)
    #if(noniter!=0):
    #    ax.hist(VolAbsorbCounts, bins=int(VolAbsorbCounts_range/binwidth),color='red',alpha=0.5)
    #-------------------------
    # fit binomial histogram curves
    x = np.linspace(0,1000)*(rangeH/1000)
    y = np.power(pr,x)*(1-pr)*(nPhotons-noniter-detec)*binwidth
    ax.plot(x,y,color='black')
    y2 = np.power(pr,x)*(1-pr)*(detec)*binwidth
    ax.plot(x,y2,color='cyan')
    y3 = np.power(pr,x)*(1-pr)*(len(DetAbsorbCountsTIR))*binwidth
    ax.plot(x,y3,color='blue')
    y4 = np.power(pr,x)*(1-pr)*(len(DetAbsorbCountsNonTIR))*binwidth
    ax.plot(x,y4,color='green')
    #-------------------------
    # other stats
    means = np.mean(reflectCounts)
    meds = np.median(reflectCounts)
    ax.axvline(means,color='red',label='mean')
    ax.axvline(meds,color='pink',label='median')
    #-------------------------
    #print(VolAbsorbCounts_range)
    #plt.hist(reflectCounts, bins=int(rangeH/5))
    #_------------------------
    # text
    ax.text(0.1,0.95,str(len(reflectState))+" total interactions with "+str(nPhotons)+" total photons ("+str(nPhotons-noniter)+" interacting).",transform=ax.transAxes)
    ax.text(xt+.025,0.90,"Left: "+str(round(cL,2))+", (average: "+str(round(meanL,2))+"+-"+str(round(errL,2))+") photons.",transform=ax.transAxes)
    ax.text(xt+.025,0.85,"Right: "+str(round(cR,2))+", (average: "+str(round(meanR,2))+"+-"+str(round(errR,2))+") photons.",transform=ax.transAxes)
    ax.text(xt+.025,0.80,"Detections = "+str(detec)+"|"+str(detecTIR)+" TIR + "+str(detecNonTIR)+" nonTIR"+"|("+str(directDetec)+" direct)",transform=ax.transAxes)
    ax.text(xt+.025,0.75,"Vol. Att. tracks (not shown) = "+str(noniter),transform=ax.transAxes)
    if(volabsorbdidnotreflect):
        ax.text(0.28,0.70,"- note none of the vol. att. tracks ever reflected!",transform=ax.transAxes)
        VolAbsorbCounts_range=binwidth
    ax.text(xt+.05,0.60,"Gray\\Cyan\\Blue\\Green: B.Absorp.\\Det.\\Det.-TIR\\Det.-NonTIR",transform=ax.transAxes)
    ax.text(xt+.05,0.55,"Black\\Cyan\\Blue\\Green Models: Resp. Binomial Dist.:(P^X)*(1-P)",transform=ax.transAxes)
    ax.text(xt+.15,0.50,"Interaction Probability P = "+str(round(pr*100,2))+"%.",transform=ax.transAxes)
    ax.text(xt+.15,0.45,"Mean (Red) = "+str(round(means,2))+", Median (Pink) = "+str(round(meds,2))+",",transform=ax.transAxes)
    ax.text(xt+.20,0.40,"Binwidth = "+str(binwidth)+" interactions.",transform=ax.transAxes)
    ax.set_xlabel("# of Interactions")
    ax.set_ylabel("Counts")
    ax.set_title("Event #"+str(eventID)+" shown, with averages computed over "+str(nPhotoEvents)+" events.")
    plt.suptitle("Photon Boundary Interactions (Reflection\\Refraction)"+Ropt)
    plt.savefig(reflectplotDIR+"BoundaryInteractionsTIR"+Ropt+".png",dpi=600)
    #-------------------------
    # figure & text
    fig,ax = plt.subplots(1,2)
    ax[0].hist(incidentTIR,bins=int((180-critical)/5))
    ax[1].hist(incidentNonTIR,bins=int((critical)/5))
    ax[0].set_xlabel("Angle [degrees]")
    ax[0].set_ylabel("Counts")
    ax[1].set_xlabel("Angle [degrees]")
    ax[1].set_ylabel("Counts")
    ax[0].set_xlim(critical,180)
    ax[1].set_xlim(0,critical)
    plt.suptitle("TIR / Non-TIR interactions (5 degree bins)"+Ropt)
    plt.savefig(reflectplotDIR+"BoundaryInteractionsHist"+Ropt+".png",dpi=600)
    #-------------------------
