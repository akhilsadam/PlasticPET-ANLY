#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file # import and setup
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file # PATH and vis
#OVERWRITE PATH
model_path = str(ML_PATH)+"Data/ML_DET_RES_KNN_"+str(photoLen)+"_Photo.pt"
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
folds = 5
batch_size = 1 # set of events to train at once
epochs = 4
lr = 0.0000001
momentum = 0.9 #SGD
beta1 = 0.5 
beta2 = 0.999 #ADAM
#-------------------------------------------------------------------------------
#Preprocessing:
with open(ML_PATH+'ML_detRes_preProcess.py') as f: exec(f.read()) # helper file # preprocessing
inputTensor,expectedTensor = MLDRESpreprocess(photoLen)
if("PCA" in MLOPT):
	PATH_OPT=PATH_OPT+"PCA"
	pcaSTD = False
if("STD" in MLOPT):
	PATH_OPT=PATH_OPT+"-STD"
	pcaSTD = True
if("MAHA" in MLOPT):
	PATH_OPT=PATH_OPT+"-MAHA"
	pcaMAHA = True
#---
print(":OPTIONS- ",PATH_OPT)
if("PCA" in MLOPT):
	with open(ML_PATH+'ML_PCA.py') as f: exec(f.read()) # helper file # PATH and vis
	print("Loaded PCA")
#-------------------------------------------------------
length = inputTensor.shape[0]
frac = 0.75
splitList = [int(length*frac),length - int(length*frac)]
initK = 2#4
finalK = 40#80
stepK = 5
veclen = int((finalK+stepK-initK)/stepK)
#n = int(length/folds)
epochs = 5
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Model Definition:
with open(ML_PATH+'ML_Model_detRes_KNN.py') as f: exec(f.read()) # helper file # model definition
drnet = DRKNN()
drnet.eval() #not train!
drnet._initialize_weights()
print(drnet)
#-------------------------------------------------------------------------------
def knntest(knn_neighbors):
	drnet.setK(knn_neighbors)
	listset = list(range(length))
	random.shuffle(listset)
	dataInd,testInd = torch.split(torch.tensor(listset),splitList)
	dataTensorX = inputTensor[dataInd]
	inptTensor = inputTensor[testInd]
	dataTensorY = expectedTensor[dataInd]
	expectTensor = expectedTensor[testInd]
	#dataTensorX,dataTensorY,inputTensor,expectTensor
	out,outs = drnet(dataTensorX,dataTensorY,inptTensor)
	ml_detRes_vis(out,expectTensor,knn_neighbors)
	ml_detRes_vis2(out,expectTensor,knn_neighbors)
	return True
def kvispp(knn_neighbors):
	drnet.setK(knn_neighbors)
	listset = list(range(length))
	random.shuffle(listset)
	dataInd,testInd = torch.split(torch.tensor(listset),splitList)
	dataTensorX = inputTensor[dataInd]
	inptTensor = inputTensor[testInd]
	dataTensorY = expectedTensor[dataInd]
	expectTensor = expectedTensor[testInd]
	#dataTensorX,dataTensorY,inputTensor,expectTensor
	out,indxs = drnet(dataTensorX,dataTensorY,inptTensor)
	
	dlength = dataTensorY.shape[0]
	kvals = dataTensorY[indxs]
	nkvals = torch.ones((indxs.shape[0],dlength-knn_neighbors,4))
	#print(dataTensorY.shape)
	#print(nkvals.shape)
	#print(indxs.shape)
	#print(dlength)
	for i in range(indxs.shape[0]):
		u = 0
		for j in range(dlength):
			if(j not in indxs[i]):
				nkvals[i,u,:] = dataTensorY[j,:]
				u = u + 1
	
	return out,kvals,nkvals,expectTensor

def kerr(knn_neighbors):
	out,kvals,nkvals,expectTensor = kvispp(knn_neighbors)
	errs = torch.pow(torch.sum(torch.pow(out-expectTensor,2),dim = 1),0.5)
	print(len(errs))
	fig,axs = plt.subplots(2,2,tight_layout=True)	
	for i in range(4):
		ax = axs[int(i/2),i%2]
		x,y = expectTensor[:,i], errs
		ax.scatter(x,y)
		ax.set_xlabel(NM[i] + ' [mm]')
		ax.set_ylabel('Error [mm]')
		if MarginalPLT:
			marginalPLT2(ax,x.numpy(),y.numpy(),i)

	plt.suptitle("KNN Output Space Error")
	plt.savefig(str(ML_PATH)+"/Models/detRes_KNN_ERRN.png")
	plt.show()

def kvis(knn_neighbors):
	out,kvals,nkvals,expectTensor = kvispp(knn_neighbors)

	evt = 5
	#plt.style.use('dark_background')
	#plt.rcParams['axes.facecolor'] = 'black'
	#plt.rcParams['savefig.facecolor'] = 'black'
	fig = plt.figure(figsize=plt.figaspect(0.5),tight_layout=True)	
	ax0 = fig.add_subplot(1, 2, 1, projection='3d')
	ax1 = fig.add_subplot(1, 2, 2, projection='3d')
	kvisplt(fig,ax0,evt,0,out,kvals,nkvals,expectTensor)
	kvisplt(fig,ax1,evt,1,out,kvals,nkvals,expectTensor)

	plt.suptitle("KNN Output Space Neighbor Visualization (Event="+str(evt)+")")
	plt.savefig(str(ML_PATH)+"/Models/detRes_KNN_VISN.png")
	plt.show()
	#plt.close()

	#print(nkvals[evt])

	
	#nkvals = dataTensorY[mask]
	#print(nkvals.shape)
	#ax.scatter(x,y,z,c=v, s=8) #neighbors (all but k)

def kvisplt(fig,ax,evt,orient,out,kvals,nkvals,expectTensor):
	# modified hsv in 256 color class
	hsv_modified = cm.get_cmap('hsv', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
	newcmp = ListedColormap(hsv_modified(np.linspace(0.5, 1.0, 256)))# show figure

	cmap=newcmp#'hsv'
	xin = (0+orient)%4
	yin = (1+orient)%4
	zin = (2+orient)%4
	tin = (3+orient)%4
	norm=mpt_col.Normalize(vmin=LM[tin,0],vmax=LM[tin,1])
	
	ax.scatter(expectTensor[evt,zin],expectTensor[evt,xin],expectTensor[evt,yin],c=expectTensor[evt,tin], s=16, marker = "^",cmap=cmap,norm=norm) #neighbors (k)
	ax.scatter(out[evt,zin],out[evt,xin],out[evt,yin],c=out[evt,tin], s=16, marker = "v",cmap=cmap,norm=norm) #neighbors (k)
	ax.scatter(kvals[evt,:,zin],kvals[evt,:,xin],kvals[evt,:,yin],c=kvals[evt,:,tin], s=14, marker = "o",cmap=cmap,norm=norm) #neighbors (k)
	ax.scatter(nkvals[evt,:,zin],nkvals[evt,:,xin],nkvals[evt,:,yin],c=nkvals[evt,:,tin], s=6, marker = ".",cmap=cmap,norm=norm) #neighbors (not k)
	ax.set_xlabel(NM[zin] + ' [mm]')
	ax.set_ylabel(NM[xin] + ' [mm]')
	ax.set_zlabel(NM[yin] + ' [mm]')

	cl = 0.98
	ax.w_xaxis.set_pane_color((cl, cl, cl, 1.0))
	ax.w_yaxis.set_pane_color((cl, cl, cl, 1.0))
	ax.w_zaxis.set_pane_color((cl, cl, cl, 1.0))

	cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
	cbar.set_label(NM[tin] + ' [mm]', rotation=90)

	visgrids(ax,orient,0.2)

	ax.set_title("(orientation="+str(orient)+")")


#-------------------------------------------------------------------------------
#TRAIN
#torch.autograd.set_detect_anomaly(True)
ML_showHIST = False
if(KVIS=="VIS"):
	kvis(knn_neighbors)
elif(KVIS=="ERR"):
	kerr(knn_neighbors)
elif(KVIS=="OPTNUM"):
	rmseP = torch.zeros((veclen,4,epochs))
	pltx = np.zeros((veclen,4,epochs))
	nk=0
	for uik in np.arange(initK,finalK,stepK):
		drnet.setK(uik)
		for jk in range(epochs):
			listset = list(range(length))
			random.shuffle(listset)
			dataInd,testInd = torch.split(torch.tensor(listset),splitList)
			dataTensorX = inputTensor[dataInd]
			inptTensor = inputTensor[testInd]
			dataTensorY = expectedTensor[dataInd]
			expectTensor = expectedTensor[testInd]
			#dataTensorX,dataTensorY,inputTensor,expectTensor
			out,outs = drnet(dataTensorX,dataTensorY,inptTensor)
			rmseP[nk,:,jk] = torch.from_numpy(ml_detRes_vis_knn(out,expectTensor,uik,noplt=False))
			ml_detRes_vis(out,expectTensor,uik)
			pltx[nk,:,jk] = [uik]*4
		nk=nk+1
	ml_detRes_vis_knn2(pltx,rmseP) #optimal number plot
elif(KVIS=="RUN"):
	print("RUN")
	with multiprocessing.Pool(processes=8) as pool:
		lise = list(tqdm(pool.map(knntest,np.arange(initK,finalK,stepK)),total=veclen))
	print("DONE")
elif(KVIS=="RUNONE"):
	print("RUN")
	knntest(knn_neighbors)
	print("DONE")

#-------------------------------------------------------
#with open(ML_PATH+'ML_detRes_LOOP.py') as f: exec(f.read()) # helper file # training loop
#-------------------------------------------------------
#losses = []
#if(input("Do you wish to load saved model? (y/n):") == ("y")):
#	drnet.load_state_dict(torch.load(model_path)) # LOAD	
#while(True):
#	inpval = input("Do you wish to train/retrain or test model? (y/n/t):")
#	if(inpval == ("y")):
#		losses.append(train(length,folds, num_epochs, batch_size, n))
#		MLDraw(losses,folds)
#	elif(inpval == ("t")):
#		test(drnet)
#		break
#	else:
#		break
#torch.save(drnet.state_dict(), model_path) # SAVE
