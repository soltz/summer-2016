import numpy as np
import matplotlib.pyplot as plt

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


#   Creat plots for the following
#   Npart vs. impact parameter
#   mult vs. impact parameter
#   mult vs. Npart
#   e2 vs. Npart
#   e3 vs. Npart

plt.figure(1)

plt.subplot(231)
plt.hexbin(impact_param, Npart, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('Npart vs. impact parameter')

plt.subplot(232)
plt.hexbin(impact_param, mult, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('mult vs. impact parameter')

plt.subplot(233)
plt.hexbin(Npart, mult, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('mult vs. Npart')

plt.subplot(234)
plt.hexbin(Npart, e2, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('e2 vs. Npart')

plt.subplot(235)
plt.hexbin(Npart, e3, cmap = 'Blues', bins = 'log', gridsize = 100)
plt.colorbar()
plt.title('e3 vs. Npart')


plt.show()


