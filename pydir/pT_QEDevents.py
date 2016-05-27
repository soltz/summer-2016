# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

# Import the Pythia module.
import pythia8
import matplotlib.pyplot as plt
import numpy as np

pT_201 = []
pT_202 = []
pT_203 = []
pT_204 = []
pT_205 = []
event_types = []

pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 200.")
pythia.readString("HardQCD:all = off")
pythia.readString("PromptPhoton:all = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.init()

# Begin event loop. Generate
for iEvent in range(0,10000):
    if not pythia.next(): break

    a = pythia.info.code()
    event_types.append(a)
    b = pythia.info.pTHat()

    if a == 201:
        pT_201.append(b)
    elif a == 202:
        pT_202.append(b)
    elif a == 203:
        pT_203.append(b)
    elif a == 204:
        pT_204.append(b)
    elif a == 205:
        pT_205.append(b)
        
# Check for uncommon event types that will not appear on plot
for a in event_types:
    if a != 201 and a != 202 and a != 203 and a != 204 and a != 205:
        print "Warning other events included: ",a
 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

# set number of desired bins(b) and range(r)
b=40
r=(20,60)

# create bins using np.histogram
w,binEdges=np.histogram(pT_201,bins=b,range=r)
wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
x,binEdges=np.histogram(pT_202,bins=b,range=r)
xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
y,binEdges=np.histogram(pT_203,bins=b,range=r)
ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
z,binEdges=np.histogram(pT_204,bins=b,range=r)
zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
v,binEdges=np.histogram(pT_205,bins=b,range=r)
vbincenters = 0.5*(binEdges[1:]+binEdges[:-1])

if len(pT_205)>0:
    plt.semilogy(vbincenters,v,'d',label='g g -> gamma gamma')
if len(pT_201)>0:
    plt.semilogy(wbincenters,w,'o',label='q g -> q gamma (udscb)')
if len(pT_202)>0:
    plt.semilogy(xbincenters,x,'*',label='q qbar -> g gamma')
if len(pT_203)>0:
    plt.semilogy(ybincenters,y,'^',label='g g -> g gamma')
if len(pT_204)>0:
    plt.semilogy(zbincenters,z,'s',label="f fbar -> gamma gamma")

plt.title("pT counts for hard QED processes")
plt.xlabel("pT")
plt.ylabel("counts")
plt.legend(loc=0)

plt.show()

