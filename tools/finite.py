from itertools import cycle, islice

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

def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))


# coerce lists
def coercion(L1,L2):
    len1 = len(L1)
    len2 = len(L2)
    llen = max(len1,len2)
    
    if(llen==len1):
        L2 = list(islice(cycle(L2), llen))
    else: L1 = list(islice(cycle(L1), llen))  
        
    return (L1,L2,llen)

# join filepath lists
def join(L1,L2): 
    L1,L2,llen = coercion(L1,L2)
    L3 = [(L1[i]+L2[i]) for i in range(llen)]
    return L3

def tuplejoin(L1,L2,L3): 
    L1,L2,llen = coercion(L1,L2)
    L2,L3,llen = coercion(L2,L3)
    
    L4 = [L1[i]+L2[i]+L3[i] for i in range(llen)]
    return L4