from tools.energyResolution.histogramOptions import *
from tools.energyResolution.fitHistograms import *
from utils.simpleimport import *

def pltDOI(counts,gammaZ,axs,cmap,legend,x,y):
    mx=histogramOptions.doiSumMax
    nplt = len(cmap)
    zvals = np.array(range(nplt))
    zval2 = (LZ/((nplt-1)))*zvals
    # zval2 = UZ+
    # # print(gammaZ[np.isfinite(gammaZ)])
    print(zval2)
    # print(np.mean(gammaZ[np.isfinite(gammaZ)]))
    # print(max(gammaZ[np.isfinite(gammaZ)]))
    # print(min(gammaZ[np.isfinite(gammaZ)]))
    # print(gammaZ.shape)
    for i in range(1,nplt):
        indx = ((zval2[i-1] < gammaZ) & (gammaZ < zval2[i])) #np.intersect1d(np.where(gammaZ < zval2[i]), np.where(gammaZ > zval2[i-1]), assume_unique=True, return_indices=False)
        if Options.MaxEventLimit:
            indx = indx[:len(counts)]
        print(indx)
        # print(zval2[i])
        counting = counts[indx]
        # print(counting)
        axs.hist(counting,bins = int(mx/histogramOptions.binwidth_1),range = [histogramOptions.binwidth_1,mx], color = cmap[i-1],alpha = 0.3,stacked = False)
        counting = counting[counting>histogramOptions.binwidth_1] # used to be non-zero, now we are cutting out the first bin
        fitPlt(counting,axs,cmap[i-1],x,y-0.05*(i-1),"left",legend[i-1])