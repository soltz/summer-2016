# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

# Import the Pythia module.
import pythia8
import matplotlib.pyplot as plt
import numpy as np
import getopt, sys

def usage():
    print 'Histograms jet pT for various QED and QCD Pythia hard processes.'
    print 'Usage: python pT_pythiaEvents.py [options]'
    print '   -h, --help      : this message'
    print '   -c, --QCD     : show only QCD processes'
    print '   -q, --QED     : show only QED processes'
    print '   -e, --eCM     = pythia beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = pythia minimum jet pT [20.0]'
    print '   -x, --pTHatMax     = pythia maximum jet pT [50.0]'
    print '   -s, --seed     = pythia initial random number seed [-1]'
    print '   -m, --num_events     = number of pythia events to analyze [1000]'
    print '   -b, --bins     = number of histogram bins [40]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hcqe:n:x:s:m:b:', \
              ['help','QCD','QED','eCM=','pTHatMin=','pTHatMax=','seed=','num_events=','bins='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)
    
    # pythia settings
    eCM  = 200.0
    pTHatMin  = 20.0
    pTHatMax  = 50.0
    seed  = -1
    num_events = 1000

    # QCD/QED
    parameters = [['on','off',211],['off','on',212]]

    # histogram bins
    bins = 40

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--QCD'):
            parameters = [['on','off',111]]
        elif o in ('-q', '--QED'):
            parameters = [['off','on',111]]
        elif o in ('-e', '--eCM'):
            eCM = float(a)
        elif o in ('-n', '--pTHatMin'):
            pTHatMin = float(a)
        elif o in ('-x', '--pTHatMax'):
            pTHatMax = float(a)
        elif o in ('-s', '--seed'):
            seed = int(a)
        elif o in ('-m', '--num_events'):
            num_events = int(a)
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

    for setting in parameters:
        QCD = setting[0]
        QED = setting[1]
        subplot = setting[2]
    
        pT_111 = []
        pT_112 = []
        pT_113 = []
        pT_114 = []
        pT_201 = []
        pT_202 = []
        pT_203 = []
        pT_204 = []
        pT_205 = []
        event_types = []
        
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
        
        # Begin event loop. Generate
        for iEvent in range(num_events):
            if not pythia.next(): break
        
            a = pythia.info.code()
            event_types.append(a)
            b = pythia.info.pTHat()
        
            if a == 111:
                pT_111.append(b)
            elif a == 112:
                pT_112.append(b)
            elif a == 113:
                pT_113.append(b)
            elif a == 114:
                pT_114.append(b)
            elif a == 201:
                pT_201.append(b)
            elif a == 202:
                pT_202.append(b)
            elif a == 203:
                pT_203.append(b)
            elif a == 204:
                pT_204.append(b)
            elif a == 205:
                pT_205.append(b)
                
        # Check for uncommon event types that will not appear on plot
        for a in event_types:
            if a != 111 and a != 112 and a != 113 and a != 114 and a != 201 and a != 202 and a != 203 and a != 204 and a != 205:
                print "Warning other events included: ",a
         
        # End of event loop. Statistics. Histogram. Done.
        pythia.stat();
        
        # set number of desired bins(b) and range(r)
        b=bins
        r=(pTHatMin,pTHatMax)
        
        # create bins using np.histogram and plot results
        plt.subplot(subplot)
        
        if QED == 'on':
            w,binEdges=np.histogram(pT_201,bins=b,range=r)
            wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            x,binEdges=np.histogram(pT_202,bins=b,range=r)
            xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            y,binEdges=np.histogram(pT_203,bins=b,range=r)
            ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            z,binEdges=np.histogram(pT_204,bins=b,range=r)
            zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            v,binEdges=np.histogram(pT_205,bins=b,range=r)
            vbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            
            if len(pT_205)>0:
                plt.semilogy(vbincenters,v,'d',label='g g -> gamma gamma')
            if len(pT_201)>0:
                plt.semilogy(wbincenters,w,'o',label='q g -> q gamma (udscb)')
            if len(pT_202)>0:
                plt.semilogy(xbincenters,x,'*',label='q qbar -> g gamma')
            if len(pT_203)>0:
                plt.semilogy(ybincenters,y,'^',label='g g -> g gamma')
            if len(pT_204)>0:
                plt.semilogy(zbincenters,z,'s',label="f fbar -> gamma gamma")
            
            plt.title("pythia pT for hard QED processes")
            plt.xlabel("pT")
            plt.ylabel("counts")
            plt.legend(loc=0)
            
        
        if QCD == 'on':
            w,binEdges=np.histogram(pT_111,bins=b,range=r)
            wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            x,binEdges=np.histogram(pT_112,bins=b,range=r)
            xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            y,binEdges=np.histogram(pT_113,bins=b,range=r)
            ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            z,binEdges=np.histogram(pT_114,bins=b,range=r)
            zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
    
            if len(pT_111)>0:
                plt.semilogy(wbincenters,w,'o',label='g g -> g g')
            if len(pT_112)>0:
                plt.semilogy(xbincenters,x,'*',label='g g -> q q(bar)')
            if len(pT_113)>0:
                plt.semilogy(ybincenters,y,'^',label='q g -> q g')
            if len(pT_114)>0:
                plt.semilogy(zbincenters,z,'s',label="q q(bar)' -> q q(bar)'")
            
            plt.title("pythia pT for hard QCD processes")
            plt.xlabel("pT")
            plt.ylabel("counts")
            plt.legend(loc = 0)
    
    plt.show(block = False)
    
    query = raw_input("<CR> to continue, p to save to pdf: ")
    if (query=='p'):
        query = raw_input("name this pdf file (do not include extension .pdf): ")
        filename = query + '.pdf'
        plt.savefig(filename)
        print 'file saved as', filename
        query = raw_input("<CR> to continue: ")
    
    
if __name__ == '__main__':main()
