
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles
from scipy.interpolate import interp1d
from scipy.optimize import leastsq


def bin_data(trento_file, tot_events):
    #   import data for trento events
    data = np.loadtxt(trento_file)
    #   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]

    #   separate data into its separate parts
    Npart = data[:,2]
    mult = data[:,3]

    #   scale mult
    mult = mult/tot_events
    mult = mult/(Npart*0.5)

    p = np.arange(0,1.05,0.05)
    quan = mquantiles(Npart, prob = p)

    binned_mult, binedges = np.histogram(Npart, bins=quan, weights = mult)

    #   create weighted bin centers
    weighted_bins = []
    for i in range(len(binedges) - 1):
        if i == len(binedges) -2 :
            weighted_bins.append(Npart[(Npart >= binedges[i]) & (Npart <= binedges[i+1])])
        else:
            weighted_bins.append(Npart[(Npart >= binedges[i]) & (Npart < binedges[i+1])])
    for i in range(len(weighted_bins)):
        if i == 0:
            weighted_bins[i] = 2
        else:
            weighted_bins[i] = np.mean(weighted_bins[i])

    #   remove first data points from trento data
    weighted_bins = weighted_bins[8:len(weighted_bins)-1]
    binned_mult = binned_mult[8:len(binned_mult)-1]

    return [weighted_bins, binned_mult]

#weighted_10k, mult2_10k = bin_data('auau_10k.txt', 10000)
weighted_100k, mult2_100k = bin_data('AuAu_200GeV_100k.txt', 100000)
#weighted_1M, mult2_1M = bin_data('AuAu_200GeV_1M.txt', 1000000)


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
#interp_10k = inter_func(weighted_10k)
interp_100k = inter_func(weighted_100k)
#interp_1M = inter_func(weighted_1M)

#   fit
def residuals(A, y1, y2):
    err = y2 - (A * y1)
    return err
def eval(x, A):
    return A * x
A0 = np.array([100])

#A_10k, jac_val = leastsq(residuals, A0, args=(mult2_10k, interp_10k))
#fit_10k = eval(mult2_10k, A_10k)

A_100k, jac_val = leastsq(residuals, A0, args=(mult2_100k, interp_100k))
fit_100k = eval(mult2_100k, A_100k)

#A_1M, jac_val = leastsq(residuals, A0, args=(mult2_1M, interp_1M))
#fit_1M = eval(mult2_1M, A_1M)

plt.figure(1)

#plt.plot(weighted_10k, interp_10k, '^', color = 'b', label = 'interp_10k')
#plt.plot(weighted_100k, interp_100k, '^', color = 'r', label = 'interp_100k')
#plt.plot(weighted_1M, interp_1M, '^', color = 'g', label = 'interp_1M')

#plt.plot(weighted_10k, mult2_10k, 'o', color = 'b', label = 'trento 10k')
#plt.plot(weighted_100k, mult2_100k, 'o', color = 'r', label = 'trento 100k')
#plt.plot(weighted_1M, mult2_1M, 'o', color = 'g', label = 'trento 1M')

#plt.plot(weighted_10k, fit_10k, 'o', color = 'b', label = 'trento 10k')
plt.plot(weighted_100k, fit_100k, 'o', color = 'r', label = 'trento 100k')
#plt.plot(weighted_1M, fit_1M, 'o', color = 'g', label = 'trento 1M')

plt.errorbar(Npart,scaled_dNch, yerr = pub_err, fmt = '.', label = 'phenix')

plt.title('phenix data / trento comparison')
plt.ylabel("(dN$_{ch}$/d$\eta$)/(N$_{part}$/2)")
plt.xlabel("\nN$_{part}$")
plt.legend(loc=0)

plt.show()
