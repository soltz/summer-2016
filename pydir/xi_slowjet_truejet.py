
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles
import numpy as np
import math
import pythia8
import getopt, sys

def usage():
    print 'Compares xi for true and reconstructed jets when trento is on/off and for QED/QCD events, four plots generated'
    print 'Usage: python compare_xi.py [options]'
    print '   -h, --help      : this message'
    print '   -f, --file     = set trento data file [AuAu_200GeV_100k.txt]'
    print '   -e, --eCM     = pythia beam center-of-mass energy (GeV) [200.0]'
    print '   -n, --pTHatMin     = pythia minimum jet pT [20.0]'
    print '   -x, --pTHatMax     = pythia maximum jet pT [25.0]'
    print '   -s, --seed     = pythia initial random number seed [-1]'
    print '   -m, --num_events     = number of pythia events to analyze [1000]'
    print '   -p, --pTjetMin     = minimum slowJet pT [15]'
    print '   -b, --bins     = number of histogram bins [30]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:e:n:x:s:m:p:b:', \
              ['help','file=','eCM=','pTHatMin=','pTHatMax=','seed=','num_events=','pTjetMin=','bins='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    # default trento file
    trento_file = 'AuAu_200GeV_100k.txt'
    
    # default pythia settings
    eCM  = 200.0
    pTHatMin  = 20.0
    pTHatMax  = 25.0
    seed  = -1
    num_events = 1000

    # default slowJet setting
    pTjetMin = 15

    # default number of histogram bins
    bins = 30

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
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
        elif o in ('-m', '--num_events'):
            num_events = int(a)
        elif o in ('-p', '--pTjetMin'):
            pTjetMin = float(a)
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

    # parameters is a list used to run the settings needed to create the four separated plots
    parameters = [[False,'off','on',221],[True,'off','on',222],[False,'on','off',223],[True,'on','off',224]]

    for settings in parameters:
        trento = settings[0]
        QCD = settings[1]
        QED = settings[2]
        subplot = settings[3]
        
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
        massSet = 2    
        
        xi_r1 = []
        xi_r2 = []
        xi_r3 = []
        xi_true = []

        # begin looping through pythia events
        for i in range(num_events):
        
            pythia.event.reset()
            pythia.next()

            # the daughters of the initial hard process are recorded below
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

            # a value of xi is calculated for each particle within each pythia jet
            for j in range(pythia.event.size()):
                prt = pythia.event[j]
                if prt.isFinal():
                    if j in daughters5:
                        jet_px = pythia.event[5].px()
                        jet_py = pythia.event[5].py()
                        jet_pz = pythia.event[5].pz()
    
                        prt_px = prt.px()
                        prt_py = prt.py()
                        prt_pz = prt.pz()
    
                        z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
    
                        if z > 0:
                            prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
                            xi_true.append(prt_xi)
    
                    if j in daughters6:
                        jet_px = pythia.event[6].px()
                        jet_py = pythia.event[6].py()
                        jet_pz = pythia.event[6].pz()
    
                        prt_px = prt.px()
                        prt_py = prt.py()
                        prt_pz = prt.pz()
    
                        z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
    
                        if z > 0:
                            prt_xi = math.log((jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz))
                            xi_true.append(prt_xi)

            # if trento is on then trento particles are created and added to the pythia data
            if trento:
                for j in range(mult[i]):
                    r1, r2, r3, r4, r5 = np.random.random(5)
                    while r5 > 0.99:
                        r5 = np.random.random(1)
                
                    # pT = transverse momentum
                    pT_r1 = T*(math.sqrt(-2*math.log(r1)))
                
                    # phi = azimuthal angle
                    phi_r2 = 2*(math.pi)*(r2 - 0.5)
                
                    # eta = pseudo-rapidity
                    eta_r3 = deta*(r3 - 0.5)
                
                    # rho = normalized radial distance 
                    rho_r4 = r4**0.5
    
                    # particle selected randomly
                    if r5 <= 0.11:
                        mass = 0.140
                        pid = 211 # pi+
                    if r5 > 0.11 and r5 <= 0.22:
                        mass = 0.140
                        pid = -211 # pi-
                    if r5 > 0.22 and r5 <= 0.33:
                        mass = 0.135
                        pid = 111 # pi0
                    if r5 > 0.33 and r5 <= 0.44:
                        mass = 0.494
                        pid = 321 # K+
                    if r5 > 0.44 and r5 <= 0.55:
                        mass = 0.494
                        pid = -321 # K-
                    if r5 > 0.55 and r5 <= 0.66:
                        mass = 0.938
                        pid = 2212 # p
                    if r5 > 0.66 and r5 <= 0.77:
                        mass = 0.938
                        pid = -2212 # pbar
                    if r5 > 0.77 and r5 <= 0.88:
                        mass = 0.940
                        pid = 2112 # n
                    if r5 > 0.88 and r5 <= 0.99:
                        mass = 0.940
                        pid = -2112 # nbar
                
                    # calculate initial transverse rapidity (yT)
                    eT = (mass*mass+pT_r1*pT_r1)**0.5
                    yT = 0.5 * np.log((eT+pT_r1)/(eT-pT_r1))
                    pT_initial = pT_r1
                    yT_initial = yT
                
                    # apply flow as additive boost to transverse rapidity
                    yBoost = rho_r4*rho_0 + rho_2*e2[i]*np.cos(2*phi_r2)
                    yT = yT_initial + yBoost
                
                    # convert back to pT
                    pT_wflow = mass*np.cosh(yT)
                
                    # add particles to the event list
                    px = pT_wflow * math.cos(phi_r2)
                    py = pT_wflow * math.sin(phi_r2)
                    pz = pT_wflow * math.sinh(eta_r3)
                    E = (pT_wflow**2 + pz**2 + mass**2)**0.5
                    pythia.event.append(pid, 200, 0, 0, px, py, pz, E, mass, 0., 9.)
                
            # Initialize slowJet for radius 0.3
            slowJet = pythia8.SlowJet( -1, 0.3, pTjetMin, etaMax, nSel, massSet)
            slowJet.analyze(pythia.event)
            jets_found = slowJet.sizeJet()
    
            # Extract jet constituents and convert nested list for ease of manipulation
            slowJetPrtList = [[] for j in range(jets_found)]
            for j in range(jets_found):
                slowJetPrtList[j] = list(slowJet.constituents(j))
    
            # Calculate xi for reconstructed jets
            for j in range(pythia.event.size()):
                prt = pythia.event[j]
                if prt.isFinal():
                    for k in range(len(slowJetPrtList)):
                        inJet = -1
                        if j in slowJetPrtList[k]:
                            inJet = k
                        if (inJet >= 0):
                            jet_pT = slowJet.pT(k)
                            jet_phi = slowJet.phi(k)
                            jet_y = slowJet.y(k)
                            
                            prt_px = prt.px()
                            prt_py = prt.py()
                            prt_pz = prt.pz()
    
                            jet_px = jet_pT * math.cos(jet_phi)
                            jet_py = jet_pT * math.sin(jet_phi)
                            jet_pz = jet_pT * math.sinh(jet_y)
    
                            z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
    
                            if z > 0:
                                prt_xi = math.log(z)
                                xi_r1.append(prt_xi)
    
            # Initialize slowJet for radius 0.5
            slowJet = pythia8.SlowJet( -1, 0.5, pTjetMin, etaMax, nSel, 1)
            slowJet.analyze(pythia.event)
            jets_found = slowJet.sizeJet()
    
            # Extract jet constituents and convert nested list for ease of manipulation
            slowJetPrtList = [[] for j in range(jets_found)]
            for j in range(jets_found):
                slowJetPrtList[j] = list(slowJet.constituents(j))
                
            # Calculate xi for reconstructed jets
            for j in range(pythia.event.size()):
                prt = pythia.event[j]
                if prt.isFinal():
                    for k in range(len(slowJetPrtList)):
                        inJet = -1
                        if j in slowJetPrtList[k]:
                            inJet = k
                        if (inJet >= 0):
                            jet_pT = slowJet.pT(k)
                            jet_phi = slowJet.phi(k)
                            jet_y = slowJet.y(k)
                            
                            prt_px = prt.px()
                            prt_py = prt.py()
                            prt_pz = prt.pz()
    
                            jet_px = jet_pT * math.cos(jet_phi)
                            jet_py = jet_pT * math.sin(jet_phi)
                            jet_pz = jet_pT * math.sinh(jet_y)
    
                            z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
    
                            if z > 0:
                                prt_xi = math.log(z)
                                xi_r2.append(prt_xi)
    
            # Initialize slowJet for radius 0.7
            slowJet = pythia8.SlowJet( -1, 0.7, pTjetMin, etaMax, nSel, 1)
            slowJet.analyze(pythia.event)
            jets_found = slowJet.sizeJet()
    
            # Extract jet constituents and convert nested list for ease of manipulation
            slowJetPrtList = [[] for j in range(jets_found)]
            for j in range(jets_found):
                slowJetPrtList[j] = list(slowJet.constituents(j))
                
            # Calculate xi for reconstructed jets
            for j in range(pythia.event.size()):
                prt = pythia.event[j]
                if prt.isFinal():
                    for k in range(len(slowJetPrtList)):
                        inJet = -1
                        if j in slowJetPrtList[k]:
                            inJet = k
                        if (inJet >= 0):
                            jet_pT = slowJet.pT(k)
                            jet_phi = slowJet.phi(k)
                            jet_y = slowJet.y(k)
                            
                            prt_px = prt.px()
                            prt_py = prt.py()
                            prt_pz = prt.pz()
    
                            jet_px = jet_pT * math.cos(jet_phi)
                            jet_py = jet_pT * math.sin(jet_phi)
                            jet_pz = jet_pT * math.sinh(jet_y)
    
                            z = (jet_px**2 + jet_py**2 + jet_pz**2)/(prt_px*jet_px + prt_py*jet_py + prt_pz*jet_pz)
    
                            if z > 0:
                                prt_xi = math.log(z)
                                xi_r3.append(prt_xi)
    
        # define function for bin error
        def bin_err(bin_counts):
            bin_err = []
            for val in bin_counts:
                if val != 0:
                    bin_err.append(val**0.5)
                else:
                    bin_err.append(0)
            return bin_err
        
        # put xi data into histogram bins
        w,binEdges = np.histogram(xi_true,bins=bins) 
        wbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        werror = bin_err(w)
    
        x,binEdges = np.histogram(xi_r1,bins=bins) 
        xbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        xerror = bin_err(x)
        
        y,binEdges = np.histogram(xi_r2,bins=bins) 
        ybincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        yerror = bin_err(y)
        
        z,binEdges = np.histogram(xi_r3,bins=bins) 
        zbincenters = 0.5*(binEdges[1:]+binEdges[:-1])
        zerror = bin_err(z)
        
        # create plot with title and legend
        plt.subplot(subplot)
        plt.errorbar(wbincenters, w, yerr = werror, fmt = 'o', label = 'true xi')
        plt.errorbar(xbincenters, x, yerr = xerror, fmt = '^', label = 'xi, r = 0.3')
        plt.errorbar(ybincenters, y, yerr = yerror, fmt = 's', label = 'xi, r = 0.5')
        plt.errorbar(zbincenters, z, yerr = zerror, fmt = 'd', label = 'xi, r = 0.7')

        plt.ylim(ymin=0)
        plt.xlabel('xi', fontsize = 15)
        plt.ylabel('counts', fontsize = 15)
        plt.xlim(0,10)

        if trento:
            if QCD == 'on':
                title = 'QCD Jets with TRENTO Background'
            if QED == 'on':
                title = 'QED Jets with TRENTO Background'
        else:
            if QCD == 'on':
                title = 'QCD Jets, no TRENTO Background'
            if QED == 'on':
                title = 'QED Jets, no TRENTO Background'
        
        plt.title(title, fontsize = 15)

        
        plt.legend(loc=0)

    plt.show(block = False)

    query = raw_input("<CR> to continue, p to save to pdf: ")
    if (query=='p'):
        query = raw_input("name this pdf file (do not include extension .pdf): ")
        filename = query + '.pdf'
        plt.savefig(filename)
        print 'file saved'
        query = raw_input("<CR> to continue: ")
    
if __name__ == '__main__':main()
