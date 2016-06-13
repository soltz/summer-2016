
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import getopt, sys

def usage():
    print 'Creats a 2d histogram for trento background.'
    print 'Usage: python 2d_hist_trento.py [options]'
    print '   -h, --help      : this message'
    print '   -f, --file     = set trento data file [AuAu_200GeV_100k.txt]'
    print '   -b, --bins     = number of histogram bins [20]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:b:', \
              ['help','file=','bins='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    trento_file = 'AuAu_200GeV_100k.txt'
    bins = 20

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-f', '--file'):
            trento_file = str(a)
        elif o in ('-b', '--bins'):
            bins = int(a)
        else:
            assert False, 'unhandled option'

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
    
    # rho_0 scaling parameter for radial flow
    # from Retiere and Lisa, PRC70.044907 (2004), table 2
    rho_0 = 0.85
    
    # e2 scaling parameter for elliptic flow
    # from Alver and Roland, PRC81.054905 (2010), fig 4
    rho_2 = 0.15
    
    for i in range(len(mult)): 
    
        pT = []
        phi = []
        eta = []
    
        print "multiplicity: ", mult[i]
        print "e2: ", e2[i]
        
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

            # particle selected randomly, mass in GeV
            if r5 <= 0.11:
                mass = 0.140 # pi+
            if r5 > 0.11 and r5 <= 0.22:
                mass = 0.140 # pi-
            if r5 > 0.22 and r5 <= 0.33:
                mass = 0.135 # pi0
            if r5 > 0.33 and r5 <= 0.44:
                mass = 0.494 # K+
            if r5 > 0.44 and r5 <= 0.55:
                mass = 0.494 # K-
            if r5 > 0.55 and r5 <= 0.66:
                mass = 0.938 # p
            if r5 > 0.66 and r5 <= 0.77:
                mass = 0.938 # pbar
            if r5 > 0.77 and r5 <= 0.88:
                mass = 0.940 # n
            if r5 > 0.88 and r5 <= 0.99:
                mass = 0.940 # nbar
    
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
    
            pT.append(pT_wflow)
            phi.append(phi_r2)
            eta.append(eta_r3)
            
    #   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
        tot_bins = bins**2
        h, xedges, yedges = np.histogram2d(eta,phi,bins=bins,range=[[-2,2], [-(np.pi), np.pi]],weights=pT)
        h = np.concatenate(h)
        xcenters = 0.5*(xedges[1:]+xedges[:-1])
        xcenters = np.repeat(xcenters,bins)
        ycenters = 0.5*(yedges[1:]+yedges[:-1])
        ycenters = np.tile(ycenters,bins)
    
        base = np.zeros(len(h))
    
    #   Create an array of colors to color the bars
        bar_colors = []
        for j in range(len(h)):
            if h[j] == 0:
                bar_colors.append('w')
            else:
                bar_colors.append('b')
                
    #   Set size of bars in plot
        d_eta = (xedges[1]-xedges[0])
        d_phi = (yedges[1]-yedges[0])
    
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.bar3d(xcenters, ycenters, base, d_eta, d_phi, h, color = bar_colors, alpha = 1)
    
        ax.set_xlabel('\n$\eta$',fontsize=20)
        ax.set_ylabel('\n$\phi$',fontsize=20)
        ax.set_zlabel('pT')
        
        title = 'trento data: multiplicity = ' + str(mult[i])
        plt.title(title)
        
        pi = np.pi
        plt.ylim(-pi,pi)
    
        plt.show(block = False)
        
        query = raw_input("q to quit, p to save to png,  <CR> to continue: ")
        if (query=='q'):
            break
        if (query=='p'):
            query = raw_input("name this png file (do not include extension .png): ")
            filename = query + '.png'
            plt.savefig(filename)
            print 'file saved as', filename
            query = raw_input("q to quit, <CR> to continue: ")
            if (query=='q'):
                break
        else: continue

if __name__ == '__main__':main()
    

