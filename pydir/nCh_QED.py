# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

# Import the Pythia module.
import pythia8
import matplotlib.pyplot as plt
import numpy as np

nCh_201 = []
nCh_202 = []
nCh_203 = []
nCh_204 = []
nCh_205 = []
event_types = []

pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 200.")
pythia.readString("HardQCD:all = off")
pythia.readString("PromptPhoton:all = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.init()

# Begin event loop. Generate. Tally charged particles for each type of hard process.
for iEvent in range(0,10000):
    if not pythia.next(): break

    a = pythia.info.code()
    event_types.append(a)

    if a == 201:
        nCharge_201 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_201 = nCharge_201 + 1
        nCh_201.append(nCharge_201)
    elif a == 202:
        nCharge_202 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_202 = nCharge_202 + 1
        nCh_202.append(nCharge_202)
    elif a == 203:
        nCharge_203 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_203 = nCharge_203 + 1
        nCh_203.append(nCharge_203)
    elif a == 204:
        nCharge_204 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_204 = nCharge_204 + 1
        nCh_204.append(nCharge_204)
    elif a == 205:
        nCharge_205 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_205 = nCharge_205 + 1
        nCh_205.append(nCharge_205)

# Check for uncommon event types that will not appear on plot
for a in event_types:
    if a != 201 and a != 202 and a != 203 and a != 204 and a != 205:
        print "Warning other events included: ",a
 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

# set number of desired bins(b)
b=40

# create bins using np.histogram
v,binEdges=np.histogram(nCh_201,bins=b)
vbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
w,binEdges=np.histogram(nCh_202,bins=b)
wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
x,binEdges=np.histogram(nCh_203,bins=b)
xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
y,binEdges=np.histogram(nCh_204,bins=b)
ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
z,binEdges=np.histogram(nCh_205,bins=b) 
zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])

plt.plot(vbincenters,v,'o',label='q g -> q gamma (udscb)')
plt.plot(wbincenters,w,'d',label='q qbar -> g gamma')
plt.plot(xbincenters,x,'*',label='g g -> g gamma')
plt.plot(ybincenters,y,'^',label='f fbar -> gamma gamma')
plt.plot(zbincenters,z,'s',label="g g -> gamma gamma")
#plt.yscale('log')

plt.title("charged multiplicity for hard QED processes")
plt.xlabel("charged multiplicity")
plt.ylabel("counts")
plt.legend()

plt.show()

