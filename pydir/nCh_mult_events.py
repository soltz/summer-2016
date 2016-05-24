# main01.py is a part of the PYTHIA event generator.
# Copyright (C) 2016 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#
# This is a simple test program. It fits on one slide in a talk.  It
# studies the charged multiplicity distribution at the LHC. To set the
# path to the Pythia 8 Python interface do either (in a shell prompt):
#      export PYTHONPATH=$(PREFIX_LIB):$PYTHONPATH
# or the following which sets the path from within Python.
# import sys
# cfg = open("Makefile.inc")
# lib = "../lib"
# for line in cfg:
#     if line.startswith("PREFIX_LIB="): lib = line[11:-1]; break
# sys.path.insert(0, lib)

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
x,binEdges=np.histogram(nCh_112,bins=b) #,range=r)
y,binEdges=np.histogram(nCh_113,bins=b) #,range=r)
z,binEdges=np.histogram(nCh_114,bins=b) #,range=r)
bincenters = 0.5*(binEdges[1:]+binEdges[:-1])


plt.plot(bincenters,w,'o',label='gg->gg')
plt.plot(bincenters,x,'*',label='gg->qq(bar)')
plt.plot(bincenters,y,'^',label='qg->qg')
plt.plot(bincenters,z,'s',label="qq(bar)'->qq(bar)'")

plt.title("charged multiplicity for hard processes")
plt.xlabel("charged multiplicity")
plt.ylabel("counts")
plt.legend()

plt.show()

