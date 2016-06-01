import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import mquantiles

data = np.loadtxt('auau_10k.txt')
#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]

#   separate data into its separate parts
event_number = data[:,0]
impact_param = data[:,1]
Npart = data[:,2]
mult = data[:,3]
e2 = data[:,4]
e3 = data[:,5]
e4 = data[:,6]
e5 = data[:,7]

p = np.arange(0,1.05,0.05)
quan = mquantiles(Npart, prob = p)

counts, binedges = np.histogram(Npart, bins = quan)
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

plt.figure(1)
plt.plot(weighted, counts, 'o')
plt.title('bins')
plt.xlabel('Npart')
plt.ylabel('counts')

plt.figure(2)
plt.plot(weighted, mult_2, 'o')
plt.title('mult vs. Npart')
plt.xlabel('Npart')
plt.ylabel('mult')

plt.show()
