#
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import pythia8
import getopt, sys

def usage():
    print 'scanPythia.py is a simple script to loop over Pythia events and print results'
    print 'Usage: python scanPythia.py [options]'
    print '   -h, --help      : this message'
    print '   -e, --eCM       = beam center-of-mass energy [200.]'
    print '   -p, --pTHatMin  = minimum jet pT [20.]'
    print '   -s, --seed      = initial random number seed [-1]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ha:e:p:s:', \
              ['help','eCM=','pTHatMin=','seed='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

# Note these inputs should match usage entries above
    eCM      = 200.
    pTHatMin = 20.
    seed     = -1

    chopt    = ''
    for o, a in opts:
        chopt += o+a
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
    eCM_string = 'Beams:eCM = ' + str(eCM)
    pTHatMin_string = 'PhaseSpace:pTHatMin = ' + str(pTHatMin)

    pythia = pythia8.Pythia()
    pythia.readString('HardQCD:all = on')
    pythia.readString(eCM_string)
    pythia.readString(pTHatMin_string)
    if seed > 0:
        pythia.readString("Random:setSeed = on")
        seed_string = 'Random:seed = ' + str(seed)
        pythia.readString(seed_string)
    
    pythia.settings.listChanged();
    pythia.init()

#   Initialize SlowJet
    etaMax = 4.
    radius = 0.7
    pTjetMin = 10.
    nSel = 2    
    slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, 1);
    
    while (True):
        if not pythia.next(): break
        print '   ', pythia.info.code(), pythia.info.name(), pythia.info.pTHat(), pythia.info.thetaHat()

#   Analyze jet and match particles to pythia.event final particles
        slowJet.analyze(pythia.event)
        slowJet.list()
        print slowJet.sizeJet()
        print '\nSlowJet Results: pT, y, phi:'
        for i in range(slowJet.sizeJet()):
            print i,slowJet.pT(i),slowJet.y(i),slowJet.phi(i)
#   Extract constituents and convert nested list for ease of manipulation
        slowJetPrtList = [[] for i in range(slowJet.sizeJet())]
        for i in range(slowJet.sizeJet()):
            slowJetPrtList[i] = list(slowJet.constituents(i))
#        print slowJetPrtList
#   Loop over pythia event particles and map onto reconstructed jet number
#   There may be more elegant ways to perform this mapping
        print '\nParticle index, name, pT, eta, phi and slowJet association:'
        for i in range(pythia.event.size()):
            prt = pythia.event[i]
            if prt.isFinal():
                inJet = -1
                for j in range(len(slowJetPrtList)):
                    if i in slowJetPrtList[j]:
                            inJet = j
                if (inJet>=0):
                    print i, prt.name(), prt.pT(), prt.eta(), prt.phi(), inJet
            
        query = raw_input("q to quit; <CR> to continue: ")
        if (query=='q'):
            sys.exit(0)
    
if __name__=='__main__':main()
