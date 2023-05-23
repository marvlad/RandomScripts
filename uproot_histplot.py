# Uproot script to read a histogram from rootfile
# Marvin Ascencio, FNAL, 05/23/23
# check more examples: https://uproot.readthedocs.io/en/latest/basic.html

import uproot
import matplotlib.pyplot as plt
import mplhep as hep

# reading the file
file = uproot.open("/Users/marvinascenciososa/Downloads/barb/files/miniprod6_FHC_valid.hist_ntuple.root")

hist1 = file["validgenie/Enu"].to_numpy()
hist2 = file["validgenie/numu/Enu"].to_numpy()

# Plotting part
fig,ax = plt.subplots()

hep.histplot(hist1,label='my label')
hep.histplot(hist2,label='my label 2')
ax.legend(prop={'size': 10})

plt.style.use(hep.style.ROOT)

# Labels
ax.set_xlabel("Energy [GeV]",fontsize=14)
ax.set_ylabel("Events ",fontsize=14)
plt.show()
