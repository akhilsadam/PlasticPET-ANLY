def pltset(i,j):
	axs[i,j].set_xlabel(Xs[i])
	axs[i,j].set_ylabel(Ys[j])
	axs[i,j].legend(["Time Method","Attenuation Method"])

sz=6
alpha=0.2
Ys = ["Z-Position Residuals (mm)","Time Residuals (ns)"]
Xs = ["True Z-Position (mm)","Detected Photon Count"]
fig, axs = plt.subplots(2,2)
axs[0,0].scatter(actEvtPosN[:,2],err_ZrecPosT[0],s=sz, alpha=alpha)
axs[0,0].scatter(actEvtPosN[:,2],errorPosN[:,2],s=sz, alpha=alpha)
axs[0,0].set_ylim([-500, 500])
pltset(0,0)
detPhot = np.sum(left+right,axis=(1,2))
#print([i for i in range(len(detPhot)) if (detPhot[i]>4000)])
axs[1,0].scatter(detPhot,err_ZrecPosT[0],s=sz, alpha=alpha)
axs[1,0].scatter(detPhot,errorPosN[:,2],s=sz, alpha=alpha)
axs[1,0].set_xlim([0, 800])
axs[1,0].set_ylim([-500, 500])
pltset(1,0)
axs[0,1].scatter(actEvtPosN[:,2],err_ZrecPosT[1],s=sz, alpha=alpha)
#axs[0,1].scatter(actEvtPosN[:,2],errorPosN[:,2])
axs[0,1].text(0.01, 0.99, "Total Events = %1.0f " %(nEvents),verticalalignment='top',horizontalalignment='left',transform=axs[0,1].transAxes, fontsize=10)
axs[0,1].set_ylim([0, 2])
pltset(0,1)
axs[1,1].scatter(detPhot,err_ZrecPosT[1],s=sz, alpha=alpha)
#axs[1,1].scatter(detPhot,errorPosN[:,2])
axs[1,1].set_xlim([0, 800])
axs[1,1].set_ylim([0, 2])
pltset(1,1)
plt.suptitle(str(photoLen)+' photon residuals')
plt.tight_layout()
plt.savefig(Options.plotDIR+str(photoLen)+'photon_sipmTimeVSattRECMethods.png',dpi=1600)
plt.show()

