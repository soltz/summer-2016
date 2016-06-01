
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles

data = np.loadtxt('AuAu_200GeV_100k.txt')
#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]

#   separate data into its separate parts
Npart = data[:,2]
mult = data[:,3]

#   scale mult
mult = mult/1000
mult = mult/(Npart*0.5)

p = np.arange(0,1.05,0.05)
quan = mquantiles(Npart, prob = p)

mult_2, binedges = np.histogram(Npart, bins=quan, weights = mult)

#   create weighted bin centers
weighted = []
for i in range(len(binedges) - 1):
    if i == len(binedges) -2 :
        weighted.append(Npart[(Npart >= binedges[i]) & (Npart <= binedges[i+1])])
    else:
        weighted.append(Npart[(Npart >= binedges[i]) & (Npart < binedges[i+1])])
for i in range(len(weighted)):
    if i == 0:
        weighted[i] = 2
    else:
        weighted[i] = np.mean(weighted[i])

#   remove first data points from trento data
weighted = weighted[6:]
mult_2 = mult_2[6:]
        
#   phenix data
#   200 GeV Au Au
Npart = np.array([350.9, 297.9, 251.0, 211.0, 176.3, 146.8, 120.9, 98.3, 78.7, 61.9, 47.6, 35.6])
Npart_err = np.array([4.7, 6.6, 7.3, 7.3, 7.0, 7.1, 7.0, 6.8, 6.1, 5.2, 4.9, 5.1])
dNch = np.array([687.4, 560.4, 456.8, 371.5, 302.5, 245.6, 197.2, 156.4, 123.5, 95.3, 70.9, 52.2])
dNch_err = np.array([36.6, 27.9, 22.3, 18.2, 15.8, 13.8, 12.2, 10.9, 9.6, 8.6, 7.6, 6.5])

scaled_dNch = dNch/(Npart*0.5)
pub_err = np.array([0.22, 0.21, 0.21, 0.21, 0.22, 0.25, 0.28, 0.31, 0.34, 0.38, 0.44, 0.56])

plt.figure(1)
plt.errorbar(Npart,scaled_dNch, yerr = pub_err, fmt = '.', label = 'phenix')
plt.plot(weighted, mult_2, 'o', label = 'trento')
plt.title('phenix data / trento comparison')
plt.ylabel("(dN$_{ch}$/d$\eta$)/(N$_{part}$/2)")
plt.xlabel("\nN$_{part}$")
plt.legend(loc=0)

plt.show()
