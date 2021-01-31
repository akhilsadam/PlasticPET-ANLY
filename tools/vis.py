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
