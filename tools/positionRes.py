guess = [[0,100],[0,50],[0,50]]
displayBinsMM = np.array([0.5,0.5,10])#*0.25
axes = ["X(Depth/Width) ","Y(Height) ","Z(Length) "]
fig, axs = plt.subplots(3)
for i in range(3):
	errorPos = errorPosN[:,i]
	errorPos = errorPos[np.isfinite(errorPos)]
	print("-------------------\n" ,i,"- axis events: ",len(errorPos)," NaN events: ",(nEvents-len(errorPos)))

	xmin,xmax = -U[i],U[i]#np.min(errorPos),np.max(errorPos)
	axs[i].set_xlim(xmin/2,xmax/2)
	nbins = len(errorPos)
	dbins = int(L[i]/displayBinsMM[i])#8*int(2*U[i]/10)
	guess_std = 0.5
	axs[i].hist(errorPos,bins = dbins, range = (xmin,xmax), density=False)	
	hist, bin_edges = np.histogram(errorPos,bins=np.arange(xmin,xmax,L[i]/nbins))
	#hist = hist*nbins/(len(errorPos)*(xmax-xmin)) #- enable if density=true
	hist = (nbins/dbins)*len(errorPos)*hist/np.sum(hist)
	print(np.sum(hist)*(L[i]/nbins))
	#hist = hist*nbins
	#print(hist)
	bins = bin_edges[0:(len(bin_edges)-1)] + 0.5*(L[i]/nbins)
	#axs[i].plot(bins,hist)

	lnspc = np.linspace(xmin,xmax,len(hist))
	def pdf(x,m,s):
		#return	(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2)) #- enable if density=true
		return	(nbins/dbins)*len(errorPos)*(L[i]/nbins)*(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2))
	def spdf(x,df,scale):
		return (len(errorPos)*(L[i]/dbins))*stats.t.pdf(x,df,0,scale)
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

	#if (i==1):
		#student dist.
	#	sparam = [8,10]
		#m=Minuit(sfcn,sparam[0],sparam[1])
		#m.migrad()
		#sparam = m.values
	#	sparam,cov = curve_fit(spdf,bins,hist,p0=sparam)
	#	pdf_s = spdf(lnspc,sparam[0],sparam[1])
	#	axs[i].plot(lnspc, pdf_s, label = 'Norm')
	#	axs[i].text(0.99, -0.01, "SRSQ = %1.2f" %(RSQ(hist,pdf_s)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)		
		

	#param,cov = curve_fit(pdf,bins,hist, p0=[0,guess_std*stdG[i]])
	#print(param)
	#mu,var = stats.norm.fit(errorPos)

	axs[i].text(0.01, 0.99, "Total Events = %1.0f " %(nEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.79, "Interacted Events = %1.0f " %(nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.59, "Usable Events = %1.0f " %(len(errorPos)),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.39, "NaN Events = %1.0f " %(nEvents-len(errorPos)-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.01, 0.19, "Bin Size = %1.2f mm" %(displayBinsMM[i]),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)

	axs[i].text(0.99, 0.99, "Mean = %4.2f mm" %(param[0]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.79, "STD = %4.2f mm" %(param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.59, "FWHM = %4.2f mm" %(FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.39, "Error = +-%4.2f mm" %(0.5*FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
	axs[i].text(0.99, 0.19, "RSQ = %1.2f" %(RSQ(hist,pdf_g)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)

	axs[i].set_title(axes[i]+"predicted/expected difference histogram in mm")
	#axs[i].margins(2, 2) 
	print("MU  =", param[0])
	print("STD =", param[1])
	print("FWHM =", FWHMC*param[1]," mm")
	print("Error = +-", 0.5*FWHMC*param[1]," mm")
plt.tight_layout()
if Strip_Based_Reconstruction:
	plt.savefig(plotDIR+'PositionResolution_StripCounts.png')
else: 
	if SiPM_Based_Reconstruction:
		plt.savefig(plotDIR+'PositionResolution_SiPMCounts_True.png')
	else:
		plt.savefig(plotDIR+'PositionResolution_Strip_Endcounts.png')
plt.show()
