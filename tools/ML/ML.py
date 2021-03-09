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
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.enabled = True
import multiprocessing
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import summary_table
from statsmodels.tools.eval_measures import rmse
from itertools import repeat
from functools import partial
import pandas as pd
from tqdm import tqdm
#-------------------------------------------------------
torch.multiprocessing.set_sharing_strategy('file_system')
num_cores = 40
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
#-------------------------------------------------------
def dataNotWithinLimits(post):
	for i in range(4):
		if ~(((LM[i,0] <= post[i]) and (LM[i,1] >= post[i]))):
			#print("f", LM[i,0],LM[i,1])
			return True
	return False
