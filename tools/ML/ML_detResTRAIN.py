#-------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file
#-------------------------------------------------------
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file
folds = 5
batch_size = 1 # set of events to train at once
epochs = 10
lr = 0.001
momentum = 0.9
#beta1 = 0.5 #SGD, not yet ADAM
#-------------------------------------------------------
#Preprocessing:
with open(ML_PATH+'ML_detRes_preProcess.py') as f: exec(f.read()) # helper file
inputTensor,expectedTensor = MLDRESpreprocess(photoLen)
#-------------------------------------------------------
length = inputTensor.shape[0]
n = int(length/folds)
num_epochs = int(epochs*n/batch_size)
#-------------------------------------------------------
#Model Definition:
with open(ML_PATH+'ML_Model_detRes.py') as f: exec(f.read()) # helper file
drnet = DRNet()
print(drnet)
#-------------------------------------------------------
#TRAIN
optimizer = optim.SGD(drnet.parameters(),lr=lr,momentum=momentum)
loss_fn = torch.nn.MSELoss()
b_losses = torch.empty(batch_size)
TestLoss = np.zeros(shape=(folds))
lossList = np.zeros(shape=(folds,num_epochs))
foldL = fold(length,n,folds)

torch.autograd.set_detect_anomaly(True)

for i in range(folds):
	# Test
	ind = foldL[i]
	n=len(ind)
	XT = inputTensor[ind].reshape(n,4,2*photoLen)
	YT = expectedTensor[ind].reshape(n,4)
	# Train
	exclude_set = {i}
	indT = list(flatten([foldL[num] for num in range(folds) if num not in exclude_set]))
	n=len(indT)
	X = inputTensor[indT].reshape(n,4,2*photoLen)
	Y = expectedTensor[indT].reshape(n,4)
	#BAR
	pbar = tqdm(total=num_epochs)
	pbar.set_description("Fold "+str(i)+":", refresh=True)
	for t in range(num_epochs):
		folded = batch(batch_size,len(indT))
		for b in range(batch_size):
			u = folded[b]
			xb = X[u].reshape(batch_size,4,2*photoLen)
			yb = Y[u].reshape(batch_size,4)
			
			y_pred = drnet(xb)			
			

			b_losses[b] = loss_fn(y_pred,yb)

		loss = torch.mean(b_losses)
		lossList[i,t] = loss.item()

		#loss.backward(retain_graph=True)
		optimizer.step()
		optimizer.zero_grad()

		#print("[Fold/Epoch]:","[",i,"/",t,"] - Loss:", loss.item())
		pbar.update(batch_size)
		#print("Fold ",i," Complete.")
	#Test Loss
	y_test = drnet(XT)
	TestLoss[i] = loss_fn(y_test,YT)
	tqdm.write("TestLoss["+str(i)+"] = "+str(TestLoss[i])+".")
	ml_detRes_vis(y_test,YT)
tqdm.write("Training Complete.")
fig, axs = plt.subplots(folds)
[axs[i].plot(lossList[i]) for i in range(folds)]
plt.show()


#-------------------------------------------------------
#SAVE
torch.save(drnet.state_dict(), model_path)
