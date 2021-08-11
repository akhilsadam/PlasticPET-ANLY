from tools.dimensions import *
#------------------------------------------------------------------------------------
#Visualization Setup
#------------------------------------------------------------------------------------
def forceAspect(ax,aspect=1):
	im = ax.get_images()
	extent = im[0].get_extent()
	ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)
def visgrids(ax,i,alpha):
	xin = (0+i)%4
	yin = (1+i)%4
	zin = (2+i)%4
	ax.axes.set_ylim3d(bottom=LM[xin,0],top=LM[xin,1])
	ax.axes.set_zlim3d(bottom=LM[yin,0],top=LM[yin,1])
	ax.axes.set_xlim3d(left=LM[zin,0],right=LM[zin,1])

	xGrid = np.arange(LM[xin,0],LM[xin,1]+BM[xin],BM[xin])
	yGrid = np.arange(LM[yin,0],LM[yin,1]+BM[yin],BM[yin])
	zGrid = np.arange(LM[zin,0],LM[zin,1]+BM[zin],BM[zin])
	XS,YS,ZS = [],[],[]
	for i in range(len(xGrid)-1):
		for j in range(len(yGrid)):
			for k in range(len(zGrid)-1):
				XS.append(zGrid[k])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4,alpha=alpha)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4,alpha=alpha)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k+1])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4,alpha=alpha)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4,alpha=alpha)
				XS,YS,ZS = [],[],[]
	ax.grid(False)

def vis(eventID):
	fig = plt.figure(figsize=(5,5))
	ax = fig.add_subplot(111)
	ax.imshow(np.dstack((0.2*left[eventID],0.01*strip[eventID],0.2*right[eventID])),alpha = 1.0, extent = [-UX,UX,-UY,UY])
	POSX = evtComptonInteract[eventID][:,0]
	POSY = evtComptonInteract[eventID][:,1]
	ax.scatter(POSX,POSY,color="xkcd:robin's egg blue")
	POSX = evtPhotoInteract[eventID][:,0]
	POSY = evtPhotoInteract[eventID][:,1]
	ax.scatter(POSX,POSY,color='xkcd:pastel blue')
	ax.scatter(recPos[eventID,0],recPos[eventID,1],color='crimson')
	ax.set_xlabel("X - depth/width")
	ax.set_ylabel("Y - height")
	forceAspect(ax,aspect=0.75)

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	p = []
	for i in range(3):
		px = evtInteract[eventID][:,i]
		px = np.insert(px,0,evtPos[eventID,i])
		p.append(px)

	visgrids(ax,0,1)

	ax.plot(p[2],p[0],p[1],label='parametric curve')
	p = []
	for i in range(3):
		p.append(evtComptonInteract[eventID][:,i])
	ax.scatter(p[2],p[0],p[1],color="xkcd:robin's egg blue")
	p = []
	for i in range(3):
		p.append(evtPhotoInteract[eventID][:,i])
	ax.scatter(p[2],p[0],p[1],color='xkcd:pastel blue')
	ax.scatter(recPos[eventID,2],recPos[eventID,0],recPos[eventID,1],color='crimson')
	ax.set_xlabel("Z - length")
	ax.set_ylabel("X - depth/width")
	ax.set_zlabel("Y - height")
	plt.show()
	#print(evtInteract[eventID])
	#print(recPos[eventID])
def visTime(eventID):
	fig = plt.figure()
	ax = fig.gca(projection='3d')
	p = []
	for i in range(3):
		px = evtInteract[eventID][:,i]
		px = np.insert(px,0,evtPos[eventID,i])
		p.append(px)

	visgrids(ax,0,1)

	ax.plot(p[2],p[0],p[1],label='parametric curve')
	p = []
	for i in range(3):
		p.append(evtComptonInteract[eventID][:,i])
	ax.scatter(p[2],p[0],p[1],color="xkcd:robin's egg blue")
	p = []
	for i in range(3):
		p.append(evtPhotoInteract[eventID][:,i])
	ax.scatter(p[2],p[0],p[1],color='xkcd:pastel blue')

	ax.scatter(actEvtPosN[eventID,2],actEvtPosN[eventID,0],actEvtPosN[eventID,1],s = 12,color='blue',marker=mk.MarkerStyle(marker='X', fillstyle='full'))

	ax.scatter(recPos[eventID,2],recPos[eventID,0],recPos[eventID,1],s=12,color='crimson')

	if(SiPMTime_Based_Reconstruction):
		ax.scatter(recPosT[2],recPosT[0],recPosT[1],s=12,color='lime')

	#photons
	psmD = photonSiPMData(eventID)
	minTimeSiPMphot = min(psmD[3])
	interactionTimeGamma = time_I_N[eventID]

	ax.scatter(psmD[2],psmD[0],psmD[1],s=2,c=(psmD[3]-minTimeSiPMphot),cmap='Spectral',norm=mpt_col.Normalize(vmin=0,vmax=2*TC_SiPM_X))	

	

	cbar = fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=0,vmax=2*TC_SiPM_X), cmap='Spectral'),ax=ax)
	cbar.set_label('Time in ns (relative to first detected photon)', rotation=90)

	ax.set_xlabel("Z - length")
	ax.set_ylabel("X - depth/width")
	ax.set_zlabel("Y - height")
	ax.set_proj_type('persp')

	
	plt.figtext(0.2, 0.84, "Total Number of Detected Photons = %1.0f" %(len(psmD[0])),fontsize=10)
	plt.figtext(0.2, 0.80, "Interaction Time = %4.4f ns" %(interactionTimeGamma),fontsize=10)
	plt.figtext(0.2, 0.76, "First Detected Photon Time = %4.4f ns" %(minTimeSiPMphot),fontsize=10)
	plt.tight_layout()
	plt.suptitle("Event "+str(eventID)+" : Photon Times")
	plt.show()
	#print(evtInteract[eventID])
	#print(recPos[eventID])
#
# 
from mpl_toolkits.axes_grid1 import make_axes_locatable
def marginalPLT0(ax,x,y,i):
	#ax.set_aspect(1.)
	# create new axes on the right and on the top of the current axes
	divider = make_axes_locatable(ax)
	# below height and pad are in inches
	ax_histx = divider.append_axes("top", 0.2, pad=0.05, sharex=ax)
	ax_histy = divider.append_axes("right", 0.2, pad=0.05, sharey=ax)
	# now determine nice limits by hand:
	binwidth = binList[i]
	bins = np.arange(int(LM[i,0]), int(LM[i,1])+ binwidth, binwidth)

	ax_histx.hist(x, bins=bins)
	ax_histy.hist(y, bins=bins, orientation='horizontal')
	ax_histx.text(locX,locY+spaY, "Bin={0:.1f} {1}".format(binwidth,unitList[i]),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

	# the xaxis of ax_histx and yaxis of ax_histy are shared with ax,
	# thus there is no need to manually adjust the xlim and ylim of these
	# axis.
	#ax_histx.set_yticks([0, 50, 100])
	#ax_histy.set_xticks([0, 50, 100])
	ax_histx.get_xaxis().set_visible(False)
	ax_histy.get_yaxis().set_visible(False)
	ax.tick_params(labelsize=8)
	ax_histx.tick_params(labelsize=8)
	ax_histy.tick_params(labelsize=8)

	plt.margins(0,0)

def marginalPLT2(ax,x,y,i):
	#ax.set_aspect(1.)
	# create new axes on the right and on the top of the current axes
	divider = make_axes_locatable(ax)
	# below height and pad are in inches
	ax_histx = divider.append_axes("top", 0.2, pad=0.05, sharex=ax)
	ax_histy = divider.append_axes("right", 0.2, pad=0.05, sharey=ax)
	# now determine nice limits by hand:
	binwidth = binList[i]
	bins = np.arange(int(LM[i,0]), int(LM[i,1])+ binwidth, binwidth)
	binzy = 20
	ymax = np.max(np.abs(y))
	binwidthy = int(ymax/binzy)
	limy = (int(ymax/binwidthy) + 1)*binwidthy
	ybins = np.arange(0, limy + binwidthy, binwidthy)
	ax_histx.hist(x, bins=bins)
	ax_histy.hist(y, bins=ybins, orientation='horizontal')
	ax_histx.text(locX,locY+spaY, "Bin={0:.1f} {1}".format(binwidth,unitList[i]),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

	# the xaxis of ax_histx and yaxis of ax_histy are shared with ax,
	# thus there is no need to manually adjust the xlim and ylim of these
	# axis.
	#ax_histx.set_yticks([0, 50, 100])
	#ax_histy.set_xticks([0, 50, 100])
	ax_histx.get_xaxis().set_visible(False)
	ax_histy.get_yaxis().set_visible(False)
	ax.tick_params(labelsize=8)
	ax_histx.tick_params(labelsize=8)
	ax_histy.tick_params(labelsize=8)

	plt.margins(0,0)

#--------------------------------------------------- vis REFLECTIONS
def visReflect(eventID):
	fig = plt.figure()
	ax0 = fig.add_subplot(1, 2, 1, projection='3d')
	ax1 = fig.add_subplot(1, 2, 2, projection='3d')
	axs=[ax0,ax1]
	
	visgrids(axs[0],0,1)
	visgrids(axs[1],0,1)
	#photons
	(nPhotons,psmD) = photonReflectData(eventID)
	minTimeSiPMphot = min(psmD[3])

	reflectState = psmD[4,:]
	rp = (reflectState == 1.0)
	kp = (reflectState == 0.0)
	other = np.count_nonzero(reflectState == 2.0)
	reflect = np.count_nonzero(rp)
	killed = np.count_nonzero(kp)
	pr = reflect/(reflect+killed+other)
	tot = len(psmD[0])
	psmDR = np.reshape(psmD[:,rp],(6,reflect))
	psmDK = np.reshape(psmD[:,kp],(6,killed))

	cmap = LinearSegmentedColormap.from_list("Segment", [(0,0,0),(0.0,0.7,1)], N=2)

	ax0.scatter(psmDR[2],psmDR[0],psmDR[1],s=2,c=psmDR[4],cmap=cmap,norm=mpt_col.Normalize(vmin=0,vmax=1.0))	
	ax1.scatter(psmDK[2],psmDK[0],psmDK[1],s=2,c=psmDK[4],cmap=cmap,norm=mpt_col.Normalize(vmin=0,vmax=1.0))

	cbar = fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=0,vmax=1), cmap=cmap),ax=axs[1])
	cbar.set_label('Alive/Killed', rotation=-90)

	for ax in axs:
		ax.set_xlabel("Z - length")
		ax.set_ylabel("X - depth/width")
		ax.set_zlabel("Y - height")
		ax.set_proj_type('persp')

	st = 0.65
	xt = 0.02
	plt.figtext(xt, st+.24, "Total Photon-Boundary Interactions = %1.0f" %(tot),fontsize=10)
	plt.figtext(xt, st+.20, "Reflected = %4.4f" %(reflect),fontsize=10)
	plt.figtext(xt, st+.16, "Killed = %4.4f" %(killed),fontsize=10)
	plt.figtext(xt, st+.12, "Unclassified = %4.4f" %(other),fontsize=10)
	plt.figtext(xt, st+.08, "Reflection Percentage = %4.4f" %(pr),fontsize=10)
	plt.figtext(xt, st+.04, "Photons~= (1-P(R))*Total = %4.4f" %((1-pr)*tot),fontsize=10)
	plt.figtext(xt, st+.00, "First Detected Photon Time = %4.4f ns" %(minTimeSiPMphot),fontsize=10)


	#plt.tight_layout()
	plt.suptitle("Single Event "+str(eventID)+" : Reflections")
	plt.show()

def visReflectBD(eventID,reflectData,kp,title,filename,saveDIR,L):
	fig = plt.figure()
	ax0 = fig.add_subplot(2, 2, 1, projection='3d')
	ax1 = fig.add_subplot(2, 2, 2, projection='3d')
	ax2 = fig.add_subplot(2, 2, 3, projection='3d')
	ax3 = fig.add_subplot(2, 2, 4, projection='3d')
	axs=[ax0,ax1,ax2,ax3]
	
	#photons

	killed = np.count_nonzero(kp)
	psmDR = np.reshape(reflectData[:,kp],(L,killed))
	anglelist = [[45,45],[0,110],[0,0],[90,90]]
	fsz = 6
	for i in range(4):
		ax = axs[i]
		ax.view_init(anglelist[i][0],anglelist[i][1])
		visgrids(ax,0,1)
		ax.scatter(psmDR[2],psmDR[0],psmDR[1],s=1,alpha = 0.4)
		ax.set_xlabel("Z - length", fontsize = fsz, clip_on=False)
		ax.set_ylabel("X - depth/width", fontsize = fsz, clip_on=False)
		ax.set_zlabel("Y - height", fontsize = fsz, clip_on=False)
		ax.tick_params(axis='x', labelsize=fsz)
		ax.tick_params(axis='y', labelsize=fsz)
		ax.tick_params(axis='z', labelsize=fsz)

	plt.margins(0)
	plt.tight_layout()
	plt.suptitle(title+" (Evt="+str(eventID)+")")
	plt.savefig(saveDIR+filename,dpi=600)
def visReflectBRD(eventID,reflectData,title,filename,saveDIR):
	reflectState = reflectData[4,:]
	rp = (reflectState == 1.0)
	kp = (reflectState == 0.0)
	other = np.count_nonzero(reflectState == 2.0)
	reflect = np.count_nonzero(rp)
	killed = np.count_nonzero(kp)
	pr = reflect/(reflect+killed+other)
	tot = len(reflectData[0])
	
	fig, axs = plt.subplots()

	st = 0.65
	xt = 0.25
	plt.figtext(xt, st+.24, "Total Photon-Boundary Interactions = %1.0f" %(tot),fontsize=10)
	plt.figtext(xt, st+.20, "Reflected = %4.4f" %(reflect),fontsize=10)
	plt.figtext(xt, st+.16, "Killed = %4.4f" %(killed),fontsize=10)
	plt.figtext(xt, st+.12, "Unclassified = %4.4f" %(other),fontsize=10)
	plt.figtext(xt, st+.08, "Reflection Percentage = %4.4f" %(pr),fontsize=10)
	plt.figtext(xt, st+.04, "Photons~= (1-P(R))*Total = %4.4f" %((1-pr)*tot),fontsize=10)
	plt.figtext(xt, st+.00, "First Detected Photon Time = %4.4f ns" %(minTimeSiPMphot),fontsize=10)

	plt.margins(0)
	plt.tight_layout()
	plt.suptitle(title+" (Evt="+str(eventID)+")")
	axs.plot([1, 2, 3])
	axs.remove()
	plt.savefig(saveDIR+filename,dpi=100)
def visReflectAAK(rp,kp,reflectData,title,filename,saveDIR,L):
	incident = abs(reflectData[6,:]*180/(np.pi))
	reflectangle = abs(reflectData[7,:]*180/(np.pi))
	rpi = incident[rp]
	kpi = incident[kp]
	binwidth = 5
	bins=int(180/binwidth)
	fig,axs = plt.subplots(2,constrained_layout=True)

	nej = 1.58

	axs[0].hist(rpi, bins=bins, color="blue")
	axs[0].hist(kpi, bins=bins, color="red")
	axs[0].set_title("Reflected+Refracted | Absorbed Histograms")
	rph,bin_edges = np.histogram(rpi,bins)
	kph,bin_edges = np.histogram(kpi,bins)
	ratio = rph/kph
	bin_centers = bin_edges[1:len(bin_edges)] - (bin_edges[1] - bin_edges[0])/2
	axs[1].set_title("Reflected|Refracted / Absorbed Ratio")	
	axs[1].plot(bin_centers,ratio, color="blue")
	for ax in axs:
		#ax.set_xlim(-180,180)
		ax.set_ylabel("Counts")
		ax.set_xlabel("Incident Angle")
		line = ax.axvline(x=np.arcsin(1/nej)*180/np.pi,color='black')
		line2 = ax.axvline(x=(np.pi-np.arcsin(1/nej))*180/np.pi,color='black')
		line.set_label('TIR')
		line2.set_label('TIR')
	
	#plt.tight_layout()
	plt.suptitle(title)
	plt.savefig(saveDIR+filename,dpi=100)
	#plt.show()
def visReflectAA(rp,reflectData,title,filename,saveDIR,L):
	incident = (reflectData[6,:]*180/(np.pi))
	reflectangle = (reflectData[7,:]*180/(np.pi))
	rpi = incident[rp]
	rpr = reflectangle[rp]
	reflected = (np.sign(rpi)==np.sign(rpr))
	refracted = (np.sign(rpi)!=np.sign(rpr))
	rpir = abs(rpi[reflected])
	rprr = abs(rpr[reflected])
	rpit = abs(rpi[refracted])
	rprt = abs(rpr[refracted])
	fig,ax = plt.subplots(1,constrained_layout=True)

	nej = 1.58

	psze = 1
	#ax.scatter(rpir,rprr,s=psze,color="blue", alpha = 0.2) #reflected (WOULD BE, but the angle signs are incorrect)
	#ax.scatter(rpit,rprt,s=psze,color="blue", alpha = 0.2) #refracted
	ax.scatter(abs(rpi),abs(rpr),s=psze,color="blue", alpha = 0.2)
	ax.set_title("Reflected+Refracted: Exit Angle vs Incidence Angle")

	#ratio = np.histogram(rpi,bins)[0]/np.histogram(kpi,bins)[0]
	#axs[1].set_title("Reflected|Refracted / Absorbed Ratio")	
	#axs[1].plot(range(1,180,binwidth),ratio, color="blue")
	#for ax in axs:
	ax.set_xlim(0,180)
	ax.set_ylim(0,180)
	ax.set_ylabel("Exit Angle")
	ax.set_xlabel("Incident Angle")
	tirval = np.arcsin(1/nej)*180/np.pi
	line = ax.axvline(x=tirval,color='black')
	line2 = ax.axvline(x=(np.pi-np.arcsin(1/nej))*180/np.pi,color='black')
	line5 = ax.axvline(x=90-tirval,color='black')
	line6 = ax.axvline(x=90+tirval,color='black')
	line.set_label('TIR')
	line2.set_label('TIR')
	line3 = ax.axhline(y=tirval,color='black')
	line4 = ax.axhline(y=(np.pi-np.arcsin(1/nej))*180/np.pi,color='black')
	line7 = ax.axhline(y=90-tirval,color='black')
	line8 = ax.axhline(y=90+tirval,color='black')
	line3.set_label('TIR')
	line4.set_label('TIR')
	ax.set_aspect(1)

	ax.text(0.4,1.1,"Red - Refraction, Cyan - Reflection,\nPurple - Transmission, Black - Critical Angles",fontsize=10)
	
	color = "red"
	lw = 1
	x_sn = np.array(range(90))
	y_sn = np.arcsin(np.sin(np.pi*(x_sn/180))*nej)*180/np.pi
	ax.plot(x_sn,y_sn,color=color,linewidth=lw)  #Fresnel Refraction 0-90 from inside EJ208, Exit Angle relative to inner normal (would this be outer VK normal?)
	x_sn2 = 90-x_sn
	y_sn2 = 90-y_sn
	y_sn3 = 90-np.arcsin(np.sin(np.pi*(x_sn/180))/nej)*180/np.pi
	ax.plot(x_sn2,y_sn3,color=color,linewidth=lw) #Fresnel Refraction 0-90 from inside EJ208, Exit Angle relative to outer normal
	ax.plot(x_sn2,y_sn2,color=color,linewidth=lw) #Fresnel Refraction 0-90 from outside EJ208, Exit Angle relative to outer normal
	ax.plot(x_sn,90-y_sn3,color=color,linewidth=lw) #Fresnel Refraction 0-90 from inside EJ208, Exit Angle relative to inner normal
	ax.plot(90+y_sn,90+x_sn,color=color,linewidth=lw)#ax.plot(x_sn,180-y_sn,color='red') #FR 90-180 from inside EJ208, exit rel. outer EJ
	ax.plot(180-y_sn,180-x_sn,color=color,linewidth=lw)  #FR 90-180 from outside EJ208, exit rel. outer EJ
	ax.plot(180-x_sn,180-y_sn,color=color,linewidth=lw)
	ax.plot(90+x_sn,90+y_sn,color=color,linewidth=lw)

	ax.plot(2*x_sn,180-2*x_sn,color="purple",linewidth=lw)
	ax.plot(2*x_sn,2*x_sn,color="cyan",linewidth=lw)

	marginalPLT0(ax,np.abs(rpi),np.abs(rpr),4)

	#plt.tight_layout()
	plt.suptitle(title)
	plt.savefig(saveDIR+filename,dpi=600)
	#plt.show()