#------------------------------------------------------------------------------------
if Options.Strip_Based_Reconstruction:
	print("ERROR! needs True Reconstruction")
	quit()
else:
	if Options.SiPM_Based_Reconstruction:	
		ds_recSignal = SiPM_Downsample(recSignal)
		signalRatio = (ds_recSignal)
	else:
		signalRatio = (recSignal)

#with open('tools/resAdd_recPhotons.py') as f: exec(f.read()) # helper file
#with open('tools/resAdd_recPhotons_Cut.py') as f: exec(f.read()) # helper file
#with open('tools/resAdd_ZrecTrue.py') as f: exec(f.read()) # helper file

