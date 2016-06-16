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
    print '   -a, --all     : show all occuring processes, includes processes that occur infrequently'
    print '   -e, --eCM     = pythia beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = pythia minimum jet pT [20.0]'
    print '   -x, --pTHatMax     = pythia maximum jet pT [50.0]'
    print '   -s, --seed     = pythia initial random number seed [-1]'
    print '   -m, --num_events     = number of pythia events to analyze [1000]'
    print '   -l, --log     : turn on log scale'
    print '   -b, --bins     = number of histogram bins [40]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hcqae:n:x:s:m:lb:', \
              ['help','QCD','QED','all','eCM=','pTHatMin=','pTHatMax=','seed=','num_events=','log','bins='])
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

    # histogram settings
    show_all = False
    bins = 40
    log = False

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-c', '--QCD'):
            parameters = [['on','off',111]]
        elif o in ('-q', '--QED'):
            parameters = [['off','on',111]]
        elif o in ('-a', '--all'):
            show_all = True
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
        elif o in ('-l', '--log'):
            log = True
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

    for setting in parameters:
        QCD = setting[0]
        QED = setting[1]
        subplot = setting[2]
        
        nCh_111 = []
        nCh_112 = []
        nCh_113 = []
        nCh_114 = []
        nCh_115 = []
        nCh_116 = []
        nCh_121 = []
        nCh_122 = []
        nCh_123 = []
        nCh_124 = []
        nCh_201 = []
        nCh_202 = []
        nCh_203 = []
        nCh_204 = []
        nCh_205 = []
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
        
        # Begin event loop. Generate. Tally charged particles for each type of hard process.
        for iEvent in range(num_events):
            if not pythia.next(): break
        
            a = pythia.info.code()
            event_types.append(a)
        
            if a == 111:
                nCharge_111 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_111 = nCharge_111 + 1
                nCh_111.append(nCharge_111)
            elif a == 112:
                nCharge_112 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_112 = nCharge_112 + 1
                nCh_112.append(nCharge_112)
            elif a == 113:
                nCharge_113 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_113 = nCharge_113 + 1
                nCh_113.append(nCharge_113)
            elif a == 114:
                nCharge_114 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_114 = nCharge_114 + 1
                nCh_114.append(nCharge_114)
            elif a == 115:
                nCharge = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge = nCharge + 1
                nCh_115.append(nCharge)
            elif a == 116:
                nCharge = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge = nCharge + 1
                nCh_116.append(nCharge)
            elif a == 121:
                nCharge = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge = nCharge + 1
                nCh_121.append(nCharge)
            elif a == 122:
                nCharge = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge = nCharge + 1
                nCh_122.append(nCharge)
            elif a == 123:
                nCharge = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge = nCharge + 1
                nCh_123.append(nCharge)
            elif a == 124:
                nCharge_124 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_124 = nCharge_124 + 1
                nCh_124.append(nCharge_124)
            elif a == 201:
                nCharge_201 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_201 = nCharge_201 + 1
                nCh_201.append(nCharge_201)
            elif a == 202:
                nCharge_202 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_202 = nCharge_202 + 1
                nCh_202.append(nCharge_202)
            elif a == 203:
                nCharge_203 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_203 = nCharge_203 + 1
                nCh_203.append(nCharge_203)
            elif a == 204:
                nCharge_204 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_204 = nCharge_204 + 1
                nCh_204.append(nCharge_204)
            elif a == 205:
                nCharge_205 = 0
                for prt in pythia.event:
                    if prt.isFinal() and prt.isCharged():
                        nCharge_205 = nCharge_205 + 1
                nCh_205.append(nCharge_205)
         
        # End of event loop. Statistics. Histogram. Done.
        pythia.stat();
        
        # set number of desired bins(b) and range(r)
        b=40
        # r=(20,60)
        
        # create bins using np.histogram
        plt.subplot(subplot)
        
        if QCD == 'on':
            w,binEdges=np.histogram(nCh_111,bins=b) #,range=r)
            wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            x,binEdges=np.histogram(nCh_112,bins=b) #,range=r)
            xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            y,binEdges=np.histogram(nCh_113,bins=b) #,range=r)
            ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            z,binEdges=np.histogram(nCh_114,bins=b) #,range=r)
            zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            ww,binEdges=np.histogram(nCh_115,bins=b) #,range=r)
            wwbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            xx,binEdges=np.histogram(nCh_116,bins=b) #,range=r)
            xxbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            yy,binEdges=np.histogram(nCh_121,bins=b) #,range=r)
            yybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            zz,binEdges=np.histogram(nCh_122,bins=b) #,range=r)
            zzbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            www,binEdges=np.histogram(nCh_123,bins=b) #,range=r)
            wwwbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            xxx,binEdges=np.histogram(nCh_124,bins=b) #,range=r)
            xxxbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            
            if len(nCh_111) > 0:
                plt.plot(wbincenters,w,'o',label='gg->gg')
            if len(nCh_113) > 0:
                plt.plot(ybincenters,y,'^',label='qg->qg')
            if len(nCh_114) > 0:
                plt.plot(zbincenters,z,'s',label="qq(bar)'->qq(bar)'")
            if show_all:
                if len(nCh_112) > 0:
                    plt.plot(xbincenters,x,'*',label='gg->qq(bar)')
                if len(nCh_115) > 0:
                    plt.plot(wwbincenters,ww,'d',label="q qbar -> g g")
                if len(nCh_116) > 0:
                    plt.plot(xxbincenters,xx,'8',label="q qbar -> q' qbar'")
                if len(nCh_121) > 0:
                    plt.plot(yybincenters,yy,'h',label="g g -> c cbar")
                if len(nCh_122) > 0:
                    plt.plot(zzbincenters,zz,'+',label="q qbar -> c cbar")
                if len(nCh_123) > 0:
                    plt.plot(wwwbincenters,www,'D',label="g g -> b bbar")
                if len(nCh_124) > 0:
                    plt.plot(xxxbincenters,xxx,'v',label="q qbar -> b bbar")
            if log:
                plt.yscale('log')
            
            plt.title("Pythia hard QCD processes")
            plt.xlabel("charged multiplicity")
            plt.ylabel("counts")
            plt.legend(loc=0)
            
        if QED == 'on':
            v,binEdges=np.histogram(nCh_201,bins=b)
            vbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            w,binEdges=np.histogram(nCh_202,bins=b)
            wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            x,binEdges=np.histogram(nCh_203,bins=b)
            xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            y,binEdges=np.histogram(nCh_204,bins=b)
            ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            z,binEdges=np.histogram(nCh_205,bins=b) 
            zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            
            if len(nCh_201) > 0:
                plt.plot(vbincenters,v,'o',label='q g -> q gamma (udscb)')
            if len(nCh_202) > 0:
                plt.plot(wbincenters,w,'d',label='q qbar -> g gamma')
            if show_all:
                if len(nCh_203) > 0:
                    plt.plot(xbincenters,x,'*',label='g g -> g gamma')
                if len(nCh_204) > 0:
                    plt.plot(ybincenters,y,'^',label='f fbar -> gamma gamma')
                if len(nCh_205) > 0:
                    plt.plot(zbincenters,z,'s',label="g g -> gamma gamma")
            if log:
                plt.yscale('log')
            
            plt.title("Pythia hard QED processes")
            plt.xlabel("charged multiplicity")
            plt.ylabel("counts")
            plt.legend(loc=0)
                    
    plt.show(block=False)

    query = raw_input("<CR> to continue, p to save to pdf: ")
    if (query=='p'):
        query = raw_input("name this pdf file (do not include extension .pdf): ")
        filename = query + '.pdf'
        plt.savefig(filename)
        print 'file saved as', filename
        query = raw_input("<CR> to continue: ")
    
    
if __name__ == '__main__':main()
