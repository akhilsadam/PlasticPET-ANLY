#------------------------------------------------------------------------------------
#Geometry Setup
#------------------------------------------------------------------------------------
#set up stripPos
stripPos = np.zeros(shape=(ny,nx,3))
for j in range(ny):
	numSiPM = int(j/4)
	VKOffset = (2*numSiPM + 1)*VKT
	y = UY - ((j+0.5)*stripWy + VKOffset)
	for i in range(nx):
		VKOffset = (2*i + 1)*VKT
		x = (i+0.5)*stripWx + VKOffset - UX
		stripPos[j,i,0] = x
		stripPos[j,i,1] = y
		stripPos[j,i,2] = UZ
