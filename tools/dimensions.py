
att_len = 4000
c_const = 299792458.0 #define as double
n_EJ208 = 1.58

nanosec = 1/1000000000

#------------------------------------------------------------------------------------
#Geometry Setup
#------------------------------------------------------------------------------------
nx = 3
ny = 16
Ox = 0.0
Oy = 8.0
Sx = 1 #length in Strips
Sy = 4

LX = 77.4
LY = 103.2
LZ = 1000
L = [LX,LY,LZ]
UX = LX/2
UY = LY/2
UZ = LZ/2
U = [UX,UY,UZ]

VKT = 0.1

TC_SiPM_X = (((LZ/1000)*n_EJ208)/c_const)/nanosec #time limit for SiPM

stripx = 25.4
stripy = 6.2
stripWx= stripx+2*VKT # strip plus individual VK
stripWy= stripy+2*VKT # strip plus individual VK
binx = LX/nx	      #--25.8 (stripWx+2*VKT)
biny = LY/ny          #--6.45 - approximately correct
binz = 1000

stdG=[binx,biny,binz]

LM = np.array([[-UX,UX],[-UY,UY],[0,LZ],[1000*(-4*nanosec)*(c_const/n_EJ208),0]])
BM = np.array([binx,biny,binz,1000*(0.5*nanosec)*(c_const/n_EJ208)])
NM = ["X (Depth)","Y (Width)", "Z (Length)", "T"]
