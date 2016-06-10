#
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import pythia8
import math

eCM  = 200.0
pTHatMin  = 20.0
seed  = -1
QCD = 'on'
QED = 'off'

#   Initialize Pythia
pythia = pythia8.Pythia()
    
eCM = str(eCM)
set_eCM = "Beams:eCM = " + eCM
pythia.readString(set_eCM)

set_QCD = "HardQCD:all = " + QCD
pythia.readString(set_QCD)

set_QED = "PromptPhoton:all = " + QED
pythia.readString(set_QED)

pTHatMin = str(pTHatMin)
set_pTHatMin = "PhaseSpace:pTHatMin = " + pTHatMin
pythia.readString(set_pTHatMin)

pythia.readString("Random:setseed = on")
    
seed = str(seed)
set_seed = "Random:seed = " + seed
pythia.readString(set_seed)

pythia.init()
pythia.next()

jet5 = []
jet6 = []

for i in range(pythia.event.size()):
    prt = pythia.event[i]
    if prt.isFinal():
        if prt.isAncestor(5):
            jet5.append(i)
        if prt.isAncestor(6):
            jet6.append(i)

print jet5
print jet6

xi = []

for i in range(pythia.event.size()):
    prt = pythia.event[i]
    if prt.isFinal():
        if prt.isAncestor(5):
            jet_px = pythia.event[5].px()
            jet_py = pythia.event[5].py()
            jet_pz = pythia.event[5].pz()
                    
            prt_px = prt.px()
            prt_py = prt.py()
            prt_pz = prt.pz()

            print i, jet_px, jet_py, jet_pz
            print i, prt_px, prt_py, prt_pz
                    
#            prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
#            xi.append(prt_xi)

        if prt.isAncestor(6):
            jet_px = pythia.event[6].px()
            jet_py = pythia.event[6].py()
            jet_pz = pythia.event[6].pz()
                    
            prt_px = prt.px()
            prt_py = prt.py()
            prt_pz = prt.pz()

            print i, jet_px, jet_py, jet_pz
            print i, prt_px, prt_py, prt_pz
                    
#            prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
#            xi.append(prt_xi)

print xi
    
