fig,axs = plt.subplots(2,sharex=True)
axs[1].set_xlabel("Z-position (Length)")
axs[0].set_ylabel("# of reconstructed photons")
axs[1].set_ylabel("# of reconstructed photons")

X=[]
Y=[]
Z=[]
for evt in range(nEvents):
	Y.append(signalRatio[evt].tolist())
	X.append([actEvtPosN[evt,2]]*(nx*ny))
	Z.append([actEvtPosN[evt,0]]*(nx*ny))
X = np.array(list(flatten(X)))
Z = np.array(list(flatten(Z)))
Y = np.array(list(flatten(flatten(Y))))
X,Z,Y = nonzeroDatas(X,Z,Y)
X,Z,Y = nonnanDatas(X,Z,Y)
X,Z,Y = ZcutDatas(X,Z,Y)
axs[0].scatter(X,Y,s=8,c=Z,cmap='Spectral',norm=mpt_col.Normalize(vmin=-UX,vmax=UX))
axs[0].text(0.99, 0.99, "color = negative interaction depth (distance penetrated into crystal)\n positive values are closer to vertex",verticalalignment='top',horizontalalignment='right',transform=axs[0].transAxes, fontsize=8)
fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=-UX,vmax=UX), cmap='Spectral'),ax=axs[0])

X=[]
Y=[]
Z=[]
for evt in range(nEvents):
	R=recSignal[evt]
	RS=np.sum(R[np.isfinite(R)])
	Y.append(RS)
	X.append(actEvtPosN[evt,2])
	Z.append(actEvtPosN[evt,0])

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
X,Z,Y = nonzeroDatas(X,Z,Y)
X,Z,Y = nonnanDatas(X,Z,Y)
X,Z,Y = ZcutDatas(X,Z,Y)
axs[1].scatter(X,Y,s=8,c=Z,cmap='Spectral',norm=mpt_col.Normalize(vmin=-UX,vmax=UX))
axs[1].text(0.99, 0.99, "color = negative interaction depth (distance penetrated into crystal)\n positive values are closer to vertex",verticalalignment='top',horizontalalignment='right',transform=axs[1].transAxes, fontsize=8)
fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=-UX,vmax=UX), cmap='Spectral'),ax=axs[1])

plt.suptitle("Reconstructed Photon Count Histogram (vs Z-position)")
if SiPM_Based_Reconstruction:
	axs[0].set_title("Each SiPM pair vs z-position")
	axs[1].set_title("Both side totals (by event)")
	plt.tight_layout()
	plt.savefig('reconstructedPhotVSzpos_SiPM.png')
else: 
	axs[0].set_title("Each strip vs z-position")
	axs[1].set_title("Both side totals (by event)")
	plt.tight_layout()
	plt.savefig('reconstructedPhotVSzpos.png')
plt.show()
