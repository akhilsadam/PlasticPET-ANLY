from analyzeOptions import *
from tools.vis import *
from tools.ML.ML_detRes import *
import tqdm
import torch
from numba import jit

import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import matplotlib.colors as mpt_col
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.cm as cm
import matplotlib.markers as mk
import matplotlib.ticker as mticker

def knntest(knn_neighbors):
	drnet.setK(knn_neighbors)
	listset = list(range(length))
	random.shuffle(listset)
	dataInd,testInd = torch.split(torch.tensor(listset),splitList)
	dataTensorX = inputTensor[dataInd]
	inptTensor = inputTensor[testInd]
	dataTensorY = expectedTensor[dataInd]
	expectTensor = expectedTensor[testInd]
	#dataTensorX,dataTensorY,inputTensor,expectTensor
	out,outs = drnet(dataTensorX,dataTensorY,inptTensor)
	ml_detRes_vis(out,expectTensor,knn_neighbors)
	ml_detRes_vis2(out,expectTensor,knn_neighbors)
	return True
def kvispp():
	drnet.setK(knn_neighbors)
	listset = list(range(length))
	random.shuffle(listset)
	dataInd,testInd = torch.split(torch.tensor(listset),splitList)
	dataTensorX = inputTensor[dataInd]
	inptTensor = inputTensor[testInd]
	dataTensorY = expectedTensor[dataInd]
	expectTensor = expectedTensor[testInd]
	#dataTensorX,dataTensorY,inputTensor,expectTensor
	out,indxs = drnet(dataTensorX,dataTensorY,inptTensor)
	
	dlength = dataTensorY.shape[0]
	kvals = dataTensorY[indxs]
	nkvals = torch.ones((indxs.shape[0],dlength-knn_neighbors,4))
	#print(dataTensorY.shape)
	#print(nkvals.shape)
	#print(indxs.shape)
	#print(dlength)
	for i in range(indxs.shape[0]):
		u = 0
		for j in range(dlength):
			if(j not in indxs[i]):
				nkvals[i,u,:] = dataTensorY[j,:]
				u = u + 1
	
	return out,kvals,nkvals,expectTensor
@jit
def kvisppN(evt,knn_neighbors,dataTensorY,dataTensorYT,out,outs):
	indxs = outs
	dlength = dataTensorY.shape[0]
	kvals = dataTensorY[indxs]
	nkvals = np.ones(shape = (indxs.shape[0],dlength-knn_neighbors,4))
	for evts in range(indxs.shape[0]):
		# print(dataTensorY[~indxs[evts]].shape)
		index = torch.ones(dlength, dtype=bool)
		index[indxs[evts]] = False
		nkvals[evts,:,:] = dataTensorY[index]
		# print(nkvals[evts])
	return out,kvals,nkvals,dataTensorYT
	# nkvals = np.ones(shape = (indxs.shape[0],dlength-knn_neighbors,4))
    # for i in range(indxs.shape[0]):
    #     u = 0
    #     for j in range(dlength):
    #         if(j not in indxs[i]):
    #             nkvals[i,u,:] = dataTensorY[j,:]
    #             u = u + 1

def kerr(knn_neighbors):
	out,kvals,nkvals,expectTensor = kvispp(knn_neighbors)
	errs = torch.pow(torch.sum(torch.pow(out-expectTensor,2),dim = 1),0.5)
	print(len(errs))
	fig,axs = plt.subplots(2,2,tight_layout=True)	
	for i in range(4):
		ax = axs[int(i/2),i%2]
		x,y = expectTensor[:,i], errs
		ax.scatter(x,y)
		ax.set_xlabel(NM[i] + ' [mm]')
		ax.set_ylabel('Error [mm]')
		if MarginalPLT:
			marginalPLT2(ax,x.numpy(),y.numpy(),i)

	plt.suptitle("KNN Output Space Error")
	plt.savefig(str(Options.ML_PATH)+"/Models/detRes_KNN_ERRN.png")
	plt.show()

def kvisNP(evt,dataTensorY,dataTensorYT,out,outs,knn_neighbors):
    outz,kvalsz,nkvalsz,expectTensorz = kvisppN(evt,knn_neighbors,dataTensorY.numpy(),dataTensorYT.numpy(),out.numpy(),outs.numpy())
    fig = plt.figure(figsize=(15,15),constrained_layout=True)
    ax0 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1 = fig.add_subplot(2, 2, 2, projection='3d')
    ax2 = fig.add_subplot(2, 2, 3, projection='3d')
    ax3 = fig.add_subplot(2, 2, 4, projection='3d')
    
    kvisplt(fig,ax0,evt,0,outz,kvalsz,nkvalsz,expectTensorz,0.75/6)
    kvisplt(fig,ax1,evt,1,outz,kvalsz,nkvalsz,expectTensorz,0.75/6)
    kvisplt(fig,ax2,evt,2,outz,kvalsz,nkvalsz,expectTensorz,0.75/6)
    kvisplt(fig,ax3,evt,3,outz,kvalsz,nkvalsz,expectTensorz,0.75/6)
    
    plt.suptitle("KNN Output Space Neighbor Visualization (Event="+str(evt)+")")
    plt.savefig(str(Options.ML_PATH)+"/Models/detRes_KNN_VISN.png")
    plt.close()#plt.show()

def kvisN(knn_neighbors):
	out,kvals,nkvals,expectTensor = kvispp(knn_neighbors)

	evt = 5
	#plt.style.use('dark_background')
	#plt.rcParams['axes.facecolor'] = 'black'
	#plt.rcParams['savefig.facecolor'] = 'black'
	fig = plt.figure(figsize=plt.figaspect(0.5),tight_layout=True)	
	ax0 = fig.add_subplot(2, 2, 1, projection='3d')
	ax1 = fig.add_subplot(2, 2, 2, projection='3d')
	kvisplt(fig,ax0,evt,0,out,kvals,nkvals,expectTensor,0.5/6)
	kvisplt(fig,ax1,evt,1,out,kvals,nkvals,expectTensor,0.5/6)
    
	ax2 = fig.add_subplot(2, 2, 3, projection='3d')
	ax3 = fig.add_subplot(2, 2, 4, projection='3d')
	kvisplt(fig,ax2,evt,2,out,kvals,nkvals,expectTensor,0.5/6)
	kvisplt(fig,ax3,evt,3,out,kvals,nkvals,expectTensor,0.5/6)

	plt.suptitle("KNN Output Space Neighbor Visualization (Event="+str(evt)+")")
	plt.savefig(str(Options.ML_PATH)+"/Models/detRes_KNN_VISN.png")
	plt.show()
	#plt.close()

	#print(nkvals[evt])

	
	#nkvals = dataTensorY[mask]
	#print(nkvals.shape)
	#ax.scatter(x,y,z,c=v, s=8) #neighbors (all but k)
def kvisplt(fig,ax,evt,orient,out,kvals,nkvals,expectTensor,multiplier):
	# modified hsv in 256 color class
	hsv_modified = cm.get_cmap('hsv', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
	newcmp = ListedColormap(hsv_modified(np.linspace(0.5, 1.0, 256)))# show figure

	cmap=newcmp#'hsv'
	xin = (0+orient)%4
	yin = (1+orient)%4
	zin = (2+orient)%4
	tin = (3+orient)%4
	norm=mpt_col.Normalize(vmin=LM[tin,0],vmax=LM[tin,1])

	ax.scatter(nkvals[evt,:,zin],nkvals[evt,:,xin],nkvals[evt,:,yin],c=nkvals[evt,:,tin], s=6*multiplier, marker = ".",cmap=cmap,norm=norm) #neighbors (not k)	
	ax.scatter(kvals[evt,:,zin],kvals[evt,:,xin],kvals[evt,:,yin],c=kvals[evt,:,tin], s=20, marker = "o",cmap=cmap,norm=norm) #neighbors (k)
	ax.scatter(expectTensor[evt,zin],expectTensor[evt,xin],expectTensor[evt,yin],c=expectTensor[evt,tin], s=22, marker = "^",cmap=cmap,norm=norm) #neighbors (k)
	ax.scatter(out[evt,zin],out[evt,xin],out[evt,yin],c=out[evt,tin], s=22, marker = "v",cmap=cmap,norm=norm) #neighbors (k)

	ax.set_xlabel(NM[zin] + ' [mm]')
	ax.set_ylabel(NM[xin] + ' [mm]')
	ax.set_zlabel(NM[yin] + ' [mm]')

	cl = 0.98
	ax.w_xaxis.set_pane_color((cl, cl, cl, 1.0))
	ax.w_yaxis.set_pane_color((cl, cl, cl, 1.0))
	ax.w_zaxis.set_pane_color((cl, cl, cl, 1.0))

	cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap),ax=ax)
	cbar.set_label(NM[tin] + ' [mm]', rotation=90)

	visgrids(ax,orient,0.2)

	ax.set_title("(orientation="+str(orient)+")")

