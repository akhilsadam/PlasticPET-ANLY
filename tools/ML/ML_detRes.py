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

	data[3] = (data[3]*n_EJ208)/(1000*nanosec*c_const)
	
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
	fig, axs = plt.subplots(types)
	plt.suptitle("ML - Det. Res. Predicted vs Actual")
	if(device=="cpu"):
		inpTS = inpT.detach().numpy()
		expTS = expT.detach().numpy()
	else:
		inpTS = inpT.detach().cpu().numpy()
		expTS = expT.detach().cpu().numpy()

	inpTS[3] = (inpTS[3]*n_EJ208)/(1000*nanosec*c_const)
	expTS[3] = (expTS[3]*n_EJ208)/(1000*nanosec*c_const)

	[axs[i].scatter(expTS[:,i],inpTS[:,i]) for i in range(types)]
	[axs[i].set_xlabel(typeList[i]) for i in range(types)]
	[axs[i].set_ylabel("Pred_"+typeList[i]) for i in range(types)]
	plt.tight_layout()
	plt.savefig(str(ML_PATH)+"/Models/detRes_Predictions.png")
	plt.show()
