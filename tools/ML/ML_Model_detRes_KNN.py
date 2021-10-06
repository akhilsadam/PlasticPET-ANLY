import torch
import psutil
import gc
import numba
import numba.cuda
import numpy as np
from tqdm import tqdm

INIT_DIST = np.Infinity

@jit(nopython=True)
# @numba.cuda.jit
def kmax(array):
	mx = np.amax(array)
	idx = np.where(array == mx)[0][0]
	# print(idx)
	# print(array)
	# print(mx)
	return mx,idx
@jit(nopython=True)
# @numba.cuda.jit
def knnp(dataTensorXnp,tensorListnp,k):
	nevt = len(tensorListnp)
	indx = np.zeros(shape=(nevt,k))
	indxs = np.zeros(shape=(k,))
	dist = np.zeros(shape=(k,))
	dist.fill(INIT_DIST)
	# print(psutil.Process().memory_info().rss / (1024 * 1024))
	mxDist = INIT_DIST
	mxIndx = 0
	# print(psutil.Process().memory_info().rss / (1024 * 1024))

	print(dataTensorXnp.shape)
	print(tensorListnp.shape)

	for j in range(nevt):
		for i in (range(len(dataTensorXnp))):
			diff = (dataTensorXnp[j,:,:] - tensorListnp[i,:,:])
			pwd = np.power(diff,2)
			dist_T = np.sum(pwd)
			# gc.collect()
			if(dist_T < mxDist):
				# print(dataTensorXnp[j,:,:])
				# print(tensorListnp[i,:,:])
				# print(diff)
				# print(pwd)
				# print(dist_T)
				# print(dist)
				# print(indx)
				indxs[mxIndx] = i
				dist[mxIndx] = dist_T
				mxDist,mxIndx = kmax(dist)
		indx[j,:] = indxs
	
	return indx

class DRKNN(nn.Module):
	def __init__(self):
		super(DRKNN, self).__init__()
		self.ngpu = ngpu
		self.k = 3
	def setK(self,kin):
		self.k = kin	

	def forward(self,dataTensorX,dataTensorY,inputTensor):
		# print(psutil.Process().memory_info().rss / (1024 * 1024))
		print(dataTensorX.shape)
		print(inputTensor.shape)

		#OPTION 1 - NOT WORKING
		# indx = knnp(dataTensorX.numpy(),inputTensor.numpy(),self.k)
		
		#OPTION 2 - MEMORY ISSUES
		# tensorList = torch.split(inputTensor,1)
		# diff = torch.stack([(dataTensorX - tensorList[i])**2 for i in range(len(inputTensor))])
		# dist = torch.sum(diff,dim=(2,3))
		# a,indx = torch.topk(dist,k=int(self.k),largest=False)

		#Option 3
		print("LOOPMEM0: ", psutil.Process().memory_info().rss / (1024 * 1024))
		tensorList = torch.split(inputTensor,1)
		print("LOOPMEM0.1: ", psutil.Process().memory_info().rss / (1024 * 1024))
		gc.collect()
		# sum = np.zeros(shape=(len(inputTensor)))
		indx = np.zeros(shape=(inputTensor.shape[0],self.k))
		for i in range((inputTensor.shape[0])):
			si = torch.sum(((dataTensorX - tensorList[i])**2),dim=(1,2))
			tpk = torch.topk(si,k=int(self.k),largest=False)[1]
			# print(tpk)
			indx[i,:] = tpk
			# print(si)
			# sum[i] = si
			# print("INTRALOOPMEM1: ", psutil.Process().memory_info().rss / (1024 * 1024))

		print("LOOPMEM1: ", psutil.Process().memory_info().rss / (1024 * 1024))
		gc.collect()
		# diff = torch.Tensor
		# print("LOOPMEM2: ", psutil.Process().memory_info().rss / (1024 * 1024))
		# gc.collect()
		# dist = torch.sum(diff,dim=(2,3))
		# dist = torch.Tensor(sum)
		print("LOOPMEM3: ", psutil.Process().memory_info().rss / (1024 * 1024))
		gc.collect()
		# a,indx = torch.topk(dist,k=int(self.k),largest=False)
		print("LOOPMEM4: ", psutil.Process().memory_info().rss / (1024 * 1024))
		gc.collect()

		# print(psutil.Process().memory_info().rss / (1024 * 1024))
			# gc.collect()
			# print("LOOPMEM: ", psutil.Process().memory_info().rss / (1024 * 1024))

		gc.collect()
		
		# dist = torch.stack([torch.sum((dataTensorX - tensorList[i])**2) for i in range(len(inputTensor))])

		# print("EVENT",psutil.Process().memory_info().rss / (1024 * 1024))
		outs = dataTensorY[indx]
		out = torch.mean(outs,1)
		print(out.shape)
		return out,indx
	
	def _initialize_weights(self):
		self.k = 3#np.random.randint(1,50)

