stripPosX = stripPos[0,:,0]
stripPosY = stripPos[:,0,1]
XS,YS=[],[]
Xval,Yval=[],[]
for evt in range(nEvents):
	actEvtPos = actEvtPosN[evt]
	if(False in np.isfinite(actEvtPos)):
		continue
	POSX = actEvtPos[0]
	POSY = actEvtPos[1]
	Xval=stripPosX-POSX
	Yval=stripPosY-POSY
	XS.append(Xval[np.argmin(np.abs(Xval))])
	YS.append(Yval[np.argmin(np.abs(Yval))])
	#ax.scatter(POSX,POSY,color="xkcd:robin's egg blue")
	#if(evt == 1000):
	#	break
#	ax.scatter(POSX,POSY,color='xkcd:pastel blue')
#	ax.scatter(recPos[eventID,0],recPos[eventID,1],color='crimson')
	#forceAspect(ax,aspect=0.75)

left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.005


rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(figsize=(8, 8))

ax_scatter = plt.axes(rect_scatter)
ax_scatter.tick_params(direction='in', top=True, right=True)
ax_histx = plt.axes(rect_histx)
ax_histx.tick_params(direction='in', labelbottom=False)
ax_histy = plt.axes(rect_histy)
ax_histy.tick_params(direction='in', labelleft=False)

# the scatter plot:
h = ax_scatter.hist2d(XS,YS,bins=17,range = [[-stripWx/2,stripWx/2],[-stripWy/2,stripWy/2]])
ax_scatter.set_xlim(-stripWx/2,stripWx/2)
ax_scatter.set_xlabel("Displacement from Strip Center (X) in mm")
ax_scatter.set_ylim(-stripWy/2,stripWy/2)
ax_scatter.set_ylabel("Displacement from Strip Center (Y) in mm")
plt.colorbar(h[3])
# now determine nice limits by hand:
binwidth = 0.25
xlim = stripWx/2
ylim = stripWy/2
#ax_scatter.set_xlim((-lim, lim))
#ax_scatter.set_ylim((-lim, lim))

xbins = np.arange(-xlim, xlim + binwidth, binwidth)
ybins = np.arange(-ylim, ylim + binwidth, binwidth)
ax_histx.hist(XS, bins=xbins)
ax_histy.hist(YS, bins=ybins, orientation='horizontal')

ax_histx.set_xlim(ax_scatter.get_xlim())
ax_histy.set_ylim(ax_scatter.get_ylim())

plt.savefig("subStripInteraction")
plt.show()

