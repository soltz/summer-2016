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
    print '   -c, --QCD     : turn hard QCD processes off'
    print '   -q, --QED     : turn hard QED processes on'
    print '   -e, --eCM     = beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = minimum jet pT [20.0]'
    print '   -x, --pTHatMax     = maximum jet pT [50.0]'
    print '   -u, --num    = number of Pythia events [300]'
    print '   -p, --pTjetMin     = minimum pT for SlowJet analysis [10.0]'
    print '   -r, --radius     = radius for SlowJet analysis [0.7]'
    print '   -m, --massSet     : set SlowJet to use +/- pion masses for analysis'
    print '   -i, --hist     : create a histogram instead of a scatter plot'
    print '   -b, --bins     = number of histogram bins [10]'
    print '   -s, --seed     = initial random number seed [-1]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hcqe:n:x:u:p:r:mib:s:', \
              ['help','QCD','QED','eCM=','pTHatMin=','pTHatMax=','num=','pTjetMin=','radius=','massSet','hist',
               'bins=','seed='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

     # Pythia settings
    eCM  = 200.0
    pTHatMin  = 20.0
    pTHatMax  = 50.0
    QCD = 'on'
    QED = 'off'
    num_events = 300
    seed  = -1

    # SlowJet settings
    radius = 0.7
    pTjetMin = 10.0
    massSet = 2

    # Plotting
    hist = False
    bins = 10

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--QCD'):
            QCD = 'off'
        elif o in ('-q', '--QED'):
            QED = 'on'
        elif o in ('-e', '--eCM'):
            eCM = float(a)
        elif o in ('-n', '--pTHatMin'):
            pTHatMin = float(a)
        elif o in ('-x', '--pTHatMax'):
            pTHatMax = float(a)
        elif o in ('-u', '--num'):
            num_events = int(a)
        elif o in ('-p', '--pTjetMin'):
            pTjetMin = float(a)
        elif o in ('-r', '--radius'):
            radius = float(a)
        elif o in ('-m', '--massSet'):
            massSet = 1
        elif o in ('-s', '--seed'):
            seed = int(a)
        elif o in ('-i', '--hist'):
            hist = True
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

#   Initialize Pythia
    pythia = pythia8.Pythia()
    
    set_eCM = "Beams:eCM = " + str(eCM)
    pythia.readString(set_eCM)
    
    set_QCD = "HardQCD:all = " + QCD
    pythia.readString(set_QCD)

    set_QED = "PromptPhoton:all = " + QED
    pythia.readString(set_QED)

    set_pTHatMin = "PhaseSpace:pTHatMin = " + str(pTHatMin)
    pythia.readString(set_pTHatMin)

    set_pTHatMax = "PhaseSpace:pTHatMax = " + str(pTHatMax)
    pythia.readString(set_pTHatMax)

    pythia.readString("Random:setseed = on")
    
    set_seed = "Random:seed = " + str(seed)
    pythia.readString(set_seed)

    pythia.init()

#   Initialize SlowJet
    etaMax = 4.
    nSel = 2    
    slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, massSet);

#   Loop over events recording both pTHat and the calculated slowJet pT
    pTHat = [[],[],[],[],[]]
    slowJet_pT = [[],[],[],[],[]]
    
    for i in range(num_events):
        pythia.next()
        slowJet.analyze(pythia.event)
        for i in range(slowJet.sizeJet()):
            pTHat[i].append(pythia.info.pTHat())
            slowJet_pT[i].append(slowJet.pT(i))
            
#   End of event loop. Statistics. Histogram. Done.
    pythia.stat();

    if hist:
        r = (pTHatMin,pTHatMax)

        def bin_err(bin_counts):
            bin_err = []
            for val in bin_counts:
                if val != 0:
                    bin_err.append(1/(val**0.5))
            return bin_err
        
        def norm(weighted_data, bincounts):
            norm_data = []
            for i in range(len(weighted_data)):
                if bincounts[i] != 0:
                    av = weighted_data[i]/bincounts[i]
                    norm_data.append(av)
            return norm_data

        def rem_emp(bincenters, bincounts):
            new_centers = []
            for i in range(len(bincenters)):
                if bincounts[i] != 0:
                    new_centers.append(bincenters[i])
            return new_centers
        
        w, wbinEdges = np.histogram(pTHat[0],bins=bins,range=r,weights=slowJet_pT[0])
        wbincenters = 0.5*(wbinEdges[1:]+wbinEdges[:-1])
        wcounts, binEdges = np.histogram(pTHat[0],bins=wbinEdges)
        w = norm(w,wcounts)
        w_error = bin_err(wcounts)
        wbincenters = rem_emp(wbincenters, wcounts)
        
        x, xbinEdges = np.histogram(pTHat[1],bins=bins,range=r,weights=slowJet_pT[1])
        xbincenters = 0.5*(xbinEdges[1:]+xbinEdges[:-1])
        xcounts, binEdges = np.histogram(pTHat[1],bins=xbinEdges)
        x = norm(x,xcounts)
        x_error = bin_err(xcounts)
        xbincenters = rem_emp(xbincenters, xcounts)

        plt.errorbar(wbincenters,w,yerr = w_error, fmt = 'o',label='slowJet 1')
        plt.errorbar(xbincenters,x,yerr = x_error, fmt = '^',label='slowJet 2')

        
    if not hist:
        plt.plot(pTHat[0],slowJet_pT[0],'o',label='slowJet 1', alpha = 0.2)
        plt.plot(pTHat[1],slowJet_pT[1],'^',label='slowJet 2', alpha = 0.2)
        plt.plot(pTHat[2],slowJet_pT[2],'s',label='slowJet 3', alpha = 0.2)
#    plt.plot(pTHat[3],slowJet_pT[3],'d',label='slowJet 4')

    
    y = np.arange(0,50,0.5)
    x = np.arange(0,50,0.5)
    plt.plot(x,y,'--',color='black')
    if QCD == 'on':
        title = 'Hard QCD Processes'
    elif QED == 'on':
        title = 'Hard QED Processes'
    plt.title(title)
    plt.xlabel('pythia jet pT')
    plt.ylabel('slowJet pT')
    plt.legend(loc=0)
    plt.show(block=False)
        
    pythia.settings.listChanged()

    query = raw_input("<CR> to continue, p to save to pdf: ")
    if (query=='p'):
        query = raw_input("name this pdf file (do not include extension .pdf): ")
        filename = query + '.pdf'
        plt.savefig(filename)
        print 'file saved as', filename
        query = raw_input("<CR> to continue: ")
    

if __name__ == '__main__':main()

