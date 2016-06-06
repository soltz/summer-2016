
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
    print '   -f, --filename     = file with trento data [AuAu_200GeV_100k.txt]'

def main():

#   Parse command line and set defaults (see http://docs.python.org/library/getopt.html)
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:', \
              ['help','filename='])
    except getopt.GetoptError, err:
        print str(err) # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)

    filename  = 'AuAu_200GeV_100k.txt'

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        elif o in ('-f', '--filename'):
            filename = str(a)
        else:
            assert False, 'unhandled option'

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
            if i == 0:
                weighted_bins[i] = 0
            else:
                weighted_bins[i] = np.mean(weighted_bins[i])

        #   remove first data points from trento data
        weighted_bins = weighted_bins[8:len(weighted_bins)-1]
        binned_mult = binned_mult[8:len(binned_mult)-1]
        bin_err = bin_err[8:len(bin_err)-1]

        return [weighted_bins, binned_mult, bin_err]

    weighted, mult2, bin_err = bin_data(filename)

    #   phenix data
    #   200 GeV Au Au
    Npart = np.array([350.9, 297.9, 251.0, 211.0, 176.3, 146.8, 120.9, 98.3, 78.7, 61.9, 47.6, 35.6])
    Npart = Npart[::-1]
    Npart_err = np.array([4.7, 6.6, 7.3, 7.3, 7.0, 7.1, 7.0, 6.8, 6.1, 5.2, 4.9, 5.1])
    Npart_err = Npart_err[::-1]
    dNch = np.array([687.4, 560.4, 456.8, 371.5, 302.5, 245.6, 197.2, 156.4, 123.5, 95.3, 70.9, 52.2])
    dNch = dNch[::-1]
    dNch_err = np.array([36.6, 27.9, 22.3, 18.2, 15.8, 13.8, 12.2, 10.9, 9.6, 8.6, 7.6, 6.5])
    dNch_err = dNch_err[::-1]
    scaled_dNch = dNch/(Npart*0.5)
    pub_err = np.array([0.22, 0.21, 0.21, 0.21, 0.22, 0.25, 0.28, 0.31, 0.34, 0.38, 0.44, 0.56])
    pub_err = pub_err[::-1]

    #   interpolation
    inter_func = interp1d(Npart, scaled_dNch, kind = 'quadratic', bounds_error = False)
    interp = inter_func(weighted)


    #   fit
    def residuals(A, y1, y2):
        err = y2 - (A * y1)
        return err
    def eval(x, A):
        return A * x
    A0 = np.array([100])

    A_fit, jac_val = leastsq(residuals, A0, args=(mult2, interp))
    fit = eval(mult2, A_fit)
    bin_err = eval(bin_err, A_fit)
    print "fit parameter: ", A_fit

    plt.figure(1)

    plt.errorbar(weighted, fit, yerr = bin_err, fmt = '.', color = 'r', label = 'trento data')
    plt.errorbar(Npart, scaled_dNch, yerr = pub_err, fmt = '.', color = 'b', label = 'phenix')

    plt.title('phenix data / trento comparison')
    plt.ylabel("(dN$_{ch}$/d$\eta$)/(N$_{part}$/2)")
    plt.xlabel("\nN$_{part}$")
    plt.legend(loc=0)

    plt.show()

if __name__ == '__main__':main()
