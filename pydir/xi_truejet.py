#
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import matplotlib.pyplot as plt
import pythia8
import math

eCM  = 200.0
pTHatMin  = 20.0
seed  = -1
QCD = 'off'
QED = 'on'

def lists_overlap(a, b):
    for i in a:
        if i in b:
            return True
    return False

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

overlap = 0
domain_error = 0
no_error = 0

xi = []
z_values = []

for i in range(1000):
    pythia.next()
    
    jet5_d = []
    jet6_d = []
    
    daughters5 = []
    daughters5.extend(pythia.event[5].daughterList())
    for j in daughters5:
       if j != 0:
           daughters5.extend(pythia.event[j].daughterList())
           
    daughters6 = []
    daughters6.extend(pythia.event[6].daughterList())
    for j in daughters6:
       if j != 0:
           daughters6.extend(pythia.event[j].daughterList())
    
    for j in range(pythia.event.size()):
        prt = pythia.event[j]
        if prt.isFinal():
            if j in daughters5:
                jet5_d.append(j)

                jet_px = pythia.event[5].px()
                jet_py = pythia.event[5].py()
                jet_pz = pythia.event[5].pz()
                       
                prt_px = prt.px()
                prt_py = prt.py()
                prt_pz = prt.pz()

                z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
                z_values.append(z)

                if z > 0:
                    prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
                    xi.append(prt_xi)
                
            if j in daughters6:
                jet6_d.append(j)

                jet_px = pythia.event[6].px()
                jet_py = pythia.event[6].py()
                jet_pz = pythia.event[6].pz()
                       
                prt_px = prt.px()
                prt_py = prt.py()
                prt_pz = prt.pz()

                z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
                z_values.append(z)

                if z > 0:
                    prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
                    xi.append(prt_xi)
                    
    if lists_overlap(jet5_d, jet6_d):
        overlap = overlap + 1

print 'jet_overlap: ', overlap

plt.figure(1)
plt.hist(xi, bins = 40)

plt.xlabel('xi')
plt.ylabel('counts')

title = 'Values of xi for true jets'
plt.title(title)

plt.figure(2)
plt.hist(z_values, range = (-150, 150), bins = 150)

plt.xlabel('z')
plt.ylabel('counts')

plt.title('z_values')

plt.show()




