#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file # import and setup
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file # PATH and vis
if Options.warmstart:
	with open(ML_PATH+'ML_Model_detRes_CNN2.py') as f: exec(f.read()) # helper file # model definition
else:
	with open(ML_PATH+'ML_Model_detRes_CNN.py') as f: exec(f.read()) # helper file # model definition
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#Preprocessing:
with open(ML_PATH+'ML_detRes_preProcess.py') as f: exec(f.read()) # helper file # preprocessing
inputTensor,expectedTensor = MLDRESpreprocess(photoLen)
#-------------------------------------------------------
with open(ML_PATH+'ML_detRes_LOOP.py') as f: exec(f.read()) # helper file # training loop
#-------------------------------------------------------
net = DRNet()
net.load_state_dict(torch.load(model_path))
net.eval()

from hilbertcurve.hilbertcurve import HilbertCurve
hilbert_curve = HilbertCurve(p=64,n=sum(p.numel() for p in net.parameters() if p.requires_grad))
loss_fn = torch.nn.SmoothL1Loss()

def hilbertxy():
	y_pred = net(inputTensor)			
	y_axval = loss_fn(y_pred,expectedTensor).detach().numpy()
	x_pp = math.pow(2,64)*(torch.cat([torch.flatten(p.data) for p in net.parameters() if p.requires_grad]).detach().numpy()*(1/200)+0.5)
	x_axval = math.pow((math.log(hilbert_curve.distances_from_points([x_pp.astype(float).tolist()])[0])/math.log(2)-92208),2)
	return [x_axval,y_axval]

[x,y] = hilbertxy()
plt.scatter(x,y,s=4,color='red')
iterate=4000
pts=np.zeros(shape=(iterate,2))
pbar = tqdm(total=iterate)
pbar.set_description("Point", refresh=True)
def hbprocess():
	net.init2()
	net.eval()
	[x,y] = hilbertxy()
	pts[i,0]=x
	pts[i,1]=y
	#return tuple(x,y)
#pool2 = multiprocessing.Pool(7)
#inptL = pool2.map(hbprocess,range(iterate))
#pts = np.array(inptL)
#pool2.close()
#pool2.join()
for i in range(iterate):
	hbprocess()
	pbar.update(1)
#plt.scatter(pts[:,0],pts[:,1],color='blue')
pts = pts[pts[:,0].argsort()]

plt.plot(pts[:,0],pts[:,1],color='black')
plt.ylabel("Loss")
plt.xlabel("Adjusted Hilbert (LN2) Distance")
plt.savefig(str(ML_PATH)+"/Models/detRes_VIS_CNN_"+str(photoLen)+".png",dpi=600)
plt.close()
#test(net)
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#c2 = 4
#c3 = 4
#M = nn.Conv2d(1,c2,[1,3])
#M2 = nn.Conv2d(c2,c3,[4,5])
#M3 = nn.Conv2d(c3,1,[1,1])

#z0 = torch.zeros(size=(35,4,10))
#z = z0[:,None,:,:]
#print(z.shape)
#z = M(z)
#print(z.shape)
#z = M2(z)
#print(z.shape)
#z = M3(z)
#print(z.shape)											
#z = z[:,0,0,:]
#print(z.shape)	

#detN = DRNet()

#print(detN(z0).shape)
