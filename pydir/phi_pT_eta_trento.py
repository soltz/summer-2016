
import matplotlib.pyplot as plt
import numpy as np
import math

#   load trento data for 10,000 Au Au events
data = np.loadtxt('auau_10k.txt')

#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
#   create a list for the initial entropy of the events
mult = data[:,3]

#   change the constituents of mult to int values
for i in range(len(mult)):
    mult[i] = round(mult[i])
mult = mult.astype(np.int64)

#   loop through events and create random values for pT, eta, and phi
T = 0.15 # temperature in GeV
deta = 4

pT = []
phi = []
eta = []

for i in range(len(mult)):
    for j in range(mult[i]):
        r1, r2, r3 = np.random.random(3)
        pT_r1 = T*(math.sqrt(-2*math.log(r1)))
        phi_r2 = 2*(math.pi)*(r2 - 0.5)
        eta_r3 = deta*(r3 - 0.5)

        pT.append(pT_r1)
        phi.append(phi_r2)
        eta.append(eta_r3)

#   create histograms for pT, phi, and eta
plt.figure(1)

plt.subplot(221)
plt.hist(pT, bins = 40)
plt.title('pT counts')
plt.xlabel('pT')

plt.subplot(222)
plt.hist(phi, bins = 40)
plt.title('phi counts')
plt.xlabel('phi')

plt.subplot(223)
plt.hist(eta, bins = 40)
plt.title('eta counts')
plt.xlabel('eta')

plt.show()



