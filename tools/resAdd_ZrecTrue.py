#------------------------------------------------------------------------------------
fig,axs = plt.subplots(2,sharex=True)
axs[1].set_xlabel("Z-position (Length)")
axs[0].set_ylabel("Z-reconstructed position")

X=[]
Y=[]
Z=[]
for evt in range(nEvents):
	Y.append(zTensor[evt].tolist())
	X.append([actEvtPosN[evt,2]]*(nx*ny))
	Z.append(recSignal[evt].tolist())
X = np.array(list(flatten(X)))
Z = np.array(list(flatten(flatten(Z))))
Y = np.array(list(flatten(flatten(Y))))
X,Z,Y = nonzeroDatas(X,Z,Y)
X,Z,Y = nonnanDatas(X,Z,Y)
X,Z,Y = ZcutDatas(X,Z,Y)
axs[0].scatter(X,Y,s=8,c=Z,cmap='Spectral',norm=mpt_col.Normalize(vmin=0,vmax=400))
axs[0].text(0.99, 0.99, "color = # of reconstructed photons (normalized)",verticalalignment='top',horizontalalignment='right',transform=axs[0].transAxes, fontsize=8)
fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=0,vmax=400),cmap='Spectral'),ax=axs[0])

X=[]
Y=[]
Z=[]
for evt in range(nEvents):
	R=recSignal[evt]
	RS=np.sum(R[np.isfinite(R)])
	Y.append(recPos[evt,2])
	X.append(actEvtPosN[evt,2])
	Z.append(RS)

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
X,Z,Y = nonzeroDatas(X,Z,Y)
X,Z,Y = nonnanDatas(X,Z,Y)
X,Z,Y = ZcutDatas(X,Z,Y)
axs[1].scatter(X,Y,s=8,c=Z,cmap='Spectral',norm=mpt_col.Normalize(vmin=0,vmax=400))
axs[1].text(0.99, 0.99, "color = # of reconstructed photons (normalized)",verticalalignment='top',horizontalalignment='right',transform=axs[1].transAxes, fontsize=8)
fig.colorbar(cm.ScalarMappable(norm=mpt_col.Normalize(vmin=0,vmax=400),cmap='Spectral'),ax=axs[1])

plt.suptitle("Reconstructed Z-position vs True Z-position (Gamma Interaction Location)")
if SiPM_Based_Reconstruction:
	axs[0].set_title("Each SiPM block vs average z-position")
	axs[1].set_title("(by event)")
	plt.tight_layout()
	plt.savefig(plotDIR+'rec_zposVSzpos_SiPM.png')
else: 
	axs[0].set_title("Each strip block vs average z-position")
	axs[1].set_title("(by event)")
	plt.tight_layout()
	plt.savefig(plotDIR+'rec_zposVSzpos.png')
plt.show()
