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
	fig, axs = plt.subplots(types)
	plt.suptitle("ML - Det. Res. Residuals (Errors)")
	[axs[i].hist(resid.detach().cpu().numpy()[:,i]) for i in range(types)]
	[axs[i].set_xlabel(typeList[i]) for i in range(types)]
	[axs[i].set_ylabel("Counts") for i in range(types)]
	plt.show()
