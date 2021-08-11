#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file # import and setup
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file # PATH and vis
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
folds = 5
batch_size = 8 # set of events to train at once
epochs = 1
lr = 0.00001
momentum = 0.9 #SGD
beta1 = 0.5 
beta2 = 0.999 #ADAM
#-------------------------------------------------------------------------------
#Model Definition
if Options.warmstart:
	with open(ML_PATH+'ML_Model_detRes_CNN2.py') as f: exec(f.read()) # helper file # model definition
else:
	with open(ML_PATH+'ML_Model_detRes_CNN.py') as f: exec(f.read()) # helper file # model definition
drnet = DRNet()
drnet.train()
drnet._initialize_weights()
print("Number Of Params:",sum(p.numel() for p in drnet.parameters() if p.requires_grad))
print("Number Of layerparams:",sum(1 for p in drnet.parameters() if p.requires_grad))
print(drnet)
#print(list(drnet.parameters()))
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#TRAIN
#torch.autograd.set_detect_anomaly(True)
ML_showHIST = True

losses = []
if Options.warmstart:
	if(input("Do you wish to load Options.warmstarted data? (y/n):") == ("y")):
		drnet.load_state_dict(torch.load(model_path0),strict=False) # LOAD
	else:
		drnet.load_state_dict(torch.load(model_path)) # LOAD
else:
	if(input("Do you wish to load saved model? (y/n):") == ("y")):
		drnet.load_state_dict(torch.load(model_path)) # LOAD	

preprocessed=False

while(True):
	inpval = input("Do you wish to train/retrain or test model? (y/n/t/(int of train loops)):")
	#-------------------------------------------------------
	if(preprocessed==False):
		#-------------------------------------------------------------------------------
		#Preprocessing:
		with open(ML_PATH+'ML_detRes_preProcess.py') as f: exec(f.read()) # helper file # preprocessing
		inputTensor,expectedTensor = MLDRESpreprocess(photoLen)
		#-------------------------------------------------------
		length = inputTensor.shape[0]
		n = int(length/folds)
		num_epochs = int(epochs*n/batch_size)
		#-------------------------------------------------------------------------------
		with open(ML_PATH+'ML_detRes_LOOP.py') as f: exec(f.read()) # helper file # training loop
		#-------------------------------------------------------
		preprocessed=True

	if(inpval == ("y")):
		losses.append(train(length,folds, num_epochs, batch_size, n))
		MLDraw(losses,folds)
	elif(inpval == ("t")):
		test(drnet)
		break
	elif(inpval == ("n")):
		break
	else:
		try:
			iterate = int(inpval)
			print("Iterating over "+str(iterate)+" training iterations:")
		except Exception as e:
			print(e)
			quit()

		pbar = tqdm(total=iterate)
		pbar.set_description("Iteration:", refresh=True)

		for it in range(iterate):
			losses.append(train(length,folds, num_epochs, batch_size, n))
			pbar.update(1)
		MLDraw(losses,folds)
		test(drnet)
		break		
		
torch.save(drnet.state_dict(), model_path) # SAVE
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
