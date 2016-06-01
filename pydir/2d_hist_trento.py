
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D

#   load trento data for 10,000 Au Au events
data = np.loadtxt('auau_10k.txt')

#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
#   create a list for the initial entropy of the events
mult = data[:,3]

#   change the constituents of mult to int values
for i in range(len(mult)):
    mult[i] = round(mult[i])
mult = mult.astype(np.int64)

T = 0.15 # temperature in GeV
deta = 4

i = 0
while (i < len(mult)): 

    pT = []
    phi = []
    eta = []

    for j in range(mult[i]):
        r1, r2, r3 = np.random.random(3)
        pT_r1 = T*(math.sqrt(-2*math.log(r1)))
        phi_r2 = 2*(math.pi)*(r2 - 0.5)
        eta_r3 = deta*(r3 - 0.5)

        pT.append(pT_r1)
        phi.append(phi_r2)
        eta.append(eta_r3)
        
#   Create bins using np.histogram2d(), the number of bins produced is the square of the value "b"
    b = 20
    tot_bins = b**2
    h, xedges, yedges = np.histogram2d(eta,phi,bins=b,range=[[-2,2], [-(np.pi), np.pi]],weights=pT)
    h = np.concatenate(h)
    xcenters = 0.5*(xedges[1:]+xedges[:-1])
    xcenters = np.repeat(xcenters,b)
    ycenters = 0.5*(yedges[1:]+yedges[:-1])
    ycenters = np.tile(ycenters,b)

    base = np.zeros(len(h))

#   Set size of bars in plot
    d_eta = (xedges[1]-xedges[0])
    d_phi = (yedges[1]-yedges[0])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.bar3d(xcenters,ycenters,base,d_eta,d_phi,h,color='b',alpha=1)

    ax.set_xlabel('\n$\eta$',fontsize=20)
    ax.set_ylabel('\n$\phi$',fontsize=20)
    ax.set_zlabel('pT')

    plt.title('trento background')
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
        query = raw_input("q to quit, <CR> to continue: ")
        if (query=='q'):
            break
    else: continue

    

