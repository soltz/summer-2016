# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

# Import the Pythia module.
import pythia8
import matplotlib.pyplot as plt
import numpy as np

nCh_111 = []
nCh_112 = []
nCh_113 = []
nCh_114 = []
event_types = []

pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 200.")
pythia.readString("HardQCD:all = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.init()

# Begin event loop. Generate. Tally charged particles for each type of hard process.
for iEvent in range(0,10000):
    if not pythia.next(): break

    a = pythia.info.code()
    event_types.append(a)

    if a == 111:
        nCharge_111 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_111 = nCharge_111 + 1
        nCh_111.append(nCharge_111)
    elif a == 112:
        nCharge_112 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_112 = nCharge_112 + 1
        nCh_112.append(nCharge_112)
    elif a == 113:
        nCharge_113 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_113 = nCharge_113 + 1
        nCh_113.append(nCharge_113)
    elif a == 114:
        nCharge_114 = 0
        for prt in pythia.event:
            if prt.isFinal() and prt.isCharged():
                nCharge_114 = nCharge_114 + 1
        nCh_114.append(nCharge_114)

# Check for uncommon event types that will not appear on plot
for a in event_types:
    if a != 111 and a != 112 and a != 113 and a != 114:
        print "Warning other events included: ",a
 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

# set number of desired bins(b) and range(r)
b=40
# r=(20,60)

# create bins using np.histogram
w,binEdges=np.histogram(nCh_111,bins=b) #,range=r)
wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
x,binEdges=np.histogram(nCh_112,bins=b) #,range=r)
xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
y,binEdges=np.histogram(nCh_113,bins=b) #,range=r)
ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
z,binEdges=np.histogram(nCh_114,bins=b) #,range=r)
zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])


plt.plot(wbincenters,w,'o',label='gg->gg')
plt.plot(xbincenters,x,'*',label='gg->qq(bar)')
plt.plot(ybincenters,y,'^',label='qg->qg')
plt.plot(zbincenters,z,'s',label="qq(bar)'->qq(bar)'")

plt.title("charged multiplicity for hard processes")
plt.xlabel("charged multiplicity")
plt.ylabel("counts")
plt.legend()

plt.show()

