import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

nist = pd.read_csv("../build/B3a/PVT_FULL.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5,6,7])
nist.columns = ["Energy", "Coherent", "Incoherent", "Photoelectric", "NuclearPairProd", "ElectronPairProd", "TotWCoherent", "TotWoCoherent"]
nistLengths = nist
nistLengths.iloc[:,1:] = (nistLengths.iloc[:,1:]*1.023*pow(10,3)/(6.022*19))

#geant4 = pd.read_csv("barns20.txt", sep=" ", header=None, usecols=[0,1])
geant4 = pd.read_csv("lambdas5.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5])
geant4.columns = ["Energy","Phot", "Compton", "Conversion", "Rayleigh", "Total"]
#geant4 = geant4[geant4["Compton"] < 10 ** 10]
barns = geant4
barns.iloc[:,1:]  = geant4.iloc[:,1:].pow(-1)
#barns.iloc[:,1:]  = geant4.iloc[:,1:]
barns.iloc[:,1:] = (geant4.iloc[:,1:]*1.023*pow(10,3)/(6.022*19))

fig, ax = plt.subplots()
ax.plot(nistLengths["Energy"], nistLengths["Coherent"], label = "Coherent/Rayleigh Scattering - NIST")
ax.plot(nistLengths["Energy"], nistLengths["Incoherent"], label = "Incoherent/Compton Scattering - NIST")
ax.plot(nistLengths["Energy"], nistLengths["Photoelectric"], label = "Photoelectric Effect - NIST")
ax.plot(nistLengths["Energy"], nistLengths["TotWCoherent"], label = "Total - NIST")
ax.plot(barns["Energy"], barns["Rayleigh"], label = "Coherent/Rayleigh Scattering - Geant4")
ax.plot(barns["Energy"], barns["Compton"], label = "Incoherent/Compton Scattering - Geant4")
ax.plot(barns["Energy"], barns["Phot"], label = "Photoelectric Effect - Geant4")
ax.plot(barns["Energy"], barns["Total"], label = "Total - Geant4")
ax.set_xlabel("Energy (MeV)")
ax.set_ylabel("Cross Section (barns)")
ax.set_yscale("log")
ax.set_xscale("log")#forCS
ax.set(xlim=(0.00001, 1), ylim=(0.01, 100000000))
ax.legend()
plt.show()
