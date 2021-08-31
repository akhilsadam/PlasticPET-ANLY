from tools.dimensions import *
from analyzeOptions import *
import numpy as np
from matplotlib import pyplot as plt
from iminuit import Minuit
def xyzResolution(errorPosIN,uninteractedEvents):
	guess = [[0,100],[0,50],[0,50]]
	displayBinsMM = np.array([0.5,0.5,5])#*0.25
	axes = ["X(Depth/Width) ","Y(Height) ","Z(Length) "]
	# fig, axs = plt.subplots(3)
	# for i in range(3):
	# 	axs[i].hist(errorPosIN[:,i],bins=200)
	# plt.savefig(Options.plotDIR+"test.png")
	# plt.close()
	fig, axs = plt.subplots(3)
	for i in range(3):
		errorPosI = errorPosIN[:,i]
		errorPosI = errorPosI[np.isfinite(errorPosI)]
		print("-------------------\n" ,i,"- axis events: ",len(errorPosI)," NaN events: ",(Options.nEvents-len(errorPosI)))

		xmin,xmax = -U[i],U[i]#np.min(errorPosI),np.max(errorPosI)
		axs[i].set_xlim(xmin/2,xmax/2)
		nbins = len(errorPosI)
		dbins = int(L[i]/displayBinsMM[i])#8*int(2*U[i]/10)
		axs[i].hist(errorPosI,bins = dbins, range = (xmin,xmax), density=False)	
		hist, bin_edges = np.histogram(errorPosI,bins=np.arange(xmin,xmax,L[i]/nbins))
		###hist = hist*nbins/(len(errorPosI)*(xmax-xmin)) #- enable if density=true
		hist = (nbins/dbins)*len(errorPosI)*hist/np.sum(hist)
		print(np.sum(hist)*(L[i]/nbins))
		bins = bin_edges[0:(len(bin_edges)-1)] + 0.5*(L[i]/nbins)

		lnspc = np.linspace(xmin,xmax,len(hist))
		def pdf(x,m,s):
			###return	(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2)) #- enable if density=true
			return	(nbins/dbins)*len(errorPosI)*(L[i]/nbins)*(1/(math.sqrt(2*math.pi)*s))*np.exp(-0.5*((x-m)**2)/(s**2))
		def spdf(x,df,scale):
			return (len(errorPosI)*(L[i]/dbins))*stats.t.pdf(x,df,0,scale)
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

		axs[i].text(0.01, 0.99, "Total Events = %1.0f " %(Options.nEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.01, 0.79, "Interacted Events = %1.0f " %(Options.nEvents-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.01, 0.59, "Usable Events = %1.0f " %(len(errorPosI)),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.01, 0.39, "NaN Events = %1.0f " %(Options.nEvents-len(errorPosI)-uninteractedEvents),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.01, 0.19, "Bin Size = %1.2f mm" %(displayBinsMM[i]),verticalalignment='top',horizontalalignment='left',transform=axs[i].transAxes, fontsize=12)

		axs[i].text(0.99, 0.99, "Mean = %4.2f mm" %(param[0]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.99, 0.79, "STD = %4.2f mm" %(param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.99, 0.59, "FWHM = %4.2f mm" %(FWHM*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.99, 0.39, "Error = +-%4.2f mm" %(0.5*FWHM*param[1]),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)
		axs[i].text(0.99, 0.19, "RSQ = %1.2f" %(RSQ(hist,pdf_g)),verticalalignment='top',horizontalalignment='right',transform=axs[i].transAxes, fontsize=12)

		axs[i].set_title(axes[i]+"predicted/expected difference histogram in mm")
		#axs[i].margins(2, 2) 
		print("MU  =", param[0])
		print("STD =", param[1])
		print("FWHM =", FWHM*param[1]," mm")
		print("Error = +-", 0.5*FWHM*param[1]," mm")
	plt.tight_layout()
	if Options.Strip_Based_Reconstruction:
		plt.savefig(Options.plotDIR+'PositionResolution_StripCounts_AR'+str(Options.ArrayNumber)+'.png')
	else: 
		if Options.SiPM_Based_Reconstruction:
			plt.savefig(Options.plotDIR+'PositionResolution_SiPMCounts_True_AR'+str(Options.ArrayNumber)+'.png')
		else:
			plt.savefig(Options.plotDIR+'PositionResolution_Strip_Endcounts_AR'+str(Options.ArrayNumber)+'.png')
	plt.show()
