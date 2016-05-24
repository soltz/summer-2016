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
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

eta = []
phi = []
pT = []
eT = []


base = []
d_eta = []
d_phi = []

pythia = pythia8.Pythia()
pythia.readString("Beams:eCM = 200.")
pythia.readString("HardQCD:all = on")
pythia.readString("PhaseSpace:pTHatMin = 20.")
pythia.init()

# Begin event loop. Generate
for iEvent in range(0,1):
    if not pythia.next(): break

    event_type = pythia.info.name()

    for prt in pythia.event:
        if prt.isFinal():
            prt_eta = prt.eta()
            prt_phi = prt.phi()
            prt_pT = prt.pT()
            prt_eT = prt.eT()

            eta.append(prt_eta)
            phi.append(prt_phi)
            pT.append(prt_pT)
            eT.append(prt_eT)
            base.append(0)
            d_eta.append(0.1)
            d_phi.append(0.1)

 
# End of event loop. Statistics. Histogram. Done.
pythia.stat();

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.bar3d(eta,phi,base,d_eta,d_phi,eT)

ax.set_xlabel('$\eta$')
ax.set_ylabel('$\phi$')
ax.set_zlabel('eT')

title = 'hard process: ' + event_type
plt.title(title)
plt.show()


