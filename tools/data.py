#------------------------------------------------------------------------------------
#Data Setup
datadir = "../build/B3a/"
#datadir = "../data/"
#------------------------------------------------------------------------------------
def SiPM_Bin(inarray):
	return np.transpose(np.array([np.transpose(np.transpose(inarray,(0,2,1)).reshape(nEvents,nx,ny//Sy,Sy).sum(3),(0,2,1))]*Sy),(1,2,0,3)).reshape(nEvents,ny,nx)/Sy
#------------------------------------------------------------------------------------
#//---------\\ PhotonCounts // photon counts for left, right SiPMs and EJ208 strips
photonCounts = np.load(datadir+"photonCounts.npy")
left = photonCounts[0:len(photonCounts):3,:,:] #left,strip,right photons - indices:evt#,y,x
strip = photonCounts[1:len(photonCounts):3,:,:]
right = photonCounts[2:len(photonCounts):3,:,:]

if MaxEventLimit:
	nEvents = MaxEvents
else:
	nEvents = int(len(photonCounts)/3)

left = left[0:nEvents]
strip = strip[0:nEvents]
right = right[0:nEvents]

if SiPM_Based_Reconstruction:
	#massage left&right data
	left = SiPM_Bin(left)
	right = SiPM_Bin(right)

print("----- Number of Events: ", nEvents)
#print(left[0]) 
#//---------\\ BeamData // position and direction of fired gamma
beamData = np.load(datadir+"beamData.npy")
evtPos = beamData[0:nEvents,0,:] # - first index is event #
evtDir = beamData[0:nEvents,1,:]
#print(evtPos)
#print(evtDir)
#//---------\\ BeamInteract // interaction positions by compton/photoelectric effect
beamInteract = open(datadir+"beamInteract.txt")
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
beamInteract.close()
#-------------
@lru_cache(maxsize=17000)
def photonSiPMData(evt):
	#import time
	#t = time.time()
	#photonSiPMFile = open("../build/B3a/photonSiPMData.txt")
	filename = datadir+"photonSiPMData.txt"
	#textLines = np.zeros(shape = (nEvents),dtype=list)
	photonList = []
	photonData = np.zeros(5) # x,y,z,t,lambda
	#for evt in range(nEvents):
		#textLines[evt] = photonSiPMFile.readline().rstrip('\n').split('|')


	#photonSiPMFile.close()
	#print("Closed PhotonSiPMFile" + str(t-time.time()))
	#t = time.time()
	with io.open(filename,'r',encoding='ISO-8859-1') as fp:
		for i, line in enumerate(fp):
			if i == evt:
				# evt+1th line
				textLine = line.strip('\n').split('|')
			elif i > evt:
				break

	#textLines = [photonSiPMFile.readline().rstrip('\n').split('|') for evt in range(0,nEvents)]
	for idv in range(0,len(textLine)-1):
		photonData = np.asarray(textLine[idv].split(" "))[0:5].astype(float)
		photonList.append(photonData)
	#photonData = float(textLines[evt][idv].split(" ")[0:5]);
	#print(photonData)
#	print(t-time.time())
		
	return np.transpose(photonList) #np.asarray(photonList).T'
#-------------
nPhotons=0
with open(datadir+"photonReflectCount"+Ropt+".txt") as f:
   nPhotoEvents = sum(1 for _ in f)
@lru_cache(maxsize=17000)
def photonReflectData(evt):
	#import time
	#t = time.time()
	#photonSiPMFile = open("../build/B3a/photonSiPMData.txt")
	filename = datadir+"photonReflectData"+Ropt+".txt"
	filename2 = datadir+"photonReflectCount"+Ropt+".txt"
	#textLines = np.zeros(shape = (nEvents),dtype=list)
	photonList = []
	L = 8
	photonData = np.zeros(L) # x,y,z,t,alive/dead,ID, incident, reflection angles
	#for evt in range(nEvents):
		#textLines[evt] = photonSiPMFile.readline().rstrip('\n').split('|')


	#photonSiPMFile.close()
	#print("Closed PhotonSiPMFile" + str(t-time.time()))
	#t = time.time()
	with io.open(filename,'r',encoding='ISO-8859-1') as fp:
		for i, line in enumerate(fp):
			if i == evt:
				# evt+1th line
				textLine = line.strip('\n').split('|')
			elif i > evt:
				break
	with io.open(filename2,'r',encoding='ISO-8859-1') as fp:
		for i, line in enumerate(fp):
			if i == evt:
				# evt+1th line
				nPhotons = int(line.strip('\n'))
			elif i > evt:
				break
	#print(textLine)
	#textLines = [photonSiPMFile.readline().rstrip('\n').split('|') for evt in range(0,nEvents)]
	for idv in range(0,len(textLine)-1):
		photonData = np.asarray(textLine[idv].split(" "))[0:L].astype(float)
		photonList.append(photonData)
	#photonData = float(textLines[evt][idv].split(" ")[0:5]);
	#print(photonData)
#	print(t-time.time())
		
	return (nPhotons,np.transpose(photonList)) #np.asarray(photonList).T'

#print(photonSiPMData[1][2]) photonSiPMData[evt][x,y,z,t,lambda][photonIndex]
#-------------
