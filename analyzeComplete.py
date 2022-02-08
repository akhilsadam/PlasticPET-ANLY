import sys

raw_only=("raw_only" in sys.argv) # show only the raw data; primitive histograms and plots, no reconstructed objects
render_only=("render_only" in sys.argv) # show only the rendered/reconstructed objects, no primitive histograms and plots

database_test_plot=("database_truth" in sys.argv) # make a render with only truth values from KNN (do not actually call the KNN)

# set max event limits in analyzeKNN.py
# CURRENTLY SET!

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