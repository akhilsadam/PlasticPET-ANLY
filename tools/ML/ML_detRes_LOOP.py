#-------------------------------------------------------
#training loop
def train(length,folds, num_epochs, batch_size, n):
	#optimizer = optim.Adam(drnet.parameters(),lr=lr,betas=(beta1,beta2))
	optimizer = optim.SGD(drnet.parameters(),lr=lr,momentum=momentum)
	loss_fn = torch.nn.L1Loss()
	b_losses = torch.empty(batch_size)
	TestLoss = np.zeros(shape=(folds))
	lossList = np.zeros(shape=(folds,num_epochs))
	foldL = fold(length,n,folds)
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
		drnet.train()
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
			b_losses = torch.empty(batch_size)

			optimizer.zero_grad()
			loss.backward(retain_graph=True)
			optimizer.step()
			

			#print("[Fold/Epoch]:","[",i,"/",t,"] - Loss:", loss.item())
			pbar.update(batch_size)
			#print("Fold ",i," Complete.")
		#Test Loss
		drnet.eval()
		y_test = drnet(XT)
		TestLoss[i] = loss_fn(y_test,YT)
		if(ML_showHIST): ml_detRes_vis(y_test,YT)
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
	ml_detRes_vis2(predictTensor,expectedTensor)
#-------------------------------------------------------
def MLDraw(lossList,folds):
	plt.plot(list(flatten(lossList)))
	plt.show()
