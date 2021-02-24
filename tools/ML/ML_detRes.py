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
	rangeList = [[-200,200],[-200,200],[-1000,1000],[-200,200]]
	fig, axs = plt.subplots(types)
	plt.suptitle("ML - Det. Res. Residuals (Errors)")
	if(device=="cpu"):
		data = resid.detach().numpy()
	else:
		data = resid.detach().cpu().numpy()

	data[:,3] = (data[:,3]*n_EJ208)/(1000*nanosec*c_const)
	
	[axs[i].hist(data[:,i], range=rangeList[i]) for i in range(types)]
	[axs[i].set_xlabel(typeList[i]) for i in range(types)]
	[axs[i].set_ylabel("Counts") for i in range(types)]
	plt.show()
def ml_detRes_vis2(inpT,expT):
	length,types = inpT.shape
	if(types!=4):
		print("ERROR = type shape not equal. Quitting.")
		quit()

	typeList = ["X (mm)","Y (mm)", "Z (mm)", "T (ns)"]
	fig, axs = plt.subplots(2,2)
	plt.suptitle("MLCNN - Det. Res. Predicted vs Actual")
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
		x,y = expTS[:,i],inpTS[:,i]

		ax.scatter(x,y,s=6,color='#0066f0')
		ax.set_xlabel(typeList[i])
		ax.set_ylabel("Pred_"+typeList[i])

		X = sm.add_constant(x)
		res = sm.OLS(y, X).fit()
		
		st, data, ss2 = summary_table(res, alpha=0.05)
		fittedvalues = data[:,2]
		predict_mean_se  = data[:,3]
		predict_mean_ci_low, predict_mean_ci_upp = data[:,4:6].T #the confidence band (95%)
		predict_ci_low, predict_ci_upp = data[:,6:8].T #the prediction band (95%)

		ax.fill_between(x,predict_ci_low,predict_ci_upp, color='lightsteelblue', alpha=0.4)
		ax.fill_between(x,predict_mean_ci_low,predict_mean_ci_upp, color='lightslategrey', alpha=0.4)
		ax.plot(x,fittedvalues,color='red')

		ax.plot(ax.get_xticks(),ax.get_xticks(),color='darkred')

	plt.tight_layout()
	plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions.png")
	plt.show()
