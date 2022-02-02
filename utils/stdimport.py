import os
import io
os.environ['MPLCONFIGDIR'] = "/home/Desktop/mplib/graph"
from tqdm import tqdm
import multiprocessing
from numba import jit
import sys

from analyzeOptions import *
from tools.dimensions import *
from tools.finite import *
from tools.geo import *