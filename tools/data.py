import numpy as np
#------------------------------------------------------------------------------------
#Data Setup
try: Options.COMPLETEDETECTOR
except NameError: Options.COMPLETEDETECTOR = True
try: Options.datadir
except NameError: Options.datadir = "../data/current/"
try: Options.MaxEventLimit
except NameError: Options.MaxEventLimit = False
try: Options.ReflectionTest
except NameError: Options.ReflectionTest = False
try: Options.SiPM_Based_Reconstruction
except NameError: Options.SiPM_Based_Reconstruction = False
try: Options.Process_Based_Breakdown
except NameError: Options.Process_Based_Breakdown = False
dataOpen = True
#Options.datadir = "../data/"
#------------------------------------------------------------------------------------
def SiPM_Bin(inarray):
	return np.transpose(np.array([np.transpose(np.transpose(inarray,(0,2,1)).reshape(Options.nEvents,nx,ny//Sy,Sy).sum(3),(0,2,1))]*Sy),(1,2,0,3)).reshape(Options.nEvents,ny,nx)/Sy
#------------------------------------------------------------------------------------
def photonSiPMDataLoad():
	filename = Options.datadir+"photonSiPMData.txt"
	with io.open(filename,'r',encoding='ISO-8859-1') as photonSiPMFile:
		for line in photonSiPMFile:
		# textLines = [photonSiPMFile.readline().rstrip('\n').split('|') for evt in range(0,301)]
			textLines.append(line.rstrip('\n').split('|'))
	# print(len(textLines))
	return textLines
	
textLines = []

def photonNPYLoad(array):
	photonCounts = np.load(Options.datadir+"photonCounts"+str(array)+".npy")
	left = photonCounts[0:3*Options.nEvents:3,:,:] #left,strip,right photons - indices:evt#,y,x
	strip = photonCounts[1:3*Options.nEvents:3,:,:]
	right = photonCounts[2:3*Options.nEvents:3,:,:]
	# print("UNIQUE LEFT ID : ",np.sum(left))
	return left,strip,right

#@lru_cache(maxsize=17000)
def photonSiPMData(evt):

	filename = Options.datadir+"photonSiPMData.txt"
	photonList = []
	photonData = np.zeros(6) # x,y,z,t,A,lambda

	# with io.open(filename,'r',encoding='ISO-8859-1') as fp:
	# 	for i, line in enumerate(fp):
	# 		if i == evt:
	# 			# evt+1th line
	# 			textLine = line.strip('\n').split('|')
	# 			print(textLine)
	# 		elif i > evt:
	# 			break

	#textLines = [photonSiPMFile.readline().rstrip('\n').split('|') for evt in range(0,Options.nEvents)]
	if evt < len(textLines):
		textLine = textLines[evt]
	else:
		return []
	for idv in range(len(textLine)-1):
		photonData = np.asarray(textLine[idv].split(" "))[:6].astype(float)
		photonList.append(photonData)
	#photonData = float(textLines[evt][idv].split(" ")[0:5]);
	#print(photonData)
	#print(np.asarray(photonList).T)
	#print(t-time.time())		
	return np.asarray(photonList).T #np.transpose(photonList) #np.asarray(photonList).T'
#//---------\\ PhotonCounts // photon counts for left, right SiPMs and EJ208 strips
print("DATALOAD ARRAY:",Options.ArrayNumber)
if Options.COMPLETEDETECTOR:
	beamData = np.load(Options.datadir+"beamData.npy")

	Options.nEvents = Options.MaxEvents if Options.MaxEventLimit else len(beamData)
	evtPos = beamData[0:Options.nEvents,0,:] # - first index is event #
	evtDir = beamData[0:Options.nEvents,1,:]

	textLines = photonSiPMDataLoad()
	# print(len(textLines))

	# completePhotonDATA = np.zeros(shape=(nArray,3*Options.nEvents,ny,nx))
	# for i in tqdm(range(nArray)):
	# 	completePhotonDATA[i,:,:,:] = np.load(Options.datadir+"photonCounts"+str(i)+".npy")

else:
	photonCounts = np.load(Options.datadir+"photonCounts.npy")
	left = photonCounts[0:len(photonCounts):3,:,:] #left,strip,right photons - indices:evt#,y,x
	strip = photonCounts[1:len(photonCounts):3,:,:]
	right = photonCounts[2:len(photonCounts):3,:,:]
	photonCountTypes = np.load(Options.datadir+"photonCountTypes.npy")
	comptCounts = photonCountTypes[0:len(photonCounts):3,:,:,:] # - indices:evt#,types,z,y,x
	photCounts = photonCountTypes[1:len(photonCounts):3,:,:,:]
	otherCounts = photonCountTypes[2:len(photonCounts):3,:,:,:]

	if Options.MaxEventLimit:
		Options.nEvents = Options.MaxEvents
	else:
		Options.nEvents = int(len(photonCounts)/3)

	left = left[0:Options.nEvents]
	strip = strip[0:Options.nEvents]
	right = right[0:Options.nEvents]
	comptCounts = comptCounts[0:Options.nEvents]
	photCounts = photCounts[0:Options.nEvents]
	otherCounts = otherCounts[0:Options.nEvents]

if Options.ReflectionTest:
	volumeCounts = np.loadtxt(Options.datadir+"volProcess.txt").astype(int)




if Options.SiPM_Based_Reconstruction:
	#massage left&right data
	left = SiPM_Bin(left)
	right = SiPM_Bin(right)

print("----- Number of Events: ", Options.nEvents)
#print(left[0]) 
#//---------\\ BeamData // position and direction of fired gamma
beamData = np.load(Options.datadir+"beamData.npy")
evtPos = beamData[0:Options.nEvents,0,:] # - first index is event #
evtDir = beamData[0:Options.nEvents,1,:]
#print(evtPos)
#print(evtDir)
#//---------\\ BeamInteract // interaction positions by compton/photoelectric effect
def beamInteraction():

	def lc(splits):
		return [float(var) if (len(var)>0) else np.nan for var in splits]

	with open(Options.datadir+"beamInteract.txt") as beamInteract:
		evtPhotoInteractG = []
		evtComptonInteractG = []
		evtInteractG = []
		pos = [] # x,y,z
		for i in range(Options.nEvents):
			for _ in range(3):
				line = beamInteract.readline()
				splits = line.rstrip(' \n').split(' ')
				#print(splits)
				pos.append(lc(splits))
			pI = np.transpose(pos)
			evtPhotoInteractG.append(pI)
			pos = []
			for _ in range(3):
				line = beamInteract.readline()
				splits = line.rstrip(' \n').split(' ')
				pos.append(lc(splits))
			cI = np.transpose(pos)
			evtComptonInteractG.append(cI)
			pos = []# x,y,z,PhotonCount,t,gammaID
			for _ in range(6):
				line = beamInteract.readline()
				splits = line.rstrip(' \n').split(' ')
				pos.append(lc(splits))
			tI = np.transpose(pos)
			evtInteractG.append(tI)
			pos = []
			line = beamInteract.readline()
			# print("TI",tI)
			# photonmask = tI[:,3]>0
			# comptonmap = np.where(np.isin(tI[:,0],cI[:,0]))
			# photomap = np.where(np.isin(tI[:,0],pI[:,0]))
			# n_Compt = int(np.sum(photonmask[comptonmap]))
			# n_Photo = int(np.sum(photonmask[photomap]))
			# evtType[i,:] = [n_Compt,n_Photo]
			# evtType2[i,:] = [len(cI),len(pI)] 
	return evtPhotoInteractG,evtComptonInteractG,evtInteractG

def localizeBeam(evtPhotoInteractG, evtComptonInteractG,evtInteractG):
	evtType = np.zeros((Options.nEvents,2),dtype=int) # nCompton, nPhoto (number of interactions for gamma by event)
	evtType2 = np.zeros((Options.nEvents,2),dtype=int) # nCompton, nPhoto (number of interactions for gamma by event, regardless of photon production)
	evtPhotoInteract = []
	evtComptonInteract = []
	evtInteract = []

	def assertlen(a):
		return len(a)==3

	for i in range(Options.nEvents):
		p0 = evtPhotoInteractG[i]
		c0 = evtComptonInteractG[i]
		t0 = evtInteractG[i]
		
		# print(t0)
		
		az = []
		for j in range(len(p0)):
			q = p0[j]
			print(q)
			if assertlen(q):
				q = np.transpose(GlobalToArrayM(q,Options.ArrayNumber)).tolist()
				az.append(q)
		
		bz = []
		for j in range(len(c0)):
			q2 = c0[j]
			if assertlen(q2):
				q2 = np.transpose(GlobalToArrayM(q2,Options.ArrayNumber)).tolist()
				bz.append(q2)
				
		cz = []
		for j in range(len(t0)):
			q3 = t0[j]
			if assertlen(q3):
				q3 = np.transpose(GlobalToArrayM(q3,Options.ArrayNumber)).tolist()
				cz.append(q3)

		pI = np.array(az)
		evtPhotoInteract.append(pI)
		cI = np.array(bz)
		evtComptonInteract.append(cI)
		tI = np.array(cz)
		evtInteract.append(tI)
		# print(tI)

		if ((len(tI)>0) and (len(cI)>0) and (len(pI)>0)) :
			# print(tI)
			photonmask = tI[:,3]>0
			comptonmap = np.where(np.isin(tI[:,0],cI[:,0]))
			photomap = np.where(np.isin(tI[:,0],pI[:,0]))
			n_Compt = int(np.sum(photonmask[comptonmap]))
			n_Photo = int(np.sum(photonmask[photomap]))
			evtType[i,:] = [n_Compt,n_Photo]
			evtType2[i,:] = [len(cI),len(pI)] 
		elif ((len(tI)>0) and (len(cI)>0)) :
			photonmask = tI[:,3]>0
			comptonmap = np.where(np.isin(tI[:,0],cI[:,0]))
			n_Compt = int(np.sum(photonmask[comptonmap]))
			evtType[i,:] = [n_Compt,0]
			evtType2[i,:] = [len(cI),0] 
		elif ((len(tI)>0) and (len(pI)>0)) :
			photonmask = tI[:,3]>0
			photomap = np.where(np.isin(tI[:,0],pI[:,0]))
			n_Photo = int(np.sum(photonmask[photomap]))
			evtType[i,:] = [0,n_Photo]
			evtType2[i,:] = [0,len(pI)] 
		else:
			evtType[i,:] = [0,0]
			evtType2[i,:] = [0,0] 

	return evtPhotoInteract,evtComptonInteract,evtInteract,evtType,evtType2

#-------------

#-------------
nPhotons=0
if Options.ReflectionTest:
	with open(Options.datadir+"photonReflectCount"+Options.Ropt+".txt") as f:
		nPhotoEvents = sum(1 for _ in f)
	@lru_cache(maxsize=17000)
	def photonReflectData(evt):
		#import time
		#t = time.time()
		#photonSiPMFile = open("../build/B3a/photonSiPMData.txt")
		filename = Options.datadir+"photonReflectData"+Options.Ropt+".txt"
		filename2 = Options.datadir+"photonReflectCount"+Options.Ropt+".txt"
		#textLines = np.zeros(shape = (Options.nEvents),dtype=list)
		photonList = []
		L = 9
		photonData = np.zeros(L) # x,y,z,t,alive/dead,ID, incident, reflection angles, processType
		#for evt in range(Options.nEvents):
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
		#textLines = [photonSiPMFile.readline().rstrip('\n').split('|') for evt in range(0,Options.nEvents)]
		for idv in range(0,len(textLine)-1):
			photonData = np.asarray(textLine[idv].split(" "))[0:L].astype(float)
			photonList.append(photonData)
		#photonData = float(textLines[evt][idv].split(" ")[0:5]);
		#print(photonData)
	#	print(t-time.time())
			
		return (nPhotons,np.transpose(photonList)) #np.asarray(photonList).T'

	#print(photonSiPMData[1][2]) photonSiPMData[evt][x,y,z,t,lambda][photonIndex]
	#-------------
if Options.Process_Based_Breakdown:
	photoA = []
	comptonA = []
	typeA = []
	#photo,photocompt,other,compt = 2,1,0,-1.
	with open(Options.datadir+"electronProcess.txt") as f:
		for line in f:
			photo = 0
			compton = 0
			split = line.split("|")
			split = split[:(len(split)-1)]
			if(len(np.unique(split))!=len(split)):
				print("ERROR")
			for word in split:
				if (word.startswith("phot")):
					photo += 1
				if (word.startswith("compt")):
					compton += 1
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
