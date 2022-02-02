import sys

raw_only=("raw_only" in sys.argv)

try: render_only
except: render_only = False

if render_only:
    remake_listmode = False # swap to get complete data!
    newData = False
else:
    newData = True # new data?

if not raw_only:
    ML_Construct = True
    defaultDatabase = True # do you want to use a previously generated KNN Event Database? Allows more events!
    with open('analyzeKNN.py') as f: exec(f.read())
    print("********************")
    print("analyzeKNN complete!")
    print("********************")

if not render_only:
    remake_listmode = True
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