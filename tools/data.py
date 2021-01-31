#------------------------------------------------------------------------------------
#Data Setup
#------------------------------------------------------------------------------------
def SiPM_Bin(inarray):
	return np.transpose(np.array([np.transpose(np.transpose(inarray,(0,2,1)).reshape(nEvents,nx,ny//Sy,Sy).sum(3),(0,2,1))]*Sy),(1,2,0,3)).reshape(nEvents,ny,nx)/Sy
#------------------------------------------------------------------------------------
#//---------\\ PhotonCounts // photon counts for left, right SiPMs and EJ208 strips
photonCounts = np.load("../build/B3a/photonCounts.npy")
nEvents = int(len(photonCounts)/3)
left = photonCounts[0:len(photonCounts):3,:,:] #left,strip,right photons - indices:evt#,y,x
strip = photonCounts[1:len(photonCounts):3,:,:]
right = photonCounts[2:len(photonCounts):3,:,:]

if SiPM_Based_Reconstruction:
	#massage left&right data
	left = SiPM_Bin(left)
	right = SiPM_Bin(right)

print("----- Number of Events: ", nEvents)
#print(left[0]) 
#//---------\\ BeamData // position and direction of fired gamma
beamData = np.load("../build/B3a/beamData.npy")
evtPos = beamData[:,0,:] # - first index is event #
evtDir = beamData[:,1,:]
#print(evtPos)
#print(evtDir)
#//---------\\ BeamInteract // interaction positions by compton/photoelectric effect
beamInteract = open("../build/B3a/beamInteract.txt")
evtPhotoInteract = []
evtComptonInteract = []
evtInteract = []
pos = []; # x,y,z
for i in range(nEvents):
	for j in range(3):
		line = beamInteract.readline()
		splits = line.rstrip(' \n').split(' ')
		#print(splits)
		pos.append([float(var) for var in splits if (len(var)>0)])
	evtPhotoInteract.append(np.transpose(np.array(pos)));
	pos = []
	for j in range(3):
		line = beamInteract.readline()
		splits = line.rstrip(' \n').split(' ')
		pos.append([float(var) for var in splits if (len(var)>0)])
	evtComptonInteract.append(np.transpose(np.array(pos)));
	pos = []# x,y,z,PhotonCount,t
	for j in range(5):
		line = beamInteract.readline()
		splits = line.rstrip(' \n').split(' ')
		pos.append([float(var) for var in splits if (len(var)>0)])
	evtInteract.append(np.transpose(np.array(pos)));
	pos = []
	line = beamInteract.readline()
#-------------
#print(evtInteract)
