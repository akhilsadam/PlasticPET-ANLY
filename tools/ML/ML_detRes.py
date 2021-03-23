if warmstart:
	model_path0 = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo.pt"
	model_path = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo2.pt"
else:
	model_path = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo.pt"
#-------------------------------------------------------
unitList = ["mm","mm", "mm", "ns"]
typeList = ["X-Resid (mm)","Y-Resid (mm)", "Z-Resid (mm)", "T-Resid (ns)"]
rangeList = [[-40,40],[-30,30],[-50,50],[-0.3,0.3]]
binList = [5,5,25,0.1]
locX = 0.95
locY = 0.05
spaY = 0.10
nbins=50
#-------------------------------------------------------
MarginalPLT = True
from mpl_toolkits.axes_grid1 import make_axes_locatable
def marginalPLT(ax,x,y,i):
	ax.set_aspect(1.)
	# create new axes on the right and on the top of the current axes
	divider = make_axes_locatable(ax)
	# below height and pad are in inches
	ax_histx = divider.append_axes("top", 0.2, pad=0.05, sharex=ax)
	ax_histy = divider.append_axes("right", 0.2, pad=0.05, sharey=ax)
	# now determine nice limits by hand:
	binwidth = binList[i]
	xymax = max(np.max(np.abs(x)), np.max(np.abs(y)))
	lim = (int(xymax/binwidth) + 1)*binwidth
	bins = np.arange(-lim, lim + binwidth, binwidth)
	ax_histx.hist(x, bins=bins)
	ax_histy.hist(y, bins=bins, orientation='horizontal')
	ax_histx.text(locX,locY+spaY, "Bin={0:.1f} {1}".format(binwidth,unitList[i]),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

	# the xaxis of ax_histx and yaxis of ax_histy are shared with ax,
	# thus there is no need to manually adjust the xlim and ylim of these
	# axis.
	#ax_histx.set_yticks([0, 50, 100])
	#ax_histy.set_xticks([0, 50, 100])
	ax_histx.get_xaxis().set_visible(False)
	ax_histy.get_yaxis().set_visible(False)
	ax.tick_params(labelsize=8)
	ax_histx.tick_params(labelsize=8)
	ax_histy.tick_params(labelsize=8)

	plt.margins(0,0)
def marginalPLT2(ax,x,y,i):
	#ax.set_aspect(1.)
	# create new axes on the right and on the top of the current axes
	divider = make_axes_locatable(ax)
	# below height and pad are in inches
	ax_histx = divider.append_axes("top", 0.2, pad=0.05, sharex=ax)
	ax_histy = divider.append_axes("right", 0.2, pad=0.05, sharey=ax)
	# now determine nice limits by hand:
	binwidth = binList[i]
	xmax = np.max(np.abs(x))
	lim = (int(xmax/binwidth) + 1)*binwidth
	bins = np.arange(-lim, lim + binwidth, binwidth)
	binzy = 20
	ymax = np.max(np.abs(y))
	binwidthy = int(ymax/binzy)
	limy = (int(ymax/binwidthy) + 1)*binwidthy
	ybins = np.arange(0, limy + binwidthy, binwidthy)
	ax_histx.hist(x, bins=bins)
	ax_histy.hist(y, bins=ybins, orientation='horizontal')
	ax_histx.text(locX,locY+spaY, "Bin={0:.1f} {1}".format(binwidth,unitList[i]),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

	# the xaxis of ax_histx and yaxis of ax_histy are shared with ax,
	# thus there is no need to manually adjust the xlim and ylim of these
	# axis.
	#ax_histx.set_yticks([0, 50, 100])
	#ax_histy.set_xticks([0, 50, 100])
	ax_histx.get_xaxis().set_visible(False)
	ax_histy.get_yaxis().set_visible(False)
	ax.tick_params(labelsize=8)
	ax_histx.tick_params(labelsize=8)
	ax_histy.tick_params(labelsize=8)

	plt.margins(0,0)
#-------------------------------------------------------
#vis
def ml_detRes_vis(inpT,expT,pl):
	resid = inpT-expT
	length,types = resid.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	fig, axs = plt.subplots(types,constrained_layout=True)
	plt.suptitle("ML - Det. Res. Residuals (Errors)")
	if(device=="cpu"):
		data = resid.detach()#.numpy()
	else:
		data = resid.detach().cpu()#.numpy()

	data[:,3] = (data[:,3]*n_EJ208)/(1000*nanosec*c_const)

	for i in range(types):
	
		result = axs[i].hist(data[:,i].numpy(), bins=nbins, range=rangeList[i],color='#0022D0')
		axs[i].set_xlabel(typeList[i])
		axs[i].set_ylabel("Counts")
		mu = torch.mean(data[:,i])
		std = math.sqrt(torch.var(data[:,i]))
		dx = result[1][1] - result[1][0]
		gy = result[0]
		gx = result[1][0:(len(result[1])-1)] + 0.5*dx
		def gaussian(x,mu,sig):
			return stats.norm.pdf(x, mu, sig)*length*dx
		popt,pcov = curve_fit(gaussian,gx,gy,p0=[mu,std])

		x = np.linspace(rangeList[i][0], rangeList[i][1], 100)
		
		axs[i].plot(x,gaussian(x,popt[0],popt[1]), color='red')
		#axs[i].plot(x,gaussian(x,popt[0],popt[1],popt[2]), color='red')
		axs[i].text(0.03, 0.90, "Mean,SD,FWHM = ({0:.3f},{1:.3f},{2:.3f}) ".format(popt[0],popt[1],FWHMC*popt[1]),verticalalignment='top',horizontalalignment='left',transform = axs[i].transAxes,fontsize=8)
		axs[i].text(0.97, 0.90, "{0} Events".format(length),verticalalignment='top',horizontalalignment='right',transform = axs[i].transAxes,fontsize=8)

	
	if(KNN):
		plt.suptitle("MLKNN (K="+str(pl)+") - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_training_KNN_"+str(pl)+".png",dpi=600)
		#plt.show()
		plt.close()
	else:
		plt.suptitle("MLCNN - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_training_CNN_"+str(photoLen)+".png",dpi=600)
		#plt.show()
		plt.close()

def ml_detRes_vis2(inpT,expT,pl):
	length,types = inpT.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (ns)"]
	fig, axs = plt.subplots(2,2, constrained_layout=True)
	if(device=="cpu"):
		inpTS = inpT.detach().numpy()
		expTS = expT.detach().numpy()
	else:
		inpTS = inpT.detach().cpu().numpy()
		expTS = expT.detach().cpu().numpy()

	inpTS[:,3] = (inpTS[:,3]*n_EJ208)/(1000*nanosec*c_const)
	expTS[:,3] = (expTS[:,3]*n_EJ208)/(1000*nanosec*c_const)

	for i in range(types):
		ax = axs[int(i/2),i%2]
		x = expTS[:,i]
		y = inpTS[:,i]

		ax.scatter(x,y,s=4,color='#0066f0')
		ax.set_xlabel(typeList[i])
		ax.set_ylabel("Pred_"+typeList[i])

		X = sm.add_constant(x)
		model = sm.OLS(y, X)
		res = model.fit()
		intercept, slope = res.params
		st, data, ss2 = summary_table(res, alpha=0.05)	
	
		x_arr = np.zeros(shape=(len(x),1))
		x_arr[:,0] = x
		datas = np.hstack((x_arr,data))
		#print(datas.shape)
		#print(data)
		data = datas[datas[:,0].argsort()]
		#print(data[:,0])
		#

		x0 = data[:,0]
		data=data[:,1:13]
		fittedvalues = data[:,2]
		predict_mean_se  = data[:,3]
		predict_mean_ci_low, predict_mean_ci_upp = data[:,4:6].T #the confidence band (95%)
		predict_ci_low, predict_ci_upp = data[:,6:8].T #the prediction band (95%)

		ax.fill_between(x0,predict_ci_low,predict_ci_upp, color='black', facecolor='lightsteelblue', alpha=0.7)
		ax.fill_between(x0,predict_mean_ci_low,predict_mean_ci_upp, color='black', facecolor='lightslategrey', alpha=0.7)
		#ax.plot(x0,predict_ci_low,color='black')
		#ax.plot(x0,predict_ci_upp,color='black')
		#ax.plot(x0,predict_mean_ci_low,color='black')
		#ax.plot(x0,predict_mean_ci_upp,color='black')
		ax.plot(x0,fittedvalues,color='red')
		ax.plot(ax.get_xticks(),ax.get_xticks(),color='darkred')
		ax.set_xlim(min(x),max(x))	
		ax.set_ylim(min(x),max(x))
		ax.text(locX,locY, "FIT:({0:.3f},{1:.3f})".format(intercept,slope),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)
		ax.text(locX,locY+2*spaY, "{0} Events".format(length),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

		#marginal axes
		if MarginalPLT:
			marginalPLT(ax,x,y,i)

	if(KNN):
		plt.suptitle("MLKNN (K="+str(pl)+") - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_KNN_"+str(pl)+"_.png",bbox_inches='tight',dpi=600)
		plt.show()
	else:
		plt.suptitle("MLCNN - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_CNN_"+str(pl)+".png",bbox_inches='tight',dpi=600)
		plt.show()

def ml_detRes_vis_knn(inpT,expT,uik,noplt):
	length,types = inpT.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	if(device=="cpu"):
		inpTS = inpT.detach().numpy()
		expTS = expT.detach().numpy()
	else:
		inpTS = inpT.detach().cpu().numpy()
		expTS = expT.detach().cpu().numpy()

	inpTS[:,3] = (inpTS[:,3]*n_EJ208)/(1000*nanosec*c_const)
	expTS[:,3] = (expTS[:,3]*n_EJ208)/(1000*nanosec*c_const)


	rmseL = np.zeros(shape=types)
	#stdL  = torch.zeros(size=types)
	
	if(noplt):
		for i in range(types):
			x,y = expTS[:,i],inpTS[:,i]
			rmseL[i] = rmse(x,y)

		return rmseL
	else:
		typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (ns)"]
		fig, axs = plt.subplots(2,2, constrained_layout=True)
		for i in range(types):
			ax = axs[int(i/2),i%2]
			x,y = expTS[:,i],inpTS[:,i]

			rmseL[i] = rmse(x,y)		

			ax.scatter(x,y,s=4,color='#0066f0')
			ax.set_xlabel(typeList[i])
			ax.set_ylabel("Pred_"+typeList[i])

			X = sm.add_constant(x)
			res = sm.OLS(y, X).fit()
			intercept, slope = res.params
			
			st, data, ss2 = summary_table(res, alpha=0.05)
			fittedvalues = data[:,2]
			predict_mean_se  = data[:,3]
			predict_mean_ci_low, predict_mean_ci_upp = data[:,4:6].T #the confidence band (95%)
			predict_ci_low, predict_ci_upp = data[:,6:8].T #the prediction band (95%)

			ax.fill_between(x,predict_ci_low,predict_ci_upp, color='black', facecolor='lightsteelblue', alpha=0.7)
			ax.fill_between(x,predict_mean_ci_low,predict_mean_ci_upp, color='black', facecolor='lightslategrey', alpha=0.7)
			ax.plot(x,fittedvalues,color='red')
			ax.plot(ax.get_xticks(),ax.get_xticks(),color='darkred')
			ax.set_xlim(min(x),max(x))	
			ax.set_ylim(min(x),max(x))
			ax.text(locX,locY, "FIT:({0:.3f},{1:.3f})".format(intercept,slope),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)
			ax.text(locX,locY+2*spaY, "{0} Events".format(length),verticalalignment='bottom',horizontalalignment='right',transform = ax.transAxes,fontsize=8)

			#marginal axes
			if MarginalPLT:
				marginalPLT(ax,x,y,i)

		plt.suptitle("MLKNN (K="+str(uik)+") - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_KNN_"+str(uik)+"_.png",bbox_inches='tight',dpi=600)
		plt.close()
		return rmseL
		#plt.show()
def ml_detRes_vis_knn2(pltx,rmseP):
	fig, axs = plt.subplots(2,2)
	typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (ns)"]
	for i in range(4):
		ax = axs[int(i/2),i%2]
		ax.scatter(pltx[:,i,:],rmseP[:,i,:])
		ax.set_xlabel("k-neighbors")
		ax.set_ylabel("RMSE in "+typeList[i])
	plt.suptitle("KNN RMSE by K-value - optimal # of neighbors")
	plt.savefig(str(ML_PATH)+"/Models/detRes_KNN_OptimalNeighbors.png")
	plt.close()
