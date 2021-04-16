# inputTensor,expectedTensor

#flatten vectors
flatinput = torch.flatten(inputTensor,start_dim=1)

#print(inputTensor.shape)
targetshape=flatinput.shape
#print(flatinput[0])
#standardize -------------------------------------------------------
#Workaround for Z-values:
#print(targetshape[1])
if(targetshape[1]==4*2*photoLen):
    #print("Z-workaround")
    d = int(2*photoLen)
    flatinput[:,(2*d):(3*d)] = np.nan
#Zero valuing
# remove all nan/zero columns in Tensor
flatinput = flatinput[:,torch.isfinite(flatinput[0])]
flatlength = len(flatinput[0])
#print(flatinput[0])
#
meaninput = torch.mean(flatinput,dim=0)
#print(meaninput.shape)
stdinput = torch.std(flatinput,dim=0)
#print(stdinput.shape)
#----
if(pcaSTD):
    standardinput = (flatinput-meaninput)
else:
    standardinput = (flatinput-meaninput)/stdinput
#covariance --------------------------------------------------------
cov = torch.tensor(np.cov(standardinput,y=None,rowvar=False),dtype=torch.float32)
#mahalanobis
ts = torch.transpose(standardinput,0,1)
mahalanobis = torch.diagonal(torch.sqrt(torch.chain_matmul(standardinput,torch.pinverse(cov),ts)))
#print(mahalanobis.shape)
#eigensystem
eigenval, eigenvect = torch.eig(cov,eigenvectors=True)
singular = torch.sqrt(eigenval[:,0])
scale = singular+(singular==0)*1
#print(scale)
# pca
pcainput = torch.matmul(standardinput,eigenvect)

if(pcaMAHA):
    pcainput = torch.divide(pcainput,singular)
    
#print(standardinput.shape)
#print(eigenvect.shape)
pcacov = np.cov(pcainput,y=None,rowvar=False)

#
OLDinput = inputTensor
target = torch.zeros(targetshape)
target[:,0:flatlength] = pcainput
#print(target.shape)
inputTensor = torch.reshape(target, inputTensor.shape)

fig,ax =plt.subplots(nrows=1,ncols=3,figsize=(15,5),constrained_layout=True)
cmap = "cool"
#[ax[0,i].set_aspect(1.) for i in range(4)]
ax[0].set_title("Covariance Matrix")
ax[0].set_xlabel("X--Y--Z--T")
ax[0].set_ylabel("T--Z--Y--X")
ax[1].set_title("High Leverage Points")
ax[1].set_xlabel("mahalanobis")
ax[1].set_ylabel("index")
ax[2].set_title("Covariance Matrix post-PCA")
ax[2].set_xlabel("X--Y--Z--T")
ax[2].set_ylabel("T--Z--Y--X")

covplot=ax[0].matshow(cov,cmap=cmap)
fig.colorbar(covplot,ax = ax[0])

ax[1].scatter(mahalanobis,range(len(mahalanobis)))

covplot=ax[2].matshow(pcacov,cmap=cmap)
fig.colorbar(covplot,ax = ax[2])
#plt.show()
plt.suptitle("DetRes PCA")
plt.savefig(str(ML_PATH)+"/Models/detRes_"+PATH_OPT+".png")
plt.close()
print("Loaded PCA")
