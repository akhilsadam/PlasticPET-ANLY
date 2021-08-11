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
# from tools.ML.ML_detRes_preProcess import *
print("KNNArrayNumber: ", ArrayNumber)
inputTensor,expectedTensor = MLDRESpreprocess(photoLen,workers)
if("PCA" in MLOPT):
	PATH_OPT=PATH_OPT+"PCA"
	pcaSTD = False
	pcaMAHA = False
if("STD" in MLOPT):
	PATH_OPT=PATH_OPT+"-STD"
	pcaSTD = True
if("MAHA" in MLOPT):
	PATH_OPT=PATH_OPT+"-MAHA"
	pcaMAHA = True
if("DISABLE-ZT" in MLOPT):
	PATH_OPT=PATH_OPT+"-DISABLE-ZT"
	inputTensor[:,2:4,:]=np.nan
	
#---
print(":OPTIONS- ",PATH_OPT)
if("PCA" in MLOPT):
	with open(ML_PATH+'ML_PCA.py') as f: exec(f.read()) # helper file # PATH and vis
elif("DISABLE-ZT" in MLOPT):
	inputTensor[:,2:4,:]=0
#-------------------------------------------------------
length = inputTensor.shape[0]
try: ML_SPLIT_FRACTION
except: ML_SPLIT_FRACTION = 0.75
splitList = [int(length*ML_SPLIT_FRACTION),length - int(length*ML_SPLIT_FRACTION)]
initK = 2#4
finalK = 40#80
stepK = 5
veclen = int((finalK+stepK-initK)/stepK)
#n = int(length/folds)
epochs = 5
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Model Definition:
try: KNNOPENED
except: KNNOPENED = False
if(KNNOPENED):
	pass
else:
	with open(ML_PATH+'ML_Model_detRes_KNN.py') as f: exec(f.read()) # helper file # model definition
	KNNOPENED = True
drnet = DRKNN()
drnet.eval() #not train!
drnet._initialize_weights()
print(drnet)
#-------------------------------------------------------------------------------
with open(ML_PATH+"ML_KNN_Functions.py") as f: exec(f.read())
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
elif(KVIS=="PICKLE"):
	print("Pickled")
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
