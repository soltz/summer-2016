
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles
import numpy as np
import math
import pythia8
import getopt, sys

def usage():
    print 'Shows the frequency of slowJet jet pT when the pT of pythia events is restricted to 20-25 GeV/c.'
    print 'Usage: python 3d_jetplot_2016.py [options]'
    print '   -h, --help      : this message'
    print '   -t, --trento     : include trento background'
    print '   -f, --file     = set trento data file [AuAu_200GeV_100k.txt]'
    print '   -e, --eCM     = pythia beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = pythia minimum jet pT [20.0]'
    print '   -x, --pTHatMax     = pythia maximum jet pT [25.0]'
    print '   -s, --seed     = pythia initial random number seed [-1]'
    print '   -c, --QCD     = pythia hard QCD processes on/off [on]'
    print '   -q, --QED     = pythia hard QED processes on/off [off]'
    print '   -p, --pTjetMin     = minimum slowJet pT [15]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'htf:e:n:x:s:c:q:p:', \
              ['help','trento','file=','eCM=','pTHatMin=','pTHatMax=','seed=','QCD=','QED=','pTjetMin='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    trento  = False
    trento_file = 'AuAu_200GeV_100k.txt'
    
    # pythia settings
    eCM  = 200.0
    pTHatMin  = 20.0
    pTHatMax  = 25.0
    seed  = -1
    QCD = 'on'
    QED = 'off'

    # minimum slowJet pT
    pTjetMin = 15

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-t', '--trento'):
            trento = True
        elif o in ('-f', '--file'):
            trento_file = str(a)
        elif o in ('-e', '--eCM'):
            eCM = float(a)
        elif o in ('-n', '--pTHatMin'):
            pTHatMin = float(a)
        elif o in ('-x', '--pTHatMax'):
            pTHatMax = float(a)
        elif o in ('-s', '--seed'):
            seed = int(a)
        elif o in ('-c', '--QCD'):
            QCD = str(a)
        elif o in ('-q', '--QED'):
            QED = str(a)
        elif o in ('-p', '--pTjetMin'):
            pTjetMin = float(a)
        else:
            assert False, 'unhandled option'

    if trento:
        #   load trento data for 100,000 Au Au events
        data = np.loadtxt(trento_file)
        
        #   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
        #   create a list for the initial entropy of the events
        mult = data[:,3]
        e2 = data[:,4]
        
        #   apply proportionality constanst to convert initial entropy to charged multiplicity
        #   constant was calculated by fitting the trento data to phenix data
        mult = 4.65905256 * mult
        
        #   change the constituents of mult to int values
        for i in range(len(mult)):
            mult[i] = round(mult[i])
        mult = mult.astype(np.int64)
            
    T = 0.15 # temperature in GeV
    deta = 4
    # set pion mass to 0.14 GeV
    mpi = 0.14
    
    # rho_0 scaling parameter for radial flow
    # from Retiere and Lisa, PRC70.044907 (2004), table 2
    rho_0 = 0.85
    
    # e2 scaling parameter for elliptic flow
    # from Alver and Roland, PRC81.054905 (2010), fig 4
    rho_2 = 0.15
    
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
    radius = [0.2,0.4,0.6,0.8]
    
    slowJet_pT = [[],[],[],[]]
    
    for i in range(1000):
    
        pythia.event.reset()
        pythia.next()

        if trento:
            for j in range(mult[i]):
                r1, r2, r3, r4 = np.random.random(4)
            
                # pT = transverse momentum
                pT_r1 = T*(math.sqrt(-2*math.log(r1)))
            
                # phi = azimuthal angle
                phi_r2 = 2*(math.pi)*(r2 - 0.5)
            
                # eta = pseudo-rapidity
                eta_r3 = deta*(r3 - 0.5)
            
                # rho = normalized radial distance 
                rho_r4 = r4**0.5
            
                # calculate initial transverse rapidity (yT)
                eT = (mpi*mpi+pT_r1*pT_r1)**0.5
                yT = 0.5 * np.log((eT+pT_r1)/(eT-pT_r1))
                pT_initial = pT_r1
                yT_initial = yT
            
                # apply flow as additive boost to transverse rapidity
                yBoost = rho_r4*rho_0 + rho_2*e2[i]*np.cos(2*phi_r2)
                yT = yT_initial + yBoost
            
                # convert back to pT
                pT_wflow = mpi*np.cosh(yT)
            
                # add particles to the event list
                px = pT_wflow * math.cos(phi_r2)
                py = pT_wflow * math.sin(phi_r2)
                pz = pT_wflow * math.sinh(eta_r3)
                E = (pT_wflow**2 + pz**2 + mpi**2)**0.5
                pythia.event.append(211, 91, 0, 0, px, py, pz, E, mpi, 0., 9.)
            
        for j in range(len(radius)):
            slowJet = pythia8.SlowJet( -1, radius[j], pTjetMin, etaMax, nSel, 1)
            slowJet.analyze(pythia.event)
            jets_found = slowJet.sizeJet()
        
            for k in range(jets_found):
                pT_jet = slowJet.pT(k)
                slowJet_pT[j].append(pT_jet)
    
    for i in range(4):
        slowJet_pT[i] = np.array(slowJet_pT[i])
        
        counts, binedges = np.histogram(slowJet_pT[i], bins = 40)
        
        #   create weighted bin centers
        weighted = []
        
        for j in range(len(binedges) - 1):
            if j == len(binedges) -2 :
                weighted.append(slowJet_pT[i][(slowJet_pT[i] >= binedges[j]) & (slowJet_pT[i] <= binedges[j+1])])
            else:
                weighted.append(slowJet_pT[i][(slowJet_pT[i] >= binedges[j]) & (slowJet_pT[i] < binedges[j+1])])
        
        for j in range(len(weighted)):
            weighted[j] = np.mean(weighted[j])
        
        plt_label = "rad: " + str(radius[i])
        plt.plot(weighted,counts,'o',label=plt_label)
        
    plt.ylabel('counts')
    
    xlabel = 'slowJet_pT: pTjetMin = ' + str(pTjetMin)
    plt.xlabel(xlabel)
    
    title = 'slowJet_pT for pythia jet pT restricted to 20-25 GeV/c: trento '
    if trento:
        title = title + 'on'
    else:
        title = title + 'off'
    plt.title(title)
    
    plt.legend(loc=0)
    plt.show()
    
if __name__ == '__main__':main()
