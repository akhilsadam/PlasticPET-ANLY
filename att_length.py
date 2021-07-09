import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

nist = pd.read_csv("../build/B3a/PVT_FULL.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5,6,7])
nist.columns = ["Energy", "Coherent", "Incoherent", "Photoelectric", "NuclearPairProd", "ElectronPairProd", "TotWCoherent", "TotWoCoherent"]
nistLengths = nist
#nistLengths.iloc[:,1:] = nistLengths.iloc[:,1:]
nistLengths.iloc[:,1:] = nistLengths.iloc[:,1:].mul(1.023).pow(-1) #multiply by the density of the material you're considering

geant4 = pd.read_csv("lambdas5.txt", sep=" ", header=None, usecols=[0,1,2,3,4,5])
geant4.columns = ["Energy","Phot", "Compton", "Conversion", "Rayleigh", "Total"]
geant4 = geant4[geant4["Compton"] < 10 ** 10]
geant4Lengths = geant4
#geant4Lengths.iloc[:,1:] = geant4Lengths.iloc[:,1:].pow(-1)
geant4Lengths.iloc[:,1:] = geant4Lengths.iloc[:,1:].mul(1.023) #divide by the density of the material you're considering

fig, ax = plt.subplots()
# ax.plot(nistLengths["Energy"], nistLengths["Coherent"], label = "Coherent/Rayleigh Scattering - NIST")
ax.plot(nistLengths["Energy"], nistLengths["Incoherent"], label = "Incoherent/Compton Scattering - NIST")
ax.plot(nistLengths["Energy"], nistLengths["Photoelectric"], label = "Photoelectric Effect - NIST")
ax.plot(nistLengths["Energy"], nistLengths["TotWCoherent"], label = "Total - NIST")
ax.plot(geant4Lengths["Energy"], geant4Lengths["Compton"], label = "Incoherent/Compton Scattering - Geant4")
ax.plot(geant4Lengths["Energy"], geant4Lengths["Phot"], label = "Photoelectric Effect - Geant4")
ax.plot(geant4Lengths["Energy"], geant4Lengths["Total"], label = "Total - Geant4")
ax.set_xlabel("Energy (MeV)")
#ax.set_ylabel("Cross Section (cm^2/g)")
ax.set_ylabel("Interaction Length (cm)")
ax.set_yscale("log")
#ax.set_xscale("log")#forCS
ax.legend()
plt.show()
