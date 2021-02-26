class DRNet(nn.Module):
	def __init__(self):
		super(DRNet, self).__init__()
		self.ngpu = ngpu
		c2 = 4 # cannot be changed due to input dimensions
		c3 = 16
		self.conv1 = nn.Conv2d(1,c2,[1,3]) #in: [n,1,4,10], out: [n,4,c3,8] 
		self.lin1  = nn.Linear(8,8)	   # do not change shape (last dimension)
		self.conv2 = nn.Conv2d(c2,c3,[4,5])#in: [n,4,c3,8], out: [n,c3,1,4]
		self.lin2  = nn.Linear(4,4)        # do not change shape (last dimension)
		self.conv3 = nn.Conv2d(c3,1,[1,1]) #in: [n,c3,1,4], out: [n,1,1,4]
		self.lin3 = nn.Linear(4,4)	   # do not change shape (last dimension)
		self.convs = nn.Sequential(
						self.conv1,
						nn.LeakyReLU(),
						self.lin1,
						self.conv2,
						nn.LeakyReLU(),
						self.lin2,						
						self.conv3)

	def forward(self,inputTensor):
		out = inputTensor[:,None,:,:]
		out2 = self.convs(out)
		#print(out2.shape)
		out3 = self.lin3(out2)
		#print(out3.shape)
		out4 = out3[:,0,0,:]
		#print(self.lin3.weight)
		return out4
	
	def _initialize_weights(self):
		init.normal_(self.conv1.weight,0.0,1.0)
		init.normal_(self.conv2.weight,0.0,1.0)
		init.normal_(self.conv3.weight,0.0,1.0)
		init.normal_(self.lin1.weight,1.0,0.5)
		init.normal_(self.lin2.weight,1.0,0.5)
		self.lin3.weight = torch.nn.Parameter(torch.diag(torch.Tensor([1/0.1,1/0.376,1,1/1.036])))
		self.lin3.bias = torch.nn.Parameter(torch.Tensor([-16.839,14.930,17.774,1000*(0.111*nanosec)*(c_const/n_EJ208)]))
