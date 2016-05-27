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

pT_111 = []
pT_112 = []
pT_113 = []
pT_114 = []
event_types = []

pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 200.")
pythia.readString("HardQCD:all = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.init()

# Begin event loop. Generate
for iEvent in range(0,10000):
    if not pythia.next(): break

    a = pythia.info.code()
    event_types.append(a)
    b = pythia.info.pTHat()

    if a == 111:
        pT_111.append(b)
    elif a == 112:
        pT_112.append(b)
    elif a == 113:
        pT_113.append(b)
    elif a == 114:
        pT_114.append(b)

# Check for uncommon event types that will not appear on plot
for a in event_types:
    if a != 111 and a != 112 and a != 113 and a != 114:
        print "Warning other events included: ",a
 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

# set number of desired bins(b) and range(r)
b=40
r=(20,60)

# create bins using np.histogram
w,binEdges=np.histogram(pT_111,bins=b,range=r)
wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
x,binEdges=np.histogram(pT_112,bins=b,range=r)
xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
y,binEdges=np.histogram(pT_113,bins=b,range=r)
ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
z,binEdges=np.histogram(pT_114,bins=b,range=r)
zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])


plt.semilogy(wbincenters,w,'o',label='gg->gg')
plt.semilogy(xbincenters,x,'*',label='gg->qq(bar)')
plt.semilogy(ybincenters,y,'^',label='qg->qg')
plt.semilogy(zbincenters,z,'s',label="qq(bar)'->qq(bar)'")

plt.title("pT counts for hard processes")
plt.xlabel("pT")
plt.ylabel("counts")
plt.legend()

plt.show()

