
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D

#   load trento data for 100,000 Au Au events
data = np.loadtxt('AuAu_200GeV_100k.txt')

#   data = [[event_number, impact_param, Npart, mult, e2, e3, e4, e5],...]
#   create a list for the initial entropy of the events
mult = data[:,3]
e2 = data[:,4]

#   apply proportionality constanst to convert initial entropy to charged multiplicity
mult = 4.65905256 * mult

#   change the constituents of mult to int values
for i in range(len(mult)):
    mult[i] = round(mult[i])
mult = mult.astype(np.int64)

T = 0.15 # temperature in GeV
deta = 4
# set pion mass to 0.14 GeV
mpi = 0.14

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
        r1, r2, r3, r4 = np.random.random(4)

        # pT = transvers momentum
        pT_r1 = T*(math.sqrt(-2*math.log(r1)))

        # phi = azimuthal angle
        phi_r2 = 2*(math.pi)*(r2 - 0.5)

        # eta = rapidity
        eta_r3 = deta*(r3 - 0.5)

        # rho = normalized radial distance 
        rho_r4 = r4**0.5

        # calculate initial transverse rapidity (yT)
        eT = (mpi*mpi+pT_r1*pT_r1)**0.5
        yT = 0.5 * np.log((eT+pT_r1)/(eT-pT_r1))
        pT_initial = pT_r1
        yT_initial = yT

        # apply flow as additive boost to transverse rapidity
        yBoost = rho_r4*rho_0 + rho_2*e2[i]*np.cos(2*phi_r2)
        yT = yT_initial + yBoost

        # convert back to pT
        pT_wflow = mpi*np.cosh(yT)

        pT.append(pT_wflow)
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

#   Create an array of colors to color the bars
    bar_colors = []
    for i in range(len(h)):
        if h[i] == 0:
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

    

