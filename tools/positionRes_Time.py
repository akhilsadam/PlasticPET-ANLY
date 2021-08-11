# redo position calculation with better numbers!
# r_z ZrecPosT[0]
# r_t ZrecPosT[1]
from tools.reconstruct import *
def recalculate_errorPos(left,right,nEvents,ZrecPosT,actEvtPosN):
	recPos = ACTreconstruct_time(left,right,nEvents,ZrecPosT[0])
	errorPosN_time = recPos - actEvtPosN #np.array([err_ZrecPosT[0],err_ZrecPosT[0],err_ZrecPosT[0]])
	return errorPosN_time

# plt.subplots(3)
# ax.hist(errorPosN[2],bins=200)
# plt.show()
# with open('tools/positionRes.py') as f: exec(f.read()) # helper file
