from tools.energyResolution.histogramOptions import *
from utils.simpleimport import *

def fitPlt(counts_in,axs,color,x,y,alignment):
    mx=histogramOptions.detSumMax
    mx2 = np.max(counts_in)
    hist, bin_edges = np.histogram(counts_in,bins=int(mx2/histogramOptions.binwidth_1))
    bin_centres = (bin_edges[:-1] + bin_edges[1:])/2

    xs = bin_centres[np.where(hist == np.max(hist))]
    p0 = [np.max(hist),int(xs[0]),5]
    fitted = False
    try:
        coeff, var_matrix = curve_fit(gauss, bin_centres, hist, p0=p0)
        fitted = True
    except:
        print("FIT FAILED")
    if fitted:
        hist_fit = gauss(bin_centres, *coeff)
        print(max(hist_fit))
        fwhm = coeff[2]*FWHM
        Mean = coeff[1]
        amplitude = coeff[0]
        minlim = Mean-2*coeff[2]
        maxlim = Mean+2*coeff[2]
        counts_inPhotopeak = np.count_nonzero(counts_in > minlim)
        totalcounts_in = len(counts_in)
        axs.plot(bin_centres, hist_fit, label='Fit', color = color)

        ENERGYRESOLUTION = fwhm/Mean
        PHOTOPEAK_SHARPNESS = amplitude/fwhm
        PHOTOPEAK_FWHM = fwhm
        PHOTOPEAK_COUNT = counts_inPhotopeak
        PHOTOPEAK_PROPORTION = counts_inPhotopeak/totalcounts_in
        # axs.text(
        #     0.95,
        #     0.80,
        #     "FWHM = %4.4f" % PHOTOPEAK_FWHM,
        #     verticalalignment='top',
        #     horizontalalignment='right',
        #     transform=axs.transAxes,
        #     fontsize=10,
        # )
        # axs.text(.95,.75,"Mean = %4.4f" %(Mean),verticalalignment='top',horizontalalignment='right',transform=axs.transAxes,fontsize=10)
        axs.text(x,y,"Energy Resolution = %4.4f" %(ENERGYRESOLUTION),verticalalignment='top',horizontalalignment=alignment,transform=axs.transAxes,fontsize=10)
    else:
        ENERGYRESOLUTION = np.nan
        PHOTOPEAK_SHARPNESS = np.nan
        PHOTOPEAK_FWHM = np.nan
        PHOTOPEAK_COUNT = np.nan
        PHOTOPEAK_PROPORTION = np.nan
        axs.text(.95,.80,"Energy Resolution Fit FAILED",verticalalignment='top',horizontalalignment=alignment,transform=axs.transAxes,fontsize=10)

    return [ENERGYRESOLUTION,PHOTOPEAK_SHARPNESS,PHOTOPEAK_FWHM,PHOTOPEAK_COUNT,PHOTOPEAK_PROPORTION]