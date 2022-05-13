from more_itertools import flatten
from utils.simpleimport import *
from analyzeOptions import *
from scipy.stats import gaussian_kde
from analyzeOptions import *
from tools.dimensions import *
from tools.geo import *
import pickle
from sklearn.neighbors import LocalOutlierFactor
import jpcm

folder = "test_gRI51"
Options.SOURCE=[0,100]

color_by_array = False
show_detections = True

Options.datadir=f"../data/{folder}/"
Options.plotDIR=f"../plot/{folder}/"
Options.ArrayNumber = 0
with open('tools/data.py') as f: exec(f.read())
evtPhotoInteractG, evtComptonInteractG,evtInteractG = beamInteraction()

# Range Check : [STATUS] Works

# u = np.array(list(flatten(evtInteractG)))
# for i in range(3):
#     # print(u)
#     k = u[:,i]
#     k = k[np.isfinite(k)]
#     print(f"RANGE {i}:{min(k)} to {max(k)}")

def getge(ArrayNumber):
    Options.ArrayNumber = ArrayNumber
    
    evtPhotoInteract, evtComptonInteract,evtInteract,evtType,evtType2 = localizeBeam(evtPhotoInteractG,evtComptonInteractG,evtInteractG,ArrayNumber)
    # good = []
    # for e in evtInteractG:
    #     egood=True
    #     for j in e:
    #         if not all(isinstance(k, (int, float)) for k in j):
    #             egood = False
    #             break
    #         else: print(j)
    #     good.append(egood)
    # # print(np.array(evtInteractG)[good])
    # print(evtInteract)
    goodevt = []
    for e,f in zip(evtInteract,evtInteractG):
        ge = []
        for j, k in zip(e, f):
            if ArrayNumber == 12 and (j[0]**2+j[1]**2)**0.5 < 100:
                print((j[0]**2+j[1]**2)**0.5)
            if all(withinLimitXYZ(j[i], i) for i in range(3)) and all(np.isfinite(j)):
                ge = k
                break

        goodevt.append(ge)
    # print(goodevt)
    return goodevt

pointset=[]
cs = []

for N in range(0,1):

    g1 = getge(N)
    g2 = getge(N+12)

    idx = [True if len(g1[i]) > 0 else False for i in range(len(g1))] #and len(g2[i]) > 0
    num = np.count_nonzero(idx)
    print(num)

    a1 = []
    a2 = []
    for i in range(len(idx)):
        if idx[i]:
            a1.append(g1[i])
            a2.append(g2[i])

    a1 = np.array(a1)
    a2 = np.array(a2)
    
    # Range Check : [STATUS] ?

    for i in range(3):
        # print(u)
        print(f"RANGE {i}:{min(a1[:,i])} to {max(a1[:,i])}")

    # print(a1,a2)
    dt = (a1[:,4]-a2[:,4]) # ns->ps (does not work with PETSYS - they give picoseconds)
    dx = tof_const*dt#mm
    center = np.array([(a1[:,0]+a2[:,0])/2, (a1[:,1]+a2[:,1])/2, (a1[:,2]+a2[:,2])/2])
    line = -np.array(((a1[:,0]-a2[:,0]), (a1[:,1]-a2[:,1]), (a1[:,2]-a2[:,2])))
    shift = line/(np.linalg.norm(line,axis=0))
    point0 = center+dx*shift

    print(f"N = {N}")
    print(f"\tmean={np.mean(point0,axis=1)}")
    print(f"\tfwhm={FWHM*np.std(point0,axis=1)}")
    pointset.append(point0)
    cs.extend([N]*num)

point = np.hstack(pointset)
# point = point - np.tile(np.reshape(np.mean(point0,axis=1),(3,1)),(1,point.shape[1]))



Options.TOTALEVENTS = len(g2)

# COPY FROM RENDER.PY

det = np.array([
    np.array([
        ArrayToGlobalCoordinates(0, 0, 0, A),
        ArrayToGlobalCoordinates(0, 0, LZ, A),
    ]).T
    for A in range(nArray)
])

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

# np.savetxt(Options.datadir+"reco_pointdata.txt",point)

xyz = point
for i in range(3):
    fig, ax = plt.subplots()
    ax.plot(xyz[i,:])
    plt.savefig(Options.plotDIR + "i_"+str(i)+".png")

with open(Options.render_pkl, 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump(xyz, f)

xy = np.vstack([xyz[0],xyz[2],xyz[1]])
# try: z = gaussian_kde(xy)(xy)
# except:
#     z = 0.5+np.zeros(len(xyz[0]))
if color_by_array:
    z = cs
elif show_detections:
    z = list(range(len(xyz[0])))
else:
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
    if show_detections:
        img = ax[i].scatter(a1[:,i%3],a1[:,(i+1)%3],a1[:,(i+2)%3], c=z,s=2,alpha = 0.4,cmap=cmap)
        ax[i].scatter(a2[:,i%3],a2[:,(i+1)%3],a2[:,(i+2)%3], c=z,s=2,alpha = 0.4,cmap=cmap)
        ax[i].scatter(xyz[i%3],xyz[(i+1)%3],xyz[(i+2)%3], c='black',s=2,alpha = 0.4,cmap=cmap)
    else:
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
    if i==1:
        ax[i].view_init(elev=10., azim=90)
cax = plt.axes([0.4875, 0.05, 0.0125, 0.8])
cbar = plt.colorbar(img,cax=cax)
cbar.set_alpha(1)
cbar.draw_all()
# plt.figtext(0.45,0.96,'Total Single Events: '+str(Options.nRTotalEvents),fontsize = Options.fontsize)
# plt.figtext(0.45,0.94,'Total Coincidence Events: '+str(point.shape[1])+' events + '+str(Options.nREvents - point.shape[1])+' outliers',fontsize = Options.fontsize)
plt.figtext(0.45,0.92,'Spatial Resolution: '+str(SPATIALRESOLUTION),fontsize = Options.fontsize)

plt.savefig(f"{Options.plotDIR}testSR.png")