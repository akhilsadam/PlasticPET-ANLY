def nonzeroData(x,y):
	nonzero = np.nonzero(y)
	return x[nonzero],y[nonzero]
def nonnanData(x,y):
	nonzero = np.isfinite(y)
	return x[nonzero],y[nonzero]
def ZcutData(x,y):
	nonzero = np.logical_and((x>=0),(x<=LZ))
	return x[nonzero],y[nonzero]
def nonzeroDatas(x,z,y):
	nonzero = np.nonzero(y)
	return x[nonzero],z[nonzero],y[nonzero]
def nonnanDatas(x,z,y):
	nonzero = np.isfinite(y)
	return x[nonzero],z[nonzero],y[nonzero]
def ZcutDatas(x,z,y):
	nonzero = np.logical_and((x>=0),(x<=LZ))
	return x[nonzero],z[nonzero],y[nonzero]
def YcutDatas(x,z,y):
	nonzero = np.logical_and((y>=0),(y<=500))
	return x[nonzero],z[nonzero],y[nonzero]
