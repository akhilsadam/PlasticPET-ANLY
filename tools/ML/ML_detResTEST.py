#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
with open(ML_PATH+'ML.py') as f: exec(f.read()) # helper file # import and setup
with open(ML_PATH+'ML_detRes.py') as f: exec(f.read()) # helper file # PATH and vis
with open(ML_PATH+'ML_Model_detRes_CNN.py') as f: exec(f.read()) # 
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
test(net)
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
