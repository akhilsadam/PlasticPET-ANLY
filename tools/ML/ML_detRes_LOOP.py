#-------------------------------------------------------
#training loop
def train(length,folds, num_epochs, batch_size, n):
	#optimizer = optim.Adam(drnet.parameters(),lr=lr,betas=(beta1,beta2))
	if Options.warmstart:
		paramList = list(drnet.parameters())
		paraml = len(paramList)
		optimizer = optim.Adam(paramList[0:(paraml-2)],lr=0.01*lr,betas=(beta1,beta2))
		optimize2 = optim.Adam(paramList[(paraml-2):(paraml-1)],lr=10*lr,betas=(beta1,beta2))	#slope
		optimize3 = optim.Adam(paramList[(paraml-1):paraml],lr=5*lr,betas=(beta1,beta2))	#bias
		#optimizer = optim.SGD(drnet.parameters(),lr=lr,momentum=momentum*0.5)
		loss_fn = torch.nn.SmoothL1Loss()
	else:	
		optimizer = optim.SGD(drnet.parameters(),lr=lr,momentum=momentum)
		loss_fn = torch.nn.L1Loss()
	#b_losses = torch.empty(batch_size)
	TestLoss = np.zeros(shape=(folds))
	lossList = np.zeros(shape=(folds,num_epochs))
	foldL = fold(length,n,folds)
	for i in range(folds):
		# Test
		ind = foldL[i]
		n=len(ind)
		XT = inputTensor[ind].reshape(n,4,2*Options.photoLen)
		YT = expectedTensor[ind].reshape(n,4)
		# Train
		exclude_set = {i}
		indT = list(flatten([foldL[num] for num in range(folds) if num not in exclude_set]))
		n=len(indT)
		X = inputTensor[indT].reshape(n,4,2*Options.photoLen)
		Y = expectedTensor[indT].reshape(n,4)
		#BAR
		pbar = tqdm(total=num_epochs)
		pbar.set_description("Fold "+str(i)+":", refresh=True)
		drnet.train()
		for t in range(num_epochs):
			folded = batch(batch_size,len(indT))
			#for b in range(batch_size):
			#	u = folded[b]
			#	print(len(u))
			#	xb = X[u].reshape(batch_size,4,2*Options.photoLen)
			#	yb = Y[u].reshape(batch_size,4)

			#	y_pred = drnet(xb)			
				
				

			#	b_losses[b] = loss_fn(y_pred,yb)

			#loss = torch.mean(b_losses)

			u = folded
			xb = X[u].reshape(batch_size,4,2*Options.photoLen)
			yb = Y[u].reshape(batch_size,4)
			y_pred = drnet(xb)			
			loss = loss_fn(y_pred,yb)

			lossList[i,t] = loss.item()

			#b_losses = torch.empty(batch_size)

			optimizer.zero_grad()
			if Options.warmstart:
				optimize2.zero_grad()
				optimize3.zero_grad()
			#penalty term ----------------------------
			# Creates gradients
			#grad_params = torch.autograd.grad(outputs=loss,inputs=drnet.parameters(),create_graph=True)
			# Computes the penalty term and adds it to the loss
			#grad_norm = 0
			#for grad in grad_params:
			#	grad_norm += grad.pow(2).sum()
			#grad_norm = grad_norm.sqrt()
			#loss = loss + grad_norm
			# ----------------------------------------

			loss.backward(retain_graph=True)
			optimizer.step()
			if Options.warmstart:
				optimize2.step()
				optimize3.step()

			#print("[Fold/Epoch]:","[",i,"/",t,"] - Loss:", loss.item())
			pbar.update(batch_size)
			#print("Fold ",i," Complete.")
		#Test Loss
		drnet.eval()
		y_test = drnet(XT)
		TestLoss[i] = loss_fn(y_test,YT)
		if(ML_showHIST): ml_detRes_vis(y_test,YT,Options.photoLen)
		tqdm.write("TestLoss["+str(i)+"] = "+str(TestLoss[i])+".")
	tqdm.write("Training Complete.")
	#fig, axs = plt.subplots(folds)
	#[axs[i].plot(lossList[i]) for i in range(folds)]
	#plt.show()
	return list(lossList.ravel())
#-------------------------------------------------------
#test
def test(net):
	net.eval()
	predictTensor = net(inputTensor)
	ml_detRes_vis(predictTensor,expectedTensor,Options.photoLen)
	ml_detRes_vis2(predictTensor,expectedTensor,Options.photoLen)
#-------------------------------------------------------
def MLDraw(lossList,folds):
	plt.plot(list(flatten(lossList)))
	plt.savefig(str(ML_PATH)+"/Models/detRes_Loss_CNN_"+str(Options.photoLen)+".png",dpi=600)
	#plt.show()
	plt.close()
