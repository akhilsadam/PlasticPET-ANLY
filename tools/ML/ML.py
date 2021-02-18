import random
import torch
import torch.nn as nn
import torch.nn.init as init
import torch.nn.functional as F
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim as optim
import torch.utils.data
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
torch.backends.cudnn.benchmark = False#True
torch.backends.cudnn.enabled = False#True
import multiprocessing
from itertools import repeat
from functools import partial
#-------------------------------------------------------
num_cores = multiprocessing.cpu_count()
ngpu = 1
device = torch.device("cuda:0" if (torch.cuda.is_available() and ngpu > 0) else "cpu")
workers = num_cores - 1
#-------------------------------------------------------
# Set random seed for reproducibility
manualSeed = 999
random.seed(manualSeed)
torch.manual_seed(manualSeed)
#-------------------------------------------------------
def fold(length,n,folds):
	x = list(range(length))
	random.shuffle(x)
	return [x[i:i + n] for i in range(0, length, n)]
def batch(batch_size,length):
	return [random.randint(0,length-1) for i in range(0,batch_size)]
