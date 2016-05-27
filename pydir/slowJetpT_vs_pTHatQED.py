# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import pythia8
import matplotlib.pyplot as plt
import numpy as np
import getopt, sys

def usage():
    print '3d_jetplot_2016.py plots a 3d bar graph for p-p events created by pythia8.'
    print 'Usage: python 3d_jetplot_2016.py [options]'
    print '   -h, --help      : this message'
    print '   -e, --eCM     = beam center-of-mass energy (GeV) [200.0]'
    print '   -p, --pTHatMin     = minimum jet pT [20.0]'
    print '   -s, --seed     = initial random number seed [-1]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'he:p:s:', \
              ['help','eCM=','pTHatMin=','seed='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    eCM  = 200.0
    pTHatMin  = 20.0
    seed  = -1

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-e', '--eCM'):
            eCM = float(a)
        elif o in ('-p', '--pTHatMin'):
            pTHatMin = float(a)
        elif o in ('-s', '--seed'):
            seed = int(a)
        else:
            assert False, 'unhandled option'

#   Initialize Pythia
    pythia = pythia8.Pythia()
    
    eCM = str(eCM)
    set_eCM = "Beams:eCM = " + eCM
    pythia.readString(set_eCM)
    
    pythia.readString("HardQCD:all = off")
    pythia.readString("PromptPhoton:all = on")

    pTHatMin = str(pTHatMin)
    set_pTHatMin = "PhaseSpace:pTHatMin = " + pTHatMin
    pythia.readString(set_pTHatMin)

    pythia.readString("Random:setseed = on")
    
    seed = str(seed)
    set_seed = "Random:seed = " + seed
    pythia.readString(set_seed)

    pythia.init()

#   Initialize SlowJet
    etaMax = 4.
    radius = 0.7
    pTjetMin = 10.
    nSel = 2    
    slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, 1);

#   Loop over events recording both pTHat and the calculated slowJet pT
    pTHat = [[],[],[],[],[]]
    slowJet_pT = [[],[],[],[],[]]
    
    for i in range(50):
        if not pythia.next(): break
        slowJet.analyze(pythia.event)
        for i in range(slowJet.sizeJet()):
            pTHat[i].append(pythia.info.pTHat())
            slowJet_pT[i].append(slowJet.pT(i))
            
#   End of event loop. Statistics. Histogram. Done.
    pythia.stat();
        
    
    plt.plot(pTHat[0],slowJet_pT[0],'o',label='slowJet 1')
    plt.plot(pTHat[1],slowJet_pT[1],'^',label='slowJet 2')
    plt.plot(pTHat[2],slowJet_pT[2],'s',label='slowJet 3')
#    plt.plot(pTHat[3],slowJet_pT[3],'d',label='slowJet 4')

    
    y = np.arange(0,50,0.5)
    x = np.arange(0,50,0.5)
    plt.plot(x,y,'--',color='black')
    plt.title('pTHat vs slowJet pT for QED processes')
    plt.xlabel('pTHat')
    plt.ylabel('slowJet pT')
    plt.legend(loc=0)
    plt.show()
        
    pythia.settings.listChanged()
    pythia.settings.list("Random:seed")

if __name__ == '__main__':main()

