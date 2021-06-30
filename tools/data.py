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
photonCountTypes = np.load(datadir+"photonCountTypes.npy")
comptCounts = photonCountTypes[0:len(photonCounts):3,:,:,:] # - indices:evt#,types,z,y,x
photCounts = photonCountTypes[1:len(photonCounts):3,:,:,:]
otherCounts = photonCountTypes[2:len(photonCounts):3,:,:,:]

if ReflectionTest:
	volumeCounts = np.loadtxt(datadir+"volProcess.txt").astype(int)

if MaxEventLimit:
	nEvents = MaxEvents
else:
	nEvents = int(len(photonCounts)/3)

left = left[0:nEvents]
strip = strip[0:nEvents]
right = right[0:nEvents]
comptCounts = comptCounts[0:nEvents]
photCounts = photCounts[0:nEvents]
otherCounts = otherCounts[0:nEvents]

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
evtType = np.zeros((nEvents,2),dtype=int) # nCompton, nPhoto (number of interactions for gamma by event)
evtType2 = np.zeros((nEvents,2),dtype=int) # nCompton, nPhoto (number of interactions for gamma by event, regardless of photon production)
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
	pI = np.transpose(np.array(pos))
	evtPhotoInteract.append(pI)
	pos = []
	for j in range(3):
		line = beamInteract.readline()
		splits = line.rstrip(' \n').split(' ')
		pos.append([float(var) for var in splits if (len(var)>0)])
	cI = np.transpose(np.array(pos))
	evtComptonInteract.append(cI)
	pos = []# x,y,z,PhotonCount,t
	for j in range(5):
		line = beamInteract.readline()
		splits = line.rstrip(' \n').split(' ')
		pos.append([float(var) for var in splits if (len(var)>0)])
	tI = np.transpose(np.array(pos))
	evtInteract.append(tI)
	pos = []
	line = beamInteract.readline()
	#print(pI[:,0])
	#print(cI[:,0])
	#print(tI[:,0])
	photonmask = tI[:,3]>0
	comptonmap = np.where(np.isin(tI[:,0],cI[:,0]))
	photomap = np.where(np.isin(tI[:,0],pI[:,0]))
	n_Compt = int(np.sum(photonmask[comptonmap]))
	n_Photo = int(np.sum(photonmask[photomap]))
	evtType[i,:] = [n_Compt,n_Photo] 
	evtType2[i,:] = [len(cI),len(pI)] 
	#print(evtType[i,:])
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
if ReflectionTest:
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
		L = 9
		photonData = np.zeros(L) # x,y,z,t,alive/dead,ID, incident, reflection angles, processType
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
photoA = []
comptonA = []
typeA = []
#photo,photocompt,other,compt = 2,1,0,-1.
with open(datadir+"electronProcess.txt") as f:
    for line in f:
        photo = 0
        compton = 0
        split = line.split("|")
        split = split[0:(len(split)-1)]
        if(len(np.unique(split))!=len(split)):
            print("ERROR")
        for word in split:
            if (word.startswith("phot")):
                photo = photo + 1
            if (word.startswith("compt")):
                compton = compton + 1    
        photoA.append(photo)
        comptonA.append(compton)
        if(photo > 0):
            if(compton>0):
                typeA.append(1)
            else:
                typeA.append(2)
        elif(compton>0):
            typeA.append(-1)
        else:
            typeA.append(0)
typeA = np.array(typeA)
photoA = np.array(photoA)
comptonA = np.array(comptonA)
