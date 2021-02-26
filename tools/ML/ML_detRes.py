if warmstart:
	model_path0 = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo.pt"
	model_path = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo2.pt"
else:
	model_path = str(ML_PATH)+"Data/ML_DET_RES_"+str(photoLen)+"_Photo.pt"
#-------------------------------------------------------
#vis
def ml_detRes_vis(inpT,expT):
	resid = inpT-expT
	length,types = resid.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	typeList = ["X-Resid (mm)","Y-Resid (mm)", "Z-Resid (mm)", "T-Resid (ns)"]
	rangeList = [[-200,200],[-200,200],[-1000,1000],[-2,2]]
	fig, axs = plt.subplots(types)
	plt.suptitle("ML - Det. Res. Residuals (Errors)")
	if(device=="cpu"):
		data = resid.detach().numpy()
	else:
		data = resid.detach().cpu().numpy()

	data[:,3] = (data[:,3]*n_EJ208)/(1000*nanosec*c_const)
	
	[axs[i].hist(data[:,i], bins=50, range=rangeList[i]) for i in range(types)]
	[axs[i].set_xlabel(typeList[i]) for i in range(types)]
	[axs[i].set_ylabel("Counts") for i in range(types)]
	plt.tight_layout()
	plt.savefig(str(ML_PATH)+"/Models/detRes_training_CNN_"+str(photoLen)+".png",dpi=600)
	plt.show()
def ml_detRes_vis2(inpT,expT,pl):
	length,types = inpT.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (ns)"]
	fig, axs = plt.subplots(2,2)
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

		ax.text(0.90, 0.90, "FIT:({0:.3f},{1:.3f}) ".format(intercept,slope),verticalalignment='top',horizontalalignment='left',transform = ax.transAxes,fontsize=8)

	plt.tight_layout()
	if(KNN):
		plt.suptitle("MLKNN (K="+str(pl)+") - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_KNN_"+str(pl)+"_.png",dpi=600)
		plt.show()
	else:
		plt.suptitle("MLCNN - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_CNN_"+str(pl)+".png",dpi=600)
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
		fig, axs = plt.subplots(2,2)
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
			ax.text(0.90, 0.90, "FIT: (intercept, slope) = ({0},{1}) ".format(intercept,slope),verticalalignment='top',horizontalalignment='right', fontsize=8)

		plt.tight_layout()
		plt.suptitle("MLKNN (K="+str(uik)+") - Det. Res. Predicted vs Actual")
		plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions_KNN_"+str(uik)+"_.png")
		plt.close()
		#plt.show()
def ml_detRes_vis_knn2(pltx,rmseP):
	fig, axs = plt.subplots(2,2)
	typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (also mm)"]
	for i in range(4):
		ax = axs[int(i/2),i%2]
		ax.scatter(pltx[:,i,:],rmseP[:,i,:])
		ax.set_xlabel("k-neighbors")
		ax.set_ylabel("RMSE in "+typeList[i])
	plt.suptitle("KNN RMSE by K-value - optimal # of neighbors")
	plt.savefig(str(ML_PATH)+"/Models/detRes_KNN_OptimalNeighbors.png")
	plt.close()
