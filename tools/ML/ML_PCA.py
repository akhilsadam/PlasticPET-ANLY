# inputTensor,expectedTensor

#flatten vectors
flatinput = torch.flatten(inputTensor,start_dim=1)
#print(inputTensor.shape)
#print(flatinput.shape)
#print(flatinput[0])
#standardize -------------------------------------------------------
meaninput = torch.mean(flatinput,dim=0)
#print(meaninput.shape)
stdinput = torch.std(flatinput,dim=0)
#print(stdinput.shape)
#workaround for Z-values:
d = int(len(meaninput)/4)
meaninput[(2*d):(3*d)] = (meaninput[2*d] + meaninput[3*d])/2
stdinput[(2*d):(3*d)] = meaninput[(2*d):(3*d)]
#----
if(pcaSTD):
    standardinput = (flatinput)
else:
    standardinput = (flatinput-meaninput)/stdinput
#covariance --------------------------------------------------------
cov = torch.tensor(np.cov(standardinput,y=None,rowvar=False),dtype=torch.float32)
#mahalanobis
ts = torch.transpose(standardinput,0,1)
mahalanobis = torch.diagonal(torch.sqrt(torch.chain_matmul(standardinput,torch.pinverse(cov),ts)))
print(mahalanobis.shape)
#eigensystem
eigenval, eigenvect = torch.eig(cov,eigenvectors=True)
singular = torch.sqrt(eigenval[:,0])
scale = singular+(singular==0)*0.2
#print(scale)
# pca
pcainput = torch.matmul(standardinput,eigenvect)

if(pcaSTD):
    #pcainput = torch.divide(pcainput,singular)
    pass

print(standardinput.shape)
print(eigenvect.shape)
pcacov = np.cov(pcainput,y=None,rowvar=False)

#
OLDinput = inputTensor
inputTensor = torch.reshape(pcainput, inputTensor.shape)

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