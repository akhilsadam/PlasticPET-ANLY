class DRNet(nn.Module):
	def __init__(self):
		super(DRNet, self).__init__()
		self.ngpu = ngpu
		c2 = 4
		c3 = 4
		self.convs = nn.Sequential(nn.Tanh(),
						nn.Conv2d(1,c2,[1,3]),
						nn.ReLU(),
						nn.Conv2d(c2,c3,[4,5]),
						nn.ReLU(),
						nn.Conv2d(c3,1,[1,1]),
						nn.ReLU())

	def forward(self,inputTensor):
		out = inputTensor[:,None,:,:]
		out2 = self.convs(out)
		out3 = out2[:,0,0,:]
		return out3
