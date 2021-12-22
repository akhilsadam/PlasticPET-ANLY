ML_Construct = True
newData = True # new data?
defaultDatabase = True # do you want to use a previously generated KNN Event Database? Allows more events!
with open('analyzeKNN.py') as f: exec(f.read())
print("********************")
print("analyzeKNN complete!")
print("********************")

ML_Construct = False
newData = False
with open('analyzeKNN.py') as f: exec(f.read())
print("******************************")
print("photopeak histograms complete!")
print("******************************")

# with open('calculateScatterFraction.py') as f: exec(f.read())
# print("**************************************")
# print("scatter fraction calculation complete!")
# print("**************************************")