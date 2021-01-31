if Creation:
	#--- produced
	fig,axs = plt.subplots(ny,nx,figsize=(10,10),sharex=True,sharey=True)
	fig.suptitle("Created Photon Distributions")
	for j in range(ny):
		for i in range(nx):
			counts = strip[:,j,i]
			mx = max(counts)
			axs[j,i].hist(counts,bins = int(mx/100),range = [1,mx])
	axs[ny-1,int(nx/2)].set_xlabel("Photons in an interacted Event")
	axs[int(ny/2),0].set_ylabel("Interacted Events")
	axs[0,nx-1].text(.95,.95,"Interacted Events = %1.0f" %(nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='right',transform=axs[0,nx-1].transAxes,fontsize=10)
	plt.tight_layout()
	plt.subplots_adjust(wspace=0,hspace=0)
	plt.savefig("Created Photon Distributions.png")
	plt.show()
if Detection:
	mx=400
	#--- produced
	fig,axs = plt.subplots(ny,nx,figsize=(10,10),sharex=True,sharey=True)
	fig.suptitle("Detected Photon Distributions")
	for j in range(ny):
		for i in range(nx):
			counts = left[:,j,i]+right[:,j,i]
			counts = counts[np.nonzero(counts)]
			axs[j,i].hist(counts,bins = int(mx/10),range = [0,mx])
	axs[ny-1,int(nx/2)].set_xlabel("Left+Right Photons in an interacted Event")
	axs[int(ny/2),0].set_ylabel("Interacted Events")
	axs[0,nx-1].text(.95,.95,"Interacted Events = %1.0f" %(nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='right',transform=axs[0,nx-1].transAxes,fontsize=10)
	plt.tight_layout()
	plt.subplots_adjust(wspace=0,hspace=0)
	plt.savefig("Detected Photon Distributions.png")
	plt.show()
if PD:
	#--- produced
	mx = 1
	fig,axs = plt.subplots(ny,nx,figsize=(10,10),sharex=True,sharey=True)
	fig.suptitle("Produced-Detected Ratio")
	for j in range(ny):
		for i in range(nx):
			counts = left[:,j,i]+right[:,j,i]
			strp = strip[:,j,i]
			idc = np.nonzero(strp)
			axs[j,i].scatter(strp[idc],counts[idc]/strp[idc])
			axs[j,i].set_ylim(0,mx)
	axs[ny-1,int(nx/2)].set_xlabel("Photons in an interacted Event")
	axs[int(ny/2),0].set_ylabel("Interacted Events")
	axs[0,nx-1].text(.95,.95,"Interacted Events = %1.0f" %(nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='right',transform=axs[0,nx-1].transAxes,fontsize=10)
	plt.tight_layout()
	plt.subplots_adjust(wspace=0,hspace=0)
	plt.savefig("Produced-Detected Ratio.png")
	plt.show()
