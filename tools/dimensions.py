import numpy as np
import math
#------------------------------------------------------------------------------------
att_len = 4000
c_const = 299792458.0 #define as double
n_EJ208 = 1.58

nanosec = np.power(10.0,-9)
tof_const = np.power(10.0,-6)*c_const*0.5
FWHM = 2*math.sqrt(2*math.log(2))

nGamma = 2 # obviously
#------------------------------------------------------------------------------------
#Geometry Setup
#------------------------------------------------------------------------------------
nx = 3
ny = 16
nz = 3
px = 8
py = 2
npx = nx*px
npy = ny*py
Ox = 0.0
Oy = 8.0
Sx = 1 #length in Strips
Sy = 4
nArray = 24
theta = 2*np.pi/nArray

LX = 77.4
LY = 103.2
LZ = 1000.0
L = [LX,LY,LZ]
UX = LX/2
UY = LY/2
UZ = LZ/2
U = [UX,UY,UZ]
Radius = (784/2)+(0.5*LX) # old value: 396.0890847

unitList = ["mm","mm", "mm", "ns", "degrees"]
typeList = ["X-Resid (mm)","Y-Resid (mm)", "Z-Resid (mm)", "T-Resid (ns)", "Angle (deg)"]
rangeList = [[-40,40],[-30,30],[-50,50],[-0.3,0.3], [0,180]]
binList = [5,5,25,0.1,5]
locX = 0.95
locY = 0.05
spaY = 0.10

VKT = 0.1

TC_SiPM_X = (((LZ/1000)*n_EJ208)/c_const)/nanosec #time limit for SiPM

stripx = 25.4
stripy = 6.2
ppx = stripx/px
ppy = stripy/py
stripWx= stripx+2*VKT # strip plus individual VK
stripWy= stripy+2*VKT # strip plus individual VK
binx = LX/(nx*px)     #--25.8/8 (stripWx+2*VKT)
biny = LY/(ny*py)     #--6.45/2 - approximately correct
binz = 1000

stdG=[binx,biny,binz]

LM = np.array([[-UX,UX],[-UY,UY],[0,LZ],[1000*(-4*nanosec)*(c_const/n_EJ208),0],[0,180]])
BM = np.array([binx,biny,binz,1000*(0.5*nanosec)*(c_const/n_EJ208),5])
NM = ["X (Depth)","Y (Width)", "Z (Length)", "T","Angle (deg)"]

opticalProcessList = np.array(["Undefined",
"FresnelRefraction",
"FresnelReflection",
"TotalInternalReflection", 	
"LambertianReflection", 	
"LobeReflection",	
"SpikeReflection",	
"BackScattering", 	
"Absorption",	
"Detection",
"NotAtBoundary",	
"SameMaterial",	
"StepTooSmall", 	
"NoRINDEX",
"PolishedLumirrorAirReflection",
"PolishedLumirrorGlueReflection", 	
"PolishedAirReflection",
"PolishedTeflonAirReflection", 	
"PolishedTiOAirReflection",
"PolishedTyvekAirReflection",	
"PolishedVM2000AirReflection",
"PolishedVM2000GlueReflection",	
"EtchedLumirrorAirReflection",
"EtchedLumirrorGlueReflection",
"EtchedAirReflection",
"EtchedTeflonAirReflection", 	
"EtchedTiOAirReflection",
"EtchedTyvekAirReflection",
"EtchedVM2000AirReflection",
"EtchedVM2000GlueReflection",	
"GroundLumirrorAirReflection",
"GroundLumirrorGlueReflection", 	
"GroundAirReflection",
"GroundTeflonAirReflection", 	
"GroundTiOAirReflection",
"GroundTyvekAirReflection",
"GroundVM2000AirReflection",
"GroundVM2000GlueReflection"])
#_-------------------------------------------=\----------------\
def RSQ(data, model):
	return 1-np.var(data-model)/np.var(data)