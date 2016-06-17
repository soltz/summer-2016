
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles
from scipy.interpolate import interp1d
from scipy.optimize import leastsq
import getopt, sys

def usage():
    print 'Fits and compares trento data with Phenix experimental data.'
    print 'Usage: python phenix_trento_comp.py [options]'
    print '   -h, --help      : this message'
    print '   -f, --filename     = file with trento data, default is to plot all files [[AuAu_200GeV_100k.txt, AuAu_130GeV_100k.txt, AuAu_62p4GeV_100k.txt, AuAu_39GeV_100k.txt, AuAu_27GeV_100k.txt, AuAu_19p6GeV_100k.txt, AuAu_15p0GeV_100k.txt, AuAu_7p7GeV_100k.txt]]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:', \
              ['help','filename='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    filename  = ['AuAu_200GeV_100k.txt', 'AuAu_130GeV_100k.txt', 'AuAu_62p4GeV_100k.txt', 'AuAu_39GeV_100k.txt', 'AuAu_27GeV_100k.txt', 'AuAu_19p6GeV_100k.txt', 'AuAu_15p0GeV_100k.txt', 'AuAu_7p7GeV_100k.txt']

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-f', '--filename'):
            filename = str(a)
            filename = [filename]
        else:
            assert False, 'unhandled option'

    for tfile in filename:
        def bin_data(trento_file):
            #   import data for trento events
            data = np.loadtxt(trento_file)
            #   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]

            #   separate data into its separate parts
            Npart = data[:,2]
            mult = data[:,3]

            #   scale mult
            mult = mult/(Npart*0.5)

            p = np.arange(0,1.05,0.05)
            quan = mquantiles(Npart, prob = p)

            binned_mult, binedges = np.histogram(Npart, bins=quan, weights = mult)

            #   compile values in each bin
            weighted_bins = []
            for i in range(len(binedges) - 1):
                if i == len(binedges) -2 :
                    weighted_bins.append(Npart[(Npart >= binedges[i]) & (Npart <= binedges[i+1])])
                else:
                    weighted_bins.append(Npart[(Npart >= binedges[i]) & (Npart < binedges[i+1])])

            #   divide each bin by count of that bin for normalization
            weighted_bins = np.array(weighted_bins)
            for i in range(len(weighted_bins)):
                if len(weighted_bins[i]) == 0:
                    binned_mult[i] = binned_mult[i]
                else:
                    binned_mult[i] = binned_mult[i]/(len(weighted_bins[i]))
            weighted_bins = list(weighted_bins)
                
            #   record bin error
            bin_err = []
            for i in range(len(weighted_bins)):
                count = len(weighted_bins[i])
                if count == 0:
                    bin_err.append(0)
                else:
                    bin_err.append(1/((count)**0.5))
            bin_err = np.array(bin_err)
    
            #   average values in each bin
            for i in range(len(weighted_bins)):
                if len(weighted_bins[i]) == 0:
                    weighted_bins[i] = 0
                else:
                    weighted_bins[i] = np.mean(weighted_bins[i])
    
            return [weighted_bins, binned_mult, bin_err]
    
        weighted, mult2, bin_err = bin_data(tfile)
    
            #   phenix data
        if tfile  == 'AuAu_200GeV_100k.txt':
            Npart = np.array([350.9, 297.9, 251.0, 211.0, 176.3, 146.8, 120.9, 98.3, 78.7, 61.9, 47.6, 35.6])
            Npart = Npart[::-1]
            dNch = np.array([687.4, 560.4, 456.8, 371.5, 302.5, 245.6, 197.2, 156.4, 123.5, 95.3, 70.9, 52.2])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.22, 0.21, 0.21, 0.21, 0.22, 0.25, 0.28, 0.31, 0.34, 0.38, 0.44, 0.56])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_130GeV_100k.txt':
            Npart = np.array([347.7, 294.0, 249.5, 211.0, 178.6, 149.7, 124.8, 102.9, 83.2, 66.3, 52.1, 40.1])
            Npart = Npart[::-1]
            dNch = np.array([601.8, 488.5, 402.7, 328.8, 270.5, 219.3, 175.7, 139.0, 109.4, 84.1, 64.3, 48.4])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.19, 0.18, 0.17, 0.18, 0.18, 0.19, 0.21, 0.22, 0.25, 0.27, 0.31, 0.35])
            pub_err = pub_err[::-1]
    
        if tfile  == 'AuAu_62p4GeV_100k.txt':
            Npart = np.array([342.6, 291.3, 244.5, 205.0, 171.3, 142.2, 116.7, 95.2, 76.1, 59.9, 46.8, 35.8])
            Npart = Npart[::-1]
            dNch = np.array([447.5, 367.4, 301.8, 248.0, 203.0, 165.1, 133.0, 105.9, 83.0, 63.9, 48.4, 35.8])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.23, 0.23, 0.23, 0.23, 0.24, 0.24, 0.26, 0.26, 0.28, 0.30, 0.29, 0.30])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_39GeV_100k.txt':
            Npart = np.array([340.0, 289.6, 244.1, 206.5, 174.1, 145.8, 120.8, 98.6, 79.8, 63.9, 50.3])
            Npart = Npart[::-1]
            dNch = np.array([363.2, 297.8, 246.6, 204.4, 168.9, 138.3, 112.6, 90.6, 72.1, 56.8, 43.7])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.19, 0.19, 0.18, 0.18, 0.18, 0.18, 0.20, 0.20, 0.20, 0.22, 0.24])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_27GeV_100k.txt':
            Npart = np.array([338.9, 288.8, 244.3, 205.7, 173.0, 144.6, 119.4, 97.6, 77.9, 60.8])
            Npart = Npart[::-1]
            dNch = np.array([321.2, 258.7, 212.6, 175.0, 143.5, 116.7, 94.2, 75.0, 59.0, 45.7])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.17, 0.16, 0.16, 0.16, 0.15, 0.16, 0.16, 0.16, 0.17, 0.20])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_19p6GeV_100k.txt':
            Npart = np.array([338.5, 288.3, 242.4, 204.3, 172.4, 143.5, 117.9, 95.7, 77.4, 61.7])
            Npart = Npart[::-1]
            dNch = np.array([285.3, 229.3, 188.8, 155.7, 128.2, 104.8, 85.1, 68.4, 54.3, 42.4])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.15, 0.14, 0.14, 0.14, 0.14, 0.14, 0.15, 0.16, 0.16, 0.16])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_15p0GeV_100k.txt':    # phenix data is listed as 14.5 GeV
            Npart = np.array([337.3, 287.7, 242.5, 205.1, 172.6, 143.6, 119.2, 98.4, 80.2, 63.9])
            Npart = Npart[::-1]
            dNch = np.array([250.9, 201.2, 164.5, 134.7, 110.0, 89.4, 72.0, 57.4, 45.2, 34.9])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.13, 0.13, 0.12, 0.12, 0.12, 0.13, 0.13, 0.12, 0.13, 0.12])
            pub_err = pub_err[::-1]
            
        if tfile  == 'AuAu_7p7GeV_100k.txt':
            Npart = np.array([332.1, 283.2, 240.1, 204.1, 172.9, 145.5, 121.0, 98.2, 78.8, 61.8])
            Npart = Npart[::-1]
            dNch = np.array([192.4, 159.2, 129.3, 105.4, 85.6, 68.8, 55.0, 43.5, 33.9, 26.1])
            dNch = dNch[::-1]
            scaled_dNch = dNch/(Npart*0.5)
            pub_err = np.array([0.10, 0.10, 0.10, 0.09, 0.09, 0.09, 0.10, 0.10, 0.11, 0.11])
            pub_err = pub_err[::-1]
    
        #   remove values from trento data that are outside the range of the phenix data
        while min(weighted) < min(Npart):
            weighted = weighted[1:]
            mult2 = mult2[1:]
            bin_err = bin_err[1:]
            
        while max(weighted) > max(Npart):
            weighted = weighted[:len(weighted)-1]
            mult2 = mult2[:len(mult2)-1]
            bin_err = bin_err[:len(bin_err)-1]
            
        #   interpolation
        inter_func = interp1d(Npart, scaled_dNch, kind = 'quadratic', bounds_error = False)
        interp = inter_func(weighted)
    
    
        #   fit
        def residuals(A, y1, y2):
            err = y2 - (A * y1)
            return err
        def eval(x, A):
            return A * x
        A0 = np.array([4])
    
        A_fit, jac_val = leastsq(residuals, A0, args=(mult2, interp))
        fit = eval(mult2, A_fit)
        bin_err = eval(bin_err, A_fit)
        print "fit parameter: ", tfile, A_fit
    
        plt.figure(1)

        if tfile  == 'AuAu_200GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = '*', markerfacecolor = 'None', color = 'orange')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = '*', color = 'orange', label = '200 GeV Au + Au')
            
        if tfile  == 'AuAu_130GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 's', markerfacecolor = 'None', color = 'r')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 's', color = 'r', label = '130 GeV Au + Au')
           
        if tfile  == 'AuAu_62p4GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = '^', markerfacecolor = 'None', color = 'g')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = '^', color = 'g', label = '62.4 GeV Au + Au')
            
        if tfile  == 'AuAu_39GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 'd', markerfacecolor = 'None', color = 'c')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 'd', color = 'c', label = '39 GeV Au + Au')
             
        if tfile  == 'AuAu_27GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 'v', markerfacecolor = 'None', color = 'm')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 'v', color = 'm', label = '27 GeV Au + Au')
            
        if tfile  == 'AuAu_19p6GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 'p', markerfacecolor = 'None', color = 'y')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 'p', color = 'y', label = '19.6 GeV Au + Au')         
            
        if tfile  == 'AuAu_15p0GeV_100k.txt':    # phenix data is listed as 14.5 GeV
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 'o', markerfacecolor = 'None', color = 'b')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 'o', color = 'b', label = '14.5 GeV Au + Au')
                       
        if tfile  == 'AuAu_7p7GeV_100k.txt':
            plt.errorbar(weighted, fit, yerr = bin_err, marker = 'h', markerfacecolor = 'None', color = 'brown')
            plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = 'h', color = 'brown', label = '7.7 GeV Au + Au')
            
    
    plt.title('PHENIX data / TRENTO comparison')
    plt.ylabel("(dN$_{ch}$/d$\eta$)/(N$_{part}$/2)", fontsize = 15)
    plt.ylim(0.5,5)
    plt.xlabel("\nN$_{part}$\n", fontsize = 20)

    plt.legend(loc=0, fontsize = 12)
    plt.show(block = False)

    query = raw_input("<CR> to continue, p to save to pdf: ")
    if (query=='p'):
        query = raw_input("name this pdf file (do not include extension .pdf): ")
        filename = query + '.pdf'
        plt.savefig(filename)
        print 'file saved as', filename
        query = raw_input("<CR> to continue: ")

if __name__ == '__main__':main()
