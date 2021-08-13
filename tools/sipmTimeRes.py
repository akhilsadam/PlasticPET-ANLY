guess = [[0,100],[0,50],[0,50]]
units = ["mm","ns","ns"]
displayBinsMM = np.array([2,0.05,0.05])#*0.25
axes = ["Z Resolution via Time","Gamma Time Resolution","Data Collection Time"]
TL = [[-UZ,UZ],[-2,2],[-8,20]]
fig, axs = plt.subplots(3)
sipmTimeplots = [err_ZrecPosT[0],err_ZrecPosT[1],ZrecPosT[2]]
for i in range(3):
	errorPos = sipmTimeplots[i]
	errorPos = errorPos[np.isfinite(errorPos)]
	print("-------------------\n" ,i,"- axis events: ",len(errorPos)," NaN events: ",(nEvents-len(errorPos)))

	xmin,xmax = TL[i]#np.min(errorPos),np.max(errorPos)
	axs[i].set_xlim(xmin/2,xmax/2)
	nbins = len(errorPos)
	LENGTH = TL[i][1] - TL[i][0]
	dbins = int(LENGTH/displayBinsMM[i])#8*int(2*U[i]/10)
	guess_std = 0.5
	axs[i].hist(errorPos,bins = dbins, range = (xmin,xmax), density=False)	
	hist, bin_edges = np.histogram(errorPos,bins=np.arange(xmin,xmax,LENGTH/nbins))
	#hist = hist*nbins/(len(errorPos)*(xmax-xmin)) #- enable if density=true
	hist = (nbins/dbins)*len(errorPos)*hist/np.sum(hist)
	print(np.sum(hist)*(LENGTH/nbins))
	#hist = hist*nbins
	#print(hist)
	bins = bin_edges[0:(len(bin_edges)-1)] + 0.5*(LENGTH/nbins)
	#axs[i].plot(bins,hist)

	lnspc = np.linspace(xmin,xmax,len(hist))
	def pdf(x,m,s):
		#return	(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2)) #- enable if density=true
		return	(nbins/dbins)*len(errorPos)*(LENGTH/nbins)*(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2))
	def spdf(x,df,scale):
		return (len(errorPos)*(LENGTH/dbins))*stats.t.pdf(x,df,0,scale)
	def fcn(m,s):
		return np.sum(np.power((hist-pdf(bins,m,s)),2))
	def sfcn(df,scale):
		return np.sum(np.power((hist-spdf(bins,df,scale)),2))
	fcn.errordef = Minuit.LEAST_SQUARES
	sfcn.errordef = Minuit.LEAST_SQUARES

	param = guess[i]
	m=Minuit(fcn,param[0],param[1])
	m.migrad()
	param = m.values
	pdf_g = pdf(lnspc,param[0],param[1])
	axs[i].plot(lnspc, pdf_g, label = 'Norm')


	axs[i].text(0.01, 0.99, "Total Events = %1.0f " %(nEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.79, "Interacted Events = %1.0f " %(nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.59, "Usable Events = %1.0f " %(len(errorPos)),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.39, "NaN Events = %1.0f " %(nEvents-len(errorPos)-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.19, "Bin Size = %1.2f" %(displayBinsMM[i]),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)

	axs[i].text(0.99, 0.99, "Mean = %4.2f" %(param[0]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.79, "STD = %4.2f" %(param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.59, "FWHM = %4.2f" %(FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.39, "Error = +-%4.2f" %(0.5*FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.19, "RSQ = %1.2f" %(RSQ(hist,pdf_g)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)

	axs[i].set_title(str(Options.photoLen)+" photon " +axes[i])
	axs[i].set_xlabel(units[i])

	print("MU  =", param[0])
	print("STD =", param[1])
	print("FWHM =", FWHMC*param[1])
	print("Error = +-", 0.5*FWHMC*param[1])
plt.tight_layout()
if Options.Strip_Based_Reconstruction:
	pass#plt.savefig(Options.plotDIR+'PositionResolution_StripCounts.png')
else: 
	if Options.SiPM_Based_Reconstruction:
		pass#plt.savefig(Options.plotDIR+'PositionResolution_SiPMCounts_True.png')
	else:
		plt.savefig(Options.plotDIR+'SiPM_TimeRes_'+str(Options.photoLen)+'_AR_'+str(Options.ArrayNumber)+'.png')
plt.close()
