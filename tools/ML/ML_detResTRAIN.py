#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file # import and setup
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file # PATH and vis
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
folds = 5
batch_size = 1 # set of events to train at once
epochs = 1
lr = 0.0001
momentum = 0.2
#beta1 = 0.5 #SGD, not yet ADAM
#-------------------------------------------------------------------------------
#Preprocessing:
with open(ML_PATH+'ML_detRes_preProcess.py') as f: exec(f.read()) # helper file # preprocessing
inputTensor,expectedTensor = MLDRESpreprocess(photoLen)
#-------------------------------------------------------
length = inputTensor.shape[0]
n = int(length/folds)
num_epochs = int(epochs*n/batch_size)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Model Definition:
with open(ML_PATH+'ML_Model_detRes.py') as f: exec(f.read()) # helper file # model definition
drnet = DRNet()
print(drnet)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#TRAIN
#torch.autograd.set_detect_anomaly(True)
#-------------------------------------------------------
with open(ML_PATH+'ML_detRes_LOOP.py') as f: exec(f.read()) # helper file # training loop
#-------------------------------------------------------
losses = []
if(input("Do you wish to load saved model? (y/n):") == ("y")):
	drnet.load_state_dict(torch.load(model_path)) # LOAD	
losses.append(train(length,folds, num_epochs, batch_size, n))
MLDraw(losses,folds)
while(input("Do you wish to retrain with same model? (y/n):") == ("y")):
	losses.append(train(length,folds, num_epochs, batch_size, n))
	MLDraw(losses,folds)
torch.save(drnet.state_dict(), model_path) # SAVE
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
