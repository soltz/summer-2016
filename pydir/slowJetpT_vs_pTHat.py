# 
# PYTHIA is licenced under the GNU GPL version 2, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
#

import pythia8
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.stats.mstats import mquantiles
import getopt, sys

def usage():
    print '3d_jetplot_2016.py plots a 3d bar graph for p-p events created by pythia8.'
    print 'Usage: python 3d_jetplot_2016.py [options]'
    print '   -h, --help      : this message'
    print '   -t, --trento     : include trento background'
    print '   -f, --file     = set trento file [AuAu_200GeV_100k.txt]'
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
        opts, args = getopt.getopt(sys.argv[1:], 'htf:cqe:n:x:u:p:r:mib:s:', \
              ['help','trento','file=','QCD','QED','eCM=','pTHatMin=','pTHatMax=','num=','pTjetMin=','radius=','massSet','hist',
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

    # trento settings
    trento = False
    trento_file = 'AuAu_200GeV_100k.txt'

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
        elif o in ('-t', '--trento'):
            trento = True
        elif o in ('-f', '--file'):
            trento_file = str(a)
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

    if trento:
        #   load trento data for 100,000 Au Au events
        data = np.loadtxt(trento_file)

        #   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
        #   create a list for the initial entropy of the events
        mult = data[:,3]
        e2 = data[:,4]

        #   apply proportionality constanst to convert initial entropy to charged multiplicity
        #   constant was calculated by fitting the trento data to phenix data
        if trento_file == 'AuAu_200GeV_100k.txt':
            fit_par = 4.65905256
        if trento_file == 'AuAu_130GeV_100k.txt':
            fit_par = 3.96639009
        if trento_file == 'AuAu_62p4GeV_100k.txt':
            fit_par = 3.13381932
        if trento_file == 'AuAu_39GeV_100k.txt':
            fit_par = 2.54804101
        if trento_file == 'AuAu_27GeV_100k.txt':
            fit_par = 2.16041632
        if trento_file == 'AuAu_19p6GeV_100k.txt':
            fit_par = 1.95015905
        if trento_file == 'AuAu_15p0GeV_100k.txt':
            fit_par = 1.6460897
        if trento_file == 'AuAu_7p7GeV_100k.txt':
            fit_par = 1.27382896
        mult = fit_par * mult

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

#   Initialize SlowJet
    etaMax = 4.
    nSel = 2    
    slowJet = pythia8.SlowJet( -1, radius, pTjetMin, etaMax, nSel, massSet);

#   Loop over events recording both pTHat and the calculated slowJet pT
    pTHat = [[] for j in range(50)]
    slowJet_pT = [[] for j in range(50)]
    
    for i in range(num_events):
        pythia.next()
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

        #  use slowJet to analyze jets
        slowJet.analyze(pythia.event)
        for i in range(slowJet.sizeJet()):
            pTHat[i].append(pythia.info.pTHat())
            slowJet_pT[i].append(slowJet.pT(i))
            
#   End of event loop. Statistics. Histogram. Done.
    pythia.stat();

    if hist:
        def bin_data(data1,data2,r,bins):
            #   create quantiles for even binning
            steps = 1.0/bins
            p = np.arange(0,(1 + steps),steps)
            quan = mquantiles(data1, prob = p)

            #   ensure data is array type
            data1 = np.array(data1)

            binned_data, binedges = np.histogram(data1,bins=quan,range=r,weights=data2)

            #   compile values in each bin
            weighted_bins = []
            for i in range(len(binedges) - 1):
                if i == len(binedges) -2 :
                    weighted_bins.append(data1[(data1 >= binedges[i]) & (data1 <= binedges[i+1])])
                else:
                    weighted_bins.append(data1[(data1 >= binedges[i]) & (data1 < binedges[i+1])])

            #   divide each bin by count of that bin for normalization
            weighted_bins = np.array(weighted_bins)
            for i in range(len(weighted_bins)):
                if len(weighted_bins[i]) == 0:
                    binned_data[i] = binned_data[i]
                else:
                    binned_data[i] = binned_data[i]/(len(weighted_bins[i]))
            weighted_bins = list(weighted_bins)
                
            #   record bin error
            bin_err = []
            for i in range(len(weighted_bins)):
                count = len(weighted_bins[i])
                if count == 0:
                    bin_err.append(0)
                else:
                    bin_err.append(1/(count**0.5))
            bin_err = np.array(bin_err)
    
            #   average values in each bin
            for i in range(len(weighted_bins)):
                if len(weighted_bins[i]) == 0:
                    weighted_bins[i] = 0
                else:
                    weighted_bins[i] = np.mean(weighted_bins[i])
    
            return [weighted_bins, binned_data, bin_err]

        # range for binning
        r = (pTHatMin,pTHatMax)

        wbincenters, w, w_error = bin_data(pTHat[0],slowJet_pT[0],r,bins)
        xbincenters, x, x_error = bin_data(pTHat[1],slowJet_pT[1],r,bins)
        zbincenters, z, z_error = bin_data(pTHat[2],slowJet_pT[2],r,bins)

        plt.errorbar(wbincenters,w,yerr = w_error, fmt = 'o',label='slowJet 1')
        plt.errorbar(xbincenters,x,yerr = x_error, fmt = '^',label='slowJet 2')
        #plt.errorbar(zbincenters,z,yerr = z_error, fmt = 's',label='slowJet 3')

        
    if not hist:
        plt.plot(pTHat[0],slowJet_pT[0],'o',label='slowJet 1', alpha = 0.2)
        plt.plot(pTHat[1],slowJet_pT[1],'^',label='slowJet 2', alpha = 0.2)
        plt.plot(pTHat[2],slowJet_pT[2],'s',label='slowJet 3', alpha = 0.2)

    
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

