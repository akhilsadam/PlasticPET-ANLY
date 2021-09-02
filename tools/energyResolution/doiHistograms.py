from tools.energyResolution.histogramOptions import *
from tools.energyResolution.fitHistograms import *
from utils.simpleimport import *

def pltDOI(counts,gammaZ,axs,cmap,legend,x,y):
    mx=histogramOptions.detSumMax
    nplt = len(cmap)
    zvals = np.array(range(nplt))
    zval2 = (LZ/(nplt-1))*zvals
    # print(gammaZ[np.isfinite(gammaZ)])
    # print(zval2)
    for i in range(1,nplt):
        indx = np.where(gammaZ < zval2[i]) and np.where(gammaZ > zval2[i-1])
        print(zval2[i])
        counting = counts[indx]
        # print(counting)
        axs.hist(counting,bins = int(mx/histogramOptions.binwidth_1),range = [0,mx], color = cmap[i-1],alpha = 0.25,stacked = False)
        counting = counting[counting>histogramOptions.binwidth_1] # used to be non-zero, now we are cutting out the first bin
        fitPlt(counting,axs,cmap[i-1],x,y-0.05*(i-1),"left")