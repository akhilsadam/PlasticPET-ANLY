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
#-------------------------------------------------------
length = inputTensor.shape[0]
frac = 0.7
splitList = [int(length*frac),length - int(length*frac)]
finalK = 50
stepK = 2
veclen = int((finalK+stepK-1)/stepK)
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
#-------------------------------------------------------------------------------
#TRAIN
#torch.autograd.set_detect_anomaly(True)
ML_showHIST = False
if(DRES_Train):
	rmseP = torch.zeros((veclen,4,epochs))
	pltx = np.zeros((veclen,4,epochs))
	nk=0
	for uik in np.arange(1,finalK,stepK):
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
			out = drnet(dataTensorX,dataTensorY,inptTensor)
			rmseP[nk,:,jk] = torch.from_numpy(ml_detRes_vis_knn(out,expectTensor,uik,noplt=True))
			pltx[nk,:,jk] = [uik]*4
		nk=nk+1
	ml_detRes_vis_knn2(pltx,rmseP)
drnet.setK(knn_neighbors)

listset = list(range(length))
random.shuffle(listset)
dataInd,testInd = torch.split(torch.tensor(listset),splitList)
dataTensorX = inputTensor[dataInd]
inptTensor = inputTensor[testInd]
dataTensorY = expectedTensor[dataInd]
expectTensor = expectedTensor[testInd]
#dataTensorX,dataTensorY,inputTensor,expectTensor
out = drnet(dataTensorX,dataTensorY,inptTensor)
ml_detRes_vis2(out,expectTensor,knn_neighbors)
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
