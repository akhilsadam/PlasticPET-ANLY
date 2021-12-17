ML_Construct = True
newData = True
recreateDatabase = True
with open('analyzeKNN.py') as f: exec(f.read())
print("********************")
print("analyzeKNN complete!")
print("********************")
ML_Construct = False
newData = False
recreateDatabase = False
with open('analyzeKNN.py') as f: exec(f.read())
print("******************************")
print("photopeak histograms complete!")
print("******************************")