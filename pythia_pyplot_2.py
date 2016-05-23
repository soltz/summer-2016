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
    elif a == 113:
        pT_113.append(b)
    elif a == 114:
        pT_114.append(b)

# Check for uncommon event types that will not appear on plot
for a in event_types:
    if a != 111 and a != 113 and a != 114:
        print "Warning other events included: ",a
 
# print pT_111
# print pT_113
# print pT_114
 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

h='step'
r=(20,60)
b=40
l=True

plt.figure(1)
plt.hist(pT_111,histtype=h,range=r,bins=b,log=l,label='gg->gg')
plt.hist(pT_113,histtype=h,range=r,bins=b,log=l,label='qg->qg')
plt.hist(pT_114,histtype=h,range=r,bins=b,log=l,label="qq(bar)'->qq(bar)'")
plt.title("pT counts for hard processes")
plt.xlabel("pT")
plt.ylabel("counts")
plt.legend()

plt.show()

