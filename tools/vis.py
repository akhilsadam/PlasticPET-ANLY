#------------------------------------------------------------------------------------
#Visualization Setup
#------------------------------------------------------------------------------------
def forceAspect(ax,aspect=1):
	im = ax.get_images()
	extent = im[0].get_extent()
	ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)
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
	ax.axes.set_ylim3d(bottom=-UX,top=UX)
	ax.axes.set_zlim3d(bottom=-UY,top=UY)
	ax.axes.set_xlim3d(left=0,right=LZ)

	xGrid = np.arange(-UX,UX+binx,binx)
	yGrid = np.arange(-UY,UY+biny,biny)
	zGrid = np.arange(0,LZ+binz,binz)
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
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k+1])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
	ax.grid(False)

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
	ax.axes.set_ylim3d(bottom=-UX,top=UX)
	ax.axes.set_zlim3d(bottom=-UY,top=UY)
	ax.axes.set_xlim3d(left=0,right=LZ)

	xGrid = np.arange(-UX,UX+binx,binx)
	yGrid = np.arange(-UY,UY+biny,biny)
	zGrid = np.arange(0,LZ+binz,binz)
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
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k+1])
				YS.append(xGrid[i])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
				XS.append(zGrid[k])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				XS.append(zGrid[k+1])
				YS.append(xGrid[i+1])
				ZS.append(yGrid[j])
				ax.plot(XS,YS,ZS,label='parametric curve',color='grey',linestyle='--',linewidth=0.4)
				XS,YS,ZS = [],[],[]
	ax.grid(False)

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
