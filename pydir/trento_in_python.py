import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('auau_10k.txt')
#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]

#   separate data into its separate parts
event_number = []
impact_param = []
Npart = []
mult = []
e2 = []
e3 = []
e4 = []
e5 = []

for i in range(len(data)):
    event_number.append(data[i][0])
    impact_param.append(data[i][1])
    Npart.append(data[i][2])
    mult.append(data[i][3])
    e2.append(data[i][4])
    e3.append(data[i][5])
    e4.append(data[i][6])
    e5.append(data[i][7])

#   Creat plots for the following
#   Npart vs. impact parameter
#   mult vs. impact parameter
#   mult vs. Npart
#   e2 vs. Npart
#   e3 vs. Npart

plt.figure(1)

plt.subplot(231)
plt.hexbin(Npart, impact_param, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('Npart vs. impact parameter')

plt.subplot(232)
plt.hexbin(mult, impact_param, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('mult vs. impact parameter')

plt.subplot(233)
plt.hexbin(mult, Npart, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('mult vs. Npart')

plt.subplot(234)
plt.hexbin(e2, Npart, cmap = 'Blues', bins = 'log')
plt.colorbar()
plt.title('e2 vs. Npart')

plt.subplot(235)
plt.hexbin(e3, Npart, cmap = 'Blues', bins = 'log', gridsize = 100)
plt.colorbar()
plt.title('e3 vs. Npart')


plt.show()


