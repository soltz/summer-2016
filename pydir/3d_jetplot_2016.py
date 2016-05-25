# main01.py is a part of the PYTHIA event generator.
# Copyright (C) 2016 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#
# To set the path to the Pythia 8 Python interface do either (in a shell prompt):
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
import getopt, sys

def usage():
    print '3d_jetplot_2016.py plots a 3d bar graph for p-p events created by pythia8.'
    print 'Usage: python 3d_jetplot_2016.py [options]'
    print '   -h, --help      : this message'
    print '   -e, --eCM     = Center of Mass Energy per Nucleon (GeV) [200.0]'
    print '   -p, --pTHatMin     = Minimum Transverse Momentum [20.0]'
    print '   -s, --seed     = Initial Seed [-1]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'he:p:s:', \
              ['help','eCM=','pTHatMin=','seed='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

#   Default values of eCM, pTHatMin, and seed

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
        
    pythia = pythia8.Pythia()
    
    eCM = str(eCM)
    set_eCM = "Beams:eCM = " + eCM
    pythia.readString(set_eCM)
    
    pythia.readString("HardQCD:all = on")

    pTHatMin = str(pTHatMin)
    set_pTHatMin = "PhaseSpace:pTHatMin = " + pTHatMin
    pythia.readString(set_pTHatMin)

    pythia.readString("Random:setseed = on")
    
    seed = str(seed)
    set_seed = "Random:seed = " + seed
    pythia.readString(set_seed)

    pythia.init()

    while True:

        eta = []
        phi = []
        pT = []
        eT = []

        if not pythia.next(): break

        a = pythia.info.code()
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

        base = np.zeros(len(eT))
         # Set size of bars in plot
        d_eta = 0.1
        d_phi = 0.1

        # End of event loop. Statistics. Histogram. Done.
        pythia.stat();

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar3d(eta,phi,base,d_eta,d_phi,eT)

        ax.set_xlabel('$\eta$')
        ax.set_ylabel('$\phi$')
        ax.set_zlabel('eT(GeV)')

        title = 'hard process: ' + event_type
        plt.title(title)
        plt.show(block=False)
        
        pythia.settings.listChanged()
        pythia.settings.list("Random:seed")

        query = raw_input("q to quit, p to save to pdf,  <CR> to continue: ")
        if (query=='q'):
            break
        if (query=='p'):
            query = raw_input("name this pdf file (do not include extension .pdf): ")
            filename = query + '.pdf'
            plt.savefig(filename)
            query = raw_input("q to quit, <CR> to continue: ")
            if (query=='q'):
                break
        else: continue

if __name__ == '__main__':main()
