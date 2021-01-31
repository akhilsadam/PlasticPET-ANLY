#------------------------------------------------------------------------------------
if Strip_Based_Reconstruction:
	print("ERROR! needs True Reconstruction")
	quit()
else:
	if SiPM_Based_Reconstruction:
		ds_strip = SiPM_Downsample(strip)	
		ds_recSignal = SiPM_Downsample(recSignal)
		signalRatio = (ds_strip/ds_recSignal)
	else:
		signalRatio = (strip/recSignal)

factor = signalRatio.flatten()
sEvents = len(factor)
factor = factor[np.isfinite(factor)]
factor = factor[np.nonzero(factor)]


plt.figure(figsize=(8, 8))
axs = plt.subplot(111)
#sbins=50
#srange=400
#axs.hist(factor,bins = sbins,range=[-srange/2,srange/2])
#x = np.linspace(-200,200,399)

guess = [20,10]
displayBinsMM = 5

xmin,xmax = -400,400#np.min(errorPos),np.max(errorPos)
axs.set_xlim(xmin/2,xmax/2)
nbins = len(factor)
dbins = int((xmax-xmin)/displayBinsMM)#8*int(2*U[i]/10)
guess_std = 0.5
axs.hist(factor,bins = dbins, range = (xmin,xmax), density=False)	
hist, bin_edges = np.histogram(factor,bins=np.arange(xmin,xmax,(xmax-xmin)/nbins))
#hist = hist*nbins/(len(errorPos)*(xmax-xmin)) #- enable if density=true
hist = (nbins/dbins)*len(factor)*hist/np.sum(hist)
#hist = hist*nbins
#print(hist)
bins = bin_edges[0:(len(bin_edges)-1)] + 0.5*((xmax-xmin)/nbins)
#axs[i].plot(bins,hist)

lnspc = np.linspace(xmin,xmax,nbins-1)
def pdf(x,m,s):
	#return	(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2)) #- enable if density=true
	return	(nbins/dbins)*len(factor)*((xmax-xmin)/nbins)*(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2))
def spdf(x,m,scale,df):
	return (len(factor)*((xmax-xmin)/dbins))*stats.t.pdf(x,df,m,scale)
def fcn(m,s):
	return np.sum(np.power((hist-pdf(bins,m,s)),2))
def sfcn(df,scale):
	return np.sum(np.power((hist-spdf(bins,df,scale)),2))
fcn.errordef = Minuit.LEAST_SQUARES
sfcn.errordef = Minuit.LEAST_SQUARES

param = guess
m=Minuit(fcn,param[0],param[1])
m.migrad()
param = m.values
pdf_g = pdf(lnspc,param[0],param[1])
axs.plot(lnspc, pdf_g, label = 'Norm')


#student dist.
sparam = [20,5,1]
#m=Minuit(sfcn,sparam[0],sparam[1])
#m.migrad()
#sparam = m.values
sparam,cov = curve_fit(spdf,bins,hist,p0=sparam)
pdf_s = spdf(lnspc,sparam[0],sparam[1],sparam[2])
axs.plot(lnspc, pdf_s, label = 'Norm')
s_sig = math.sqrt(np.sum(np.power((sparam[0]-factor),2))/(len(factor)-1))

		
	

#param,cov = curve_fit(pdf,bins,hist, p0=[0,guess_std*stdG[i]])
#print(param)
#mu,var = stats.norm.fit(errorPos)
axs.text(0.01, 0.99, "Total Events = %1.0f" %(nEvents),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
if SiPM_Based_Reconstruction:
	axs.text(0.01, 0.94, "Total Event SiPM Pairs = %1.0f" %(sEvents),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
	axs.text(0.01, 0.89, "Usable Event SiPM Pairs = %1.0f" %(len(factor)),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
else:
	axs.text(0.01, 0.94, "Total Event Strips = %1.0f" %(sEvents),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
	axs.text(0.01, 0.89, "Usable Event Strips = %1.0f" %(len(factor)),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.84, "Bin Size = %1.0f" %(displayBinsMM),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.79, "Student's T: Mean = %4.2f" %(sparam[0]),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.74, "Student's T: Df = %4.2f" %(sparam[2]),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.69, "Sample: STD = %4.2f" %(s_sig),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.64, "Sample: FWHM = %1.2f" %(FWHMC*s_sig),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.59, "Sample: Error = +-%1.2f" %(FWHMC*s_sig/2),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)
axs.text(0.01, 0.54, "Sample: RSQ = %1.2f" %(RSQ(hist,pdf_s)),verticalalignment='top',horizontalalignment='left',transform=axs.transAxes, fontsize=12)

axs.text(0.99, 0.99, "Gaussian: Mean = %4.2f" %(param[0]),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes, fontsize=12)
axs.text(0.99, 0.94, "Gaussian: STD = %4.2f" %(param[1]),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes, fontsize=12)
axs.text(0.99, 0.89, "Gaussian: FWHM = %4.2f" %(FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes, fontsize=12)
axs.text(0.99, 0.84, "Gaussian: Error = +-%4.2f" %(0.5*FWHMC*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes, fontsize=12)
axs.text(0.99, 0.79, "Gaussian: RSQ = %1.2f" %(RSQ(hist,pdf_g)),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes, fontsize=12)
if SiPM_Based_Reconstruction:
	axs.set_title("Signal amplitude actual/predicted ratio histogram for each SiPM pair")
	plt.tight_layout()
	plt.savefig('signalResolution_SiPM.png')
else: 
	axs.set_title("Signal amplitude actual/predicted ratio histogram for each strip")
	plt.tight_layout()
	plt.savefig('signalResolution.png')
plt.show()
