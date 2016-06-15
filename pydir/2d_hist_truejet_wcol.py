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
    print '   -l, --labels     : turn off color labels on plot'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'he:n:m:s:cqp:r:b:l', \
              ['help','eCM=','pTHatMin=','pTHatMax=','seed=','QCD','QED','pTjetMin=','radius=','bins=','labels'])
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

    # plot settings
    bins = 20
    labels = True

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
        elif o in ('-l', '--labels'):
            labels = False
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
#   Empty lists to store data for particles correctly identified as jets
#   "t" for true jet    
        tjet_eta = []
        tjet_phi = []
        tjet_pT = []
        tjet_eT = []
#   Empty lists to store data for background particles misidentified as jets
#   "f" for false jet
        fjet_eta = []
        fjet_phi = []
        fjet_pT = []
        fjet_eT = []
#   Empty lists to store data for true jet particles not included in jets
#   "m" for missed jet
        mjet_eta = []
        mjet_phi = []
        mjet_pT = []
        mjet_eT = []
#   Empty lists to store data for background particles not identified as jets
        bg_eta = []
        bg_phi = []
        bg_pT = []
        bg_eT = []

        if not pythia.next(): break
        pythia.event.list()

#   The daughters of the initial hard process are recorded below
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
        daughters5.extend(daughters6)
        daughters = daughters5

#   Run slowJet and analyze Pythia particles                
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
                if i in totJetPrtList and i in daughters:
                    tjet_eta.append(prt_eta)
                    tjet_phi.append(prt_phi)
                    tjet_pT.append(prt_pT)
                    tjet_eT.append(prt_eT)
                elif i in totJetPrtList:
                    fjet_eta.append(prt_eta)
                    fjet_phi.append(prt_phi)
                    fjet_pT.append(prt_pT)
                    fjet_eT.append(prt_eT)
                elif i in daughters:
                    mjet_eta.append(prt_eta)
                    mjet_phi.append(prt_phi)
                    mjet_pT.append(prt_pT)
                    mjet_eT.append(prt_eT)
                else:
                    bg_eta.append(prt_eta)
                    bg_phi.append(prt_phi)
                    bg_pT.append(prt_pT)
                    bg_eT.append(prt_eT)
                

#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "bins"
        tot_bins = bins**2
    
#   Data from true background particles is binned
        bg_h, xedges, yedges = np.histogram2d(bg_eta,bg_phi,bins=bins,range=[[-2,2], [-(np.pi), np.pi]],weights=bg_eT)
        bg_h = np.concatenate(bg_h)
    
#   Data from true jet particles identified as background is binned    
        mjet_h, mjet_xedges, mjet_yedges = np.histogram2d(mjet_eta,mjet_phi,bins=[xedges,yedges],weights=mjet_eT)
        mjet_h = np.concatenate(mjet_h)
    
#   Data from background particles misidentified as jets is binned
        fjet_h, fjet_xedges, fjet_yedges = np.histogram2d(fjet_eta,fjet_phi,bins=[xedges,yedges],weights=fjet_eT)
        fjet_h = np.concatenate(fjet_h)
    
#   Data from true jet particles identified as jets is binned
        tjet_h, tjet_xedges, tjet_yedges = np.histogram2d(tjet_eta,tjet_phi,bins=[xedges,yedges],weights=tjet_eT)
        tjet_h = np.concatenate(tjet_h)
    
#   x and y coordinates for bincenters are created using bin edges
        xcenters = 0.5*(xedges[1:]+xedges[:-1])
        xcenters = np.repeat(xcenters,bins)
        ycenters = 0.5*(yedges[1:]+yedges[:-1])
        ycenters = np.tile(ycenters,bins)
    
#   arrays of bin centers are extended to match the length of the data sets
        xcenters = list(xcenters)
        ycenters = list(ycenters)
        xcenters.extend(xcenters)
        ycenters.extend(ycenters)
        xcenters.extend(xcenters)
        ycenters.extend(ycenters)
            
#   Bars associated with jets will sit on top of bars associated with background
#   the order bars will be stacked is true jets correctly identified, fake jets, missed jets, background     
    
    #   the base for background will be all zeroes
        bg_base = np.zeros(len(bg_h))
        bg_base = list(bg_base)
    
    #   the base for missed jets will be the top of the actual background
        mjet_base = bg_h
        mjet_base = list(mjet_base)
        bg_base.extend(mjet_base)
        mjet_base = np.array(mjet_base)
    
    #   the base for fake jets will be the top of background and missed jets
        fjet_base = mjet_base + mjet_h
        fjet_base = list(fjet_base)
        bg_base.extend(fjet_base)
        fjet_base = np.array(fjet_base)
    
    #   the base for true jets will be on top of background, missed jets, and fake jets
        tjet_base = fjet_base + fjet_h
        tjet_base = list(tjet_base)
        bg_base.extend(tjet_base)
    
        base = bg_base
            
        bg_h = list(bg_h)
        mjet_h = list(mjet_h)
        fjet_h = list(fjet_h)
        tjet_h = list(tjet_h)
        bg_h.extend(mjet_h)
        bg_h.extend(fjet_h)
        bg_h.extend(tjet_h)
    
        h = bg_h
            
    #   Set size of bars in plot
        d_eta = (xedges[1]-xedges[0])
        d_phi = (yedges[1]-yedges[0])
    
    #   Create an array of colors where bars associated with jet particles are red
    #   Background bars are blue and bars with no value are white
        jet_colors=[]
        
        bg_col = 'blue'
        mjet_col = 'red'
        fjet_col = 'yellow'
        tjet_col = 'green'
        
        for j in h[0:tot_bins]:
            if j > 0:
                jet_colors.append(bg_col)
            else:
                jet_colors.append('w')
        for j in range(len(mjet_h)):
            if mjet_h[j] > 0:
                jet_colors.append(mjet_col)
            elif h[j] > 0:
                jet_colors.append(bg_col)
            else:
                jet_colors.append('w')
        for j in range(len(fjet_h)):
            if fjet_h[j] > 0:
                jet_colors.append(fjet_col)
            elif mjet_h[j] > 0:
                jet_colors.append(mjet_col)
            elif h[j] > 0:
                jet_colors.append(bg_col)
            else:
                jet_colors.append('w')
        for j in range(len(tjet_h)):
            if tjet_h[j] > 0:
                jet_colors.append(tjet_col)
            elif fjet_h[j] > 0:
                jet_colors.append(fjet_col)
            elif mjet_h[j] > 0:
                jet_colors.append(mjet_col)
            elif h[j] > 0:
                jet_colors.append(bg_col)
            else:
                jet_colors.append('w')
    
    #   End of event loop. Statistics. Histogram. Done.
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar3d(xcenters,ycenters,base,d_eta,d_phi,h,color=jet_colors,alpha=1)
    
        ax.set_xlabel('\n$\eta$',fontsize=20)
        ax.set_ylabel('\n$\phi$',fontsize=20)
        ax.set_zlabel('eT (GeV)')

        event_type = pythia.info.name()
        title = 'hard process: %s (pTHat = %.2f)' % (event_type, pythia.info.pTHat())
        plt.title(title, loc = 'left')
        pi = np.pi
        plt.ylim(-pi,pi)

        for i in range(slowJet.sizeJet()):
            pT_jet = slowJet.pT(i)
            pT_label = 'slowJet pT = %.2f' % pT_jet
            ax.text(slowJet.y(i),slowJet.phi(i),max(h)+1,pT_label,horizontalalignment='center')

        if labels:
            blue_proxy = plt.Rectangle((0, 0), 1, 1, fc="b")
            red_proxy = plt.Rectangle((0, 0), 1, 1, fc="r")
            yellow_proxy = plt.Rectangle((0, 0), 1, 1, fc="y")
            green_proxy = plt.Rectangle((0, 0), 1, 1, fc="g")
            ax.legend([green_proxy,yellow_proxy,red_proxy,blue_proxy],['true jets','false jets','missed jets','background'])   
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

