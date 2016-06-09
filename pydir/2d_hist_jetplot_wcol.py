#
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import pythia8
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import getopt, sys

def usage():
    print 'Plots a 2d histogram for pythia p-p events and identifies jets as red with slowJet.'
    print 'Usage: python 2d_hist_jetplot_wcol.py [options]'
    print '   -h, --help      : this message'
    print '   -e, --eCM     = beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = minimum jet pT [20.0]'
    print '   -m, --pTHatMax     = maximum jet pT [25.0]'
    print '   -s, --seed     = initial random number seed [-1]'
    print '   -c, --QCD     : turn hard QCD processes off'
    print '   -q, --QED     : turn hard QED processes on'
    print '   -p, --pTjetMin     = minimum slowJet pT [10]'
    print '   -r, --radius     = slowJet radius [0.7]'
    print '   -b, --bins     = number of histogram bins on each axis [20]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'he:n:m:s:cqp:r:b:', \
              ['help','eCM=','pTHatMin=','pTHatMax=','seed=','QCD','QED','pTjetMin=','radius=','bins='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    # pythia settings
    eCM  = 200.0
    pTHatMin  = 20.0
    pTHatMax  = 25.0
    seed  = -1
    QCD = 'on'
    QED = 'off'

    # slowJet settings
    radius = 0.7
    pTjetMin = 10.

    bins = 20

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-e', '--eCM'):
            eCM = float(a)
        elif o in ('-n', '--pTHatMin'):
            pTHatMin = float(a)
        elif o in ('-m', '--pTHatMax'):
            pTHatMax = float(a)
        elif o in ('-s', '--seed'):
            seed = int(a)
        elif o in ('-c', '--QCD'):
            QCD = 'off'
        elif o in ('-q', '--QED'):
            QED = 'on'
        elif o in ('-p', '--pTjetMin'):
            pTjetMin = float(a)
        elif o in ('-r', '--radius'):
            radius = float(a)
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

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

    pTHatMax = str(pTHatMax)
    set_pTHatMax = "PhaseSpace:pTHatMax = " + pTHatMax
    pythia.readString(set_pTHatMax)

    pythia.readString("Random:setseed = on")
    
    seed = str(seed)
    set_seed = "Random:seed = " + seed
    pythia.readString(set_seed)

    pythia.init()

#   Initialize SlowJet
    etaMax = 4.
    nSel = 2    
    slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, 1);
    
    while True:
#   Empty lists to store data from jet particles        
        jet_eta = []
        jet_phi = []
        jet_pT = []
        jet_eT = []
#   Empty lists to store data from background particles
        bg_eta = []
        bg_phi = []
        bg_pT = []
        bg_eT = []

        if not pythia.next(): break
        pythia.event.list()

        slowJet.analyze(pythia.event)
        slowJet.list()

#   Extract constituents and convert nested list for ease of manipulation
        slowJetPrtList = [[] for i in range(slowJet.sizeJet())]
        for i in range(slowJet.sizeJet()):
            slowJetPrtList[i] = list(slowJet.constituents(i))
        totJetPrtList = np.concatenate(slowJetPrtList)
        
#   Loop over pythia event particles
        for i in range(pythia.event.size()):
            prt = pythia.event[i]
            if prt.isFinal():
                prt_eta = prt.eta()
                prt_phi = prt.phi()
                prt_pT = prt.pT()
                prt_eT = prt.eT()
                if i in totJetPrtList:
                    jet_eta.append(prt_eta)
                    jet_phi.append(prt_phi)
                    jet_pT.append(prt_pT)
                    jet_eT.append(prt_eT)
                else:
                    bg_eta.append(prt_eta)
                    bg_phi.append(prt_phi)
                    bg_pT.append(prt_pT)
                    bg_eT.append(prt_eT)
                

#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
        tot_bins = bins**2
        bg_h, xedges, yedges = np.histogram2d(bg_eta,bg_phi,bins=bins,range=[[-6,6], [-(np.pi), np.pi]],weights=bg_eT)
        bg_h = np.concatenate(bg_h)
        xcenters = 0.5*(xedges[1:]+xedges[:-1])
        xcenters = np.repeat(xcenters,bins)
        ycenters = 0.5*(yedges[1:]+yedges[:-1])
        ycenters = np.tile(ycenters,bins)

#   Data from jet particles is binned separately        
        jet_h, jet_xedges, jet_yedges = np.histogram2d(jet_eta,jet_phi,bins=[xedges,yedges],weights=jet_eT)
        jet_h = np.concatenate(jet_h)

        xcenters = list(xcenters)
        ycenters = list(ycenters)
        xcenters.extend(xcenters)
        ycenters.extend(ycenters)
        
#   Bars associated with jets will sit on top of bars associated with background        
        bg_base = np.zeros(len(jet_h))
        bg_base = list(bg_base)
        jet_base = bg_h
        bg_base.extend(jet_base)
        base = bg_base
        
        bg_h = list(bg_h)
        jet_h = list(jet_h)
        bg_h.extend(jet_h)
        h = bg_h
        
#   Set size of bars in plot
        d_eta = (xedges[1]-xedges[0])
        d_phi = (yedges[1]-yedges[0])

#   Create an array of colors where bars associated with jet particles are red
#   Background bars are blue and bars with no value are white
        jet_colors=[]
        for i in h[0:tot_bins]:
            if i > 0:
                jet_colors.append('b')
            else:
                jet_colors.append('w')
        for i in range(len(jet_h)):
            if jet_h[i] > 0:
                jet_colors.append('r')
            elif h[i] > 0:
                jet_colors.append('b')
            else:
                jet_colors.append('w')

#   End of event loop. Statistics. Histogram. Done.
        pythia.stat();
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar3d(xcenters,ycenters,base,d_eta,d_phi,h,color=jet_colors,alpha=1)

        ax.set_xlabel('\n$\eta$',fontsize=20)
        ax.set_ylabel('\n$\phi$',fontsize=20)
        ax.set_zlabel('eT(GeV)')

        event_type = pythia.info.name()
        title = 'hard process: %s (pTHat = %.2f)' % (event_type, pythia.info.pTHat())
        plt.title(title)
        pi = np.pi
        plt.ylim(-pi,pi)
        
        pythia.settings.listChanged()
        pythia.settings.list("Random:seed")

        for i in range(slowJet.sizeJet()):
            pT_jet = slowJet.pT(i)
            pT_label = 'slowJet pT = %.2f' % pT_jet
            ax.text(slowJet.y(i),slowJet.phi(i),max(h)+1,pT_label,horizontalalignment='center')
        plt.show(block=False)

        query = raw_input("q to quit, p to save to png,  <CR> to continue: ")
        if (query=='q'):
            break
        if (query=='p'):
            query = raw_input("name this png file (do not include extension .png): ")
            filename = query + '.png'
            plt.savefig(filename)
            query = raw_input("q to quit, <CR> to continue: ")
            if (query=='q'):
                break
        else: continue

if __name__ == '__main__':main()

