# redo position calculation with better numbers!
# r_z ZrecPosT[0]
# r_t ZrecPosT[1]
recPos,recSignal,zTensor = ACTreconstruct_time(left,right,nEvents,ZrecPosT[0])
errorPosN = recPos - actEvtPosN #np.array([err_ZrecPosT[0],err_ZrecPosT[0],err_ZrecPosT[0]])
plt.hist(errorPosN[2],bins=200)
plt.show()
#with open('tools/positionRes.py') as f: exec(f.read()) # helper file
