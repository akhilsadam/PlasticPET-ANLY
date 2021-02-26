class DRKNN(nn.Module):
	def __init__(self):
		super(DRKNN, self).__init__()
		self.ngpu = ngpu
		self.k = 3;
	def setK(self,kin):
		self.k = kin	

	def forward(self,dataTensorX,dataTensorY,inputTensor):
		tensorList = torch.split(inputTensor,1)
		diff = torch.stack([(dataTensorX - tensorList[i])**2 for i in range(len(inputTensor))])
		dist = torch.sum(diff,dim=(2,3))
		a,indx = torch.topk(dist,k=int(self.k),largest=False)
		outs = dataTensorY[indx]
		out = torch.mean(outs,1)
		return out
	
	def _initialize_weights(self):
		self.k = 3#np.random.randint(1,50)

